from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings, SQLDatabase
from llama_index.core.indices.struct_store import SQLTableRetrieverQueryEngine
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index.core import VectorStoreIndex
from cf_db_model import DatabaseManager
import os


### This code is written to use the Ollama local server for LLM models
# Reference file for LlamaIndex ObjectIndex class
# https://docs.llamaindex.ai/en/stable/examples/objects/object_index/

class LlamaIndexManager:
    def __init__(self, db_manager: DatabaseManager,
                 ollama_embedding_model, ollama_base_url, ollama_llm_model,
                 persist_dir="./svs_storage"):
        
        self.db_manager = db_manager
        self.persist_dir = persist_dir
        # Ollama server for embeddings
        self.embedding_model = OllamaEmbedding(
            model_name=ollama_embedding_model,
            base_url=ollama_base_url,
            ollama_additional_kwargs={"mirostat": 0}
        )
        # Required global settings for LlamaIndex
        Settings.embed_model = self.embedding_model
        # Ollama Server for the LLM model
        self.llm_model = Ollama(model=ollama_llm_model, base_url=ollama_base_url, request_timeout=120.0)
        
        # Setup LlamaIndex
        print("Setup LlamaIndex SQLDatabase")
        self.sql_database = SQLDatabase(self.db_manager.get_engine())
        print("Setup LlamaIndex ObjectIndex")
        self.obj_index = self._create_object_index()
        print("Setup LlamaIndex SQLTableRetrieverQueryEngine")
        self.query_engine = self._create_query_engine()

    def _get_table_schema_objs(self):
        all_table_names = self.db_manager.get_all_table_names()
        table_schema_objs = []
        for table_name in all_table_names:
            table_schema_objs.append(SQLTableSchema(table_name=table_name))
        return table_schema_objs

    def _create_object_index(self):
        # Check if the storage directory exists
        if not os.path.exists(self.persist_dir):
            os.makedirs(self.persist_dir)
        
        # Check if all necessary files exist
        files_exist = all(
            os.path.exists(os.path.join(self.persist_dir, f))
            # if the file 'index_store.json' exists inside the self.persist_dir, the skip building the index
            for f in ['index_store.json']
        )
        
        if files_exist:
            print("Loading existing Object index from disk.")
            # table_node_mapping needs to be recalculated, assumes there's been no changes to the database
            # if the database has changed, then delete the file "self.persist_dir\index_store.json" to force a new index
            table_node_mapping = SQLTableNodeMapping(self.sql_database)
            obj_index = ObjectIndex.from_persist_dir(
            persist_dir = self.persist_dir,
            object_node_mapping = table_node_mapping  # without this, an error will be thrown
            )

        else:
            print("Building new Object index and saving to disk.")
            table_node_mapping = SQLTableNodeMapping(self.sql_database)
            table_schema_objs = self._get_table_schema_objs()
            obj_index = ObjectIndex.from_objects(
                table_schema_objs,
                table_node_mapping,
                VectorStoreIndex,
            )

            # save obj_index to disk
            obj_index.persist(persist_dir=self.persist_dir)
        
        return obj_index

    def _create_query_engine(self):
        query_engine = SQLTableRetrieverQueryEngine(
            self.sql_database,
            self.obj_index.as_retriever(similarity_top_k=1),
            llm=self.llm_model,
            dialect="mssql"
        )
        return query_engine

    def get_query_engine(self):
        return self.query_engine