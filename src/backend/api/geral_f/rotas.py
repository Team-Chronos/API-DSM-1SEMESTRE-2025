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
from functools import wraps
from typing import Dict, List, Any, Optional, Union

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log', mode='a', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

CacheType = Dict[str, Union[List[Dict[str, Any]], Dict[str, List[Union[str, float]]], datetime]]

cache_data: CacheType = {
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

def configurar_rotas(app: Flask) -> Flask:
    """Configura todas as rotas da aplicação Flask."""
    
    def handle_database_errors(func):
        """Decorator para tratamento consistente de erros de banco de dados."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Tentativa {attempt + 1} falhou em {func.__name__}: {str(e)}")
                    if attempt == max_attempts - 1:
                        logger.error(f"Falha final em {func.__name__} após {max_attempts} tentativas")
                        return pd.DataFrame()
                    time.sleep(min(2 ** attempt, 4))
        return wrapper

    @handle_database_errors
    def carregar_dados_banco(query: str, params: Optional[Dict] = None, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Carrega dados do banco com tratamento robusto."""
        engine = get_db_engine()
        if engine is None:
            logger.warning("Engine do banco de dados não disponível")
            return pd.DataFrame(columns=columns) if columns else pd.DataFrame()
        
        with engine.connect() as conn:
            if isinstance(query, str):
                query = text(query)
            return pd.read_sql(query, conn, params=params)

    def formatar_moeda(valor: float, divisor: float = 1, sufixo: str = '') -> str:
        """Formata valores monetários de forma consistente."""
        if divisor <= 0:
            divisor = 1
        valor_formatado = valor / divisor
        if valor_formatado >= 1_000_000_000:
            return f'R$ {valor_formatado/1_000_000_000:,.2f}B{sufixo}'
        elif valor_formatado >= 1_000_000:
            return f'R$ {valor_formatado/1_000_000:,.2f}M{sufixo}'
        elif valor_formatado >= 1_000:
            return f'R$ {valor_formatado/1_000:,.2f}k{sufixo}'
        return f'R$ {valor_formatado:,.2f}{sufixo}'

    def formatar_peso(kg: float) -> str:
        """Formata valores de peso de forma consistente."""
        if kg >= 1_000_000:
            return f'{kg/1_000_000:,.1f}kt'
        elif kg >= 1_000:
            return f'{kg/1_000:,.0f}t'
        return f'{kg:,.0f}kg'

    def processar_top_produtos(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Processa dados de top produtos para o formato esperado."""
        if df.empty:
            return []
            
        top_produtos = df.groupby(['codigo', 'produto', 'municipio']).agg({
            'valor_raw': 'sum',
            'NO_PAIS': pd.Series.nunique
        }).reset_index()
        
        top_produtos['valor'] = top_produtos['valor_raw'].apply(
            lambda x: formatar_moeda(x, 1000))
        return top_produtos.sort_values('valor_raw', ascending=False).head(10).to_dict('records')

    def processar_top_cargas(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Processa dados de top cargas para o formato esperado."""
        if df.empty:
            return []
            
        top_cargas = df.groupby('TIPO_CARGA').agg({
            'valor_raw': 'sum',
            'NO_PAIS': pd.Series.nunique,
            'KG_LIQUIDO': 'sum'
        }).reset_index()
        
        top_cargas['valor_total'] = top_cargas['valor_raw'].apply(
            lambda x: formatar_moeda(x, 1_000_000))
        top_cargas['kg_total'] = top_cargas['KG_LIQUIDO'].apply(formatar_peso)
        return top_cargas.sort_values('valor_raw', ascending=False).head(10).to_dict('records')

    def processar_dados_mensais(df_exp: pd.DataFrame, df_imp: pd.DataFrame) -> Dict[str, List[Union[str, float]]]:
        """Processa dados mensais para o formato esperado."""
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        exportacoes = [0.0] * 12
        importacoes = [0.0] * 12
        
        if not df_exp.empty:
            mensal_exp = df_exp.groupby('CO_MES')['valor'].sum().reset_index()
            for _, row in mensal_exp.iterrows():
                if 1 <= (mes := int(row['CO_MES'])) <= 12:
                    exportacoes[mes - 1] = float(row['valor'])
        
        if not df_imp.empty:
            mensal_imp = df_imp.groupby('CO_MES')['valor'].sum().reset_index()
            for _, row in mensal_imp.iterrows():
                if 1 <= (mes := int(row['CO_MES'])) <= 12:
                    importacoes[mes - 1] = float(row['valor'])

        return {
            'meses': meses,
            'exportacoes': exportacoes,
            'importacoes': importacoes
        }

    def processar_top_cargas_valor(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Processa dados de valor agregado para o formato esperado."""
        if df.empty:
            return []
            
        top_cargas_valor = df.groupby(['TIPO_CARGA', 'NO_MUN_MIN', 'ano']).agg({
            'VL_FOB': 'sum',
            'KG_LIQUIDO': 'sum'
        }).reset_index()
        
        top_cargas_valor['valor_agregado'] = (
            top_cargas_valor['VL_FOB'] / top_cargas_valor['KG_LIQUIDO'].replace(0, pd.NA))
        top_cargas_valor = top_cargas_valor.dropna(subset=['valor_agregado'])
        
        top_cargas_valor['carga_resumida'] = top_cargas_valor['TIPO_CARGA'].str.slice(0, 15) + '...'
        top_cargas_valor['municipio_resumido'] = top_cargas_valor['NO_MUN_MIN'].str.slice(0, 10) + '...'
        
        return top_cargas_valor.sort_values('valor_agregado', ascending=False).head(10).to_dict('records')

    def carregar_dados_iniciais() -> None:
        """Carrega dados iniciais em background."""
        try:
            start_time = datetime.now()
            logger.info("Iniciando carregamento de dados...")
            
            queries_basicas = {
                'municipios': ("SELECT DISTINCT NO_MUN_MIN FROM exportacao ORDER BY NO_MUN_MIN", None, ['NO_MUN_MIN']),
                'anos': ("SELECT DISTINCT CO_ANO FROM exportacao ORDER BY CO_ANO", None, ['CO_ANO']),
                'paises': ("SELECT DISTINCT NO_PAIS FROM exportacao ORDER BY NO_PAIS", None, ['NO_PAIS']),
                'cargas': ("SELECT DISTINCT TIPO_CARGA FROM exportacao ORDER BY TIPO_CARGA", None, ['TIPO_CARGA'])
            }
            
            results = {
                key: carregar_dados_banco(query, params, cols)
                for key, (query, params, cols) in queries_basicas.items()
            }
            
            ano_padrao = 2023
            municipio_padrao = 'São Paulo'
            
            queries_especificas = {
                'top_produtos': ("""
                    SELECT SH4 as codigo, TIPO_CARGA as produto, 
                           NO_MUN_MIN as municipio, 
                           VL_FOB as valor_raw,
                           NO_PAIS
                    FROM exportacao 
                    WHERE CO_ANO = :ano AND NO_MUN_MIN = :municipio
                """, {'ano': ano_padrao, 'municipio': municipio_padrao}),
                
                'top_cargas': ("""
                    SELECT TIPO_CARGA, 
                           VL_FOB as valor_raw,
                           KG_LIQUIDO,
                           NO_PAIS
                    FROM exportacao
                    WHERE CO_ANO = :ano AND NO_MUN_MIN = :municipio
                """, {'ano': ano_padrao, 'municipio': municipio_padrao}),
                
                'mensal_exp': ("""
                    SELECT CO_MES, VL_FOB as valor
                    FROM exportacao
                    WHERE CO_ANO = :ano
                """, {'ano': ano_padrao}),
                
                'mensal_imp': ("""
                    SELECT CO_MES, VL_FOB as valor
                    FROM importacao
                    WHERE CO_ANO = :ano
                """, {'ano': ano_padrao}),
                
                'top_cargas_valor': ("""
                    SELECT 
                        TIPO_CARGA,
                        NO_MUN_MIN,
                        CO_ANO as ano,
                        VL_FOB,
                        KG_LIQUIDO
                    FROM exportacao
                """, None)
            }
            
            for key, (query, params) in queries_especificas.items():
                results[key] = carregar_dados_banco(text(query), params)
                if results[key].empty:
                    logger.warning(f"Dados vazios para {key}")

            processed_data = {
                'municipios': results['municipios']['NO_MUN_MIN'].tolist() if not results['municipios'].empty else [],
                'anos': [int(ano) for ano in results['anos']['CO_ANO'].tolist()] if not results['anos'].empty else [],
                'paises': results['paises']['NO_PAIS'].tolist() if not results['paises'].empty else [],
                'cargas': results['cargas']['TIPO_CARGA'].tolist() if not results['cargas'].empty else [],
                'top_produtos': processar_top_produtos(results['top_produtos']),
                'top_cargas': processar_top_cargas(results['top_cargas']),
                'dados_mensais': processar_dados_mensais(results['mensal_exp'], results['mensal_imp']),
                'top_cargas_valor': processar_top_cargas_valor(results['top_cargas_valor']),
                'ultima_atualizacao': datetime.now()
            }
            
            with cache_lock:
                cache_data.update(processed_data)
            
            logger.info(f"Dados carregados com sucesso em {(datetime.now() - start_time).total_seconds():.2f} segundos")
            
        except Exception as e:
            logger.error(f"Erro geral ao carregar dados iniciais: {str(e)}", exc_info=True)

    Thread(target=carregar_dados_iniciais, daemon=True).start()

    @app.route('/')
    def index():
        """Rota principal que renderiza a página inicial."""
        try:
            with cache_lock:
                fig_linha = criar_grafico_linha(
                    cache_data['dados_mensais']['meses'],
                    cache_data['dados_mensais']['exportacoes'],
                    cache_data['dados_mensais']['importacoes']
                )
                
                fig_barras = criar_grafico_barras_valor_agregado(
                    cache_data['top_cargas_valor']
                )

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
            logger.error(f"Erro na rota principal: {str(e)}", exc_info=True)
            context = criar_contexto_fallback()

        return render_template('index.html', **context)

    def criar_grafico_linha(meses: List[str], 
                           exportacoes: List[float], 
                           importacoes: List[float]) -> go.Figure:
        """Cria gráfico de linhas para dados mensais."""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=meses,
            y=exportacoes,
            name='Exportações',
            line=dict(color='limegreen', width=2),
            hovertemplate='%{x}<br>R$ %{y:,.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=meses,
            y=importacoes,
            name='Importações',
            line=dict(color='tomato', width=2),
            hovertemplate='%{x}<br>R$ %{y:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Exportações e Importações Mensais (R$)',
            plot_bgcolor='#0B0121',
            paper_bgcolor='#0B0121',
            font=dict(color='white'),
            xaxis=dict(title='Mês'),
            yaxis=dict(title='Valor (R$)'),
            showlegend=True,
            margin=dict(l=40, r=40, t=60, b=40),
            hovermode='x unified'
        )
        
        return fig

    def criar_grafico_barras_valor_agregado(dados: List[Dict[str, Any]]) -> go.Figure:
        """Cria gráfico de barras horizontais para valor agregado."""
        if not dados:
            return go.Figure(
                layout=go.Layout(
                    title='Nenhum dado disponível',
                    plot_bgcolor='#0B0121',
                    paper_bgcolor='#0B0121',
                    font=dict(color='white')
                )
            )

        dados_ordenados = sorted(dados, key=lambda x: x['valor_agregado'], reverse=True)
        
        labels = [
            f"{item['carga_resumida']}<br>{item['municipio_resumido']} ({item['ano']})"
            for item in dados_ordenados
        ]
        valores = [item['valor_agregado'] for item in dados_ordenados]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=labels,
            x=valores,
            orientation='h',
            marker=dict(color='rgb(55, 12, 148)', line=dict(color='rgba(55, 12, 148)', width=1)),
            hovertemplate=(
                '<b>Tipo Carga:</b> %{customdata[0]}<br>'
                '<b>Município:</b> %{customdata[1]}<br>'
                '<b>Ano:</b> %{customdata[2]}<br>'
                '<b>Valor Agregado:</b> R$ %{x:,.2f}/kg<extra></extra>'
            ),
            customdata=[
                [d['carga_resumida'], d['municipio_resumido'], d['ano']]
                for d in dados_ordenados
            ],
            text=[f'R$ {x:,.2f}/kg' for x in valores],
            textposition='auto',
            insidetextanchor='middle',
            textfont=dict(color='white', size=10),
            cliponaxis=False
        ))
        
        if valores:
            media = sum(valores) / len(valores)
            fig.add_shape(
                type="line",
                x0=media, y0=-0.5,
                x1=media, y1=len(valores)-0.5,
                line=dict(color='tomato', width=2, dash="dot"),
                name="Média"
            )
            
            fig.add_annotation(
                x=media,
                y=len(valores)-0.5,
                text=f"Média: R$ {media:,.2f}/kg",
                showarrow=True,
                arrowhead=1,
                ax=-50,
                ay=0,
                bgcolor="rgba(255,255,0,0.3)",
                bordercolor="yellow"
            )
        
        fig.update_layout(
            title='Top 10 Cargas por Valor Agregado (R$/kg)',
            plot_bgcolor='#0B0121',
            paper_bgcolor='#0B0121',
            font=dict(color='white'),
            yaxis=dict(title='', automargin=True, tickfont=dict(size=10), showgrid=False),
            xaxis=dict(title='Valor Agregado (R$/kg)', showgrid=True, gridcolor='rgba(255, 255, 255, 0.1)'),
            height=500,
            margin=dict(l=150, r=20, t=60, b=40),
            hoverlabel=dict(bgcolor='#1A1A3D', font_size=12, font_family="Rockwell"),
            dragmode=False
        )
        
        return fig

    def criar_contexto_fallback() -> Dict[str, Any]:
        """Cria contexto padrão quando ocorrem erros."""
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

    @app.route('/filtrar-dados')
    def filtrar_dados():
        """Rota unificada para filtrar todos os dados."""
        try:
            params = {
                'ano': request.args.get('ano', '2023'),
                'municipio': request.args.get('municipio', 'São Paulo'),
                'tipo_operacao': request.args.get('tipo_operacao', 'exportacao'),
                'pais': request.args.get('pais', ''),
                'carga': request.args.get('carga', '')
            }

            resultado = {
                'top_produtos': [],
                'top_cargas': [],
                'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                'exportacoes': [0.0] * 12,
                'importacoes': [0.0] * 12,
                'top_cargas_valor': []
            }

            try:
                engine = get_db_engine()
                if engine:
                    with engine.connect() as conn:
                        query_produtos = text("""
                            SELECT SH4 as codigo, TIPO_CARGA as produto, 
                                   NO_MUN_MIN as municipio, 
                                   VL_FOB as valor_raw,
                                   NO_PAIS
                            FROM exportacao 
                            WHERE CO_ANO = :ano 
                              AND NO_MUN_MIN = :municipio
                              AND (:pais = '' OR NO_PAIS = :pais)
                              AND (:carga = '' OR TIPO_CARGA = :carga)
                        """)
                        produtos = pd.read_sql(query_produtos, conn, params=params)
                        resultado['top_produtos'] = processar_top_produtos(produtos)

                        query_cargas = text("""
                            SELECT TIPO_CARGA, 
                                   VL_FOB as valor_raw,
                                   KG_LIQUIDO,
                                   NO_PAIS
                            FROM exportacao
                            WHERE CO_ANO = :ano 
                              AND NO_MUN_MIN = :municipio
                              AND (:pais = '' OR NO_PAIS = :pais)
                              AND (:carga = '' OR TIPO_CARGA = :carga)
                        """)
                        cargas = pd.read_sql(query_cargas, conn, params=params)
                        resultado['top_cargas'] = processar_top_cargas(cargas)

                        if params['tipo_operacao'] in ['exportacao', 'todos']:
                            query_mensal_exp = text("""
                                SELECT CO_MES, VL_FOB as valor
                                FROM exportacao
                                WHERE CO_ANO = :ano 
                                  AND NO_MUN_MIN = :municipio
                                  AND (:pais = '' OR NO_PAIS = :pais)
                                  AND (:carga = '' OR TIPO_CARGA = :carga)
                            """)
                            result_exp = pd.read_sql(query_mensal_exp, conn, params=params)
                            
                        if params['tipo_operacao'] in ['importacao', 'todos']:
                            query_mensal_imp = text("""
                                SELECT CO_MES, VL_FOB as valor
                                FROM importacao
                                WHERE CO_ANO = :ano 
                                  AND NO_MUN_MIN = :municipio
                                  AND (:pais = '' OR NO_PAIS = :pais)
                                  AND (:carga = '' OR TIPO_CARGA = :carga)
                            """)
                            result_imp = pd.read_sql(query_mensal_imp, conn, params=params)
                        
                        mensais = processar_dados_mensais(
                            result_exp if params['tipo_operacao'] in ['exportacao', 'todos'] else pd.DataFrame(),
                            result_imp if params['tipo_operacao'] in ['importacao', 'todos'] else pd.DataFrame()
                        )
                        resultado.update(mensais)

                        query_valor_agregado = text("""
                            SELECT 
                                TIPO_CARGA,
                                NO_MUN_MIN,
                                CO_ANO as ano,
                                VL_FOB,
                                KG_LIQUIDO
                            FROM exportacao
                            WHERE CO_ANO = :ano
                              AND (:municipio = '' OR NO_MUN_MIN = :municipio)
                              AND (:pais = '' OR NO_PAIS = :pais)
                              AND (:carga = '' OR TIPO_CARGA = :carga)
                        """)
                        cargas_valor = pd.read_sql(query_valor_agregado, conn, params=params)
                        resultado['top_cargas_valor'] = processar_top_cargas_valor(cargas_valor)

            except Exception as e:
                logger.error(f"Erro ao filtrar dados: {str(e)}", exc_info=True)
                return jsonify({
                    'success': False,
                    'error': str(e)
                })

            fig_linha = criar_grafico_linha(
                resultado['meses'],
                resultado['exportacoes'],
                resultado['importacoes']
            )
            
            fig_barras = criar_grafico_barras_valor_agregado(
                resultado['top_cargas_valor']
            )

            return jsonify({
                'success': True,
                'top_produtos': resultado['top_produtos'],
                'top_cargas': resultado['top_cargas'],
                'meses': resultado['meses'],
                'exportacoes': resultado['exportacoes'],
                'importacoes': resultado['importacoes'],
                'top_cargas_valor': resultado['top_cargas_valor'],
                'grafico_linha': json.loads(json.dumps(fig_linha, cls=plotly.utils.PlotlyJSONEncoder)),
                'grafico_barras': json.loads(json.dumps(fig_barras, cls=plotly.utils.PlotlyJSONEncoder)),
                'params': params
            })

        except Exception as e:
            logger.error(f"Erro em /filtrar-dados: {str(e)}", exc_info=True)
            return jsonify({
                'success': False,
                'error': str(e)
            })

    @app.route('/atualizar-dados')
    def atualizar_dados():
        """Rota para forçar atualização dos dados em background."""
        try:
            Thread(target=carregar_dados_iniciais).start()
            return jsonify({
                'success': True, 
                'message': 'Atualização iniciada em background'
            })
        except Exception as e:
            logger.error(f"Erro em /atualizar-dados: {str(e)}", exc_info=True)
            return jsonify({
                'success': False, 
                'error': str(e)
            })

    return app