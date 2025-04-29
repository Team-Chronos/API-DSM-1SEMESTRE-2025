# API - Primeiro Semestre de DSM

> Status: Em desenvolvimento ⚠️👷🏼 

Este projeto é uma API (Aprendizado por Projetos Integrados) desenvolvida durante o primeiro semestre do curso de Desenvolvimento de Software Multiplataforma da Fatec de São José dos Campos para monitoramento de tendências do mercado de importação e exportação no estado de São Paulo. Este projeto utiliza a metodologia ágil SCRUM, garantindo um desenvolvimento iterativo e colaborativo, tarefas organizadas em sprints, seguindo as prioridades definidas em um backlog estruturado com funcionalidades priorizadas.

<br>

## 📝 Índice
* <a href='#projeto'> Sobre o Projeto </a>
* <a href='#requisitos'> Requisitos </a>
* <a href='#tecnologias'> Tecnologias Utilizadas </a>
* <a href='#calendario'> Calendário da API </a>
* <a href='#sprints'> Sprints </a>
* <a href='#prototipo'> Protótipo </a>
* <a href='#colab'> Colab </a>
* <a href='#backlog'> Backlog do Produto </a>
* <a href='#equipe'> Equipe </a>

<br>

<span id='projeto'>

## 📍 Sobre o Projeto

O objetivo do projeto é fornecer uma solução eficiente para monitorar as tendências de mercado (importação e exportação de produtos) específicas do estado de São Paulo, permitindo que usuários acessem e analisem dados de forma intuitiva e prática. A API oferece funcionalidades que facilitam a visualização de diversos dados como conteúdo, peso e caminho feito pela carga de cada município e comparar com outros produtos do mesmo município ou comparar o mesmo produto de duas cidades diferentes.

</span>

<br>
 
<span id="requisitos">

## 📋 Requisitos
> **Requisitos Funcionais**

* Desenvolver visualizações gráficas contendo segmentação por município. 

* Desenvolver uma interface de dados contendo as principais cargas movimentadas.

* Desenvolver uma visualização gráfica de um ranking por valor agregado de exportação e importação.

* Desenvolver uma interface de dados contendo a evoluçao histórica da balança comercial.

* Desenvolver visualizações gráficas com busca e filtros.

* Desenvolver interface de dados contendo um painel de estatísticas.
 
<br>

> **Requisitos Não-Funcionais**

* Uso de colab e site do governo para dados. 

* Desenvolvimento do back-end com a linguagem Python 3+ e micro framework Flask.

* Utilizar sistema gerenciador de banco de MariaDM/MySQL.

* Utilizar HTML 5 para arquitetura da informação.

* Utilizar CSS 3 para estilização do layout.

* Utilizar GitHub para controle de versão dos artefatos de projeto.

* Interface com navegação intuitiva.

* Interface responsiva.

* Evitar de usar framework de mapeamento para implementar as operações em banco de dados.

</span>

<br>

<span id='tecnologias'>

## 🛠️ Tecnologias Utilizadas

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![FIGMA](https://img.shields.io/badge/Figma-0D1117?style=for-the-badge&logo=figma) ![GitHub](https://img.shields.io/badge/GitHub-111217?style=for-the-badge&logo=github&logoColor=white)

</span>

<br>

<span id='calendario'>

## 📆 Calendário da API

<table>
        <tr>
            <th>
                Sprint
            </th>
            <th>
                Previsão
            </th>
            <th>
                Status
            </th>
        </tr>
        <tr>
            <td>
                <h5>Kick-Off geral</h5>
            </td>
            <td>
                <h5>24/02/2025 - 28/02/2025</h5>
            </td>
            <td>
                <h5>Concluído</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>01</h5>
            </td>
            <td>
                <h5>10/03/2025 - 30/03/2025</h5>
            </td>
            <td>
                <h5>Concluído</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Review/Planning</h5>
            </td>
            <td>
                <h5>31/03/2025 - 04/04/2025</h5>
            </td>
            <td>
                <h5>Concluído</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>02</h5>
            </td>
            <td>
                <h5>07/04/2025 - 27/04/2025</h5>
            </td>
            <td>
                <h5>Concluído</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Review/Planning</h5>
            </td>
            <td>
                <h5>28/04/2025 - 02/05/2025</h5>
            </td>
            <td>
                <h5>Não Iniciado</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>03</h5>
            </td>
            <td>
                <h5>05/05/2025 - 25/05/2025</h5>
            </td>
            <td>
                <h5>Não Iniciado</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Review</h5>
            </td>
            <td>
                <h5>26/05/2025 - 30/05/2025</h5>
            </td>
            <td>
                <h5>Não Iniciado</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Feira de Soluções</h5>
            </td>
            <td>
                <h5>17/06/2025</h5>
            </td>
            <td>
                <h5>Não Iniciado</h5>
            </td>
        </tr>
    </table>

</span>

<br>

<span id='sprints'>

## 📊 Sprints

### Sprint 1:

- [✅] Análise e requerimento de requisitos;

- [✅] Criação do protótipo;

- [✅] Criação do template principal;
      
- [✅] Definição de variáveis;

- [✅] Realização da raspagem de dados;

- [✅] Implementação do Colab.

- [✅] Criação e implementação do filtro de ano.

- [✅] Criação e implementação do filtro de cidade de origem.

- [✅] Criação e implementação do filtro de mês.

<br>
 
### Sprint 2:

- [✅] Criação e implementação do filtro de tipo de carga.

- [✅] Criação e implementação do filtro de país de destino.

- [✅] Criação e implementação do filtros por valor agregado.

- [✅] Criação e implementação do filtros por kg líquido.

- [✅] Criação e conexão do banco de dados My Sql.

<br>

### Sprint 3:

> ⚠️EM PLANEJAMENTO⚠️
 
</span>

<br>

<span id='prototipo'>

## 💡 Protótipo
#### Clique no link abaixo para visualizar o modelo do projeto.

> <a href="https://www.figma.com/design/mc8GD7tXoYRSMAFkBeYB6c/Rascunho-de-site-1?node-id=0-1&p=f&t=gajjBhKlRLZUvRXe-0" target="_blank">Protótipo do Produto</a>

</span>

<br>

<span id='colab'>

## 💡 Colab
#### Clique no link abaixo para visualizar o colab do protótipo.

> <a href="https://colab.research.google.com/drive/1aWN-OI6syXCUm7__WN7sJGFusBUmCEvE" target="_blank">Colab</a>

</span>

<br>

<span id="backlog">

## 📊 Backlog do Produto
#### Clique no link abaixo para visualizar o backlog do produto. 
> <a href="https://1drv.ms/x/c/1d641dc3ff0a667d/ETTn_kcS7y9DrYVoLKRHPSoBLDIeg1XFQF3H6kwbM6CItQ?e=G0cl1h" target="_blank">Backlog do Produto</a>

<details>
    <summary>Backlog - Sprint 1</summary>
    <br>
    <table>
        <tr>
            <th>
                Prioridade
            </th>
            <th>
                User Story
            </th>
            <th>
                Estimativa
            </th>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero que os arquivos sejam limpos no Google Colab, para que os dados estejam organizados e prontos para uso no sistema.</h5>
            </td>
            <td>
                <h5>13</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero acessar essas visualizações por meio de um site, para que eu possa usar a ferramenta de forma prática e acessível.</h5>
            </td>
            <td>
                <h5>8</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero aplicar filtro de ano, para que eu possa personalizar as visualizações de acordo com meu interesse.</h5>
            </td>
            <td>
                <h5>5</h5>
            </td>
         <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero aplicar filtro de cidade de origem, para que eu possa personalizar as visualizações de acordo com meu interesse.</h5>
            </td>
            <td>
                <h5>5</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero aplicar filtro de mês, para que eu possa personalizar as visualizações de acordo com meu interesse.</h5>
            </td>
            <td>
                <h5>5</h5>
            </td>
        </tr>
        </tr>
    </table>

  </details>

<details>
    <summary>Backlog - Sprint 2</summary>
    <br>
    <table>
        <tr>
            <th>
                Prioridade
            </th>
            <th>
                User Story
            </th>
            <th>
                Estimativa
            </th>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero aplicar filtro de tipo de carga, para que eu possa personalizar as visualizações de acordo com meu interesse.</h5>
            </td>
            <td>
                <h5>5</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero aplicar filtro de país de destino, para que eu possa personalizar as visualizações de acordo com meu interesse.</h5>
            </td>
            <td>
                <h5>5</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero aplicar filtros por valor agregado, para que eu possa personalizar as visualizações de acordo com meu interesse.</h5>
            </td>
            <td>
                <h5>5</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero aplicar filtros por kg líquido, para que eu possa personalizar as visualizações de acordo com meu interesse.</h5>
            </td>
            <td>
                <h5>5</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero importar os dados tratados para um banco MySql, para que os dados estejam disponíveis para serem consultados via aplicação.</h5>
            </td>
            <td>
                <h5>3</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero conectar o site ao banco de dados, para que os dados sejam consultados em tempo real com base nos filtros aplicados.</h5>
            </td>
            <td>
                <h5>13</h5>
            </td>
        </tr>
    </table>

  </details>

<details>
    <summary>Backlog - Sprint 3</summary>
    <br>
<table>
        <tr>
            <th>
                Prioridade
            </th>
            <th>
                User Story
            </th>
            <th>
                Estimativa
            </th>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero visualizar um gráfico com Top 10 cargas, para que eu veja as que mais se destacam em valor agregado, kg líquido e cidade (usando kg líquido)</h5>
            </td>
            <td>
                <h5>8</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero visualizar um gráfico com Top 10 cargas, para que eu veja as cidades com maior valor agregado, kg líquido e os tipos de carga exportados.</h5>
            </td>
            <td>
                <h5>8</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero visualizar um gráfico com Top 10 países, para que eu veja os principais destinos por tipo de carga e kg líquido.</h5>
            </td>
            <td>
                <h5>5</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>ALTA</h5>
            </td>
            <td>
                <h5>Como usuário, quero visualizar a rota da carga (país de origem, país de destino e tipo de carga), para entender melhor o caminho que os produtos percorrem e analisar padrões logísticos.</h5>
            </td>
            <td>
                <h5>8</h5>
            </td>
        </tr>
    </table>

  </details>

</span>

<br>

<span id='equipe'>

## 👥 Equipe

<table>
        <tr>
            <th>
                Função
            </th>
            <th>
                Nome
            </th>
        </tr>
        <tr>
            <td>
                <h5>Scrum Master</h5>
            </td>
            <td>
                <h5>Enzo Gabriel</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Product Owner</h5>
            </td>
            <td>
                <h5>Rafael Sette</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Dev Team</h5>
            </td>
            <td>
                <h5>Rebeca Lima</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Dev Team</h5>
            </td>
            <td>
                <h5>João Vitor Moura</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Dev Team</h5>
            </td>
            <td>
                <h5>Ana Julia Rubim</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Dev Team</h5>
            </td>
            <td>
                <h5>Gabriel Lázaro</h5>
            </td>
        </tr>
        <tr>
            <td>
                <h5>Dev Team</h5>
            </td>
            <td>
                <h5>Samuel Henrique</h5>
            </td>
        </tr>
    </table>

</span>

<br>
