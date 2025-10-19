# To test database connection and query tables, run this script independently:
# python test_db_conn.py
# Make sure venv is activated and required packages are installed
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv("DB_URL")


def main():
    conn = psycopg2.connect(DATABASE_URL)

    query_sql = 'SELECT VERSION()'

    cur = conn.cursor()
    cur.execute(query_sql)

    version = cur.fetchone()
    print(version)

    # Query information_schema.tables to get table names
    # Exclude system tables from pg_catalog and information_schema
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        AND table_schema NOT IN ('pg_catalog', 'information_schema');
    """)

    table_names = [row[0] for row in cur.fetchall()]
    print("Tables in the database:")  # currently 1 table: 'users'
    for table_name in table_names:
        print(table_name)

    # Get all users from the users table
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    print("Users in the users table:")
    for user in users:
        print(user)

    cur.close()
    # conn.close()


if __name__ == "__main__":
    main()