from flask import Flask, render_template
import pandas as pd

dados = pd.read_csv('lista_exemplo.csv')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)