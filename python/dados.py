import pandas as pd

ex2024 = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/EXP_2024_MUN.csv'

ex2024_df = pd.read_csv(ex2024, sep=";", encoding="latin1")
display(ex2024_df)