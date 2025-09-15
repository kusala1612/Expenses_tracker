import psycopg2

conn = psycopg2.connect(
    host="your-host",
    database="your-db",
    user="your-user",
    password="your-password",
    port=5432
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  password TEXT NOT NULL
);
""")

conn.commit()
cursor.close()
conn.close()
print("Users table created.")
