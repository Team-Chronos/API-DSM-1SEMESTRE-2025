from flask_sqlalchemy import SQLAlchemy
import pandas as pd

db = SQLAlchemy()

class Exportacao(db.Model):
    __tablename__ = 'exportacoes'
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer)
    uf = db.Column(db.String(2))
    co_mun = db.Column(db.Integer)
    co_pais = db.Column(db.Integer)
    sh4 = db.Column(db.String(10))
    valor_fob = db.Column(db.Float)
    kg_liquido = db.Column(db.Float)

class Importacao(db.Model):
    __tablename__ = 'importacoes'
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer)
    uf = db.Column(db.String(2))
    co_mun = db.Column(db.Integer)
    co_pais = db.Column(db.Integer)
    sh4 = db.Column(db.String(10))
    valor_fob = db.Column(db.Float)
    kg_liquido = db.Column(db.Float)

class Municipio(db.Model):
    __tablename__ = 'municipios'
    co_mun = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))

class Pais(db.Model):
    __tablename__ = 'paises'
    co_pais = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))

class TipoCarga(db.Model):
    __tablename__ = 'tipos_carga'
    sh4 = db.Column(db.String(10), primary_key=True)
    tipo = db.Column(db.String(100))

def processar_dados(df, mun_df, pais_df, tipo_df):
    df = df.rename(columns={'co_mun': 'CO_MUN', 'co_pais': 'CO_PAIS', 'sh4': 'SH4'})
    df = df.merge(mun_df, on='CO_MUN', how='left')
    df = df.merge(pais_df, on='CO_PAIS', how='left')
    df = df.merge(tipo_df, on='SH4', how='left')
    df['VALOR_AGREGADO'] = df['valor_fob'] / df['kg_liquido']
    df['VALOR_AGREGADO_FORMATADO'] = df['VALOR_AGREGADO'].apply(lambda x: f"{x:,.2f}")
    return df

def calcular_totais_mensais(df, cidade, uf='SP'):
    df = df[(df['uf'] == uf) & (df['NO_MUN_MIN'] == cidade)]
    if 'mes' not in df.columns:
        df['mes'] = pd.to_datetime(df['ano'].astype(str), errors='coerce').dt.month.fillna(1).astype(int)
    totais = df.groupby('mes')['kg_liquido'].sum().reindex(range(1, 13), fill_value=0)
    return totais.tolist()
