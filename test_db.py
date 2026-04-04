import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="user",
        password="password",
        database="taskdb"
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
