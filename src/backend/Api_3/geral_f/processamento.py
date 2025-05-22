import pandas as pd
import plotly.graph_objects as go
from geral_f.informacao import Exportacao, Importacao, Municipio, Pais, TipoCarga
from geral_f.informacao import db, processar_dados, calcular_totais_mensais, Top_Pais_cargas

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
        fig.add_trace(go.Scatter(x=meses, y=exportacoes_mensais, mode='lines+markers',
                                 name='Exportações', line=dict(color='limegreen', width=2), marker=dict(size=8)))
        fig.add_trace(go.Scatter(x=meses, y=importacoes_mensais, mode='lines+markers',
                                 name='Importações', line=dict(color='tomato', width=2), marker=dict(size=8)))

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

        fig.write_html("grafico_export_import.html", full_html=True)

        kg_por_pais = imp_df.groupby("NO_PAIS")["KG_LIQUIDO"].sum().sort_values(ascending=False).head(10)
        paises_completo = kg_por_pais.index
        paises_curto = [nome[:30] + '...' if len(nome) > 30 else nome for nome in paises_completo]
        valores = kg_por_pais.values

        fig = go.Figure(go.Funnel(
            y=paises_curto,
            x=valores,
            text=[f"{valor:,.0f} kg" for valor in valores],
            textinfo="text",
            hovertext=paises_completo,
            hoverinfo="text+x",
            marker=dict(color='skyblue')
        ))

        fig.update_layout(
            title=f"Top 10 países dos quais as cidades de SP mais importaram (KG Líquido)",
            plot_bgcolor="#0B0121",
            paper_bgcolor="#0B0121",
            font=dict(color="white")
        )
        


        fig.write_image("grafico_funnel.png", width=800, height=600)
        fig.write_html("grafico_funnel.html", full_html=True)

        
        df_cidade = pd.concat([exp_df, imp_df])
        df_cidade = df_cidade[df_cidade["NO_MUN_MIN"] == cidade]

        kg_por_carga = df_cidade.groupby("TIPO_CARGA")["KG_LIQUIDO"].sum().sort_values(ascending=False).head(10)
        cargas_completo = kg_por_carga.index
        cargas_curto = [c[:30] + '...' if len(c) > 30 else c for c in cargas_completo]
        valores = kg_por_carga.values

        fig = go.Figure(data=[
            go.Bar(
                x=cargas_curto,
                y=valores,
                marker_color='skyblue',
                hovertemplate=[f'{c}<br>KG Líquido: {v:,.0f} kg' for c, v in zip(cargas_completo, valores)],
                text=[f"{v:,.0f} kg" for v in valores],
                textposition="outside"
            )
        ])

        fig.update_layout(
            title=f"Top 10 Cargas com Maior KG Líquido (Cidade: {cidade})",
            xaxis_title="Tipo de Carga",
            yaxis_title="KG Líquido",
            plot_bgcolor="#0B0121",
            paper_bgcolor="#0B0121",
            font=dict(color="white"),
            xaxis_tickangle=-45
        )

        fig.write_image("grafico_cargas.png", width=800, height=600)
        fig.write_html("grafico_cargas.html", full_html=True)

        df_rota_simples = exp_df[["TIPO_CARGA", "NO_MUN_MIN", "NO_PAIS"]].dropna()

        rota_html = df_rota_simples.head(20).to_html(index=False, classes='table table-striped', border=0)

        with open("rota_exportacao_tabela.html", "w", encoding="utf-8") as f:
            f.write(rota_html)

        df_rota_simples_imp = imp_df[["TIPO_CARGA", "NO_MUN_MIN", "NO_PAIS"]].dropna()

        rota_html_imp = df_rota_simples_imp.head(20).to_html(index=False, classes='table table-striped', border=0)

        with open("rota_importacao_tabela.html", "w", encoding="utf-8") as f:
            f.write(rota_html_imp)


