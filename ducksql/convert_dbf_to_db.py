import csv
import os
import duckdb
import time
from dbfread import DBF

def dbf_to_database(table: DBF, database: duckdb.DuckDBPyConnection):
    # DBF TO CSV
    start_time = time.time()
    csv_path = f"{output_directory}/{table.name}.csv" 
    with open(csv_path, 'w', newline = '') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(table.field_names)
        for record in table:
            writer.writerow(list(record.values()))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Criado {table.name}.csv em {round(elapsed_time, 2)} segundos")
    start_time = time.time()
    database.sql(f"CREATE TABLE {table.name} AS FROM read_csv('{output_directory}/{table.name}.csv');")
    os.remove(csv_path)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Criado a Tabela {table.name} na Database em {round(elapsed_time, 2)} segundos")

def csv_to_database(csv_name):
    start_time = time.time()
    database.sql(f"CREATE TABLE {csv_name} AS FROM read_csv('{dnrs_directory}/aux/{csv_name}.csv');")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Criado a Tabela {csv_name} na Database em {round(elapsed_time, 2)} segundos")

dnrs_directory = "./data"
output_directory = "./output_juntadb"


if not os.path.exists(output_directory):
    os.mkdir(output_directory) 

database = duckdb.connect(f"{output_directory}/databasemuitofoda.db")

dnrs_db_files = [f for f in os.listdir(dnrs_directory) if f.endswith('.dbf')]
aux_db_files = [f for f in os.listdir(dnrs_directory+"/aux") if f.endswith('.csv')]
for dbf_name in dnrs_db_files:
    table = DBF(f'{dnrs_directory}/{dbf_name}')
    dbf_to_database(table, database)

# for csv_name in aux_db_files:
#     csv_to_database(csv_name)