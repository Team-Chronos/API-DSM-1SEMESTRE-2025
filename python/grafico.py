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


