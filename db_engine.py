from sqlalchemy import create_engine
from db_config import DB_CONFIG


def get_engine():

    user = DB_CONFIG["user"]
    password = DB_CONFIG["password"]
    host = DB_CONFIG["host"]
    database = DB_CONFIG["database"]
    port = DB_CONFIG["port"]

    engine_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(engine_url)

    return engine
