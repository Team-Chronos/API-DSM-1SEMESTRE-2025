import pandas as pd
import plotly.graph_objects as go
from conexao import Exportacao, Importacao, Municipio, Pais, TipoCarga
from conexao import db, flask_app, processar_dados, calcular_totais_mensais

cidade = 'São Paulo'  
ano = 2023    

with flask_app.app_context():
    
    exp_df = pd.read_sql(Exportacao.query.statement, db.session.bind)
    imp_df = pd.read_sql(Importacao.query.statement, db.session.bind)
    mun_df = pd.read_sql(Municipio.query.statement, db.session.bind)
    pais_df = pd.read_sql(Pais.query.statement, db.session.bind)
    tipo_df = pd.read_sql(TipoCarga.query.statement, db.session.bind)

    exp_df = exp_df[(exp_df['uf'] == 'SP') & (exp_df['kg_liquido'] > 0) & (exp_df['co_pais'] != 0)]
    imp_df = imp_df[(imp_df['uf'] == 'SP') & (imp_df['kg_liquido'] > 0) & (imp_df['co_pais'] != 0)]

    mun_df = mun_df.rename(columns={'co_mun': 'CO_MUN', 'nome': 'NO_MUN_MIN'})
    pais_df = pais_df.rename(columns={'co_pais': 'CO_PAIS', 'nome': 'NO_PAIS'})
    tipo_df = tipo_df.rename(columns={'sh4': 'SH4', 'tipo': 'TIPO_CARGA'})

    for name, df in zip(['exp_df', 'imp_df'], [exp_df, imp_df]):
        df.rename(columns={'co_mun': 'CO_MUN', 'co_pais': 'CO_PAIS', 'sh4': 'SH4'}, inplace=True)
        df = df.merge(mun_df, on='CO_MUN', how='left')
        df = df.merge(pais_df, on='CO_PAIS', how='left')
        df = df.merge(tipo_df, on='SH4', how='left')

        df['VALOR_AGREGADO'] = df['valor_fob'] / df['kg_liquido']
        df['VALOR_AGREGADO_FORMATADO'] = df['VALOR_AGREGADO'].apply(lambda x: f"{x:,.2f}")

        if name == 'exp_df':
            exp_df = df
        else:
            imp_df = df

    print(exp_df.sample(5))
    print(imp_df.sample(5))

    exp_df = exp_df[(exp_df['uf'] == 'SP') & (exp_df['kg_liquido'] > 0) & (exp_df['co_pais'] != 0)]
    imp_df = imp_df[(imp_df['uf'] == 'SP') & (imp_df['kg_liquido'] > 0) & (imp_df['co_pais'] != 0)]

    mun_df = mun_df.rename(columns={'co_mun': 'CO_MUN', 'nome': 'NO_MUN_MIN'})
    pais_df = pais_df.rename(columns={'co_pais': 'CO_PAIS', 'nome': 'NO_PAIS'})
    tipo_df = tipo_df.rename(columns={'sh4': 'SH4', 'tipo': 'TIPO_CARGA'})

    exp_df = processar_dados(exp_df, mun_df, pais_df, tipo_df)
    imp_df = processar_dados(imp_df, mun_df, pais_df, tipo_df)

    print(exp_df.sample(5))
    print(imp_df.sample(5))

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