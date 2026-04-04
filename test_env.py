from app.config import settings
import psycopg2

url = settings.database_url
print(f"Trying to connect using URL: {url}")

try:
    conn = psycopg2.connect(url)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")