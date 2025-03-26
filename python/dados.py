import pandas as pd

# importação das tabelas em CSV
mun = 'https://balanca.economia.gov.br/balanca/bd/tabelas/UF_MUN.csv'
sh4 = 'https://balanca.economia.gov.br/balanca/bd/tabelas/NCM_SH.csv'

# Criando a variável de cidade e de ano(primeiros filtro)
ano = 2024
cidade = "Pirapozinho"

if ano == 2024:
  # importação das tabelas em CSV
  ex = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/EXP_2024_MUN.csv'
  imp = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/IMP_2024_MUN.csv'
elif ano == 2023:
  # importação das tabelas em CSV
  ex = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/EXP_2023_MUN.csv'
  imp = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/IMP_2023_MUN.csv'
elif ano == 2022:
  # importação das tabelas em CSV
  ex = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/EXP_2022_MUN.csv'
  imp = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/IMP_2022_MUN.csv'
elif ano == 2021:
  # importação das tabelas em CSV
  ex = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/EXP_2021_MUN.csv'
  imp = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/IMP_2021_MUN.csv'
elif ano == 2020:
  # importação das tabelas em CSV
  ex = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/EXP_2020_MUN.csv'
  imp = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/IMP_2020_MUN.csv'
elif ano == 2019:
  # importação das tabelas em CSV
  ex = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/EXP_2019_MUN.csv'
  imp = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/IMP_2019_MUN.csv'

ex_df = pd.read_csv(ex, sep=";", encoding="latin1")
imp_df = pd.read_csv(imp, sep=";", encoding="latin1")
mun_df = pd.read_csv(mun, sep=";", encoding="latin1")
sh4_df = pd.read_csv(sh4, sep=";", encoding="latin1")

# Renomeando tabelas
mun_df = mun_df.rename(columns={"CO_MUN_GEO": "CO_MUN"})
sh4_df = sh4_df.rename(columns={"CO_SH4": "SH4", "NO_SH4_POR": "PRODUTO"})
ex_df = ex_df.merge(mun_df, on=["CO_MUN"], how="left")
imp_df = imp_df.merge(mun_df, on=["CO_MUN"], how="left")

# Criando variáveis de exportação
ex_mes_ = ex_df['CO_MES']
ex_sh4_ = ex_df['SH4']
ex_estado_ = ex_df['SG_UF_MUN']
ex_municipio_ = ex_df['CO_MUN']
ex_liquido_ = ex_df['KG_LIQUIDO']
ex_valorFob_ = ex_df['VL_FOB']

# Criando variáveis de importação
imp_mes_ = imp_df['CO_MES']
imp_sh4_ = imp_df['SH4']
imp_estado_ = imp_df['SG_UF_MUN']
imp_municipio_ = imp_df['CO_MUN']
imp_liquido_ = imp_df['KG_LIQUIDO']
imp_valorFob_ = imp_df['VL_FOB']


# Filtrar os dados por mês, estado, municipio e calcular o total de exportações de todos os meses
ex_janeiro = ex_df.loc[ex_mes_ == 1]
ex_janeiro = ex_janeiro[ex_janeiro["SG_UF_MUN"] == "SP"]
ex_janeiro = ex_janeiro[ex_janeiro["NO_MUN_MIN"] == cidade]
ex_janeiro_total = ex_janeiro["KG_LIQUIDO"].sum()

ex_fev = ex_df.loc[ex_mes_ == 2]
ex_fev = ex_fev[ex_fev["SG_UF_MUN"] == "SP"]
ex_fev = ex_fev[ex_fev["NO_MUN_MIN"] == cidade]
ex_fev_total = ex_fev["KG_LIQUIDO"].sum()

ex_mar = ex_df.loc[ex_mes_ == 3]
ex_mar = ex_mar[ex_mar["SG_UF_MUN"] == "SP"]
ex_mar = ex_mar[ex_mar["NO_MUN_MIN"] == cidade]
ex_mar_total = ex_mar["KG_LIQUIDO"].sum()

ex_abr = ex_df.loc[ex_mes_ == 4]
ex_abr = ex_abr[ex_abr["SG_UF_MUN"] == "SP"]
ex_abr = ex_abr[ex_abr["NO_MUN_MIN"] == cidade]
ex_abr_total = ex_abr["KG_LIQUIDO"].sum()

ex_mai = ex_df.loc[ex_mes_ == 5]
ex_mai = ex_mai[ex_mai["SG_UF_MUN"] == "SP"]
ex_mai = ex_mai[ex_mai["NO_MUN_MIN"] == cidade]
ex_mai_total = ex_mai["KG_LIQUIDO"].sum()

ex_jun = ex_df.loc[ex_mes_ == 6]
ex_jun = ex_jun[ex_jun["SG_UF_MUN"] == "SP"]
ex_jun = ex_jun[ex_jun["NO_MUN_MIN"] == cidade]
ex_jun_total = ex_jun["KG_LIQUIDO"].sum()

ex_jul = ex_df.loc[ex_mes_ == 7]
ex_jul = ex_jul[ex_jul["SG_UF_MUN"] == "SP"]
ex_jul = ex_jul[ex_jul["NO_MUN_MIN"] == cidade]
ex_jul_total = ex_jul["KG_LIQUIDO"].sum()

ex_ago = ex_df.loc[ex_mes_ == 8]
ex_ago = ex_ago[ex_ago["SG_UF_MUN"] == "SP"]
ex_ago = ex_ago[ex_ago["NO_MUN_MIN"] == cidade]
ex_ago_total = ex_ago["KG_LIQUIDO"].sum()

ex_set = ex_df.loc[ex_mes_ == 9]
ex_set = ex_set[ex_set["SG_UF_MUN"] == "SP"]
ex_set = ex_set[ex_set["NO_MUN_MIN"] == cidade]
ex_set_total = ex_set["KG_LIQUIDO"].sum()

ex_out = ex_df.loc[ex_mes_ == 10]
ex_out = ex_out[ex_out["SG_UF_MUN"] == "SP"]
ex_out = ex_out[ex_out["NO_MUN_MIN"] == cidade]
ex_out_total = ex_out["KG_LIQUIDO"].sum()

ex_nov = ex_df.loc[ex_mes_ == 11]
ex_nov = ex_nov[ex_nov["SG_UF_MUN"] == "SP"]
ex_nov = ex_nov[ex_nov["NO_MUN_MIN"] == cidade]
ex_nov_total = ex_nov["KG_LIQUIDO"].sum()

ex_dez = ex_df.loc[ex_mes_ == 12]
ex_dez = ex_dez[ex_dez["SG_UF_MUN"] == "SP"]
ex_dez = ex_dez[ex_dez["NO_MUN_MIN"] == cidade]
ex_dez_total = ex_dez["KG_LIQUIDO"].sum()

# Filtrar os dados por mês, estado, municipio e calcular o total de exportações de todos os meses
imp_janeiro = imp_df.loc[imp_mes_ == 1]
imp_janeiro = imp_janeiro[imp_janeiro["SG_UF_MUN"] == "SP"]
imp_janeiro = imp_janeiro[imp_janeiro["NO_MUN_MIN"] == cidade]
imp_janeiro_total = imp_janeiro["KG_LIQUIDO"].sum()

imp_fev = imp_df.loc[imp_mes_ == 2]
imp_fev = imp_fev[imp_fev["SG_UF_MUN"] == "SP"]
imp_fev = imp_fev[imp_fev["NO_MUN_MIN"] == cidade]
imp_fev_total = imp_fev["KG_LIQUIDO"].sum()

imp_mar = imp_df.loc[imp_mes_ == 3]
imp_mar = imp_mar[imp_mar["SG_UF_MUN"] == "SP"]
imp_mar = imp_mar[imp_mar["NO_MUN_MIN"] == cidade]
imp_mar_total = imp_mar["KG_LIQUIDO"].sum()

imp_abr = imp_df.loc[imp_mes_ == 4]
imp_abr = imp_abr[imp_abr["SG_UF_MUN"] == "SP"]
imp_abr = imp_abr[imp_abr["NO_MUN_MIN"] == cidade]
imp_abr_total = imp_abr["KG_LIQUIDO"].sum()

imp_mai = imp_df.loc[imp_mes_ == 5]
imp_mai = imp_mai[imp_mai["SG_UF_MUN"] == "SP"]
imp_mai = imp_mai[imp_mai["NO_MUN_MIN"] == cidade]
imp_mai_total = imp_mai["KG_LIQUIDO"].sum()

imp_jun = imp_df.loc[imp_mes_ == 6]
imp_jun = imp_jun[imp_jun["SG_UF_MUN"] == "SP"]
imp_jun = imp_jun[imp_jun["NO_MUN_MIN"] == cidade]
imp_jun_total = imp_jun["KG_LIQUIDO"].sum()

imp_jul = imp_df.loc[imp_mes_ == 7]
imp_jul = imp_jul[imp_jul["SG_UF_MUN"] == "SP"]
imp_jul = imp_jul[imp_jul["NO_MUN_MIN"] == cidade]
imp_jul_total = imp_jul["KG_LIQUIDO"].sum()

imp_ago = imp_df.loc[imp_mes_ == 8]
imp_ago = imp_ago[imp_ago["SG_UF_MUN"] == "SP"]
imp_ago = imp_ago[imp_ago["NO_MUN_MIN"] == cidade]
imp_ago_total = imp_ago["KG_LIQUIDO"].sum()

imp_set = imp_df.loc[imp_mes_ == 9]
imp_set = imp_set[imp_set["SG_UF_MUN"] == "SP"]
imp_set = imp_set[imp_set["NO_MUN_MIN"] == cidade]
imp_set_total = imp_set["KG_LIQUIDO"].sum()

imp_out = imp_df.loc[imp_mes_ == 10]
imp_out = imp_out[imp_out["SG_UF_MUN"] == "SP"]
imp_out = imp_out[imp_out["NO_MUN_MIN"] == cidade]
imp_out_total = imp_out["KG_LIQUIDO"].sum()

imp_nov = imp_df.loc[imp_mes_ == 11]
imp_nov = imp_nov[imp_nov["SG_UF_MUN"] == "SP"]
imp_nov = imp_nov[imp_nov["NO_MUN_MIN"] == cidade]
imp_nov_total = imp_nov["KG_LIQUIDO"].sum()

imp_dez = imp_df.loc[imp_mes_ == 12]
imp_dez = imp_dez[imp_dez["SG_UF_MUN"] == "SP"]
imp_dez = imp_dez[imp_dez["NO_MUN_MIN"] == cidade]
imp_dez_total = imp_dez["KG_LIQUIDO"].sum()

#
# Parte dos gráficos para colocar os valores da tabela

import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline

# Definir os meses e valores fictícios
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
x = np.arange(len(meses))
valores = [ex_janeiro_total, ex_fev_total, ex_mar_total, ex_abr_total, ex_mai_total, ex_jun_total, ex_jul_total, ex_ago_total, ex_set_total, ex_out_total, ex_nov_total, ex_dez_total]

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