import psycopg2
from app import Config

def execute_query(query, params=None):
    conn = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI)
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()