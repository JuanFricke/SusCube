import csv
import os
import duckdb
import time
from dbfread import DBF

def dbf_create_to_database(table: DBF, database: duckdb.DuckDBPyConnection):
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


def dbf_insert_to_database(table: DBF, database: duckdb.DuckDBPyConnection):
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

dbf_directory = "./data"
output_directory = "./output_juntadb"

if os.path.exists(output_directory+"/databasemuitofoda.db"):
    os.remove(output_directory+"/databasemuitofoda.db")
if not os.path.exists(output_directory):
    os.mkdir(output_directory) 

database = duckdb.connect(f"{output_directory}/databasemuitofoda.db")

dnrs_db_files = [f for f in os.listdir(dbf_directory) if f.endswith('.dbf')]
aux_db_files = [f for f in os.listdir(dbf_directory+"/aux") if f.endswith('.csv')]


## IGNORA ESSA PARADA DE MACACO FOI LITERAL PRA TESTE OK 
## O BANCO JA VAI TA GERADO, DPS TENHO Q VER COMO EU PASSO UM ARQUIVO SQL PRA RODAR

# Open and read the file as a single buffer
fd = open('./ducksql/database_creation.sql', 'r')
sqlFile = fd.read()
fd.close()

database.execute(sqlFile)
start_time = time.time()
counter = 0
# dnrs_db_files.remove("DNRS2013.dbf")
for dbf_name in dnrs_db_files:
    table = DBF(f'{dbf_directory}/{dbf_name}', 'latin-1')
    dbf_insert_to_database(table, database)
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
    counter += 1
    print(f"\r{counter}/{len(aux_db_files)} {round((counter/len(aux_db_files))*100, 2)}%",end="")
print(f"\nTodos os DBFs foram inseridos na Base de Dados em {round(time.time() - start_time, 2)} segundos")