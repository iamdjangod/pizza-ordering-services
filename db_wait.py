import psycopg2
import time
import os

params = {
  'database': os.environ.get('DB_NAME'),
  'user': os.environ.get('DB_USER'),
  'password': os.environ.get('DB_PWD'),
  'host': os.environ.get('DB_HOST'),
  'port': os.environ.get('DB_PORT')
}

conn = None

while conn is None:
    try:
        conn = psycopg2.connect(**params)
    except psycopg2.OperationalError:
        conn = None
        print("Database not yet ready, sleeping 1 sec...")
        time.sleep(1)

print("Database is ready, lets do some migrations!!!")
