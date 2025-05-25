from flask import render_template, request, jsonify
import pandas as pd
from sqlalchemy.sql import text
import plotly.graph_objects as go
import plotly
import json
from .banco import get_db_engine
from threading import Lock
from datetime import datetime

# Dados em cache para melhor performance
cache_data = {
    'municipios': [],
    'anos': [],
    'top_produtos': [],
    'top_cargas': [],
    'dados_mensais': {'meses': [], 'exportacoes': [], 'importacoes': []},
    'top_cargas_valor': [],
    'paises': [],
    'cargas': [],
    'ultima_atualizacao': None
}
cache_lock = Lock()

def configurar_rotas(app):
    
    def carregar_dados_iniciais():
        """Carrega os dados iniciais do banco de dados para o cache"""
        try:
            engine = get_db_engine()
            if not engine:
                app.logger.error("Não foi possível conectar ao banco de dados")
                return

            with engine.connect() as conn:
                # Carrega dados básicos
                with cache_lock:
                    cache_data['municipios'] = pd.read_sql(
                        "SELECT DISTINCT NO_MUN_MIN FROM exportacao ORDER BY NO_MUN_MIN", 
                        conn
                    )['NO_MUN_MIN'].tolist()
                    
                    cache_data['anos'] = [int(ano) for ano in pd.read_sql(
                        "SELECT DISTINCT CO_ANO FROM exportacao ORDER BY CO_ANO", 
                        conn
                    )['CO_ANO'].tolist()]
                    
                    cache_data['paises'] = pd.read_sql(
                        "SELECT DISTINCT NO_PAIS FROM exportacao ORDER BY NO_PAIS", 
                        conn
                    )['NO_PAIS'].tolist()
                    
                    cache_data['cargas'] = pd.read_sql(
                        "SELECT DISTINCT TIPO_CARGA FROM exportacao ORDER BY TIPO_CARGA", 
                        conn
                    )['TIPO_CARGA'].tolist()
                    
                    # Dados padrão
                    ano_padrao = max(cache_data['anos']) if cache_data['anos'] else 2023
                    municipio_padrao = 'São Paulo'
                    
                    # Carrega dados específicos
                    carregar_dados_especificos(conn, ano_padrao, municipio_padrao)
                    
                    cache_data['ultima_atualizacao'] = datetime.now()
                    
        except Exception as e:
            app.logger.error(f"Erro ao carregar dados iniciais: {e}")

    def carregar_dados_especificos(conn, ano, municipio):
        """Carrega dados específicos para um ano e município"""
        try:
            # Top produtos
            cache_data['top_produtos'] = pd.read_sql(text("""
                SELECT SH4 as codigo, TIPO_CARGA as produto, 
                       NO_MUN_MIN as municipio, 
                       CONCAT('R$ ', FORMAT(SUM(VL_FOB)/1000, 2), 'k') as valor
                FROM exportacao 
                WHERE CO_ANO = :ano AND NO_MUN_MIN = :municipio
                GROUP BY SH4, TIPO_CARGA, NO_MUN_MIN
                ORDER BY SUM(VL_FOB) DESC
                LIMIT 10
            """), conn, params={'ano': ano, 'municipio': municipio}).to_dict('records')
            
            # Top cargas
            cache_data['top_cargas'] = pd.read_sql(text("""
                SELECT TIPO_CARGA, 
                       CONCAT('R$ ', FORMAT(SUM(VL_FOB)/1000000, 2), 'M') as valor_total,
                       COUNT(DISTINCT NO_PAIS) as num_paises,
                       CONCAT(FORMAT(SUM(KG_LIQUIDO)/1000, 0), 't') as kg_total
                FROM exportacao
                WHERE CO_ANO = :ano AND NO_MUN_MIN = :municipio
                GROUP BY TIPO_CARGA 
                ORDER BY SUM(VL_FOB) DESC 
                LIMIT 10
            """), conn, params={'ano': ano, 'municipio': municipio}).to_dict('records')
            
            # Dados mensais
            processar_dados_mensais(conn, ano)
            
            # Top cargas por valor agregado
            cache_data['top_cargas_valor'] = pd.read_sql(text("""
                SELECT TIPO_CARGA, CO_ANO, NO_MUN_MIN, 
                       SUM(VL_FOB)/NULLIF(SUM(KG_LIQUIDO), 0) AS valor_agregado
                FROM exportacao
                GROUP BY TIPO_CARGA, CO_ANO, NO_MUN_MIN
                HAVING valor_agregado IS NOT NULL
                ORDER BY valor_agregado DESC
                LIMIT 10
            """), conn).to_dict('records')

            # Verifique se os dados foram carregados
            app.logger.info(f"Top cargas valor: {cache_data['top_cargas_valor']}")
            
        except Exception as e:
            app.logger.error(f"Erro ao carregar dados específicos: {e}")
            raise

    def processar_dados_mensais(conn, ano):
        """Processa dados mensais de exportação e importação"""
        try:
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            exportacoes = [0.0] * 12
            importacoes = [0.0] * 12
            
            # Exportações
            mensal_exp = pd.read_sql(text("""
                SELECT CO_MES, SUM(VL_FOB) as valor
                FROM exportacao
                WHERE CO_ANO = :ano
                GROUP BY CO_MES
                ORDER BY CO_MES
            """), conn, params={'ano': ano})
            
            for _, row in mensal_exp.iterrows():
                mes = int(row['CO_MES']) - 1
                if 0 <= mes < 12:
                    exportacoes[mes] = float(row['valor'])
            
            # Importações
            mensal_imp = pd.read_sql(text("""
                SELECT CO_MES, SUM(VL_FOB) as valor
                FROM importacao
                WHERE CO_ANO = :ano
                GROUP BY CO_MES
                ORDER BY CO_MES
            """), conn, params={'ano': ano})
            
            for _, row in mensal_imp.iterrows():
                mes = int(row['CO_MES']) - 1
                if 0 <= mes < 12:
                    importacoes[mes] = float(row['valor'])
            
            cache_data['dados_mensais'] = {
                'meses': meses,
                'exportacoes': exportacoes,
                'importacoes': importacoes
            }
            
        except Exception as e:
            app.logger.error(f"Erro ao processar dados mensais: {e}")
            raise

    # Carrega dados iniciais ao iniciar
    with app.app_context():
        carregar_dados_iniciais()

    @app.route('/')
    def index():
        """Rota principal que exibe os dashboards"""
        try:
            with cache_lock:
                # Verifica se precisa atualizar o cache (a cada 1 hora)
                if (cache_data['ultima_atualizacao'] is None or 
                    (datetime.now() - cache_data['ultima_atualizacao']).total_seconds() > 3600):
                    carregar_dados_iniciais()

                # Prepara contexto seguro para o template
                context = {
                    'titulo': "Estatísticas de Comércio Exterior",
                    'municipio_selecionado': 'São Paulo',
                    'ano_selecionado': max(cache_data['anos']) if cache_data['anos'] else 2023,
                    'tipo_operacao': 'exportacao',
                    'tabela_dados': cache_data['top_produtos'] or [],
                    'top_cargas': cache_data['top_cargas'] or [],
                    'municipios': cache_data['municipios'] or [],
                    'anos': cache_data['anos'] or [],
                    'paises': cache_data['paises'] or [],
                    'cargas': cache_data['cargas'] or [],
                    'meses': cache_data['dados_mensais']['meses'] or [],
                    'exportacoes': cache_data['dados_mensais']['exportacoes'] or [],
                    'importacoes': cache_data['dados_mensais']['importacoes'] or [],
                    'top_cargas_valor': cache_data['top_cargas_valor'] or []
                }

                # Cria gráficos apenas se houver dados
                if cache_data['dados_mensais']['meses']:
                    fig_linha = criar_grafico_linha()
                    context['grafico_linha'] = json.dumps(fig_linha, cls=plotly.utils.PlotlyJSONEncoder)
                
                if cache_data['top_cargas_valor']:
                    fig_barras = criar_grafico_barras()
                    context['grafico_barras'] = json.dumps(fig_barras, cls=plotly.utils.PlotlyJSONEncoder)

            return render_template('index.html', **context)

        except Exception as e:
            app.logger.error(f"Erro em /index: {e}")
            return render_template('error.html', error=str(e)), 500

    def criar_grafico_linha():
        """Cria gráfico de linhas para dados mensais"""
        return go.Figure(
            data=[
                go.Scatter(
                    x=cache_data['dados_mensais']['meses'],
                    y=cache_data['dados_mensais']['exportacoes'],
                    name='Exportações',
                    line=dict(color='limegreen', width=2),
                    hovertemplate='%{x}<br>R$ %{y:,.2f}<extra></extra>'
                ),
                go.Scatter(
                    x=cache_data['dados_mensais']['meses'],
                    y=cache_data['dados_mensais']['importacoes'],
                    name='Importações',
                    line=dict(color='tomato', width=2),
                    hovertemplate='%{x}<br>R$ %{y:,.2f}<extra></extra>'
                )
            ],
            layout=go.Layout(
                title='Exportações e Importações Mensais (R$)',
                plot_bgcolor='#0B0121',
                paper_bgcolor='#0B0121',
                font=dict(color='white'),
                xaxis=dict(title='Mês'),
                yaxis=dict(title='Valor (R$)'),
                showlegend=True,
                margin=dict(l=40, r=40, t=60, b=40)
            )
        )

    def criar_grafico_barras():
        """Cria gráfico de barras para top cargas"""
        df_cargas = pd.DataFrame(cache_data['top_cargas_valor'])
        
        # Verifique se df_cargas contém dados
        app.logger.info(f"DataFrame para gráfico de barras: {df_cargas}")

        if df_cargas.empty:
            app.logger.warning("Não há dados para criar o gráfico de barras.")
            return go.Figure()  # Retorna um gráfico vazio se não houver dados

        return go.Figure(
            data=[go.Bar(
                y=df_cargas['TIPO_CARGA'].str.slice(0, 25) + ' - ' + df_cargas['NO_MUN_MIN'].str.slice(0, 25) + ' (' + df_cargas['CO_ANO'].astype(str) + ')',
                x=df_cargas['valor_agregado'],
                orientation='h',
                marker=dict(color='rgba(55, 12, 148, 0.8)'),
                hovertemplate='<b>%{y}</b><br>Valor Agregado: R$ %{x:,.2f}/kg<extra></extra>'
            )],
            layout=go.Layout(
                title='Top 10 Cargas por Valor Agregado (R$/kg)',
                plot_bgcolor='#0B0121',
                paper_bgcolor='#0B0121',
                font=dict(color='white'),
                xaxis=dict(title='Valor Agregado (R$/kg)'),
                yaxis=dict(title='Carga - Município (Ano)', automargin=True),
                height=500,
                margin=dict(l=200, r=40, t=60, b=40)
            )
        )

    @app.route('/filtrar')
    def filtrar():
        """Filtra os dados com base nos parâmetros fornecidos"""
        ano = request.args.get('ano', type=int)
        municipio = request.args.get('municipio', 'Todos')
        tipo = request.args.get('tipo', 'exportacao')

        engine = get_db_engine()
        with engine.connect() as conn:
            table = 'exportacao' if tipo == 'exportacao' else 'importacao'
            
            query = text(f"""
                SELECT TIPO_CARGA, 
                       SUM(VL_FOB) as valor_total,
                       COUNT(DISTINCT NO_PAIS) as num_paises
                FROM {table}
                WHERE 1=1
            """)
            
            params = {}
            
            if ano:
                query = text(str(query) + " AND CO_ANO = :ano")
                params['ano'] = ano
            
            if municipio != 'Todos':
                query = text(str(query) + " AND NO_MUN_MIN = :municipio")
                params['municipio'] = municipio
            
            query = text(str(query) + """
                GROUP BY TIPO_CARGA
                ORDER BY valor_total DESC
                LIMIT 10
            """)
            
            result = conn.execute(query, params)
            cargas = []
            valores = []
            
            for row in result:
                cargas.append(row['TIPO_CARGA'])
                valores.append(float(row['valor_total']))
            
            return jsonify({
                'success': True,
                'cargas': cargas,
                'valores': valores,
                'tipo': tipo
            })

    @app.route('/filtrar-top10')
    def filtrar_top10():
        """Filtra os top 10 produtos/cargas"""
        municipio = request.args.get('municipio', 'Todos')
        carga = request.args.get('carga', 'Todas')
        pais = request.args.get('pais', 'Todos')
        tipo = request.args.get('tipo', 'exportacao')
        
        engine = get_db_engine()
        with engine.connect() as conn:
            table = 'exportacao' if tipo == 'exportacao' else 'importacao'
            
            query = text(f"""
                SELECT TIPO_CARGA, 
                       SUM(VL_FOB) as valor_total,
                       COUNT(DISTINCT NO_PAIS) as num_paises
                FROM {table}
                WHERE 1=1
            """)
            
            params = {}
            
            if municipio != 'Todos':
                query = text(str(query) + " AND NO_MUN_MIN = :municipio")
                params['municipio'] = municipio
            
            if carga != 'Todas':
                query = text(str(query) + " AND TIPO_CARGA = :carga")
                params['carga'] = carga
            
            if pais != 'Todos':
                query = text(str(query) + " AND NO_PAIS = :pais")
                params['pais'] = pais
            
            query = text(str(query) + """
                GROUP BY TIPO_CARGA
                ORDER BY valor_total DESC
                LIMIT 10
            """)
            
            result = conn.execute(query, params)
            cargas = []
            valores = []
            
            for row in result:
                cargas.append(row['TIPO_CARGA'])
                valores.append(float(row['valor_total']))
            
            return jsonify({
                'success': True,
                'cargas': cargas,
                'valores': valores,
                'tipo': tipo
            })
