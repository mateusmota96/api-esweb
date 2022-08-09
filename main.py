# THIS BOT SENDS MESSAGE IN TELEGRAM_BOT WHEN YOUR WEBSITE IS DOWN
from logger import ErrorLog
from configparser import ConfigParser
import telebot
import requests
import json
import time

parser = ConfigParser()
parser.read('config.ini')
bot = telebot.TeleBot("5097997910:AAGJDPbxF1DazJx6r96KlwzNueh7AzvUehk")
limit = 9999
request_header = 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'

while True:
    urlapi = "http://sentinel-web.api.esweb.com.br/domain/list?limit=" + str(limit) + "&status=all"
    req = requests.get(urlapi, headers={'User-Agent': request_header}, timeout=10)
    arrayjson = json.loads(req.content)
    for element in arrayjson:
        url = str(element['url'])
        http_code = int(element['http_code'])
        status = str(element['status'])
        error = int(element['error'])
        notify = int(element['notify'])
        identify = int(element['id'])
        send_notify = int(element['send_notify'])
        if error == 1 and notify == 1:
            # STATUS
            status = "'ERROR'"
            error_dict = parser.get('http_error', str(http_code))
            strstatus = status.replace("'", "")
            message_http = "❌ [<b>" + strstatus + "</b>]\n"

            # MESSAGE
            server = "<b>Server:</b> " + url + "\n<b>Status Code:</b> [" + str(http_code) + "] - "
            message = message_http + server + error_dict
            data = {"id": str(identify)}
            try:
                bot.send_message('-648269755', message, parse_mode='html')
                # UNSET NOTIFY -> notify = 0
                requests.post('http://sentinel-web.api.esweb.com.br/notify/post',
                                    headers={'User-Agent': request_header}, data=data)
            except Exception as err:
                ErrorLog('ERROR', err)

        elif error == 0 and send_notify == 1:
            # STATUS
            status = "'RE-UP'"
            error_dict = parser.get('http_error', str(http_code))
            strstatus = status.replace("'", "")
            message_http = "✅ [<b>" + strstatus + "</b>]\n"

            # MESSAGE
            server = "<b>Server:</b> " + url + "\n<b>Status Code:</b> [" + str(http_code) + "] - "
            message = message_http + server + error_dict + "\n<i>Server is Up Again!</i>"
            data = {"id": str(identify)}
            try:
                # UNSET SEND-NOTIFY -> send_notify = 0
                requests.post('http://sentinel-web.api.esweb.com.br/notify/del',
                              headers={'User-Agent': request_header}, data=data)
                bot.send_message('-648269755', message, parse_mode='html')

            except Exception as err:
                ErrorLog('ERROR', err)

    time.sleep(10)
