import csv
from os import mkdir, remove, listdir
from os.path import join, realpath, dirname, exists
import duckdb
import time
from dbfread import DBF


def DBF_to_CSV(dbf_table: DBF, output_location: str, output_name="temp.csv") -> str:
    csv_path = join(output_location, output_name)
    
    with open(csv_path, 'w', encoding="utf-8", newline = '') as file:
        # Get writer object
        writer = csv.writer(file)
        
        # Registra cabecalho
        writer.writerow(dbf_table.field_names)
        
        # Registra registros
        for record in dbf_table:
            writer.writerow(list(record.values()))
            
    return csv_path

def print_progress(counter: int, iterable: list) -> str:
    print(f"\r{counter}/{len(iterable)} {(counter/len(iterable))*100:.2f}%",end="")
    
def main():
    PROJECT_DIR = realpath(join(dirname(realpath(__file__)), ".."))    
    DATA_DIR = join(PROJECT_DIR, "data")
    DB_SCHEMA = join(PROJECT_DIR, "ducksql", "database_creation.sql")
    OUTPUT_DIR = join(PROJECT_DIR, "output_db")
    OUTPUT_DB_PATH = join(OUTPUT_DIR, "database.db")

    # Remove db existente
    if exists(OUTPUT_DB_PATH): remove(OUTPUT_DB_PATH)
            
    # Cria pasta de output
    if not exists(OUTPUT_DIR): mkdir(OUTPUT_DIR) 

    # Conecta ao banco de dados
    database = duckdb.connect(OUTPUT_DB_PATH)

    # Lista de arquivos DBFS
    dnrs_db_files = [file for file in listdir(DATA_DIR) if file.endswith('.dbf')]
    
    # Lista de arquivos CSVs
    aux_csv_files = [file for file in listdir(join(DATA_DIR, "aux", "CSV"))]
        
    # Lista de arquivos DBFs auxiliares
    aux_dbf_files = [file for file in listdir(join(DATA_DIR, "aux", "DBF"))]
        
    # Executa script sql no banco de dados
    with open(DB_SCHEMA, 'r') as file:
        database.execute(file.read())
    
    # Concatenando registros ATDRS ____________________________________________
    start_time = time.time()
    
    print("Inserindo DBFs ATDRS na Base de Dados:")
    
    counter = 0
    # dnrs_db_files.remove("DNRS2013.dbf")
    for file_name in dnrs_db_files:
        # Abre o arquivo DBF
        dbf_table = DBF(join(DATA_DIR, file_name), 'latin-1')
        
        # Salva o nome das colunas do DBF
        table_columns = ",".join(dbf_table.field_names)
        
        # Converte arquivo DBF para CSV
        csv_path = DBF_to_CSV(dbf_table, OUTPUT_DIR)
        
        # Inserindo CSV na Database
        database.sql(
            f"INSERT INTO atdrs({table_columns}) SELECT * FROM read_csv('{csv_path}');"
        )
        
        # Excluindo csv criado
        remove(csv_path)
        
        # Contador de progresso
        counter += 1
        print_progress(counter, dnrs_db_files)
        
    print(f"\nATRDS gerado em {(time.time() - start_time):.2f} segundos")


    # Inserindo DBFs auxiliares na Base de Dados ______________________________
    start_time = time.time()
    
    print("Inserindo DBFs auxiliares na Base de Dados:")
    
    counter = 0
    for dbf_name in aux_dbf_files:
        # Abre o arquivo DBF
        dbf_table = DBF(join(DATA_DIR, "aux", "DBF", dbf_name), 'latin-1')
                
        # Converte arquivo para CSV
        csv_path = DBF_to_CSV(dbf_table, OUTPUT_DIR)
        
        # Inserindo CSV na Database
        database.sql(f"CREATE TABLE {dbf_table.name} AS FROM read_csv('{csv_path}');")
        
        # Excluindo csv criado
        remove(csv_path)
        
        # Contador de progresso
        counter += 1
        print_progress(counter, aux_dbf_files)
        
    print(f"\nCSVs auxiliares importados em {(time.time() - start_time):.2f} segundos")
    
    # Inserindo CSVs auxiliares na Base de Dados ______________________________
    start_time = time.time()
    
    print("Inserindo CSVs na Base de Dados:")
    
    counter = 0
    for csv_name in aux_csv_files:                
        table_name = csv_name.replace(".csv", "")         
        csv_path = join(DATA_DIR, "aux", "CSV", csv_name)
        
        database.sql(
            f"CREATE TABLE {table_name} AS FROM read_csv('{csv_path}');"
        )
        
        # Contador de progresso
        counter += 1
        print_progress(counter, aux_csv_files)
        
    print(f"\nTodos os DBFs foram inseridos na Base de Dados em {(time.time() - start_time):.2f} segundos")
    
main()