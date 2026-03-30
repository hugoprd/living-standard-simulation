-----

* [Descrição PT-BR](#descrição)

* [US-EN description](#description)

-----

# Descrição

O projeto concentra-se em dados do estado e da capital do Rio de Janeiro. Devido a inconsistências nos relatórios, como variações nas taxas de normalização (por 100 mil habitantes) e diferentes períodos temporais, foram integrados dados censitários do IBGE para a padronização de todas as bases de dados.

## Dados utilizados para o treinamento do modelo:

- Dados para a normalização de bases necessitadas:
    - [População Residente, Área territorial e Densidade demográfica (Estado Rio de Janeiro)](https://sidra.ibge.gov.br/tabela/4714/#)

- [Dados de Segurança do Rio de Janeiro](https://www.ispdados.rj.gov.br/estatistica.html):
    - [Estatísticas de segurança: série histórica mensal por área de delegacia desde 01/2003 (taxas por 100 mil habitantes)](https://www.ispdados.rj.gov.br/Arquivos/BaseEstadoTaxaMes.csv)
    - [Feminicídio (Lei 7.448/2016): série histórica mensal por área de delegacia desde 10/2016](https://www.ispdados.rj.gov.br/Arquivos/BaseFeminicidioEvolucaoMensalCisp.csv)
- [Dados de Trabalho e Rendimento](https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html?edicao=44663&t=resultados):
    - [Pessoas de 14 anos ou mais de idade, ocupadas na semana de referência, com rendimento de trabalho, Valor do rendimento nominal mensal médio e mediano de todos os trabalhos, por sexo e segundo a posição na ocupação e categoria do emprego no trabalho principal (Estado Rio de Janeiro)]()
- [Dados de Condição de Vida](http://www.atlasbrasil.org.br/acervo/biblioteca):
    - [Bases do Censo e das UDHs por Regiões Metropolitanas: Rio de Janeiro](http://www.atlasbrasil.org.br/consulta/planilha)

# Separação dos Dados

Cada base de dado foi separada em diferentes "tipos" de dados:

- Demografia (DEMOGRAFIA)
- Condição de Vida (CONDICAO_DE_VIDA)
- Empregabilidade (EMPREGABILIDADE)
- Segurança (SEGURANCA)
- Feminicídio (FEMINICIDIO)

-----

# Description

The project focuses on data from Rio de Janeiro State and the capital city. Due to inconsistencies in reporting—such as varying normalization rates (per 100k inhabitants) and different timeframes—IBGE census data was integrated to standardize all databases.

## Data used for model training:

- Data for dataset normalization:
    - [Resident Population, Land Area, and Population Density (Rio de Janeiro State)](https://sidra.ibge.gov.br/tabela/4714/#)

- [Rio de Janeiro Security Data](https://www.ispdados.rj.gov.br/estatistica.html):
    - [Security statistics: monthly time series per policy precinct since 01/2003 (Rates per 100,000 inhabitants)](https://www.ispdados.rj.gov.br/Arquivos/BaseEstadoTaxaMes.csv)
    - [Femicide (Law 7,448/2016): monthly time series by police precinct since 10/2016](https://www.ispdados.rj.gov.br/Arquivos/BaseFeminicidioEvolucaoMensalCisp.csv)
- [Labor and Income Data](https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html?edicao=44663&t=resultados):
    - [Persons aged 14 and over, employed in the reference week, with labor income; Average and median monthly nominal income from all jobs, by sex, occupational status, and employment category in the main job (Rio de Janeiro State)]()
- [Living Conditions Data](http://www.atlasbrasil.org.br/acervo/biblioteca)):
    - [Census and HDU (Human Development Units) Databases by Metropolitan Regions: Rio de Janeiro](http://www.atlasbrasil.org.br/consulta/planilha)

# Data Separation

Each database were separated in different "types" of data:

- Demography (DEMOGRAPHY)
- LIFE CONDITION (LIFE_CONDITION)
- Empregability (EMPREGABILITY)
- Security (SECURITY)
- Femicide (FEMICIDE)

-----