from flask import render_template, Blueprint

route = Blueprint('route', __name__)

@route.route('/', methods=['GET'])
def index():
    return render_template('index.html') 

@route.route('/2019', methods=['GET'])
def index():
    return render_template('grafico2019.html')

@route.route('/2020', methods=['GET'])
def index():
    return render_template('grafico2020.html')

@route.route('/2021', methods=['GET'])
def index():
    return render_template('grafico2021.html')

@route.route('/2022', methods=['GET'])
def index():
    return render_template('grafico2022.html')

@route.route('/2023', methods=['GET'])
def index():
    return render_template('grafico2023.html')

@route.route('/2024', methods=['GET'])
def index():
    return render_template('grafico2024.html')
