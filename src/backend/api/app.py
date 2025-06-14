from flask import Flask
from geral_f.rotas import configurar_rotas
import os
import atexit
from geral_f.banco import close_db_engine

base_dir = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.abspath(os.path.join(base_dir, '../../frontend/static'))
template_dir = os.path.abspath(os.path.join(base_dir, '../../frontend/templates'))

app = Flask(__name__, 
            template_folder=template_dir, 
            static_folder=static_dir, 
            static_url_path='/static')

atexit.register(close_db_engine)

configurar_rotas(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)