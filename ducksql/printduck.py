import duckdb

# Caminho para o banco de dados DuckDB
db_path = 'sus_cube.db'

# Conexão com o banco de dados DuckDB
conn = duckdb.connect(database=db_path)

# Obtém uma lista de todas as tabelas no banco de dados
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

# Para cada tabela, imprime o conteúdo dela
for table in tables:
    table_name = table[0]
    print(f"Tabela: {table_name}")
    
    # Obtém todos os dados da tabela
    table_data = conn.execute(f"SELECT * FROM {table_name}").fetchall()
    
    # Obtém os nomes das colunas
    column_names = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    column_names = [col[1] for col in column_names]
    
    # Imprime os nomes das colunas
    print("Campos:", ", ".join(column_names))
    
    # Imprime os dados da tabela
    for row in table_data:
        print(row)

    print()  # Adiciona uma linha em branco entre as tabelas

# Fecha a conexão com o banco de dados DuckDB
conn.close()
