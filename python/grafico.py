# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from scipy.interpolate import make_interp_spline

# # Definir os meses e valores fictícios
# meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
# x = np.arange(len(meses))
# valores = [50000, 120000, 200000, 150000, 10000, 70000, 50000, 30000, 8000, 16000, 14000, 100000]

# # Criar valores interpolados para suavizar a curva
# x_smooth = np.linspace(x.min(), x.max(), 300)
# spline = make_interp_spline(x, valores, k=3)
# y_smooth = spline(x_smooth)

# # Estilizar gráfico
# sns.set_style("dark")
# plt.figure(figsize=(10, 5), facecolor='#0B0121')
# ax = plt.gca()
# ax.set_facecolor('#0B0121')

# # Plotar linha suavizada
# plt.plot(x_smooth, y_smooth, color='white', linestyle='-', linewidth=2)

# # Adicionar pontos principais
# plt.scatter(x, valores, color='white', edgecolors='black', zorder=3)

# # Configurar rótulos
# plt.xticks(x, meses, color='white')
# plt.yticks(np.arange(0, 210000, 10000), color='white')  # Aumentar os números no eixo Y
# plt.ylim(0, 210000)  # Ajustar o limite do eixo Y
# plt.grid(True, which='major', linestyle='--', linewidth=0.5, color='gray', alpha=0.5)  # Adicionar linhas horizontais

# # Exibir gráfico
# plt.savefig("./img/grafico.png")

import numpy as np
import plotly.graph_objects as go

# Definir os meses e valores fictícios
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
x = np.arange(len(meses))
valores = [50000, 120000, 200000, 150000, 10000, 70000, 50000, 30000, 8000, 16000, 14000, 100000]

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
fig.write_html("grafico_interativo.html")


