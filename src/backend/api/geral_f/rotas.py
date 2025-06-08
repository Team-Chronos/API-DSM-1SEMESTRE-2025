from flask import Flask, render_template, request, jsonify
from sqlalchemy.sql import text
import pandas as pd
import plotly.graph_objects as go
import plotly
import json
from threading import Lock, Thread
import logging
from datetime import datetime
from geral_f.banco import get_db_engine, close_db_engine
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

cache_data = {
    'municipios': [],
    'anos': [],
    'top_produtos': [],
    'top_cargas': [],
    'dados_mensais': {
        'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
        'exportacoes': [0] * 12,
        'importacoes': [0] * 12
    },
    'top_cargas_valor': [],
    'paises': [],
    'cargas': [],
    'ultima_atualizacao': None
}
cache_lock = Lock()

def configurar_rotas(app):
    
    def carregar_dados_banco(query, params=None, columns=None):
        """Função auxiliar para carregar dados do banco com tratamento robusto"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                engine = get_db_engine()
                if engine is None:
                    logger.warning("Engine do banco de dados não disponível")
                    return pd.DataFrame(columns=columns) if columns else pd.DataFrame()
                
                with engine.connect() as conn:
                    result = pd.read_sql(query, conn, params=params)
                    return result
                
            except Exception as e:
                logger.error(f"Tentativa {attempt + 1} falhou: {str(e)}")
            if attempt == max_attempts - 1:
                return pd.DataFrame(columns=columns) if columns else pd.DataFrame()
            time.sleep(min(2 ** attempt, 4))

    def carregar_dados_iniciais():
        """Carrega dados iniciais em background"""
        try:
            start_time = datetime.now()
            logger.info("Iniciando carregamento de dados...")
            
            
            queries = {
                'municipios': ("SELECT DISTINCT NO_MUN_MIN FROM exportacao ORDER BY NO_MUN_MIN", None, ['NO_MUN_MIN']),
                'anos': ("SELECT DISTINCT CO_ANO FROM exportacao ORDER BY CO_ANO", None, ['CO_ANO']),
                'paises': ("SELECT DISTINCT NO_PAIS FROM exportacao ORDER BY NO_PAIS", None, ['NO_PAIS']),
                'cargas': ("SELECT DISTINCT TIPO_CARGA FROM exportacao ORDER BY TIPO_CARGA", None, ['TIPO_CARGA'])
            }
            
            results = {}
            for key, (query, params, cols) in queries.items():
                results[key] = carregar_dados_banco(query, params, cols)
                if results[key].empty:
                    logger.warning(f"Dados vazios para {key}")

            ano_padrao = 2023
            municipio_padrao = 'São Paulo'
            
            queries_especificas = {
                'top_produtos': ("""
                    SELECT SH4 as codigo, TIPO_CARGA as produto, 
                           NO_MUN_MIN as municipio, 
                           CONCAT('R$ ', FORMAT(SUM(VL_FOB)/1000, 2), 'k') as valor
                    FROM exportacao 
                    WHERE CO_ANO = :ano AND NO_MUN_MIN = :municipio
                    GROUP BY SH4, TIPO_CARGA, NO_MUN_MIN
                    ORDER BY SUM(VL_FOB) DESC
                    LIMIT 10
                """, {'ano': ano_padrao, 'municipio': municipio_padrao}),
                
                'top_cargas': ("""
                    SELECT TIPO_CARGA, 
                           CONCAT('R$ ', FORMAT(SUM(VL_FOB)/1000000, 2), 'M') as valor_total,
                           COUNT(DISTINCT NO_PAIS) as num_paises,
                           CONCAT(FORMAT(SUM(KG_LIQUIDO)/1000, 0), 't') as kg_total
                    FROM exportacao
                    WHERE CO_ANO = :ano AND NO_MUN_MIN = :municipio
                    GROUP BY TIPO_CARGA 
                    ORDER BY SUM(VL_FOB) DESC 
                    LIMIT 10
                """, {'ano': ano_padrao, 'municipio': municipio_padrao}),
                
                'mensal_exp': ("""
                    SELECT CO_MES, SUM(VL_FOB) as valor
                    FROM exportacao
                    WHERE CO_ANO = :ano
                    GROUP BY CO_MES
                    ORDER BY CO_MES
                """, {'ano': ano_padrao}),
                
                'mensal_imp': ("""
                    SELECT CO_MES, SUM(VL_FOB) as valor
                    FROM importacao
                    WHERE CO_ANO = :ano
                    GROUP BY CO_MES
                    ORDER BY CO_MES
                """, {'ano': ano_padrao}),
                
                'top_cargas_valor': ("""
                    SELECT TIPO_CARGA, CO_ANO, NO_MUN_MIN, 
                           SUM(VL_FOB)/NULLIF(SUM(KG_LIQUIDO), 0) AS valor_agregado
                    FROM exportacao
                    GROUP BY TIPO_CARGA, CO_ANO, NO_MUN_MIN
                    HAVING valor_agregado IS NOT NULL
                    ORDER BY valor_agregado DESC
                    LIMIT 10
                """, None)
            }
            
            for key, (query, params) in queries_especificas.items():
                results[key] = carregar_dados_banco(text(query), params)
                if results[key].empty:
                    logger.warning(f"Dados vazios para {key}")

            
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            exportacoes = [0.0] * 12
            importacoes = [0.0] * 12
            
            if not results['mensal_exp'].empty:
                for _, row in results['mensal_exp'].iterrows():
                    if 'CO_MES' in row and 'valor' in row:
                        mes = int(row['CO_MES'])  
                        if 1 <= mes <= 12:
                            exportacoes[mes - 1] = float(row['valor'])
            
            if not results['mensal_imp'].empty:
                for _, row in results['mensal_imp'].iterrows():
                    if 'CO_MES' in row and 'valor' in row:
                        mes = int(row['CO_MES'])  
                        if 1 <= mes <= 12:
                            importacoes[mes - 1] = float(row['valor'])

            
            with cache_lock:
                cache_data.update({
                    'municipios': results['municipios']['NO_MUN_MIN'].tolist() if not results['municipios'].empty else [],
                    'anos': [int(ano) for ano in results['anos']['CO_ANO'].tolist()] if not results['anos'].empty else [],
                    'paises': results['paises']['NO_PAIS'].tolist() if not results['paises'].empty else [],
                    'cargas': results['cargas']['TIPO_CARGA'].tolist() if not results['cargas'].empty else [],
                    'top_produtos': results['top_produtos'].to_dict('records') if not results['top_produtos'].empty else [],
                    'top_cargas': results['top_cargas'].to_dict('records') if not results['top_cargas'].empty else [],
                    'dados_mensais': {
                        'meses': meses,
                        'exportacoes': exportacoes,
                        'importacoes': importacoes
                    },
                    'top_cargas_valor': results['top_cargas_valor'].where(
                        pd.notnull(results['top_cargas_valor']), None
                    ).to_dict('records') if not results['top_cargas_valor'].empty else [],
                    'ultima_atualizacao': datetime.now()
                })
            
            logger.info(f"Dados carregados com sucesso em {(datetime.now() - start_time).total_seconds():.2f} segundos")
            
        except Exception as e:
            logger.error(f"Erro geral ao carregar dados iniciais: {str(e)}")

    
    Thread(target=carregar_dados_iniciais, daemon=True).start()

    @app.route('/')
    def index():
        """Rota principal que renderiza a página inicial"""
        try:
            with cache_lock:
                
                fig_linha = criar_grafico_linha()
                fig_barras = criar_grafico_barras()

                context = {
                    'titulo': "Estatísticas de Comércio Exterior",
                    'municipio_selecionado': 'São Paulo',
                    'ano_selecionado': 2023,
                    'tipo_operacao': 'exportacao',
                    'tabela_dados': cache_data['top_produtos'],
                    'top_cargas': cache_data['top_cargas'],
                    'grafico_linha': json.dumps(fig_linha, cls=plotly.utils.PlotlyJSONEncoder),
                    'grafico_barras': json.dumps(fig_barras, cls=plotly.utils.PlotlyJSONEncoder),
                    'municipios': cache_data['municipios'],
                    'anos': cache_data['anos'],
                    'paises': cache_data['paises'],
                    'cargas': cache_data['cargas'],
                    'meses': cache_data['dados_mensais']['meses'],
                    'exportacoes': cache_data['dados_mensais']['exportacoes'],
                    'importacoes': cache_data['dados_mensais']['importacoes'],
                    'top_cargas_valor': cache_data['top_cargas_valor'],
                    'ultima_atualizacao': cache_data['ultima_atualizacao'].strftime('%d/%m/%Y %H:%M:%S') 
                    if cache_data['ultima_atualizacao'] else 'Nunca'
                }

        except Exception as e:
            logger.error(f"Erro na rota principal: {str(e)}")
            context = criar_contexto_fallback()

        return render_template('index.html', **context)

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
        """Cria gráfico de barras horizontais para top cargas"""
        if cache_data['top_cargas_valor']:
            df_cargas = pd.DataFrame(cache_data['top_cargas_valor'])
            return go.Figure(
                data=[go.Bar(
                    y=df_cargas.apply(
                        lambda row: f"{row['TIPO_CARGA'][:8]}...-{row['NO_MUN_MIN'][:6]}...({row['CO_ANO']})", 
                    axis=1),
                    x=df_cargas['valor_agregado'],
                    orientation='h',
                    marker=dict(color='rgba(55, 12, 148, 0.8)'),
                    hovertemplate='<b>%{y}</b><br>Valor Agregado: R$ %{x:,.2f}/kg<extra></extra>',
                    text=df_cargas['valor_agregado'].apply(lambda x: f'R$ {x:,.2f}'),
                    textposition='inside',
                    insidetextanchor='middle',
                    textfont=dict(color='white')
                )],
                layout=go.Layout(
                    title='Top 10 Cargas por Valor Agregado (R$/kg)',
                    plot_bgcolor='#0B0121',
                    paper_bgcolor='#0B0121',
                    font=dict(color='white'),
                    xaxis=dict(title='Valor Agregado (R$/kg)'),
                    yaxis=dict(title='', automargin=True),  
                    height=500,
                    width=1400, 
                    margin=dict(l=80, r=10, t=60, b=40)
            )
        )
        return go.Figure(
            layout=go.Layout(
                title='Nenhum dado disponível',
                plot_bgcolor='#0B0121',
                paper_bgcolor='#0B0121',
                font=dict(color='white'),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )

    def criar_contexto_fallback():
        """Cria contexto padrão quando ocorrem erros"""
        return {
            'titulo': "Estatísticas de Comércio Exterior",
            'municipio_selecionado': 'São Paulo',
            'ano_selecionado': 2023,
            'tipo_operacao': 'exportacao',
            'tabela_dados': [],
            'top_cargas': [],
            'grafico_linha': None,
            'grafico_barras': None,
            'municipios': [],
            'anos': [],
            'paises': [],
            'cargas': [],
            'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            'exportacoes': [0] * 12,
            'importacoes': [0] * 12,
            'top_cargas_valor': [],
            'ultima_atualizacao': 'Nunca'
        }

    @app.route('/filtrar')
    def filtrar():
        """Filtra dados mensais com base nos parâmetros"""
        try:
            params = {
                'ano': request.args.get('ano', 'Todos'),
                'municipio': request.args.get('municipio', 'São Paulo'),
                'tipo': request.args.get('tipo', 'exportacao')
            }
            
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            dados = {
                'exportacoes': [0.0] * 12,
                'importacoes': [0.0] * 12
            }
            
            try:
                engine = get_db_engine()
                if engine:
                    with engine.connect() as conn:
                        if params['tipo'] in ['exportacao', 'todos']:
                            query_exp = criar_query_mensal(params['ano'], 'exportacao')
                            result_exp = conn.execute(query_exp, 
                                {'municipio': params['municipio']} if params['ano'] == 'Todos' else 
                                {'ano': params['ano'], 'municipio': params['municipio']})
                            processar_resultado(result_exp, dados['exportacoes'])
                        
                        if params['tipo'] in ['importacao', 'todos']:
                            query_imp = criar_query_mensal(params['ano'], 'importacao')
                            result_imp = conn.execute(query_imp, 
                                {'municipio': params['municipio']} if params['ano'] == 'Todos' else 
                                {'ano': params['ano'], 'municipio': params['municipio']})
                            processar_resultado(result_imp, dados['importacoes'])
            
            except Exception as e:
                logger.error(f"Erro ao filtrar dados: {str(e)}")
            
            return jsonify({
                'success': True,
                'meses': meses,
                'exportacoes': dados['exportacoes'],
                'importacoes': dados['importacoes'],
                **params
            })
            
        except Exception as e:
            logger.error(f"Erro em /filtrar: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
                'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                'exportacoes': [0.0] * 12,
                'importacoes': [0.0] * 12,
                'tipo': 'exportacao',
                'ano': 'Todos',
                'municipio': 'São Paulo'
            })

    def criar_query_mensal(ano, tabela):
        """Cria query SQL para dados mensais baseado nos parâmetros"""
        if ano == 'Todos':
            return text(f"""
                SELECT CO_MES, SUM(VL_FOB) as valor
                FROM {tabela}
                WHERE NO_MUN_MIN = :municipio
                GROUP BY CO_MES
                ORDER BY CO_MES
            """)
        return text(f"""
            SELECT CO_MES, SUM(VL_FOB) as valor
            FROM {tabela}
            WHERE CO_ANO = :ano AND NO_MUN_MIN = :municipio
            GROUP BY CO_MES
            ORDER BY CO_MES
        """)

    def processar_resultado(result, lista_saida):
        """Processa resultado SQL e preenche lista de saída"""
        for row in result:
            if 'CO_MES' in row and 'valor' in row:
                mes = int(row['CO_MES'])
                if 1 <= mes <= 12:
                    lista_saida[mes - 1] = float(row['valor'])

    @app.route('/filtrar-top10')
    def filtrar_top10():
        """Filtra os top 10 produtos/cargas"""
        try:
            params = {
                'municipio': request.args.get('municipio', 'São Paulo'),
                'ano': request.args.get('ano', 2023),
                'tipo': request.args.get('tipo', 'exportacao')
            }
            
            resultado = {
                'top_produtos': [],
                'top_cargas': []
            }
            
            try:
                engine = get_db_engine()
                if engine:
                    with engine.connect() as conn:
                        query_produtos = text("""
                            SELECT SH4 as codigo, TIPO_CARGA as produto, 
                                   NO_MUN_MIN as municipio, 
                                   CONCAT('R$ ', FORMAT(SUM(VL_FOB)/1000, 2), 'k') as valor
                            FROM exportacao 
                            WHERE CO_ANO = :ano AND NO_MUN_MIN = :municipio
                            GROUP BY SH4, TIPO_CARGA, NO_MUN_MIN
                            ORDER BY SUM(VL_FOB) DESC
                            LIMIT 10
                        """)
                        produtos = pd.read_sql(query_produtos, conn, params=params)
                        resultado['top_produtos'] = produtos.to_dict('records')
                        
                        query_cargas = text("""
                            SELECT TIPO_CARGA, 
                                   CONCAT('R$ ', FORMAT(SUM(VL_FOB)/1000000, 2), 'M') as valor_total,
                                   COUNT(DISTINCT NO_PAIS) as num_paises,
                                   CONCAT(FORMAT(SUM(KG_LIQUIDO)/1000, 0), 't') as kg_total
                            FROM exportacao
                            WHERE CO_ANO = :ano AND NO_MUN_MIN = :municipio
                            GROUP BY TIPO_CARGA 
                            ORDER BY SUM(VL_FOB) DESC 
                            LIMIT 10
                        """)
                        cargas = pd.read_sql(query_cargas, conn, params=params)
                        resultado['top_cargas'] = cargas.to_dict('records')
            
            except Exception as e:
                logger.error(f"Erro ao filtrar top10: {str(e)}")
            
            return jsonify({
                'success': True,
                **resultado
            })
            
        except Exception as e:
            logger.error(f"Erro em /filtrar-top10: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
                'top_produtos': [],
                'top_cargas': []
            })

    @app.route('/atualizar-dados')
    def atualizar_dados():
        """Rota para forçar atualização dos dados em background"""
        try:
            Thread(target=carregar_dados_iniciais).start()
            return jsonify({'success': True, 'message': 'Atualização iniciada em background'})
        except Exception as e:
            logger.error(f"Erro em /atualizar-dados: {str(e)}")
            return jsonify({'success': False, 'error': str(e)})

    return app