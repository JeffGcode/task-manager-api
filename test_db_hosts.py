import psycopg2

def test_connect(host):
    try:
        conn = psycopg2.connect(
            host=host,
            port=5432,
            user="user",
            password="password",
            database="taskdb"
        )
        print(f"✅ Connection successful via {host}")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed via {host}: {e}")
        return False

test_connect("localhost")
test_connect("127.0.0.1")
test_connect("::1")