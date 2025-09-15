import psycopg2

conn = psycopg2.connect(
    host="your-host",
    database="your-db-name",
    user="your-db-user",
    password="your-db-password",
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
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  date VARCHAR(20),
  description TEXT,
  amount NUMERIC,
  category VARCHAR(50)
);
""")

conn.commit()
cursor.close()
conn.close()
print("Users table created.")
