import json
import statistics

import matplotlib.pyplot as plt
import networkx as nx
from numpy.core.defchararray import upper

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
        # nx.draw_networkx(g, pos=nx.get_node_attributes(g, 'pos'), node_size=10, with_labels=False, width=0.3)
        # plt.show()
        print('**************')
        print(upper(i['name']))
        print('\tNumber of hotstops: ' + str(nx.number_of_nodes(g)))
        print('\tNumber of witnessing: ' + str(nx.number_of_edges(g)))
        print('\tMax in degree: ' + str(max(list(len(g.in_edges(i)) for i in nx.nodes(g)))))
        print('\tMax out degree: ' + str(max(list(len(g.out_edges(i)) for i in nx.nodes(g)))))
        print('\tAvg in degree: ' + str(statistics.mean(list(len(g.in_edges(i)) for i in nx.nodes(g)))))
        print('\tAvg out degree: ' + str(statistics.mean(list(len(g.out_edges(i)) for i in nx.nodes(g)))))
        print('\tAvg clustering coefficient: ' + str(nx.average_clustering(g)))
