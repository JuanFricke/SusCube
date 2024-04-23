import os
import duckdb
from dbfread import DBF
import pandas as pd
import time

# Caminho para o diretório de dados
data_directory = '../data'

# Lista de arquivos DBF
dbf_files = [f for f in os.listdir(data_directory) if f.endswith('.dbf')]

# Lista de arquivos CSV na subpasta 'aux'
csv_files = [f for f in os.listdir(os.path.join(data_directory, 'aux')) if f.endswith('.csv')]

# Inicializa conexão com o banco de dados DuckDB
conn = duckdb.connect(database='sus_cube.db')

# Convertendo arquivos DBF para SQL
print("Convertendo arquivos DBF para SQL:")
start_time = time.time()
for dbf_file in dbf_files:
    # Obtém o nome da tabela removendo a extensão do arquivo
    table_name = os.path.splitext(dbf_file)[0]

    # Lê o arquivo DBF
    dbf_data = DBF(os.path.join(data_directory, dbf_file))

    # Converte os dados do DBF para DataFrame
    df = pd.DataFrame(iter(dbf_data))

    print("Criando tabela '{}'...".format(table_name))

    # Itera sobre as linhas do DataFrame e imprime cada linha
    for index, row in df.iterrows():
        print("Adicionando linha:", row)

    # Salva o DataFrame no banco de dados DuckDB
    df.to_sql(table_name, conn, index=False)

    print("Tabela '{}' criada.".format(table_name))

# Convertendo arquivos CSV para SQL
print("\nConvertendo arquivos CSV para SQL:")
for csv_file in csv_files:
    # Obtém o nome da tabela removendo a extensão do arquivo
    table_name = os.path.splitext(csv_file)[0]

    # Lê o arquivo CSV
    df = pd.read_csv(os.path.join(data_directory, 'aux', csv_file))

    print("Criando tabela '{}'...".format(table_name))

    # Itera sobre as linhas do DataFrame e imprime cada linha
    for index, row in df.iterrows():
        print("Adicionando linha:", row)

    # Salva o DataFrame no banco de dados DuckDB
    df.to_sql(table_name, conn, index=False)

    print("Tabela '{}' criada.".format(table_name))

# Fecha a conexão com o banco de dados DuckDB
conn.close()

end_time = time.time()
elapsed_time = end_time - start_time
print("\nBase de dados criada com sucesso.")
print("Tempo decorrido: {:.2f} segundos.".format(elapsed_time))
