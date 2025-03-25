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

# Criando variáveis
ex_mes_24 = ex24_df['CO_MES']
ex_sh4_24 = ex24_df['SH4']
ex_estado_24 = ex24_df['SG_UF_MUN']
ex_municipio_24 = ex24_df['CO_MUN']
ex_liquido_24 = ex24_df['KG_LIQUIDO']
ex_valorFob_24 = ex24_df['VL_FOB']

# Criando a variável de cidade(primeiro filtro)
cidade = "Pirapozinho"

# Filtrar os dados por mês, estado, municipio e calcular o total de exportações de todos os meses
janeiro24 = ex24_df.loc[ex_mes_24 == 1]
janeiro24 = janeiro24[janeiro24["SG_UF_MUN"] == "SP"]
janeiro24 = janeiro24[janeiro24["NO_MUN_MIN"] == cidade]
janeiro24_total = janeiro24["KG_LIQUIDO"].sum()

fev24 = ex24_df.loc[ex_mes_24 == 2]
fev24 = fev24[fev24["SG_UF_MUN"] == "SP"]
fev24 = fev24[fev24["NO_MUN_MIN"] == cidade]
fev24_total = fev24["KG_LIQUIDO"].sum()

mar24 = ex24_df.loc[ex_mes_24 == 3]
mar24 = mar24[mar24["SG_UF_MUN"] == "SP"]
mar24 = mar24[mar24["NO_MUN_MIN"] == cidade]
mar24_total = mar24["KG_LIQUIDO"].sum()

abr24 = ex24_df.loc[ex_mes_24 == 4]
abr24 = abr24[abr24["SG_UF_MUN"] == "SP"]
abr24 = abr24[abr24["NO_MUN_MIN"] == cidade]
abr24_total = abr24["KG_LIQUIDO"].sum()

mai24 = ex24_df.loc[ex_mes_24 == 5]
mai24 = mai24[mai24["SG_UF_MUN"] == "SP"]
mai24 = mai24[mai24["NO_MUN_MIN"] == cidade]
mai24_total = mai24["KG_LIQUIDO"].sum()

jun24 = ex24_df.loc[ex_mes_24 == 6]
jun24 = jun24[jun24["SG_UF_MUN"] == "SP"]
jun24 = jun24[jun24["NO_MUN_MIN"] == cidade]
jun24_total = jun24["KG_LIQUIDO"].sum()

jul24 = ex24_df.loc[ex_mes_24 == 7]
jul24 = jul24[jul24["SG_UF_MUN"] == "SP"]
jul24 = jul24[jul24["NO_MUN_MIN"] == cidade]
jul24_total = jul24["KG_LIQUIDO"].sum()

ago24 = ex24_df.loc[ex_mes_24 == 8]
ago24 = ago24[ago24["SG_UF_MUN"] == "SP"]
ago24 = ago24[ago24["NO_MUN_MIN"] == cidade]
ago24_total = ago24["KG_LIQUIDO"].sum()

set24 = ex24_df.loc[ex_mes_24 == 9]
set24 = set24[set24["SG_UF_MUN"] == "SP"]
set24 = set24[set24["NO_MUN_MIN"] == cidade]
set24_total = set24["KG_LIQUIDO"].sum()

out24 = ex24_df.loc[ex_mes_24 == 10]
out24 = out24[out24["SG_UF_MUN"] == "SP"]
out24 = out24[out24["NO_MUN_MIN"] == cidade]
out24_total = out24["KG_LIQUIDO"].sum()

nov24 = ex24_df.loc[ex_mes_24 == 11]
nov24 = nov24[nov24["SG_UF_MUN"] == "SP"]
nov24 = nov24[nov24["NO_MUN_MIN"] == cidade]
nov24_total = nov24["KG_LIQUIDO"].sum()

dez24 = ex24_df.loc[ex_mes_24 == 12]
dez24 = dez24[dez24["SG_UF_MUN"] == "SP"]
dez24 = dez24[dez24["NO_MUN_MIN"] == cidade]
dez24_total = dez24["KG_LIQUIDO"].sum()

#
# Parte dos gráficos para colocar os valores da tabela

import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline

# Definir os meses e valores fictícios
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
x = np.arange(len(meses))
valores = [janeiro24_total, fev24_total, mar24_total, abr24_total, mai24_total, jun24_total, jul24_total, ago24_total, set24_total, out24_total, nov24_total, dez24_total]

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