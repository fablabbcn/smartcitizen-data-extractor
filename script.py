import json, urllib, logging
from urllib.request import Request, urlopen

logging.basicConfig(filename='log.log', level=logging.DEBUG)
logging.debug('Starting...')

# 1. Fetch rules and device list
with urllib.request.urlopen('https://raw.githubusercontent.com/fablabbcn/smartcitizen-data-extractor/master/default_rules.json') as f:
    default_rules = json.loads( f.read().decode() )

with urllib.request.urlopen('https://raw.githubusercontent.com/fablabbcn/smartcitizen-data-extractor/master/special_rules.json') as f:
    special_rules = json.loads( f.read().decode() )

with urllib.request.urlopen('https://raw.githubusercontent.com/fablabbcn/smartcitizen-data-extractor/master/device_list.json') as f:
    device_list = json.loads( f.read().decode() )

# 2. Fetch all devices from the API
final = {}
final['devices'] = []

for dev in device_list:
    url = "https://api.smartcitizen.me/v0/devices/%s" % dev

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    data_bytes = urlopen(req).read()
    data_string = data_bytes.decode('utf8')
    current_device = json.loads(data_string)

    # Clean / remove unwanted data
    current_device.pop('kit', None)
    current_device.pop('owner', None)
    current_device.pop('system_tags', None)
    current_device.pop('user_tags', None)
    current_device.pop('last_reading_at', None)
    current_device.pop('state', None)
    current_device.pop('mac_address', None)
    current_device.pop('last_reading_at', None)
    for sens in current_device['data']['sensors']:
        sens.pop('ancestry', None)
        sens.pop('created_at', None)
        sens.pop('description', None)
        sens.pop('measurement_id', None)
        sens.pop('name', None)
        sens.pop('prev_raw_value', None)
        sens.pop('prev_value', None)
        sens.pop('unit', None)
        sens.pop('uuid', None)
    final['devices'].append(current_device)

# FUNCTIONS
def get_rule(deviceid, key, sensorid):
    for i in special_rules:
        # If we find deviceID inside the special_rules, we apply its magic values
        if deviceid == i['device_id']:
            #print('special_rule:', (deviceid, key, sensorid))
            for j in special_rules:
                if j['id'] == sensorid:
                    return j[key]
        else:
            #print('default_rule:', (deviceid, key, sensorid))
            for j in default_rules:
                if j['id'] == sensorid:
                    return j[key]

def calculate(deviceid, sensorid, current_value):
    high = get_rule(deviceid, 'high', sensorid)
    low =  get_rule(deviceid, 'low', sensorid)
    logging.debug('high: %f low: %f' %(high,low))

    if current_value == None:
        logging.debug('Value is null. Nothing to do')
        return 0
    else:
        new_value = (current_value - low) / (high - low)
        new_value = abs(new_value)
        new_value = round(new_value, 3)
        #print(new_value)

    """
    if new_value > 1:
        print('ERR')
    if new_value < 0:
        print('ERR')
    """

    return new_value

# 4. Extract data
# Real value / HIGH value?
for device in final['devices']:
    for sensor in device['data']['sensors']:
        if sensor['id'] == 12:
            #print('air temp')
            sensor['value'] = calculate(device['id'], sensor['id'], sensor['value'])
        if sensor['id'] == 13:
            #print('humidity')
            sensor['value'] = calculate(device['id'], sensor['id'], sensor['value'])
        if sensor['id'] == 14:
            #print('light')
            sensor['value'] = calculate(device['id'], sensor['id'], sensor['value'])
        if sensor['id'] == 16:
            #print('car exhaust')
            sensor['value'] = calculate(device['id'], sensor['id'], sensor['value'])
        if sensor['id'] == 29:
            #print('noise data')

#print(final)
# 6. Write final data file
with open('./data.json', 'w') as outfile:
    json.dump(final, outfile, indent=2, sort_keys=True)
