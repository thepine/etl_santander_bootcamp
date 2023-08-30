import sqlite3
import openai
import pandas as pd
import requests
import json

# Conectar ao banco de dados SQLite
con = sqlite3.connect('../banco_etl.db')
# Ler os dados da tabela 'usuarios' do banco de dados SQLite
usuarios_df = pd.read_sql_query("SELECT id, nome, topico FROM usuarios", con)
# Fechar a conexão com o banco de dados
con.close()

# Fazer uma solicitação à API do IBGE para obter as notícias
request = requests.get('http://servicodados.ibge.gov.br/api/v3/noticias/?tipo=noticia')
# Extrair as notícias da resposta da API
noticias = request.json()['items']
# Criar um DataFrame com as notícias e filtrar as colunas desejadas
noticias_df = pd.DataFrame(noticias).filter(items=['editorias', 'titulo', 'introducao', 'link'])

# Juntar os DataFrames 'usuarios_df' e 'noticias_df' usando a coluna 'topico' como chave
# Usamos 'how='inner'' para fazer uma junção interna mantendo apenas as correspondências
# Drop_duplicates() é usado para remover quaisquer duplicatas com base na coluna 'id'
merged_df = usuarios_df.merge(noticias_df, left_on='topico', right_on='editorias', how='inner').drop_duplicates(subset='id')

# Filtrar e reorganizar as colunas para o DataFrame final
result_df = merged_df.filter(items=['nome', 'topico', 'titulo', 'introducao', 'link'])

# Exportar o DataFrame final para uma planilha Excel chamada 'resultado_etl.xlsx'
# O parâmetro index=False evita a inclusão do índice na planilha
result_df.to_excel('resultado_etl.xlsx', index=False)
