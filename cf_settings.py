# This file includes all the configuration settings

# Example with the MS SQL Server database connection parameters

db_server = 'localhost'
mssql_db_port = 1433
mysql_db_port = 3306
db_database = 'chinook'
db_username = 'sa'
db_password = 'root'

# For MS SQL Server
# for MS SQL Server requires: pip install pyodbc
db_url = f'mssql+pyodbc://{db_username}:{db_password}@{db_server}:{mssql_db_port}/{db_database}?driver=ODBC+Driver+17+for+SQL+Server'

# For MySQL or MariaDB
# for MySQL requires: pip install pymysql
# db_url = f'mysql+pymysql://{db_username}:{db_password}@{db_server}:{mysql_db_port}/{db_database}'

# For SQLite
path_to_db_file = 'db/Chinook_Sqlite.sqlite'
# db_url = f'sqlite:///{path_to_db_file}'


# Define the Ollama connection parameters
ollama_llm_model = "llama3"
# ollama_embedding_model = "mxbai-embed-large"  # num_ctx 512
ollama_embedding_model = "nomic-embed-text"     # num_ctx 8192
ollama_base_url = "http://localhost:11434"
# Reminder: Ollama must be installed on the local PC!
# Pull the models above with:
# ollama pull llama3
# ollama pull nomic-embed-text
# Start Ollama with "ollama serve" before running this program
