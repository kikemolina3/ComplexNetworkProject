import json
import time

import requests

from definitions import zones

# Script for collect all data from Helium REST API,
# Writes data into .json files

if __name__ == "__main__":
    for i in zones:
        data = []
        hotspots = requests.get(i['url'])
        finish = False
        while not finish:
            response = hotspots.json()
            data.extend(response['data'])
            if 'cursor' in response:
                hotspots = requests.get(i['url'] + 'cursor=' + response['cursor'])
            else:
                finish = True
        with open('hotspots/hotspots-' + i['name'] + '.json', 'w') as f:
            json.dump(data, f)
        witness_list = []
        for j in data:
            witnesses = requests.get('https://api.helium.io/v1/hotspots/' + j['address'] + '/witnesses')
            response = witnesses.json()
            print('---\n')
            witness_list.append({'hotspot_id': j['address'], 'witnesses': response['data']})
            time.sleep(1)
        with open('witness/witness-' + i['name'] + '.json', 'w') as f:
            json.dump(witness_list, f)
