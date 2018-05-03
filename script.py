import json
from urllib.request import Request, urlopen

# 1. Fetch rules into a json variable
with open('./rules.json', 'r') as f:
    rules = json.load(f)

# 2. Fetch new data as json
device_list = [2300, 2301]
url = "https://api.smartcitizen.me/v0/devices/2300"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

data_bytes = urlopen(req).read()
data_string = data_bytes.decode('utf8')
api_json = json.loads(data_string)

# Clean / remove unwanted data
api_json.pop('kit', None)
api_json.pop('owner', None)
api_json.pop('system_tags', None)
api_json.pop('user_tags', None)
api_json.pop('last_reading_at', None)
api_json.pop('state', None)
api_json.pop('mac_address', None)
api_json.pop('last_reading_at', None)

final = {}

# 3. Add each device to the final json
final['devices'] = [api_json, api_json]

def get_rule(key, sensorid):
    for i in rules:
        if i['id'] == sensorid:
            return i[key]

def change_key_with_value(key, value):
    print('changing sensor id: %s with value %f' % (key, value))
    print('-----')
    for device in final['devices']:
        for sensor in device['data']['sensors']:
            if sensor['id'] == key:
                #print('FOUND', key)
                sensor['value'] = value

# 4. Extract data
for i in api_json['data']['sensors']:
    if i['id'] == 12:
        #print('air temp')
        change_key_with_value(i['id'], 0.22)
    if i['id'] == 13:
        #print('humidity')
        change_key_with_value(i['id'], 0.33)
    if i['id'] == 14:
        #print('light')
        change_key_with_value(i['id'], 0.44)
    if i['id'] == 16:
        #print('car exhaust')
        #print(get_rule('low', i['id']) * i['raw_value'] )
        #print(get_rule('high',i['id']) * 10 )
        change_key_with_value(i['id'], 0.66)
    if i['id'] == 29:
        #print('noise data')
        change_key_with_value(i['id'], 0.99)



#print(final)
# 6. Write final data file
with open('./data.json', 'w') as outfile:
    json.dump(final, outfile, indent=2, sort_keys=True)
