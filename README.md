# LlamaIndex-ObjectIndex-Ollama
 Tutorial on using LlamaIndex-ObjectIndex-Ollama
 Tested on LlamaIndex 0.10.55  

## LlamaIndexManager Class  
Uses the LlamaIndex ObjectIndex class to create an index of all the tables in an existing database.  
Then, persists the index to the local disk, to avoid having to rebuild the embeddings every time that the program runs. 
Reference:  
https://docs.llamaindex.ai/en/stable/examples/objects/object_index/  

### Overview

The `LlamaIndexManager` class is designed to interface with a SQL database and the Ollama LLM local server, utilizing the LlamaIndex library to create and manage an object index for efficient querying. This class also supports persisting the object index to disk, ensuring that it can be reloaded efficiently without needing to rebuild from scratch each time.

### Key Components

1. **DatabaseManager**: An external class responsible for managing database connections and operations.
2. **OllamaEmbedding**: Utilized for embedding models using the Ollama local server.
3. **Ollama**: Represents the LLM model used for processing queries.
4. **Settings**: Global settings for the LlamaIndex library.
5. **SQLDatabase**: Handles the SQL database operations.
6. **ObjectIndex**: Manages the index of database tables for efficient retrieval and querying.
7. **SQLTableRetrieverQueryEngine**: A query engine for retrieving data from SQL tables.

### Initialization

The `LlamaIndexManager` is initialized with the following parameters:

- `db_manager`: An instance of `DatabaseManager`.
- `ollama_embedding_model`: The name of the Ollama embedding model.
- `ollama_base_url`: The base URL for the Ollama server.
- `ollama_llm_model`: The name of the Ollama LLM model.
- `persist_dir`: Directory path for persisting the index data.

```python
def __init__(self, db_manager: DatabaseManager,
             ollama_embedding_model, ollama_base_url, ollama_llm_model,
             persist_dir="./svs_storage"):
```

### Creating Object Index

The `_create_object_index` method checks if the necessary files exist in the persistence directory:

- If the files exist, it loads the existing index from disk.
- If the files do not exist, it builds a new index and saves it to disk.

```python
def _create_object_index(self):
    # Check if the storage directory exists
    if not os.path.exists(self.persist_dir):
        os.makedirs(self.persist_dir)
    
    # Check if all necessary files exist
    files_exist = all(
        os.path.exists(os.path.join(self.persist_dir, f))
        for f in ['index_store.json']
    )
    
    if files_exist:
        # Load existing index from disk
        # notice that it requires the object mappings and the persist dir  
        table_node_mapping = SQLTableNodeMapping(self.sql_database)
        obj_index = ObjectIndex.from_persist_dir(
            persist_dir = self.persist_dir,
            object_node_mapping = table_node_mapping
        )
    else:
        # Build new index and save to disk
        table_node_mapping = SQLTableNodeMapping(self.sql_database)
        table_schema_objs = self._get_table_schema_objs()
        obj_index = ObjectIndex.from_objects(
            table_schema_objs,
            table_node_mapping,
            VectorStoreIndex,
        )
        obj_index.persist(persist_dir=self.persist_dir)
    
    return obj_index
```

### Query Engine

The `_create_query_engine` method sets up a query engine using the SQLTableRetrieverQueryEngine, which enables efficient querying of the SQL database through the object index.

```python
def _create_query_engine(self):
    query_engine = SQLTableRetrieverQueryEngine(
        self.sql_database,
        self.obj_index.as_retriever(similarity_top_k=1),
        llm=self.llm_model,
        dialect="mssql"
    )
    return query_engine
```

### Usage

To use the `LlamaIndexManager`, initialize it with the required parameters and then call the `get_query_engine` method to obtain the query engine for executing queries.

```python
# Initialize LlamaIndexManager
index_manager = LlamaIndexManager(
    db_manager=your_db_manager_instance,
    ollama_embedding_model='the_name_of_your_embedding_model',
    ollama_base_url='http://servername:port',
    ollama_llm_model='the_name_of_your_llm_model'
)

# Get query engine
query_engine = index_manager.get_query_engine()
```

### Persistence

The `ObjectIndex` can be persisted to disk to avoid the overhead of rebuilding the index. This is managed through the `persist_dir` parameter, ensuring that the index is saved and loaded from the specified directory.

```python
# Persist object index to disk
obj_index.persist(persist_dir=self.persist_dir)
```

*Beware:* The ObjectIndex class requires that the `table_node_mapping` be passed in when reloading the index from disk:  
# Load existing index from disk
```python  
table_node_mapping = SQLTableNodeMapping(self.sql_database)
obj_index = ObjectIndex.from_persist_dir(
    persist_dir = self.persist_dir,
    object_node_mapping = table_node_mapping
)
```  

 # Running the Ollama local server on your PC
1. Install Ollama  
https://ollama.com/download  
This code requires Ollama running on your local PC, if you wish to use another LLM API, then you need to change the code.  
  
2. Pull these two models, run these commands in the command line  
ollama pull lamma3  
ollama pull nomic-embed-text  
  
3. Start ollama, run this in the command line  
ollama serve  
  
# Configure the Python Environment  
4. Create a new directory, create a python venv  
mkdir myLLMProject  
cd myLLMProject  
python -m venv env  
.\env\scripts\activate.bat  

5. Use pip to install all the python libraries  
pip install -r requirements.txt  

6. Run the main program  
python main_svs.py  

7. Tested on  
Windows 11 Pro  
Python 3.11  

# Chinook database
 Used the Chinook database for testing:  
 https://github.com/lerocha/chinook-database