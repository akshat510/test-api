# ============================================================
#  Configuration — update these values before running
# ============================================================

# SQL Server instance name
# Examples: "localhost", "DESKTOP-XYZ\\SQLEXPRESS", ".\\SQLEXPRESS"
SERVER   = "YOUR_SERVER_NAME"

# Target database
DATABASE = "YOUR_DATABASE_NAME"

# Target table (must already exist in the database)
TABLE    = "YOUR_TABLE_NAME"

# Path to the CSV file
CSV_PATH = r"C:\path\to\your\file.csv"

# CSV delimiter (most common is comma; change to ";" if needed)
DELIMITER = ","

# Batch size for bulk insert (tune this for performance)
CHUNK_SIZE = 1000
