from psycopg2 import extensions
import psycopg2 as psc

def database():
     db_params = {
    "dbname": "rkrish_db",
    "user": "radhakrishnan",
    "password": "weJyKwjSj60UNzr4MXIEZ79FV7sf2ZHY",
    "host": "dpg-coiuro5jm4es739v1hvg-a.oregon-postgres.render.com",
    "port": "5432"  # Default PostgreSQL port is 5432
     }
     # db_params = " postgresql://radhakrishnan:weJyKwjSj60UNzr4MXIEZ79FV7sf2ZHY@dpg-coiuro5jm4es739v1hvg-a.oregon-postgres.render.com/rkrish_db"
     dsn = extensions.make_dsn(**db_params)
     conn = psc.connect(dsn)
     cursor = conn.cursor()
     return cursor