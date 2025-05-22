from flask import render_template
import pandas as pd
from sqlalchemy.sql import text
import plotly.graph_objects as go
import plotly
import json
from .banco import get_db_engine, generate_sample_data


def configurar_rotas(app):

    @app.route('/')
    def index():
        ano_selecionado = 2023
        municipio_selecionado = 'São Paulo'
        estado_selecionado = 'São Paulo'

        try:
            engine = get_db_engine()
            if engine:
                with engine.connect() as conn:
                    tabelas = pd.read_sql(text("SHOW TABLES"), conn)
                    if 'exportacoes' not in tabelas.values or 'importacoes' not in tabelas.values:
                        tabela_dados, top_cargas = generate_sample_data()
                    else:
                        tabela_dados = pd.read_sql(text("""
                            SELECT CO_NCM as codigo, TIPO_CARGA as produto, 
                                   CONCAT(NO_MUN_MIN, ' - ', SG_UF_NCM) as municipio,
                                   CONCAT('R$ ', FORMAT(VL_FOB, 2, 'de_DE')) as valor
                            FROM exportacoes
                            WHERE YEAR(CO_DATA) = :ano AND NO_MUN_MIN = :municipio AND SG_UF_NCM = :estado
                            LIMIT 5
                        """), conn, params={
                            'ano': ano_selecionado,
                            'municipio': municipio_selecionado,
                            'estado': estado_selecionado
                        }).to_dict('records')

                        top_cargas = pd.read_sql(text("""
                            SELECT 
                                TIPO_CARGA,
                                CONCAT('R$ ', FORMAT(SUM(VL_FOB), 2, 'de_DE')) as valor_total,
                                COUNT(DISTINCT NO_PAIS) as num_paises,
                                CONCAT(FORMAT(SUM(KG_LIQUIDO), 2, 'de_DE'), ' kg') as kg_total
                            FROM exportacoes
                            WHERE YEAR(CO_DATA) = :ano AND NO_MUN_MIN = :municipio AND SG_UF_NCM = :estado
                            GROUP BY TIPO_CARGA ORDER BY SUM(VL_FOB) DESC LIMIT 5
                        """), conn, params={
                            'ano': ano_selecionado,
                            'municipio': municipio_selecionado,
                            'estado': estado_selecionado
                        }).to_dict('records')
            else:
                tabela_dados, top_cargas = generate_sample_data()
        except Exception as e:
            print(f"Erro ao obter dados: {e}")
            tabela_dados, top_cargas = generate_sample_data()

        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        exportacoes = [i * 1000000 for i in range(1, 13)]
        importacoes = [i * 800000 for i in range(1, 13)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=exportacoes, mode='lines+markers', name='Exportações'))
        fig.add_trace(go.Scatter(x=meses, y=importacoes, mode='lines+markers', name='Importações'))
        fig.update_layout(
            title='Exportações e Importações Mensais',
            xaxis_title='Mês',
            yaxis_title='Valor (R$)',
            template='plotly_white'
        )
        grafico_linha = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        context = {
            'titulo': "Estatísticas de Comércio Exterior",
            'municipio_selecionado': municipio_selecionado,
            'ano_selecionado': ano_selecionado,
            'meses': meses,
            'exportacoes': exportacoes,
            'importacoes': importacoes,
            'tabela_dados': tabela_dados,
            'top_cargas': top_cargas,
            'grafico_linha': grafico_linha,
            'municipios': ['São Paulo', 'Campinas', 'Santos', 'São José dos Campos', 'Jacareí'],
            'anos': list(range(2013, 2025))
        }

        return render_template('index.html', **context)
