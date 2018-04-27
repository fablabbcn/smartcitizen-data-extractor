import json
from urllib.request import Request, urlopen

url = "https://api.smartcitizen.me/v0/devices/2300"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

data_bytes = urlopen(req).read()

data_string = data_bytes.decode('utf8')

data_json = json.loads(data_string)


print(data_json['id'])
print(data_json['state'])
print(data_json['kit']['updated_at'])
print(data_json['owner']['location']['city'])

sensors = data_json['data']['sensors']

for i in sensors:
    if i['id'] == 29:
        print('found id 29')
    if i['id'] == 16:
        print('found id 16')

#print(sensors)

