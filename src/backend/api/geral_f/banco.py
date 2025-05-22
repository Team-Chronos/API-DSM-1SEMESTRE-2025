from sqlalchemy import create_engine
import pandas as pd

DB_CONFIG = {
    'usuario': 'admin',
    'senha': 'APIdsm2025',
    'host': 'db-comercio-sp.coode8ymmacx.us-east-1.rds.amazonaws.com',
    'porta': '3306',
    'banco': 'db_comercio_sp'
}

def get_db_engine():
    try:
        engine = create_engine(
            f"mysql+pymysql://{DB_CONFIG['usuario']}:{DB_CONFIG['senha']}@{DB_CONFIG['host']}:{DB_CONFIG['porta']}/{DB_CONFIG['banco']}"
        )
        return engine
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def generate_sample_data():
    tabela_dados = [
        {'codigo': '854231', 'produto': 'Circuitos Integrados Eletrônicos', 'municipio': 'São Paulo - SP', 'valor': 'R$ 12.450.000,00'},
        {'codigo': '870322', 'produto': 'Automóveis de Passageiros', 'municipio': 'São José dos Campos - SP', 'valor': 'R$ 8.730.500,00'},
        {'codigo': '300490', 'produto': 'Medicamentos para Tratamento', 'municipio': 'Campinas - SP', 'valor': 'R$ 6.920.300,00'},
        {'codigo': '847130', 'produto': 'Computadores Portáteis', 'municipio': 'São Paulo - SP', 'valor': 'R$ 5.410.200,00'},
        {'codigo': '271019', 'produto': 'Óleos de Petróleo', 'municipio': 'Santos - SP', 'valor': 'R$ 4.980.600,00'}
    ]
    top_cargas = [
        {'TIPO_CARGA': 'Circuitos Integrados', 'valor_total': 'R$ 58.200.000,00', 'num_paises': 15, 'kg_total': '1.250.000 kg'},
        {'TIPO_CARGA': 'Veículos Automotores', 'valor_total': 'R$ 42.750.000,00', 'num_paises': 12, 'kg_total': '3.450.000 kg'},
        {'TIPO_CARGA': 'Produtos Farmacêuticos', 'valor_total': 'R$ 32.180.000,00', 'num_paises': 8, 'kg_total': '850.000 kg'},
        {'TIPO_CARGA': 'Equipamentos de TI', 'valor_total': 'R$ 28.950.000,00', 'num_paises': 10, 'kg_total': '1.120.000 kg'},
        {'TIPO_CARGA': 'Derivados de Petróleo', 'valor_total': 'R$ 25.430.000,00', 'num_paises': 6, 'kg_total': '5.780.000 kg'}
    ]
    return tabela_dados, top_cargas
