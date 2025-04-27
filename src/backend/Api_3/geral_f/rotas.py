import os
from flask import Blueprint, render_template

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho CORRETO para os estáticos (onde o Flask já procura)
static_dir = os.path.join(base_dir, 'static')  # Agora aponta para api_3/static/

index_bp = Blueprint('index', __name__,
                    template_folder=os.path.join(base_dir, '../../frontend/templates'),
                    static_folder=static_dir,  # Mudei para usar o caminho local
                    static_url_path='/static')  # Mantém como '/static'

@index_bp.route('/')
def home():
    try:
        grafico_path = os.path.join(static_dir, 'grafico_export_import.html')
        tabela_path = os.path.join(static_dir, 'exportacoes_tabela.html')
        
        print(f"Arquivos em static_dir: {os.listdir(static_dir)}")  # Debug
        
        with open(grafico_path, encoding='utf-8') as f:
            grafico_html = f.read()
            
        with open(tabela_path, encoding='utf-8') as f:
            tabela_html = f.read()
            
        return render_template("index.html", grafico=grafico_html, tabela=tabela_html)
        
    except Exception as e:
        return f"Erro: {str(e)}", 500