import threading
import time
from dict import error_dict
import requests
import mysql.connector

# STRING UPDATE BD
update_status = "UPDATE monitor SET status = "
update_http = ", http_code = "

# HEADER HTTP
request_header = 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'



# CONNECTOR MYSQL
conn = mysql.connector.connect(
    host="localhost",
    user="botmon",
    password="seila123",
    database="monitoring"
)
c = conn.cursor(buffered=True)

# SELECT URL
status = c.execute("select url from monitor where id in (1,2,3,4,5,6,7,8,9,10)")
status2 = c.execute("select url from monitor where id in (11,12,13,14,15,16,17,18,19,20)")
status3 = c.execute("select url from monitor where id in (21,22,23,24,25,26,27,28,29,30)")
status = c.execute("select url from monitor where id in (1,2,3,4,5,6,7,8,9,10)")
status = c.execute("select url from monitor where id in (1,2,3,4,5,6,7,8,9,10)")
string = str.replace(str(c.fetchall()), "(", "").replace(",", "").replace(")", "").replace("[", "").replace("]", "").replace(" ", ",").replace('"',"")
urls = string.split(",")


start = time.time()
array = (0,1,2,3)

while True:
    def funcao(num):
        start = time.time()
        for n in num:
            print("Tread1, number: ",n)
        print("Time execution: ", float(time.time()) - start, " sec")

    def funcao2(num):
        start = time.time()
        for n in num:
            print("Tread2, number: ",n)
        print("Time execution: ", float(time.time()) - start, " sec")

    t1= threading.Thread(target=funcao(array), args=(array,))
    t2= threading.Thread(target=funcao2(array), args=(array,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

