from pydantic_settings import BaseSettings
class BakingConfig(BaseSettings):
    is_debug: bool = False
    service_name: str = "testing-service"  # will be replaced in env var

    log_level: str = "DEBUG"

    db_conn_str: str
    db_name: str

    db_debug_drop_in_startup: bool = False

    root_path:str = ""

    azure_storage_connection_string: str
    azure_cdn_storage_base_url: str = "https://images.baking.reubinoff.com"

settings = BakingConfig()
