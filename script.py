import json
from urllib.request import Request, urlopen

# 1. Fetch default_rules into a json variable
with open('./default_rules.json', 'r') as f:
    default_rules = json.load(f)

with open('./special_rules.json', 'r') as f:
    special_rules = json.load(f)

# 2. Fetch all devices from the API
#device_list = [2300, 2301, 2304]
device_list = [2300, 2301]
final = {}
final['devices'] = []

for dev in device_list:
    url = "https://api.smartcitizen.me/v0/devices/%s" % dev

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
    for sens in api_json['data']['sensors']:
        sens.pop('ancestry', None)
        sens.pop('created_at', None)
        sens.pop('description', None)
        sens.pop('measurement_id', None)
        sens.pop('name', None)
        sens.pop('prev_raw_value', None)
        sens.pop('prev_value', None)
        sens.pop('unit', None)
        sens.pop('uuid', None)
    final['devices'].append(api_json)

# 3. Add each device to the final json

# FUNCTIONS

def get_rule(deviceid, key, sensorid):
    for i in special_rules:
        if deviceid == i['device_id']:
            print('SPECIAL')
            for i in special_rules:
                if i['id'] == sensorid:
                    return i[key]
        else:
            print('NOT SPECIAL')
            for i in default_rules:
                if i['id'] == sensorid:
                    return i[key]

def update_key_with_value(key, value):
    print('Normalizing sensor id: %s with value %f' % (key, value))
    for device in final['devices']:
        for sensor in device['data']['sensors']:
            if sensor['id'] == key:
                #print('FOUND', key)
                sensor['value'] = value

# 4. Extract data
for device in final['devices']:
    for i in device['data']['sensors']:
        if i['id'] == 12:
            #print('air temp')
            # Apply correct rule
            update_key_with_value(i['id'], 0.22222)
        if i['id'] == 13:
            #print('humidity')
            update_key_with_value(i['id'], 0.33333)
        if i['id'] == 14:
            #print('light')
            update_key_with_value(i['id'], 0.44444)
        if i['id'] == 16:
            #print('car exhaust')
            #print(get_rule(device['id'], 'low', i['id']) * i['raw_value'] )
            tmp_val = get_rule(device['id'], 'high', i['id'])
            print('tmp_val', tmp_val)
            update_key_with_value(i['id'], 0.66666)
        if i['id'] == 29:
            #print('noise data')
            update_key_with_value(i['id'], 0.99999)


#print(final)
# 6. Write final data file
with open('./data.json', 'w') as outfile:
    json.dump(final, outfile, indent=2, sort_keys=True)
