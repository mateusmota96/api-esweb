import time

from dict import error_dict
import requests
import mysql.connector

# STRING UPDATE BD
update_status = "UPDATE monitor SET status = "
update_http = ", http_code = "

# HEADER HTTP
request_header = 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'

while True:

    # CONNECTOR MYSQL
    conn = mysql.connector.connect(
        host="localhost",
        user="botmon",
        password="seila123",
        database="monitoring"
    )
    c = conn.cursor(buffered=True)

    # SELECT URL
    status = c.execute("SELECT url FROM monitor")
    string = str.replace(str(c.fetchall()), "(", "").replace(",", "").replace(")", "").replace("[", "").replace("]", "").replace(" ", ",").replace('"',"")
    urls = string.split(",")

    for url in urls:
        try:
            url = str.replace(url, "'", "")

            # REQUISICAO
            req = requests.get(url, headers={'User-Agent': request_header}, timeout=3)
            http_code = int(req.status_code)
            condiction = " WHERE url = '" + str(url) + "'"

            # STRING ERROR
            str_error = "SELECT error FROM monitor" + condiction
            c.execute(str_error)
            bd_error = int(str.replace(str(c.fetchone()),"(","").replace(",)",""))

            # STRING NOTIFY
            str_notify = "SELECT notify FROM monitor" + condiction
            c.execute(str_notify)
            bd_notify = int(str.replace(str(c.fetchone()),"(","").replace(",)",""))

            # STRING SEND_NOTIFY
            str_send = "SELECT send_notify FROM monitor" + condiction
            c.execute(str_send)
            send_notify = int(str.replace(str(c.fetchone()),"(","").replace(",)",""))

            # CHECK IF ERROR
            # IF ERROR !=200 AND (ERROR AND NOTIFY = 0) THEN SET ERROR = 1
            if http_code != 200 and http_code != 403 and http_code != 302 and bd_error == 0 and send_notify == 0:
                str_error = " , error = 1, notify = 1 "
                up_stat = str(update_status + str(str(error_dict[str(http_code)])))
                updateall= up_stat + update_http + str(http_code) + str_error + condiction
                c.execute(updateall)
                conn.commit()
            # ELIF ERROR != 200 AND ERROR = 1 AND NOTIFY = 0 THEN SET NOTIFY = 1
            elif ((http_code != 200 and http_code != 403 and http_code != 302) and bd_error == 1 and bd_notify == 0 and send_notify == 0) or (http_code == 200 and bd_error == 1 and bd_notify == 0):
                str_error = " , error = 1"
                str_notify = " , notify = 1"
                up_stat = str(update_status + str(str(error_dict[str(http_code)])))
                updateall = up_stat + update_http + str(http_code) + str_error + str_notify + condiction
                c.execute(updateall)
                conn.commit()
            # ELIF HTTP_CODE = 200 AND ERROR = 1 THEN STILL SET ERROR 1 TO (RE-UP)
            elif http_code == 200 and bd_error == 1 and send_notify == 0:
                str_error = " , error = 1"
                up_stat = str(update_status + str(str(error_dict[str(http_code)])))
                updateall = up_stat + update_http + str(http_code) + str_error + str_notify + condiction
                c.execute(updateall)
                conn.commit()
            # ELIF HTTP_CODE = 200 AND ERROR = 1 AND NOTIFY = 1 THEN ZERO ALL FIELDS
            elif http_code == 200 and bd_error == 1 and send_notify == 1:
                update_http = ", http_code = "
                str_error = " , error = 0, notify = 0, send_notify = 1"
                up_stat = str(update_status + str(str(error_dict[str(http_code)])))
                updateall = up_stat + update_http + str(http_code) + str_error + condiction
                c.execute(updateall)
                conn.commit()

            # ELIF
            elif http_code == 200 and bd_error == 0 and bd_notify == 0:
                str_error = " , error = 0"
                up_stat = str(update_status + str(str(error_dict[str(http_code)])))
                updateall = up_stat + update_http + str(http_code) + condiction
                print(updateall)
                c.execute(updateall)
                conn.commit()

        except:
            http_code = 999
            # UPDATE STATUS ERROR IN BD
            str_error = " , error = 1"
            condiction = " WHERE url = '" + str(url) + "'"
            dicio = str(http_code)
            up_stat = str(update_status + str(str(error_dict[dicio])) + str_error + condiction)
            up_http = str(update_http + str(http_code) + str_error + condiction)
            c.execute(up_stat)
            c.execute(up_http)
            conn.commit()