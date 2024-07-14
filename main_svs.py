from cf_settings import *
from cf_db_model import DatabaseManager
from cf_llama_index_svs import LlamaIndexManager
import time

# Start here
print("Welcome! Let's get started...")

### Start the Database ###
# Record the start time
start_time = time.time()

# Connect to the Database
print("Connecting to the database.")
db_manager = DatabaseManager(db_url)

# Record the end time
db_end_time = time.time()
# Calculate the elapsed time
elapsed_time = db_end_time - start_time
print(f"It took: {elapsed_time:.4f} seconds to get the Database started.\n")

### Create the LLM Query Engine ###
# db_manager: created above
# ollama_embedding_model, ollama_base_url, ollama_llm_model: pulled from cf_settings.py
print("Creating the LLM Query Engine.")
llama_index_manager = LlamaIndexManager(
    db_manager,
    ollama_embedding_model,
    ollama_base_url,
    ollama_llm_model
)

query_engine = llama_index_manager.get_query_engine()
print("Query engine configured and ready to use.")

# Record the end time
llm_end_time = time.time()
# Calculate the elapsed time
elapsed_time = llm_end_time - db_end_time
print(f"It took: {elapsed_time:.4f} seconds to get the LLM Query engine started.\n")

### testing the LLM Query engine ###
print("How many tables are there in the database?")
response = query_engine.query("how many tables are there in the database")
print(response.response)
print("\n", response.metadata)

### Main Loop ###
while True:
    user_query = input("\nEnter your query (type /q to quit): ")
    if user_query == "/q":
        print("Quiting...")
        break
    else:
        # Record the start time
        start_time = time.time()
        
        print("\nGetting your answer...")
        response = query_engine.query(user_query)
        print(response.response)
        print("\nHere's the SQL query used:")
        print(response.metadata)
        
        # Record the end time
        end_time = time.time()
        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        print(f"It took: {elapsed_time:.4f} seconds to get your answer.\n")

### The end ###
print("The program ends here. Goodbye.")