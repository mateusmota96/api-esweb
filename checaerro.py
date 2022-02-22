import sqlite3
import time

while True:
    conn = sqlite3.connect('monitoraesweb.db')
    c = conn.cursor()
    status = c.execute("SELECT * FROM monitoramento WHERE erro = 1")

    linha = c.fetchall()
    conn.commit()
    print(linha)

    conn.close()
    time.sleep(10)