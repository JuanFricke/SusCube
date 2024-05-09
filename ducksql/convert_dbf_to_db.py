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
    start_time = time.time()
    csv_path = f"{output_directory}/{table.name}.csv"
    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(table.field_names)
        for record in table:
            writer.writerow(list(record.values()))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Criado {table.name}.csv em {round(elapsed_time, 2)} segundos")
    start_time = time.time()
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
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        f"Inserido a Tabela {table.name} na Database em {round(elapsed_time, 2)} segundos"
    )


def csv_to_database(csv_name):   
    # "sequencia","descricao","codigos"
    start_time = time.time()
    csv_name = csv_name.split(".")[0]
    database.sql(
        f"INSERT INTO {csv_name} SELECT * FROM read_csv('{dbf_directory}/aux/{csv_name}.csv', null_padding = true, ignore_errors = true);"
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Inserido {csv_name} na Database em {round(elapsed_time, 2)} segundos")

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
database.execute("""
CREATE TABLE atdrs(
  ap_mvm     VARCHAR(6),
  ap_condic  VARCHAR(2),
  ap_gestao  VARCHAR(6),
  ap_coduni  VARCHAR(7),
  ap_autoriz VARCHAR(13),
  ap_cmp     VARCHAR(6),
  ap_pripal  VARCHAR(10),
  ap_vl_ap   DECIMAL(20,2),
  ap_ufmun   VARCHAR(6),
  ap_tpups   VARCHAR(2),
  ap_tippre  VARCHAR(2),
  ap_mn_ind  VARCHAR(1),
  ap_cnpjcpf VARCHAR(14),
  ap_cnpjmnt VARCHAR(14),
  ap_cnspcn  VARCHAR(15),
  ap_coidade VARCHAR(1),
  ap_nuidade VARCHAR(2),
  ap_sexo    VARCHAR(1),
  ap_racacor VARCHAR(2),
  ap_munpcn  VARCHAR(6),
  ap_ufnacio VARCHAR(3),
  ap_ceppcn  VARCHAR(8),
  ap_ufdif   VARCHAR(1),
  ap_mndif   VARCHAR(1),
  ap_dtinic  VARCHAR(8),
  ap_dtfim   VARCHAR(8),
  ap_tpaten  VARCHAR(2),
  ap_tpapac  VARCHAR(1),
  ap_motsai  VARCHAR(2),
  ap_obito   VARCHAR(1),
  ap_encerr  VARCHAR(1),
  ap_perman  VARCHAR(1),
  ap_alta    VARCHAR(1),
  ap_transf  VARCHAR(1),
  ap_dtocor  VARCHAR(8),
  ap_codemi  VARCHAR(10),
  ap_catend  VARCHAR(2),
  ap_apacant VARCHAR(13),
  ap_unisol  VARCHAR(7),
  ap_dtsolic VARCHAR(8),
  ap_dtaut   VARCHAR(8),
  ap_cidcas  VARCHAR(4),
  ap_cidpri  VARCHAR(4),
  ap_cidsec  VARCHAR(4),
  ap_etnia   VARCHAR(4),
  atd_caract VARCHAR(1),
  atd_dtpdr  VARCHAR(8),
  atd_dtcli  VARCHAR(8),
  atd_acevas VARCHAR(1),
  atd_maisne VARCHAR(1),
  atd_sitini VARCHAR(1),
  atd_sittra VARCHAR(1),
  atd_seapto VARCHAR(1),
  atd_hb     VARCHAR(4),
  atd_fosfor VARCHAR(4),
  atd_ktvsem VARCHAR(4),
  atd_tru    VARCHAR(4),
  atd_albumi VARCHAR(4),
  atd_pth    VARCHAR(4),
  atd_hiv    VARCHAR(1),
  atd_hcv    VARCHAR(1),
  atd_hbsag  VARCHAR(1),
  atd_interc VARCHAR(1),
  atd_seperi VARCHAR(1),
  ap_natjur  VARCHAR(4)
);
""")

# dnrs_db_files.remove("DNRS2013.dbf")
for dbf_name in dnrs_db_files:
    table = DBF(f'{dbf_directory}/{dbf_name}', 'latin-1')
    dbf_insert_to_database(table, database)

# for csv_name in aux_db_files:
#     # with open(f'{dbf_directory}/aux/{csv_name}', 'r+',encoding="ISO 8859-1") as file:
#         # line = ['sequencial', 'descricao', 'codigos']
#         # print(f"abrindo {csv_name}")
#         # csvreader = csv.writer(file)
#         # csvreader.writerow(line)
#     csv_to_database(csv_name)
