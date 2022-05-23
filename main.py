import json
import time

import matplotlib.pyplot as plt
import networkx as nx
import requests

if __name__ == "__main__":
    main_url = 'https://api.helium.io/v1/hotspots/location/box?'
    query_box = 'swlat=40.537004&swlon=0.435048&nelat=42.504967&nelon=3.400427'
    # main_url='https://api.helium.io/v1/cities/'
    # query_box='dGFycmFnb25hY2F0YWx1bnlhc3BhaW4/hotspots'
    data = list()
    hotspots = requests.get(main_url + query_box)
    finish = False
    while not finish:
        response = hotspots.json()
        data.extend(response['data'])
        if 'cursor' in response:
            hotspots = requests.get(main_url + 'cursor=' + response['cursor'])
        else:
            finish = True
    g = nx.DiGraph()
    for i in data:
        g.add_node(i['address'], pos=(i['lat'], i['lng']))
    # witness_list = []
    # for i in nx.nodes(g):
    #     witnesses = requests.get('https://api.helium.io/v1/hotspots/' + i + '/witnesses')
    #     response = witnesses.json()
    #     witness_list.append({'hotspot_id': i, 'witnesses': response['data']})
    #     print(i+'\n')
    #     for j in response['data']:
    #         if j['address'] in nx.nodes(g):
    #             g.add_edge(i, j['address'])
    #     time.sleep(1)
    # with open('witness.json', 'w') as f:
    #     json.dump(witness_list, f)
    with open('witness.json') as f:
        data = json.load(f)
        for i in data:
            for j in i['witnesses']:
                if j['address'] in nx.nodes(g):
                    g.add_edge(i['hotspot_id'], j['address'])
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    nx.draw_networkx(g, pos=nx.get_node_attributes(g, 'pos'), node_size=10, with_labels=False, width=0.3)
    plt.show()
    print('esd')
