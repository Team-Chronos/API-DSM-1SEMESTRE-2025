import pandas as pd
import plotly.graph_objects as go
from geral_f.informacao import Exportacao, Importacao, Municipio, Pais, TipoCarga
from geral_f.informacao import db, processar_dados, calcular_totais_mensais

def gerar_graficos(app):
    with app.app_context():
        cidade = 'São Paulo'
        ano = 2023

        exp_df = pd.read_sql(db.session.query(Exportacao).statement, db.engine)
        imp_df = pd.read_sql(db.session.query(Importacao).statement, db.engine)
        mun_df = pd.read_sql(db.session.query(Municipio).statement, db.engine)
        pais_df = pd.read_sql(db.session.query(Pais).statement, db.engine)
        tipo_df = pd.read_sql(db.session.query(TipoCarga).statement, db.engine)

        exp_df = exp_df[(exp_df['uf'] == 'SP') & (exp_df['kg_liquido'] > 0) & (exp_df['co_pais'] != 0)]
        imp_df = imp_df[(imp_df['uf'] == 'SP') & (imp_df['kg_liquido'] > 0) & (imp_df['co_pais'] != 0)]

        mun_df = mun_df.rename(columns={'co_mun': 'CO_MUN', 'nome': 'NO_MUN_MIN'})
        pais_df = pais_df.rename(columns={'co_pais': 'CO_PAIS', 'nome': 'NO_PAIS'})
        tipo_df = tipo_df.rename(columns={'sh4': 'SH4', 'tipo': 'TIPO_CARGA'})

        exp_df = processar_dados(exp_df, mun_df, pais_df, tipo_df)
        imp_df = processar_dados(imp_df, mun_df, pais_df, tipo_df)

        exp_html = exp_df.to_html(index=False, classes='table table-striped', border=0)
        imp_html = imp_df.to_html(index=False, classes='table table-striped', border=0)

        with open("exportacoes_tabela.html", "w", encoding="utf-8") as f:
            f.write(exp_html)

        with open("importacoes_tabela.html", "w", encoding="utf-8") as f:
            f.write(imp_html)

        exportacoes_mensais = calcular_totais_mensais(exp_df, cidade)
        importacoes_mensais = calcular_totais_mensais(imp_df, cidade)

        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=meses, y=exportacoes_mensais,
            mode='lines+markers',
            name='Exportações',
            line=dict(color='limegreen', width=2),
            marker=dict(size=8)
        ))

        fig.add_trace(go.Scatter(
            x=meses, y=importacoes_mensais,
            mode='lines+markers',
            name='Importações',
            line=dict(color='tomato', width=2),
            marker=dict(size=8)
        ))

        fig.update_layout(
            title=f"Exportações e Importações Mensais em {cidade.title()} ({ano})",
            xaxis_title="Mês",
            yaxis_title="Kg Líquido",
            plot_bgcolor="#0B0121",
            paper_bgcolor="#0B0121",
            font=dict(color="white"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="gray"),
        )

        html_output = fig.to_html(full_html=True)
        with open("grafico_export_import.html", "w", encoding="utf-8") as f:
            f.write(html_output)
