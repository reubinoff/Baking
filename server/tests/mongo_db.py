from os import environ

environ["DB_CONN_STR"] = "mongodb://root:test@localhost:27017/"

environ["azure_storage_connection_string"] = ""
environ["is_debug"] = "True"

environ["DB_NAME"] = "test"

from baking.database.manage import init_database

mongo_db = init_database()

