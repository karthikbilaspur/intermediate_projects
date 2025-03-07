import mysql.connector
import psycopg2
def backup_mysql(db_host, db_user, db_password, db_name):
    cnx = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )
    cursor = cnx.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"SELECT * FROM {table[0]}")
        rows = cursor.fetchall()
def backup_postgresql(db_host, db_user, db_password, db_name):
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )
    cur = conn.cursor()
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    tables = cur.fetchall()
    for table in tables:
        cur.execute(f"SELECT * FROM {table[0]}")
        rows = cur.fetchall()
