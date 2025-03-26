import pandas as pd

# importação das tabelas em CSV
ex24 = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/EXP_2024_MUN.csv'
imp24 = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/IMP_2024_MUN.csv'
mun = 'https://balanca.economia.gov.br/balanca/bd/tabelas/UF_MUN.csv'
sh4 = 'https://balanca.economia.gov.br/balanca/bd/tabelas/NCM_SH.csv'

ex24_df = pd.read_csv(ex24, sep=";", encoding="latin1")
imp24_df = pd.read_csv(imp24, sep=";", encoding="latin1")
mun_df = pd.read_csv(mun, sep=";", encoding="latin1")
sh4_df = pd.read_csv(sh4, sep=";", encoding="latin1")

# Renomeando tabelas
mun_df = mun_df.rename(columns={"CO_MUN_GEO": "CO_MUN"})
sh4_df = sh4_df.rename(columns={"CO_SH4": "SH4", "NO_SH4_POR": "PRODUTO"})
ex24_df = ex24_df.merge(mun_df, on=["CO_MUN"], how="left")
imp24_df = imp24_df.merge(mun_df, on=["CO_MUN"], how="left")

# Criando variáveis de exportação
ex_mes_24 = ex24_df['CO_MES']
ex_sh4_24 = ex24_df['SH4']
ex_estado_24 = ex24_df['SG_UF_MUN']
ex_municipio_24 = ex24_df['CO_MUN']
ex_liquido_24 = ex24_df['KG_LIQUIDO']
ex_valorFob_24 = ex24_df['VL_FOB']

# Criando variáveis de importação
imp_mes_24 = imp24_df['CO_MES']
imp_sh4_24 = imp24_df['SH4']
imp_estado_24 = imp24_df['SG_UF_MUN']
imp_municipio_24 = imp24_df['CO_MUN']
imp_liquido_24 = imp24_df['KG_LIQUIDO']
imp_valorFob_24 = imp24_df['VL_FOB']

# Criando a variável de cidade(primeiro filtro)
cidade = "Pirapozinho"

# Filtrar os dados por mês, estado, municipio e calcular o total de exportações de todos os meses
ex_janeiro24 = ex24_df.loc[ex_mes_24 == 1]
ex_janeiro24 = ex_janeiro24[ex_janeiro24["SG_UF_MUN"] == "SP"]
ex_janeiro24 = ex_janeiro24[ex_janeiro24["NO_MUN_MIN"] == cidade]
ex_janeiro24_total = ex_janeiro24["KG_LIQUIDO"].sum()

ex_fev24 = ex24_df.loc[ex_mes_24 == 2]
ex_fev24 = ex_fev24[ex_fev24["SG_UF_MUN"] == "SP"]
ex_fev24 = ex_fev24[ex_fev24["NO_MUN_MIN"] == cidade]
ex_fev24_total = ex_fev24["KG_LIQUIDO"].sum()

ex_mar24 = ex24_df.loc[ex_mes_24 == 3]
ex_mar24 = ex_mar24[ex_mar24["SG_UF_MUN"] == "SP"]
ex_mar24 = ex_mar24[ex_mar24["NO_MUN_MIN"] == cidade]
ex_mar24_total = ex_mar24["KG_LIQUIDO"].sum()

ex_abr24 = ex24_df.loc[ex_mes_24 == 4]
ex_abr24 = ex_abr24[ex_abr24["SG_UF_MUN"] == "SP"]
ex_abr24 = ex_abr24[ex_abr24["NO_MUN_MIN"] == cidade]
ex_abr24_total = ex_abr24["KG_LIQUIDO"].sum()

ex_mai24 = ex24_df.loc[ex_mes_24 == 5]
ex_mai24 = ex_mai24[ex_mai24["SG_UF_MUN"] == "SP"]
ex_mai24 = ex_mai24[ex_mai24["NO_MUN_MIN"] == cidade]
ex_mai24_total = ex_mai24["KG_LIQUIDO"].sum()

ex_jun24 = ex24_df.loc[ex_mes_24 == 6]
ex_jun24 = ex_jun24[ex_jun24["SG_UF_MUN"] == "SP"]
ex_jun24 = ex_jun24[ex_jun24["NO_MUN_MIN"] == cidade]
ex_jun24_total = ex_jun24["KG_LIQUIDO"].sum()

ex_jul24 = ex24_df.loc[ex_mes_24 == 7]
ex_jul24 = ex_jul24[ex_jul24["SG_UF_MUN"] == "SP"]
ex_jul24 = ex_jul24[ex_jul24["NO_MUN_MIN"] == cidade]
ex_jul24_total = ex_jul24["KG_LIQUIDO"].sum()

ex_ago24 = ex24_df.loc[ex_mes_24 == 8]
ex_ago24 = ex_ago24[ex_ago24["SG_UF_MUN"] == "SP"]
ex_ago24 = ex_ago24[ex_ago24["NO_MUN_MIN"] == cidade]
ex_ago24_total = ex_ago24["KG_LIQUIDO"].sum()

ex_set24 = ex24_df.loc[ex_mes_24 == 9]
ex_set24 = ex_set24[ex_set24["SG_UF_MUN"] == "SP"]
ex_set24 = ex_set24[ex_set24["NO_MUN_MIN"] == cidade]
ex_set24_total = ex_set24["KG_LIQUIDO"].sum()

ex_out24 = ex24_df.loc[ex_mes_24 == 10]
ex_out24 = ex_out24[ex_out24["SG_UF_MUN"] == "SP"]
ex_out24 = ex_out24[ex_out24["NO_MUN_MIN"] == cidade]
ex_out24_total = ex_out24["KG_LIQUIDO"].sum()

ex_nov24 = ex24_df.loc[ex_mes_24 == 11]
ex_nov24 = ex_nov24[ex_nov24["SG_UF_MUN"] == "SP"]
ex_nov24 = ex_nov24[ex_nov24["NO_MUN_MIN"] == cidade]
ex_nov24_total = ex_nov24["KG_LIQUIDO"].sum()

ex_dez24 = ex24_df.loc[ex_mes_24 == 12]
ex_dez24 = ex_dez24[ex_dez24["SG_UF_MUN"] == "SP"]
ex_dez24 = ex_dez24[ex_dez24["NO_MUN_MIN"] == cidade]
ex_dez24_total = ex_dez24["KG_LIQUIDO"].sum()

# Filtrar os dados por mês, estado, municipio e calcular o total de exportações de todos os meses
imp_janeiro24 = imp24_df.loc[imp_mes_24 == 1]
imp_janeiro24 = imp_janeiro24[imp_janeiro24["SG_UF_MUN"] == "SP"]
imp_janeiro24 = imp_janeiro24[imp_janeiro24["NO_MUN_MIN"] == cidade]
imp_janeiro24_total = imp_janeiro24["KG_LIQUIDO"].sum()

imp_fev24 = imp24_df.loc[imp_mes_24 == 2]
imp_fev24 = imp_fev24[imp_fev24["SG_UF_MUN"] == "SP"]
imp_fev24 = imp_fev24[imp_fev24["NO_MUN_MIN"] == cidade]
imp_fev24_total = imp_fev24["KG_LIQUIDO"].sum()

imp_mar24 = imp24_df.loc[imp_mes_24 == 3]
imp_mar24 = imp_mar24[imp_mar24["SG_UF_MUN"] == "SP"]
imp_mar24 = imp_mar24[imp_mar24["NO_MUN_MIN"] == cidade]
imp_mar24_total = imp_mar24["KG_LIQUIDO"].sum()

imp_abr24 = imp24_df.loc[imp_mes_24 == 4]
imp_abr24 = imp_abr24[imp_abr24["SG_UF_MUN"] == "SP"]
imp_abr24 = imp_abr24[imp_abr24["NO_MUN_MIN"] == cidade]
imp_abr24_total = imp_abr24["KG_LIQUIDO"].sum()

imp_mai24 = imp24_df.loc[imp_mes_24 == 5]
imp_mai24 = imp_mai24[imp_mai24["SG_UF_MUN"] == "SP"]
imp_mai24 = imp_mai24[imp_mai24["NO_MUN_MIN"] == cidade]
imp_mai24_total = imp_mai24["KG_LIQUIDO"].sum()

imp_jun24 = imp24_df.loc[imp_mes_24 == 6]
imp_jun24 = imp_jun24[imp_jun24["SG_UF_MUN"] == "SP"]
imp_jun24 = imp_jun24[imp_jun24["NO_MUN_MIN"] == cidade]
imp_jun24_total = imp_jun24["KG_LIQUIDO"].sum()

imp_jul24 = imp24_df.loc[imp_mes_24 == 7]
imp_jul24 = imp_jul24[imp_jul24["SG_UF_MUN"] == "SP"]
imp_jul24 = imp_jul24[imp_jul24["NO_MUN_MIN"] == cidade]
imp_jul24_total = imp_jul24["KG_LIQUIDO"].sum()

imp_ago24 = imp24_df.loc[imp_mes_24 == 8]
imp_ago24 = imp_ago24[imp_ago24["SG_UF_MUN"] == "SP"]
imp_ago24 = imp_ago24[imp_ago24["NO_MUN_MIN"] == cidade]
imp_ago24_total = imp_ago24["KG_LIQUIDO"].sum()

imp_set24 = imp24_df.loc[imp_mes_24 == 9]
imp_set24 = imp_set24[imp_set24["SG_UF_MUN"] == "SP"]
imp_set24 = imp_set24[imp_set24["NO_MUN_MIN"] == cidade]
imp_set24_total = imp_set24["KG_LIQUIDO"].sum()

imp_out24 = imp24_df.loc[imp_mes_24 == 10]
imp_out24 = imp_out24[imp_out24["SG_UF_MUN"] == "SP"]
imp_out24 = imp_out24[imp_out24["NO_MUN_MIN"] == cidade]
imp_out24_total = imp_out24["KG_LIQUIDO"].sum()

imp_nov24 = imp24_df.loc[imp_mes_24 == 11]
imp_nov24 = imp_nov24[imp_nov24["SG_UF_MUN"] == "SP"]
imp_nov24 = imp_nov24[imp_nov24["NO_MUN_MIN"] == cidade]
imp_nov24_total = imp_nov24["KG_LIQUIDO"].sum()

imp_dez24 = imp24_df.loc[imp_mes_24 == 12]
imp_dez24 = imp_dez24[imp_dez24["SG_UF_MUN"] == "SP"]
imp_dez24 = imp_dez24[imp_dez24["NO_MUN_MIN"] == cidade]
imp_dez24_total = imp_dez24["KG_LIQUIDO"].sum()

#
# Parte dos gráficos para colocar os valores da tabela

import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline

# Definir os meses e valores fictícios
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
x = np.arange(len(meses))
valores = [ex_janeiro24_total, ex_fev24_total, ex_mar24_total, ex_abr24_total, ex_mai24_total, ex_jun24_total, ex_jul24_total, ex_ago24_total, ex_set24_total, ex_out24_total, ex_nov24_total, ex_dez24_total]

# Criar gráfico interativo
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=meses,
    y=valores,
    mode='lines+markers',  # Linha + Pontos
    line=dict(color='white', width=2),
    marker=dict(size=8, color='red', line=dict(color='black', width=1)),
    hoverinfo='x+y'
))

# Estilizar layout (cor de fundo e grid)
fig.update_layout(
    title="Gráfico Interativo de Valores Mensais",
    xaxis_title="Mês",
    yaxis_title="Valor",
    plot_bgcolor="#0B0121",
    paper_bgcolor="#0B0121",
    font=dict(color="white"),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="gray"),
)

# Exibir no navegador
fig.write_html("./templates/grafico_interativo.html")