import sqlite3

sites = [
    'http://www.example.com/',
    'http://www.example2.com/'
]

conn = sqlite3.connect('monitoraesweb.db')
c = conn.cursor()
try:
    c.execute("""SELECT * FROM monitora""")
except sqlite3.OperationalError:
    # CRIA O BANCO E A TABELA
    c.execute("""CREATE TABLE monitora (
        id int auto_increment,
        http_status integer,
        status text,
        site text,    
        erro integer
        )""")
    conn.commit()

    # INSERE OS VALORES DE ACORDO COM OS SITES
    for site in sites:
        execute = "INSERT INTO monitora VALUES (null, 200, 'OK', '" + str(site) + "', 0)"
        c.execute(execute)
        conn.commit()

conn.close()