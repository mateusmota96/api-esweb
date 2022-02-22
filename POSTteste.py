import requests

cliente = 'SERRANO'
id = 1

data = {"id": str(id)}
# Aviso = 1 x = requests.post('http://sentinel-webtest.api.mateus.com.br/delnotify/postaviso', data)
x = requests.post('http://sentinel-webtest.api.mateus.com.br/delnotify/delaviso', data) # Aviso = 0
print(x.content)