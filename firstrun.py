import mysql.connector

# URLS for INSERT into table
urls = [
    'http://www.balbinoleiloes.com.br',
    'http://www.carloferrarileiloes.com.br',
    'http://www.cearaleiloes.com.br',
    'http://www.cidafixerleiloes.com.br',
    'http://www.danieloliveiraleiloes.com.br',
    'http://www.deonizialeiloes.com.br',
    'http://www.dinizmartinsleiloes.com.br',
    'http://www.dmleiloesjudiciais.com.br',
    'http://www.fabiobarbosaleiloes.com.br',
    'http://www.fabioleiloes.com.br',
    'http://www.fernandoserranopalestras.com.br',
    'http://www.fidelisleiloes.com.br',
    'http://www.gilsoninumaruleiloes.com.br',
    'http://www.gilsonleiloes.com.br',
    'http://www.hdleiloes.com.br',
    'http://www.imobiliariaportugal.com.br',
    'http://www.jdleiloes.com.br',
    'http://www.leiloeirofernandoserrano.com.br',
    'http://www.leiloesdajustica.com.br',
    'http://www.leiloesjudiciaisbahia.com.br',
    'http://www.leiloesjudiciaismg.com.br',
    'http://www.leiloesjudiciaismgnorte.com.br',
    'http://www.leiloesjudiciaisparaiba.com.br',
    'http://www.vicenteleiloes.com.br',
    'http://www.leiloesjudiciaisdf.com.br',
    'http://www.docsleilao.esweb.com.br',
    'http://www.nortebahialeiloes.com.br',
    'http://www.alessandroteixeiraleiloes.com.br',
    'http://www.giordanoleiloes.com.br',
    'http://www.administracaodeativos.com.br',
    'http://www.leiloesjudiciaisparana.com.br',
    'http://www.nortebahialeiloes.com.br',
    'http://www.galvanileiloes.com.br',
    'http://www.leiloescentrooeste.com.br',
    'http://www.giordanoleiloes.com.br',
    'http://www.brunoleiloes.com.br',
    'http://www.brunoleiloesjudiciais.com.br',
    'http://www.matogrossoleiloes.com.br',
    'http://www.dasilvaleiloes.com.br',
    'http://www.sudesteleiloes.com.br',
    'http://www.bomnegocioleiloes.com.br',
    'http://www.desouzaleiloes.com.br',
    'http://www.cearaleiloes.com.br',
    'http://www.verdeamareloleiloes.com.br',
    'http://www.akimotoleiloes.com.br',
    'http://www.paulistanaleiloes.com.br',
    'http://www.alvaroleiloes.com.br',
    'http://localhost/phpinfo.php'
]

conn = mysql.connector.connect(
    host="localhost",
    user="botmon",
    password="seila123",
)
c = conn.cursor()

# CREATE DB
c.execute("""CREATE DATABASE IF NOT EXISTS monitoring""")
conn.commit()

try:
    # CREATE TABLE
    c.execute("USE monitoring")
    conn.commit()
    c.execute("""CREATE TABLE monitor (
        id int auto_increment,
        client varchar(50),
        url varchar(100),
        http_code int,
        status varchar(50),                    
        error int,
        notify int,
        send_notify int,
        PRIMARY KEY (id)
        )""")
    conn.commit()
except:
    print("Error into DB creation")

# INSERT URLS INTO monitor
for url in urls:
    execute = "INSERT INTO monitor VALUES (null, 'SERRANO', '" + str(url) + "', 200, 'OK' , 0, 0, 0)"
    c.execute(execute)
    conn.commit()

conn.close()