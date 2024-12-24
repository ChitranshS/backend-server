from psycopg_pool import ConnectionPool

import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")

connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}
connection_pool = ConnectionPool(
    conninfo=DB_URI,
    max_size=20,
    kwargs=connection_kwargs,
)