import psycopg2

 conn = psycopg2.connect(
            host="dpg-d3412cjuibrs73b0m3t0-a.singapore-postgres.render.com",
            database="expense_tracker_db_i6nk",
            user="expense_tracker_db_i6nk_user",
            password="SWoddph65axD4fgQrLUpGtY0nYA35K7F",
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
