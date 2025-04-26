import pandas as pd

# Link dos arquivos CSV auxiliares
mun = 'https://balanca.economia.gov.br/balanca/bd/tabelas/UF_MUN.csv'
sh4 = 'https://balanca.economia.gov.br/balanca/bd/tabelas/NCM_SH.csv'
pais = 'https://balanca.economia.gov.br/balanca/bd/tabelas/PAIS.csv'

# Lendo os arquivos com o pandas
mun_df = pd.read_csv(mun, sep=";", usecols=['CO_MUN_GEO', 'NO_MUN_MIN'], encoding="latin1")
sh4_df = pd.read_csv(sh4, sep=";", usecols=['CO_SH4', 'NO_SH4_POR'], encoding="latin1")
pais_df = pd.read_csv(pais, sep=";", usecols=['CO_PAIS', 'NO_PAIS'], encoding="latin1")

# Renomeação de alguns campos dessas tabelas para melhor entendimento
mun_df = mun_df.rename(columns={"CO_MUN_GEO": "CO_MUN"})
sh4_df = sh4_df.rename(columns={"CO_SH4": "SH4", "NO_SH4_POR": "TIPO_CARGA"})

# Tabela de Exportações
resultado = []
for a in range(13, 24 + 1):  # de 2013 a 2024
    ex = f'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/EXP_20{a}_MUN.csv'
    print(f'Processando ano: 20{a}')

    try:
        for chunk in pd.read_csv(ex, sep=';', encoding='latin1', chunksize=100000):
            filtro = chunk[
                (chunk['SG_UF_MUN'] == 'SP') &
                (chunk['KG_LIQUIDO'] > 0) &
                (chunk['VL_FOB'] > 0) &
                (chunk['CO_PAIS'] != 0)
            ]

            # Merge com municípios
            filtro = filtro.merge(mun_df[['CO_MUN', 'NO_MUN_MIN']].drop_duplicates(), on='CO_MUN', how='left')

            # Merge com países
            filtro = filtro.merge(pais_df[['CO_PAIS', 'NO_PAIS']].drop_duplicates(), on='CO_PAIS', how='left')

            # Merge com tipo de carga
            filtro = filtro.merge(sh4_df[['SH4', 'TIPO_CARGA']].drop_duplicates(), on='SH4', how='left')

            # Calcula valor agregado
            filtro['VALOR_AGREGADO'] = filtro['VL_FOB'] / filtro['KG_LIQUIDO']
            filtro["VALOR_AGREGADO_FORMATADO"] = filtro["VALOR_AGREGADO"].apply(lambda x: f"{x:,.2f}")

            # Organiza as colunas porque organização é importante
            filtro.insert(filtro.columns.get_loc("CO_MUN") + 1, "NO_MUN_MIN", filtro.pop("NO_MUN_MIN"))
            filtro.insert(filtro.columns.get_loc("CO_PAIS") + 1, "NO_PAIS", filtro.pop("NO_PAIS"))
            filtro.insert(filtro.columns.get_loc("SH4") + 1, "TIPO_CARGA", filtro.pop("TIPO_CARGA"))

            resultado.append(filtro)

    except Exception as e:
        print(f'Erro no ano 20{a}:', e)

# Junta tudo no final, já limpo
ex_df = pd.concat(resultado, ignore_index=True)

# Tabela de Importações
resultado = []
for a in range(13, 24 + 1):  # de 2013 a 2024
    im = f'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/IMP_20{a}_MUN.csv'
    print(f'Processando ano: 20{a}')

    try:
        for chunk in pd.read_csv(ex, sep=';', encoding='latin1', chunksize=100000):
            filtro = chunk[
                (chunk['SG_UF_MUN'] == 'SP') &
                (chunk['KG_LIQUIDO'] > 0) &
                (chunk['VL_FOB'] > 0) &
                (chunk['CO_PAIS'] != 0)
            ]

            # Merge com municípios
            filtro = filtro.merge(mun_df[['CO_MUN', 'NO_MUN_MIN']].drop_duplicates(), on='CO_MUN', how='left')

            # Merge com países
            filtro = filtro.merge(pais_df[['CO_PAIS', 'NO_PAIS']].drop_duplicates(), on='CO_PAIS', how='left')

            # Merge com tipo de carga
            filtro = filtro.merge(sh4_df[['SH4', 'TIPO_CARGA']].drop_duplicates(), on='SH4', how='left')

            # Calcula valor agregado
            filtro['VALOR_AGREGADO'] = filtro['VL_FOB'] / filtro['KG_LIQUIDO']
            filtro["VALOR_AGREGADO_FORMATADO"] = filtro["VALOR_AGREGADO"].apply(lambda x: f"{x:,.2f}")

            # Organiza as colunas porque organização é importante
            filtro.insert(filtro.columns.get_loc("CO_MUN") + 1, "NO_MUN_MIN", filtro.pop("NO_MUN_MIN"))
            filtro.insert(filtro.columns.get_loc("CO_PAIS") + 1, "NO_PAIS", filtro.pop("NO_PAIS"))
            filtro.insert(filtro.columns.get_loc("SH4") + 1, "TIPO_CARGA", filtro.pop("TIPO_CARGA"))

            resultado.append(filtro)

    except Exception as e:
        print(f'Erro no ano 20{a}:', e)

# Junta tudo no final, já limpo
im_df = pd.concat(resultado, ignore_index=True)