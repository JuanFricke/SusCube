import os
import duckdb
from dbfread import DBF
import pandas as pd

# DIretório de onde vai pegar os duck db
data_directory = './output_dbs'

# Diretório onde vai largar eles
output_directory = "./output_juntadb"


# ver se o diretório existe, se não existir cria né
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
if os.path.exists(f"{output_directory}/databasemuitofoda.db"):
    os.remove(f"{output_directory}/databasemuitofoda.db")
# pega o nome dos arquivos dentro do diretório
dnrs_db_files = [f for f in os.listdir(data_directory) if f.endswith('.db')]

print(f"Bases: {dnrs_db_files}")

# conecta com o banco que vai ser usado como principal entre tabelas
conn_merge = duckdb.connect(f"{output_directory}/databasemuitofoda.db")

# iterar em todos os nomes dos arquivos
for database_name in dnrs_db_files:
    # conexão com o banco iterado
    conn = duckdb.connect(data_directory+"/"+database_name)
    # pega o nome da tabelas
    query = conn.sql("SHOW TABLES").fetchall()
    # como só tem sempre 1 tabela por banco, ele pega o primeiro valor dela
    table = query[0][0]
    # converte a tabela pra csv
    conn.sql(f"COPY {table} to '{output_directory}/{table}.csv' (HEADER, DELIMITER ','); ")
    print(f"EXPORTADO {database_name}")
    conn.close()
    # pega o banco principal, e importa a tabela pra dentro como csv pra banco
    conn_merge.sql(f"CREATE TABLE {table} AS FROM read_csv('{output_directory}/{table}.csv');")
    print(f"IMPORTADO DADOS de {database_name}")
    # deleta o csv
    os.remove(f"{output_directory}/{table}.csv")
    print(f"REMOVIDO O CSV : {table}")

# printa todas as tabelas que tem no banco
print(conn_merge.sql("SHOW TABLES").fetchall())
conn_merge.close()
    
