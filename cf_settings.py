# This file includes all the configuration settings

# Example with the MS SQL Server database connection parameters
# for MS SQL Server requires: pip install pyodbc
db_server = 'localhost'
db_port = 1433
db_database = 'BD_formacao'
db_username = 'root_formacao'
db_password = 'root'
db_url = f'mssql+pyodbc://{db_username}:{db_password}@{db_server}:{db_port}/{db_database}?driver=ODBC+Driver+17+for+SQL+Server'

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
