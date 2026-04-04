from app.config import settings
import psycopg2

print(f"Using DATABASE_URL: {settings.database_url}")

try:
    conn = psycopg2.connect(settings.database_url)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")