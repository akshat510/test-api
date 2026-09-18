"""
load_csv_to_db.py
-----------------
Reads a CSV file and loads it into an existing SQL Server table.
Strategy: TRUNCATE the table first, then bulk INSERT from the CSV.

Requirements:
    pip install pandas sqlalchemy pyodbc
"""

import sys
import pandas as pd
from sqlalchemy import create_engine, text
from config import SERVER, DATABASE, TABLE, CSV_PATH, DELIMITER, CHUNK_SIZE


def get_engine():
    """Create a SQLAlchemy engine using Windows Authentication."""
    connection_string = (
        f"mssql+pyodbc://{SERVER}/{DATABASE}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
        f"&trusted_connection=yes"
    )
    return create_engine(connection_string, fast_executemany=True)


def load_csv(path: str, delimiter: str) -> pd.DataFrame:
    """Read the CSV file into a DataFrame."""
    print(f"[1/3] Reading CSV: {path}")
    try:
        df = pd.read_csv(path, delimiter=delimiter, encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback encoding for files exported from Excel/Windows
        df = pd.read_csv(path, delimiter=delimiter, encoding="latin-1")

    print(f"      Rows loaded : {len(df):,}")
    print(f"      Columns     : {list(df.columns)}")
    return df


def truncate_table(engine, table: str):
    """Truncate the target table before loading."""
    print(f"[2/3] Truncating table: {table}")
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table}"))
    print("      Table truncated successfully.")


def insert_data(df: pd.DataFrame, engine, table: str, chunk_size: int):
    """Bulk insert the DataFrame into the SQL Server table."""
    print(f"[3/3] Inserting {len(df):,} rows into [{table}] in chunks of {chunk_size}...")
    df.to_sql(
        name=table,
        con=engine,
        if_exists="append",   # table already exists; just append
        index=False,          # don't write the DataFrame index as a column
        chunksize=chunk_size,
    )
    print(f"      Done! {len(df):,} rows inserted successfully.")


def main():
    engine = get_engine()

    # Step 1 — Read CSV
    df = load_csv(CSV_PATH, DELIMITER)

    if df.empty:
        print("WARNING: CSV file is empty. Nothing to load. Exiting.")
        sys.exit(0)

    # Step 2 — Truncate
    truncate_table(engine, TABLE)

    # Step 3 — Insert
    insert_data(df, engine, TABLE, CHUNK_SIZE)

    print("\n✅ Load complete.")


if __name__ == "__main__":
    main()
