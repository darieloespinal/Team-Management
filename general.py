from pydantic import BaseModel
import sqlalchemy as db_al
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define Pydantic data model for a general manager
class GeneralModel(BaseModel):
    id: int
    name: str
    team: str = None
    birthdate: str = None
    startdate: int = None
    enddate: int = None
    email: str = None
    championships: int = None

# Class to interact with the database for general manager-related operations
class GeneralResource:
    def __init__(self):
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = str(os.getenv("DB_PORT"))
        db_name = os.getenv("DB_NAME")

        # Create a SQLAlchemy engine
        #db_url = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        db_url = f"mysql+mysqlconnector://doe2102:sql_for_mgmt@34.23.76.102/Managers"
        self.engine = db_al.create_engine(db_url)
        self.conn = self.engine.connect()

        # Metadata instance for extracting the metadata: structures, table infos, etc.
        self.metadata = db_al.MetaData()

        # Table object for the general managers table
        self.managers_table = db_al.Table('General_Managers', self.metadata, autoload_with=self.engine)

    def get_manager_by_id(self, manager_id):
        query = self.managers_table.select().where(self.managers_table.columns.id == manager_id)
        exe = self.conn.execute(query)

        column_names = exe.keys()
        result = exe.fetchall()
        result_dicts = [dict(zip(column_names, row)) for row in result]

        return result_dicts

    def get_paginated_managers(self, limit, offset):
        query = self.managers_table.select().limit(limit).offset(offset)
        exe = self.conn.execute(query)

        column_names = exe.keys()
        result = exe.fetchall()
        result_dicts = [dict(zip(column_names, row)) for row in result]

        return result_dicts

    def add_manager(self, manager: GeneralModel):
        ins_query = self.managers_table.insert().values(
            id=manager.id,
            name=manager.name,
            team=manager.team,
            birthdate=manager.birthdate,
            startdate=manager.startdate,
            enddate=manager.enddate,
            email=manager.email,
            championships=manager.championships
        )
        result = self.conn.execute(ins_query)
        self.conn.commit()
        return result

    def modify_manager(self, manager: GeneralModel, manager_id: int):
        update_data = {
            "name": manager.name,
            "team": manager.team,
            "birthdate": manager.birthdate,
            "startdate": manager.startdate,
            "enddate": manager.enddate,
            "email": manager.email,
            "championships": manager.championships
        }
        update_query = self.managers_table.update().where(self.managers_table.columns.id == manager_id).values(update_data)
        result = self.conn.execute(update_query)
        self.conn.commit()
        return result

    def delete_manager(self, manager_id):
        del_query = self.managers_table.delete().where(self.managers_table.columns.id == manager_id)
        result = self.conn.execute(del_query)
        self.conn.commit()
        return result
