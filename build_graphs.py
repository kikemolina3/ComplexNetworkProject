import json

import matplotlib.pyplot as plt
import networkx as nx

from definitions import zones

# Script for read .json data files and build the networks

if __name__ == "__main__":
    for i in zones:
        g = nx.DiGraph()
        with open('hotspots/hotspots-' + i['name'] + '.json') as f:
            data = json.load(f)
        for j in data:
            g.add_node(j['address'], pos=(j['lat'], j['lng']))
        with open('witness/witness-' + i['name'] + '.json') as f:
            data = json.load(f)
            for k in data:
                for m in k['witnesses']:
                    if m['address'] in nx.nodes(g):
                        g.add_edge(k['hotspot_id'], m['address'])
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
        # wm = plt.get_current_fig_manager()
        # wm.window.state('zoomed')
        nx.draw_networkx(g, pos=nx.get_node_attributes(g, 'pos'), node_size=10, with_labels=False, width=0.3)
        plt.show()
