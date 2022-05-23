import json
import time

import matplotlib.pyplot as plt
import networkx as nx
import requests

if __name__ == "__main__":
    main_url = 'https://api.helium.io/v1/hotspots/location/box?'
    query_box = 'swlat=40.537004&swlon=0.435048&nelat=42.504967&nelon=3.400427'
    g = nx.DiGraph()
    with open('hotspots.json') as f:
        data = json.load(f)
    for i in data:
        g.add_node(i['address'], pos=(i['lat'], i['lng']))
    with open('witness.json') as f:
        data = json.load(f)
        for i in data:
            for j in i['witnesses']:
                if j['address'] in nx.nodes(g):
                    g.add_edge(i['hotspot_id'], j['address'])
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    nx.draw_networkx(g, pos=nx.get_node_attributes(g, 'pos'), node_size=10, with_labels=False, width=0.3)
    plt.show()
