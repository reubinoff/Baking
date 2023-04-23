from os import environ

environ["DB_PASS"] = "test"
environ["DB_HOST"] = "localhost"
environ["DB_NAME"] = "test"
environ["DB_USER"] = "root"
environ["azure_storage_connection_string"] = ""
environ["is_debug"] = "True"


from baking.database.manage import init_database

mongo_db = init_database()

