import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
  conn = psycopg2.connect(
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ.get("POSTGRES_HOST", "localhost"),
    port=os.environ.get("POSTGRES_PORT", 5432),
  )

  print('b1')

  cur = conn.cursor()
  cur.execute("select 1;")
  print(cur.fetchone()[0])

  cur.close()
  conn.close()
except Exception:
  print('connection to database failed')
  print(Exception)
