import time
from dict import error_dict
import telebot
import requests
import json

bot = telebot.TeleBot("5097997910:AAGJDPbxF1DazJx6r96KlwzNueh7AzvUehk")
limit = 9999
client = 'SERRANO'

while True:
    urlapi = "http://sentinel-webtest.api.mateus.com.br/domain/list?limit=" + str(limit) + "&client=" + client
    req = requests.get(urlapi)
    arrayjson = json.loads(req.content)
    for element in arrayjson:
        url = element['url']
        http_code = int(element['http_code'])
        status = element['status']
        error = int(element['error'])
        notify = int(element['notify'])
        identify = element['id']
        send_notify = element['send_notify']

        if http_code != 200 and http_code != 403 and http_code != 301 and http_code != 302 and \
                (error == 1 and notify == 1 and send_notify == 0):
            # STATUS
            status = "'ERROR'"
            dicio = str(http_code)
            strstatus = status.replace("'", "")
            message_http = "❌ [<b>" + strstatus + "</b>]\n"

            # MENSAGEM
            servidor = "<b>Servidor:</b> " + url + "\n<b>Status Code:</b> [" + str(http_code) + "] - "
            message = message_http + servidor + error_dict[dicio]
            data = {"id": str(identify)}
            try:
                bot.send_message('-606686746', message, parse_mode='html')
                requests.post('http://sentinel-webtest.api.mateus.com.br/notify/post', data)
                requests.post('http://sentinel-webtest.api.mateus.com.br/delnotify/postsend', data)
            except TimeoutError:
                print("Timeout ERROR")
            except:
                print("UNKNOWN ERROR")

        elif (http_code == 200 or http_code == 301 or http_code == 302) and \
                (error == 0 and notify == 0 and send_notify == 1):
            # STATUS
            status = "'RE-UP'"
            dicio = str(http_code)
            strstatus = status.replace("'", "")
            message_http = "✅ [<b>" + strstatus + "</b>]\n"

            # MENSAGEM
            servidor = "<b>Servidor:</b> " + url + "\n<b>Status Code:</b> [" + str(http_code) + "] - "
            message = message_http + servidor + error_dict[dicio] + "\n<i>Servidor Voltou a Responder!</i>"
            data = {"id": str(identify)}
            try:
                requests.post('http://sentinel-webtest.api.mateus.com.br/notify/post', data)
                requests.post('http://sentinel-webtest.api.mateus.com.br/delnotify/delsend', data)
                bot.send_message('-606686746', message, parse_mode='html')

            except TimeoutError:
                print("Timeout ERROR")
            except:
                print("UNKNOWN ERROR")

    time.sleep(10)