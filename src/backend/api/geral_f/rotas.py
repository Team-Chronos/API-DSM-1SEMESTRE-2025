from flask import render_template
import pandas as pd
from sqlalchemy.sql import text
import plotly.graph_objects as go
import plotly
import json
from .banco import get_db_engine, generate_sample_data


def configurar_rotas(app):

    @app.route('/teste')
    def testar():
        tabelas = 'oi'
        try:
            engine = get_db_engine()
            if engine:
                with engine.connect() as conn:
                    tabelas = pd.read_sql(text("SHOW TABLES"), conn)
                    if 'exportacao' not in tabelas.values or 'importacao' not in tabelas.values:
                        tabela_dados = generate_sample_data()
                    else:
                        tabela_dados = pd.read_sql(text("""
                            select CO_ANO, sum(VL_FOB)/sum(KG_LIQUIDO) AS VALOR_AGREGADO_TOTAL FROM exportacao group by CO_ANO;
                        """), conn).to_dict('records')
        except Exception as e:
            print(f"Erro ao obter dados: {e}")
        return render_template("teste.html", testeBanco = tabela_dados)

    @app.route('/')
    def index():
        ano_selecionado = 2023
        municipio_selecionado = 'São Paulo'
        estado_selecionado = 'São Paulo'

        try:
            engine = get_db_engine()
            if engine:
                with engine.connect() as conn:
                    tabelas = pd.read_sql(text("SHOW TABLES"), conn)
                    if 'exportacao' not in tabelas.values or 'importacao' not in tabelas.values:
                        tabela_dados, top_cargas = generate_sample_data()
                    else:
                        tabela_dados = pd.read_sql(text("""
                            SELECT CO_NCM as codigo, TIPO_CARGA as produto, 
                                   CONCAT(NO_MUN_MIN, ' - ', SG_UF_NCM) as municipio,
                                   CONCAT('R$ ', FORMAT(VL_FOB, 2, 'de_DE')) as valor
                            FROM exportacoes
                            WHERE YEAR(CO_DATA) = :ano AND NO_MUN_MIN = :municipio AND SG_UF_NCM = :estado
                            LIMIT 5
                        """), conn, params={
                            'ano': ano_selecionado,
                            'municipio': municipio_selecionado,
                            'estado': estado_selecionado
                        }).to_dict('records')

                        top_cargas = pd.read_sql(text("""
                            SELECT 
                                TIPO_CARGA,
                                CONCAT('R$ ', FORMAT(SUM(VL_FOB), 2, 'de_DE')) as valor_total,
                                COUNT(DISTINCT NO_PAIS) as num_paises,
                                CONCAT(FORMAT(SUM(KG_LIQUIDO), 2, 'de_DE'), ' kg') as kg_total
                            FROM exportacoes
                            WHERE YEAR(CO_DATA) = :ano AND NO_MUN_MIN = :municipio AND SG_UF_NCM = :estado
                            GROUP BY TIPO_CARGA ORDER BY SUM(VL_FOB) DESC LIMIT 5
                        """), conn, params={
                            'ano': ano_selecionado,
                            'municipio': municipio_selecionado,
                            'estado': estado_selecionado
                        }).to_dict('records')
            else:
                tabela_dados, top_cargas = generate_sample_data()
        except Exception as e:
            print(f"Erro ao obter dados: {e}")
            tabela_dados, top_cargas = generate_sample_data()

        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        exportacoes = [i * 1000000 for i in range(1, 13)]
        importacoes = [i * 800000 for i in range(1, 13)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=exportacoes, mode='lines+markers', name='Exportações'))
        fig.add_trace(go.Scatter(x=meses, y=importacoes, mode='lines+markers', name='Importações'))
        fig.update_layout(
            title='Exportações e Importações Mensais',
            xaxis_title='Mês',
            yaxis_title='Valor (R$)',
            template='plotly_white'
        )
        grafico_linha = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        context = {
            'titulo': "Estatísticas de Comércio Exterior",
            'municipio_selecionado': municipio_selecionado,
            'ano_selecionado': ano_selecionado,
            'meses': meses,
            'exportacoes': exportacoes,
            'importacoes': importacoes,
            'tabela_dados': tabela_dados,
            'top_cargas': top_cargas,
            'grafico_linha': grafico_linha,
            'municipios': [
    'Adamantina', 'Adolfo', 'Aguaí', 'Águas da Prata', 'Águas de Lindóia',
    'Águas de Santa Bárbara', 'Águas de São Pedro', 'Agudos', 'Alambari', 'Alfredo Marcondes',
    'Altair', 'Altinópolis', 'Alto Alegre', 'Alumínio', 'Álvares Florence',
    'Álvares Machado', 'Álvaro de Carvalho', 'Alvinlândia', 'Americana', 'Américo Brasiliense',
    'Américo de Campos', 'Amparo', 'Analândia', 'Andradina', 'Angatuba',
    'Anhembi', 'Anhumas', 'Aparecida', 'Aparecida d\'Oeste', 'Apiaí',
    'Araçariguama', 'Araçatuba', 'Araçoiaba da Serra', 'Aramina', 'Arandu',
    'Arapeí', 'Araraquara', 'Araras', 'Arco-Íris', 'Arealva',
    'Areias', 'Areiópolis', 'Ariranha', 'Artur Nogueira', 'Arujá',
    'Aspásia', 'Assis', 'Atibaia', 'Auriflama', 'Avaí',
    'Avanhandava', 'Avaré', 'Bady Bassitt', 'Balbinos', 'Bálsamo',
    'Bananal', 'Barão de Antonina', 'Barbosa', 'Bariri', 'Barra Bonita',
    'Barra do Chapéu', 'Barra do Turvo', 'Barretos', 'Barrinha', 'Barueri',
    'Bastos', 'Batatais', 'Bauru', 'Bebedouro', 'Bento de Abreu',
    'Bernardino de Campos', 'Bertioga', 'Bilac', 'Birigui', 'Biritiba-Mirim',
    'Boa Esperança do Sul', 'Bocaina', 'Bofete', 'Boituva', 'Bom Jesus dos Perdões',
    'Bom Sucesso de Itararé', 'Borá', 'Boracéia', 'Borborema', 'Borebi',
    'Botucatu', 'Bragança Paulista', 'Braúna', 'Brejo Alegre', 'Brodowski',
    'Brotas', 'Buri', 'Buritama', 'Buritizal', 'Cabrália Paulista',
    'Cabreúva', 'Caçapava', 'Cachoeira Paulista', 'Caconde', 'Cafelândia',
    'Caiabu', 'Caieiras', 'Caiuá', 'Cajamar', 'Cajati','Cajobi', 'Cajuru', 'Campina do Monte Alegre', 'Campinas', 'Campo Limpo Paulista',
    'Campos do Jordão', 'Campos Novos Paulista', 'Cananéia', 'Canas', 'Cândido Mota',
    'Cândido Rodrigues', 'Canitar', 'Capão Bonito', 'Capela do Alto', 'Capivari',
    'Caraguatatuba', 'Carapicuíba', 'Cardoso', 'Casa Branca', 'Cássia dos Coqueiros',
    'Castilho', 'Catanduva', 'Catiguá', 'Cedral', 'Cerqueira César',
    'Cerquilho', 'Cesário Lange', 'Charqueada', 'Chavantes', 'Clementina',
    'Colina', 'Colômbia', 'Conchal', 'Conchas', 'Cordeirópolis',
    'Coroados', 'Coronel Macedo', 'Corumbataí', 'Cosmópolis', 'Cosmorama',
    'Cotia', 'Cravinhos', 'Cristais Paulista', 'Cruzália', 'Cruzeiro',
    'Cubatão', 'Cunha', 'Descalvado', 'Diadema', 'Dirce Reis',
    'Divinolândia', 'Dobrada', 'Dois Córregos', 'Dolcinópolis', 'Dourado',
    'Dracena', 'Duartina', 'Dumont', 'Echaporã', 'Eldorado',
    'Elias Fausto', 'Elisiário', 'Embaúba', 'Embu das Artes', 'Embu-Guaçu',
    'Emilianópolis', 'Engenheiro Coelho', 'Espírito Santo do Pinhal', 'Espírito Santo do Turvo', 'Estiva Gerbi',
    'Estrela d\'Oeste', 'Estrela do Norte', 'Euclides da Cunha Paulista', 'Fartura', 'Fernandópolis',
    'Fernando Prestes', 'Fernão', 'Ferraz de Vasconcelos', 'Flora Rica', 'Floreal',
    'Florínea', 'Franca', 'Francisco Morato', 'Franco da Rocha', 'Gabriel Monteiro',
    'Gália', 'Garça', 'Gastão Vidigal', 'Gavião Peixoto', 'General Salgado',
    'Getulina', 'Glicério', 'Guaiçara', 'Guaimbê', 'Guaíra',
    'Guapiaçu', 'Guapiara', 'Guará', 'Guaraçaí', 'Guaraci',
    'Guarani d\'Oeste', 'Guarantã', 'Guararapes', 'Guararema', 'Guaratinguetá','Guareí', 'Guariba', 'Guarujá', 'Guarulhos', 'Guatapará',
    'Guzolândia', 'Herculândia', 'Holambra', 'Hortolândia', 'Iacanga',
    'Iacri', 'Iaras', 'Ibaté', 'Ibirá', 'Ibirarema',
    'Ibitinga', 'Ibiúna', 'Icém', 'Iepê', 'Igaraçu do Tietê',
    'Igarapava', 'Igaratá', 'Iguape', 'Ilha Comprida', 'Ilha Solteira',
    'Ilhabela', 'Indaiatuba', 'Indiana', 'Indiaporã', 'Inúbia Paulista',
    'Ipaussu', 'Iperó', 'Ipeúna', 'Ipiguá', 'Iporanga',
    'Ipuã', 'Iracemápolis', 'Irapuã', 'Irapuru', 'Itaberá',
    'Itaí', 'Itajobi', 'Itaju', 'Itanhaém', 'Itaóca',
    'Itapecerica da Serra', 'Itapetininga', 'Itapeva', 'Itapevi', 'Itapira',
    'Itapirapuã Paulista', 'Itápolis', 'Itaporanga', 'Itapuí', 'Itapura',
    'Itaquaquecetuba', 'Itararé', 'Itariri', 'Itatiba', 'Itatinga',
    'Itirapina', 'Itirapuã', 'Itobi', 'Itu', 'Itupeva',
    'Ituverava', 'Jaborandi', 'Jaboticabal', 'Jacareí', 'Jaci',
    'Jacupiranga', 'Jaguariúna', 'Jales', 'Jambeiro', 'Jandira',
    'Jardinópolis', 'Jarinu', 'Jaú', 'Jeriquara', 'Joanópolis',
    'João Ramalho', 'José Bonifácio', 'Júlio Mesquita', 'Jumirim', 'Jundiaí',
    'Junqueirópolis', 'Juquiá', 'Juquitiba', 'Lagoinha', 'Laranjal Paulista',
    'Lavínia', 'Lavrinhas', 'Leme', 'Lençóis Paulista', 'Limeira',
    'Lindóia', 'Lins', 'Lorena', 'Lourdes', 'Louveira',
    'Lucélia', 'Lucianópolis', 'Luís Antônio', 'Luiziânia', 'Lupércio','Lutécia', 'Macatuba', 'Macaubal', 'Macedônia', 'Magda',
    'Mairinque', 'Mairiporã', 'Manduri', 'Marabá Paulista', 'Maracaí',
    'Marapoama', 'Mariápolis', 'Marília', 'Marinópolis', 'Martinópolis',
    'Matão', 'Mauá', 'Mendonça', 'Meridiano', 'Mesópolis',
    'Miguelópolis', 'Mineiros do Tietê', 'Mira Estrela', 'Miracatu', 'Mirandópolis',
    'Mirante do Paranapanema', 'Mirassol', 'Mirassolândia', 'Mococa', 'Mogi das Cruzes',
    'Mogi Guaçu', 'Moji Mirim', 'Mombuca', 'Monções', 'Mongaguá',
    'Monte Alegre do Sul', 'Monte Alto', 'Monte Aprazível', 'Monte Azul Paulista', 'Monte Castelo',
    'Monte Mor', 'Monteiro Lobato', 'Morro Agudo', 'Morungaba', 'Motuca',
    'Murutinga do Sul', 'Nantes', 'Narandiba', 'Natividade da Serra', 'Nazaré Paulista',
    'Neves Paulista', 'Nhandeara', 'Nipoã', 'Nova Aliança', 'Nova Campina',
    'Nova Canaã Paulista', 'Nova Castilho', 'Nova Europa', 'Nova Granada', 'Nova Guataporanga',
    'Nova Independência', 'Nova Luzitânia', 'Nova Odessa', 'Novais', 'Novo Horizonte',
    'Nuporanga', 'Ocauçu', 'Óleo', 'Olímpia', 'Onda Verde',
    'Oriente', 'Orindiúva', 'Orlândia', 'Osasco', 'Oscar Bressane',
    'Osvaldo Cruz', 'Ourinhos', 'Ouro Verde', 'Ouroeste', 'Pacaembu',
    'Palestina', 'Palmares Paulista', 'Palmeira d\'Oeste', 'Palmital', 'Panorama',
    'Paraguaçu Paulista', 'Paraibuna', 'Paraíso', 'Paranapanema', 'Paranapuã',
    'Parapuã', 'Pardinho', 'Pariquera-Açu', 'Parisi', 'Patrocínio Paulista',
    'Paulicéia', 'Paulínia', 'Paulistânia', 'Paulo de Faria', 'Pederneiras',
    'Pedra Bela', 'Pedranópolis', 'Pedregulho', 'Pedreira', 'Pedrinhas Paulista','Pedro de Toledo', 'Penápolis', 'Pereira Barreto', 'Pereiras', 'Peruíbe',
    'Piacatu', 'Piedade', 'Pilar do Sul', 'Pindamonhangaba', 'Pindorama',
    'Pinhalzinho', 'Piquerobi', 'Piquete', 'Piracaia', 'Piracicaba',
    'Piraju', 'Pirajuí', 'Pirangi', 'Pirapora do Bom Jesus', 'Pirapozinho',
    'Pirassununga', 'Piratininga', 'Pitangueiras', 'Planalto', 'Platina',
    'Poá', 'Poloni', 'Pompéia', 'Pongaí', 'Pontal',
    'Pontalinda', 'Pontes Gestal', 'Populina', 'Porangaba', 'Porto Feliz',
    'Porto Ferreira', 'Potim', 'Potirendaba', 'Pracinha', 'Pradópolis',
    'Praia Grande', 'Pratânia', 'Presidente Alves', 'Presidente Bernardes', 'Presidente Epitácio',
    'Presidente Prudente', 'Presidente Venceslau', 'Promissão', 'Quadra', 'Quatá',
    'Queiroz', 'Queluz', 'Quintana', 'Rafard', 'Rancharia',
    'Redenção da Serra', 'Regente Feijó', 'Reginópolis', 'Registro', 'Restinga',
    'Ribeira', 'Ribeirão Bonito', 'Ribeirão Branco', 'Ribeirão Corrente', 'Ribeirão do Sul',
    'Ribeirão dos Índios', 'Ribeirão Grande', 'Ribeirão Pires', 'Ribeirão Preto', 'Rifaina',
    'Rincão', 'Rinópolis', 'Rio Claro', 'Rio das Pedras', 'Rio Grande da Serra',
    'Riolândia', 'Riversul', 'Rosana', 'Roseira', 'Rubiácea',
    'Rubinéia', 'Sabino', 'Sagres', 'Sales', 'Sales Oliveira',
    'Salesópolis', 'Salmourão', 'Saltinho', 'Salto', 'Salto de Pirapora',
    'Salto Grande', 'Sandovalina', 'Santa Adélia', 'Santa Albertina', 'Santa Bárbara d\'Oeste',
    'Santa Branca', 'Santa Clara d\'Oeste', 'Santa Cruz da Conceição', 'Santa Cruz da Esperança', 'Santa Cruz das Palmeiras',
    'Santa Cruz do Rio Pardo', 'Santa Ernestina', 'Santa Fé do Sul', 'Santa Gertrudes', 'Santa Isabel',
    'Santa Lúcia', 'Santa Maria da Serra', 'Santa Mercedes', 'Santa Rita d\'Oeste', 'Santa Rita do Passa Quatro','Santa Rosa de Viterbo', 'Santa Salete', 'Santana da Ponte Pensa', 'Santana de Parnaíba', 'Santo Anastácio',
    'Santo André', 'Santo Antônio da Alegria', 'Santo Antônio de Posse', 'Santo Antônio do Aracanguá', 'Santo Antônio do Jardim',
    'Santo Antônio do Pinhal', 'Santo Expedito', 'Santópolis do Aguapeí', 'Santos', 'São Bento do Sapucaí',
    'São Bernardo do Campo', 'São Caetano do Sul', 'São Carlos', 'São Francisco', 'São João da Boa Vista',
    'São João das Duas Pontes', 'São João de Iracema', 'São João do Pau d\'Alho', 'São Joaquim da Barra', 'São José da Bela Vista',
    'São José do Barreiro', 'São José do Rio Pardo', 'São José do Rio Preto', 'São José dos Campos', 'São Lourenço da Serra',
    'São Luiz do Paraitinga', 'São Manuel', 'São Miguel Arcanjo', 'São Paulo', 'São Pedro',
    'São Pedro do Turvo', 'São Roque', 'São Sebastião', 'São Sebastião da Grama', 'São Simão',
    'São Vicente', 'Sarapuí', 'Sarutaiá', 'Sebastianópolis do Sul', 'Serra Azul',
    'Serra Negra', 'Serrana', 'Sertãozinho', 'Sete Barras', 'Severínia',
    'Silveiras', 'Socorro', 'Sorocaba', 'Sud Mennucci', 'Sumaré',
    'Suzanápolis', 'Suzano', 'Tabapuã', 'Tabatinga', 'Taboão da Serra',
    'Taciba', 'Taguaí', 'Taiaçu', 'Taiúva', 'Tambaú',
    'Tanabi', 'Tapiraí', 'Tapiratiba', 'Taquaral', 'Taquaritinga',
    'Taquarituba', 'Taquarivaí', 'Tarabai', 'Tarumã', 'Tatuí',
    'Taubaté', 'Tejupá', 'Teodoro Sampaio', 'Terra Roxa', 'Tietê',
    'Timburi', 'Torre de Pedra', 'Torrinha', 'Trabiju', 'Tremembé',
    'Três Fronteiras', 'Tuiuti', 'Tupã', 'Tupi Paulista', 'Turiúba',
    'Turmalina', 'Ubarana', 'Ubatuba', 'Ubirajara', 'Uchoa',
    'União Paulista', 'Urânia', 'Uru', 'Urupês', 'Valentim Gentil','Valinhos', 'Valparaíso', 'Vargem', 'Vargem Grande do Sul', 'Vargem Grande Paulista',
    'Várzea Paulista', 'Vera Cruz', 'Vinhedo', 'Viradouro', 'Vista Alegre do Alto',
    'Vitória Brasil', 'Votorantim', 'Votuporanga', 'Zacarias'
]
,
            'anos': list(range(2013, 2025))
        }

        return render_template('index.html', **context)
