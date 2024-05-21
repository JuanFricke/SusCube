import csv
from os import mkdir, remove, listdir
from os.path import join, realpath, dirname, exists
import duckdb
import time
from dbfread import DBF

# Funcao nao utilizada!!!!!!!!!!!!!!!
# def dbf_create_to_database(table: DBF, database: duckdb.DuckDBPyConnection):
#     # DBF TO CSV
#     start_time = time.time()
    
#     csv_path = f"{output_directory}/{table.name}.csv" 
#     with open(csv_path, 'w', newline = '') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerow(table.field_names)
#         for record in table:
#             writer.writerow(list(record.values()))
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"Criado {table.name}.csv em {round(elapsed_time, 2)} segundos")
#     start_time = time.time()
#     database.sql(f"CREATE TABLE {table.name} AS FROM read_csv('{output_directory}/{table.name}.csv');")
#     os.remove(csv_path)
    
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"Criado a Tabela {table.name} na Database em {round(elapsed_time, 2)} segundos")

def DBF_to_CSV(dbf_table: DBF, output_location: str, output_name="temp.csv") -> str:
    with open(join(output_location, output_name), 'w', newline = '') as file:
        

def insert_DBF_in_database(table: DBF, database: duckdb.DuckDBPyConnection, file_location: str):
    # DBF TO CSV
    csv_path = f"{output_directory}/{table.name}.csv"
    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(table.field_names)
        for record in table:
            writer.writerow(list(record.values()))
    columns = ""
    for i in range(len(table.field_names)):
        if (i+1) != len(table.field_names):
            columns += table.field_names[i] + ", "
        else:
            columns += table.field_names[i]
    database.sql(
        f"INSERT INTO atdrs({columns}) SELECT * FROM read_csv('{output_directory}/{table.name}.csv');"
    )

    os.remove(csv_path)


def csv_to_database(csv_name):   
    csv_name = csv_name.split(".")[0]
    database.sql(
        f"INSERT INTO {csv_name} SELECT * FROM read_csv('{dbf_directory}/aux/{csv_name}.csv', null_padding = true, ignore_errors = true);"
    )
    
def main():
    PROJECT_DIR = realpath(join(dirname(realpath(__file__)), ".."))    
    DATA_DIR = join(PROJECT_DIR, "data")
    DB_SCHEMA = join(PROJECT_DIR, "ducksql", "database_creation.sql")
    OUTPUT_DIR = join(PROJECT_DIR, "output_db")
    OUTPUT_DB_PATH = join(OUTPUT_DIR, "database.db")
    dbf_directory = "./data"
    output_directory = "./output_juntadb"

    # Remove db existente
    if exists(OUTPUT_DB_PATH): remove(OUTPUT_DB_PATH)
            
    # Cria pasta de output
    if not exists(OUTPUT_DIR): mkdir(OUTPUT_DIR) 

    database = duckdb.connect(OUTPUT_DB_PATH)

    dnrs_db_files = [file for file in listdir(DATA_DIR) if file.endswith('.dbf')]
    aux_db_files = [file for file in listdir(join(DATA_DIR)) if file.endswith('.csv')]
    
    start_time = time.time()
    
    counter = 0
    # dnrs_db_files.remove("DNRS2013.dbf")
    for file_name in dnrs_db_files:
        table = DBF(join(DATA_DIR, file_name), 'latin-1')
        
        insert_DBF_in_database(table, database)
        
        # Contador de progresso
        counter += 1
        print(f"\r{counter}/{len(dnrs_db_files)} {round((counter/len(dnrs_db_files))*100, 2)}%",end="")
        
    print(f"\nTodos os DBFs foram inseridos na Base de Dados em {round(time.time() - start_time, 2)} segundos")

    start_time = time.time()
    
    counter = 0
    for csv_name in aux_db_files:
        # with open(f'{dbf_directory}/aux/{csv_name}', 'r+',encoding="ISO 8859-1") as file:
            # line = ['sequencial', 'descricao', 'codigos']
            # print(f"abrindo {csv_name}")
            # csvreader = csv.writer(file)
            # csvreader.writerow(line)
            
        csv_to_database(csv_name)
        
        # Contador de progresso
        counter += 1
        print(f"\r{counter}/{len(aux_db_files)} {round((counter/len(aux_db_files))*100, 2)}%",end="")
        
    print(f"\nTodos os DBFs foram inseridos na Base de Dados em {round(time.time() - start_time, 2)} segundos")
    
main()