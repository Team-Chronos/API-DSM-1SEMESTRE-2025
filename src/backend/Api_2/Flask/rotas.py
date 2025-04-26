from flask import Blueprint, render_template
import os

base_direcao = os.path.abspath(os.path.dirname(__file__))
template_direcao = os.path.abspath('../../frontend/templates')
static_direcao = os.path.join(base_direcao, '../../frontend/static')

index_bp = Blueprint( __name__, template_folder=template_direcao, static_folder=static_direcao)

@index_bp.route('/')
def home():

    with open('grafico_export_import.html', encoding='utf-8') as f:
        grafico_html = f.read()

    with open('exportacoes_tabela.html', encoding='utf-8') as f:
        tabela_html = f.read()

    return render_template('index.html', grafico=grafico_html, tabela=tabela_html)
