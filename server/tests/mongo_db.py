from os import environ

environ["DB_PASS"] = "test"
environ["DB_HOST"] = "localhost"
environ["DB_NAME"] = "test"
environ["DB_USER"] = "root"
environ["azure_storage_connection_string"] = "test.com"
environ["is_debug"] = "True"


from baking.database.manage import get_client
from baking.config import settings as app_settings

mongo_db = get_client()[app_settings.db_name]

