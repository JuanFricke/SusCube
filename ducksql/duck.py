import os
import duckdb
from dbfread import DBF
import pandas as pd
from tqdm import tqdm

# Caminho para o diretório de dados
data_directory = '../data'

# Lista de arquivos DBF
dbf_files = [f for f in os.listdir(data_directory) if f.endswith('.dbf')]

# Lista de arquivos CSV na subpasta 'aux'
csv_files = [f for f in os.listdir(os.path.join(data_directory, 'aux')) if f.endswith('.csv')]

# Inicializa conexão com o banco de dados DuckDB
conn = duckdb.connect(database='sus_cube.db')

# Configura a barra de progresso para os arquivos DBF
with tqdm(total=len(dbf_files), desc="Convertendo DBF para SQL") as pbar:
    # Loop sobre os arquivos DBF
    for dbf_file in dbf_files:
        # Obtém o nome da tabela removendo a extensão do arquivo
        table_name = os.path.splitext(dbf_file)[0]
        
        # Lê o arquivo DBF
        dbf_data = DBF(os.path.join(data_directory, dbf_file))
        
        # Converte os dados do DBF para DataFrame
        df = pd.DataFrame(iter(dbf_data))
        
        # Salva o DataFrame no banco de dados DuckDB
        df.to_sql(table_name, conn, index=False)
        
        # Atualiza a mensagem da barra de progresso
        pbar.set_postfix(File=dbf_file)
        # Atualiza a barra de progresso
        pbar.update(1)

# Configura a barra de progresso para os arquivos CSV
with tqdm(total=len(csv_files), desc="Convertendo CSV para SQL") as pbar:
    # Loop sobre os arquivos CSV
    for csv_file in csv_files:
        # Obtém o nome da tabela removendo a extensão do arquivo
        table_name = os.path.splitext(csv_file)[0]
        
        # Lê o arquivo CSV
        df = pd.read_csv(os.path.join(data_directory, 'aux', csv_file))
        
        # Salva o DataFrame no banco de dados DuckDB
        df.to_sql(table_name, conn, index=False)
        
        # Atualiza a mensagem da barra de progresso
        pbar.set_postfix(File=csv_file)
        # Atualiza a barra de progresso
        pbar.update(1)

# Fecha a conexão com o banco de dados DuckDB
conn.close()

print("Base de dados criada com sucesso.")
