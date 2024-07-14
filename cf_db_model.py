from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select, insert, text

class DatabaseManager:
    def __init__(self, db_url):
        
        self.connection_string = db_url
        self.engine = create_engine(self.connection_string)
        self.metadata_obj = MetaData()
        print("The db engine was created.")

    def reflect_schema(self):
        # call this method if you need the SQLAlchemy Metadata Object to reflect the Database Schema
        self.metadata_obj.reflect(bind=self.engine)

    def get_engine(self):
        return self.engine

    def get_metadata(self):
        return self.metadata_obj

    def get_all_table_names(self):
        return [table_name for table_name in self.metadata_obj.tables.keys()]