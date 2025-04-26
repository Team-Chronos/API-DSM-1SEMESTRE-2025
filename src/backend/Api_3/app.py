from geral_f.banco import create_app
from geral_f.processamento import gerar_graficos


app = create_app()
gerar_graficos(app)


if __name__ == "__main__":
    app.run(debug=True)
