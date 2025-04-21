from flask import Blueprint, render_template
from conexao import grafico, tabela 
# arrumar a conexão com o banco de dados para pegar o grafico e tabela

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def home():
    tabela = tabela.query.all()
    grafico = grafico.query.all()
    return render_template('index.html', grafico=grafico, tabela=tabela)
