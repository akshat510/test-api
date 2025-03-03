import pandas as pd
import pyodbc

csv_file_path = "D:\\CP\\data1.csv"  
server = "LAPTOP-NC6GQ5MF"
database = "master"
table_name = "dbo.tmpEmp"
chunk_size = 10000  

conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.fast_executemany = True  

    for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size):
        try:
            data_tuples = [tuple(row) for row in chunk.itertuples(index=False, name=None)]

            # **Fix: Wrap column names in square brackets**
            columns = ", ".join([f"[{col}]" for col in chunk.columns])  
            placeholders = ", ".join(["?"] * len(chunk.columns))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            cursor.executemany(sql, data_tuples)
            conn.commit()
        except Exception as e:
            print(f"Error inserting chunk: {e}")
            conn.rollback()

except Exception as e:
    print(f"Database connection failed: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()

print("CSV data successfully loaded into SQL Server table.")
