import os
import duckdb
from dbfread import DBF
import pandas as pd
import time
from concurrent.futures import ProcessPoolExecutor

data_directory = '../data'
output_directory = '../output_dbs'

dbf_files = [f for f in os.listdir(data_directory) if f.endswith('.dbf')]
csv_files = [f for f in os.listdir(os.path.join(data_directory, 'aux')) if f.endswith('.csv')]

# Verificar e criar diretório de saída se não existir
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def convert_dbf_to_sql(dbf_file):
    try:
        table_name = os.path.splitext(dbf_file)[0]
        print("Convertendo arquivo DBF '{}' para SQL...".format(dbf_file))
        dbf_data = DBF(os.path.join(data_directory, dbf_file))

        df = pd.DataFrame(iter(dbf_data))
        db_path = os.path.join(output_directory, f"{table_name}.db")
        with duckdb.connect(database=db_path) as conn:
            df.to_sql(table_name, conn, index=False)
        print("Tabela '{}' criada.".format(table_name))
    except Exception as e:
        print(f"Erro ao converter o arquivo DBF '{dbf_file}': {e}")

def convert_csv_to_sql(csv_file):
    try:
        table_name = os.path.splitext(csv_file)[0]
        print("Convertendo arquivo CSV '{}' para SQL...".format(csv_file))
        df = pd.read_csv(os.path.join(data_directory, 'aux', csv_file), encoding='ISO-8859-1')
        db_path = os.path.join(output_directory, f"{table_name}.db")
        with duckdb.connect(database=db_path) as conn:
            df.to_sql(table_name, conn, index=False)
        print("Tabela '{}' criada.".format(table_name))
    except Exception as e:
        print(f"Erro ao converter o arquivo CSV '{csv_file}': {e}")

print("Convertendo arquivos DBF para SQL:")
start_time = time.time()
with ProcessPoolExecutor() as executor:
    executor.map(convert_dbf_to_sql, dbf_files)

print("\nConvertendo arquivos CSV para SQL:")
with ProcessPoolExecutor() as executor:
    executor.map(convert_csv_to_sql, csv_files)

end_time = time.time()
elapsed_time = end_time - start_time
print("\nTabelas criadas em bancos de dados separados.")

# Juntando todos os bancos de dados em um único banco
output_db_path = os.path.join(output_directory, 'merged_db.db')
for db_file in os.listdir(output_directory):
    if db_file.endswith(".db") and db_file != 'merged_db.db':
        db_path = os.path.join(output_directory, db_file)
        with duckdb.connect(database=db_path) as conn:
            conn.execute("ATTACH DATABASE '{}' AS merged_db".format(output_db_path))
            conn.execute("CREATE TABLE IF NOT EXISTS merged_db.table AS SELECT * FROM main.table")
            conn.execute("DETACH DATABASE merged_db")
        os.remove(db_path)  # Excluindo o banco de dados antigo

print("Todas as tabelas foram juntadas em um único banco de dados.")
print("Tempo decorrido: {:.2f} segundos.".format(elapsed_time))
