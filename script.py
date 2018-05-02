import json
from urllib.request import Request, urlopen

# Put rules in a json variable
with open('./rules.json', 'r') as f:
    rules = json.load(f)

# Fetch json
url = "https://api.smartcitizen.me/v0/devices/2300"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

data_bytes = urlopen(req).read()

data_string = data_bytes.decode('utf8')

data_json = json.loads(data_string)


#print(data_json['id'], data_json['state'], data_json['kit']['updated_at'])
#print(data_json['owner']['location']['city'])
#print('---')

def get_rule(key, sensorid):
    for i in rules:
        if i['id'] == sensorid:
            return i[key]


#car exhausts id:16, noise data id: 29, air temperature: 12, humidity: 13 and light: 14

for i in data_json['data']['sensors']:
    if i['id'] == 12:
        print('air temp')
    if i['id'] == 13:
        print('humidity')
    if i['id'] == 14:
        print('light')
    if i['id'] == 16:
        print('car exhaust')
        print(get_rule('low', i['id']) * 10 )
        print(get_rule('high',i['id']) * 10 )
    if i['id'] == 29:
        print('noise data')


#print(sensors)
