import duckdb

conn_merge = duckdb.connect("output_juntadb/databasemuitofoda.db")

tables = conn_merge.sql("SHOW TABLES").fetchall()

query = conn_merge.sql(f"Select * from {tables[1][0]}")
print(query)