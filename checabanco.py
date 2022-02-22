import mysql.connector
import time

while True:
    conn = mysql.connector.connect(
    host="localhost",
    user="botmon",
    password="seila123",
    database="monitoring"
    )
    c = conn.cursor()
    status = c.execute("SELECT * FROM monitor")

    linha = c.fetchall()
    conn.commit()
    print(linha)

    conn.close()
time.sleep(10)