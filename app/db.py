import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv
from dotenv import load_dotenv


class DB:
    load_dotenv()
    HOST = getenv("host")
    USER = getenv("user")
    PASSWORD = getenv("password")
    DBNAME = getenv("database")

    def conn(self):
        try:
            conn = psycopg2.connect(
                host=self.HOST,
                database=self.DBNAME,
                user=self.USER,
                password=self.PASSWORD,
                cursor_factory=RealDictCursor,
            )
            return conn
        except Exception as e:
            print("cant connect")
