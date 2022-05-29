import json
import statistics

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy
from networkx.algorithms.community import greedy_modularity_communities, louvain_communities
from numpy.core.defchararray import upper

from definitions import zones, colors

# Script for read .json data files and build the networks

if __name__ == "__main__":
    for i in zones:
        g = nx.DiGraph()
        pos = {}
        with open('hotspots/hotspots-' + i['name'] + '.json') as f:
            data = json.load(f)
        for j in data:
            g.add_node(j['address'], pos=(j['lat'], j['lng']))
            pos[j['address']] = numpy.array([j['lat'], j['lng']])
        with open('witness/witness-' + i['name'] + '.json') as f:
            data = json.load(f)
            for k in data:
                for m in k['witnesses']:
                    if m['address'] in nx.nodes(g):
                        g.add_edge(k['hotspot_id'], m['address'])
        matplotlib.use('pdf')
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()

        nx.draw_networkx(g, pos=nx.get_node_attributes(g, 'pos'), node_size=10, with_labels=False, width=0.3, arrowstyle='->')
        plt.savefig(i['name'] + ".pdf")
        plt.clf()
        print('**************')
        print(upper(i['name']))
        print('\tNumber of hotstops: ' + str(nx.number_of_nodes(g)))
        print('\tNumber of witnessing: ' + str(nx.number_of_edges(g)))
        print('\tMax in degree: ' + str(max(list(len(g.in_edges(i)) for i in nx.nodes(g)))))
        print('\tMax out degree: ' + str(max(list(len(g.out_edges(i)) for i in nx.nodes(g)))))
        print('\tAvg in degree: ' + str(statistics.mean(list(len(g.in_edges(i)) for i in nx.nodes(g)))))
        print('\tAvg out degree: ' + str(statistics.mean(list(len(g.out_edges(i)) for i in nx.nodes(g)))))
        print('\tAvg clustering coefficient: ' + str(nx.average_clustering(g)))

        if i['name'] == 'catalunya':
            plt.gca().invert_xaxis()
            plt.gca().invert_yaxis()
            nx.draw_networkx_edges(g, pos, edge_color='k', width=0.3, node_size=20, arrowstyle='->')
            color = 0
            communities = [list(i) for i in greedy_modularity_communities(g)]
            for c in communities:
                if len(c) > 10:
                    color += 1
                    color_index = color
                else:
                    color_index = 0
                nx.draw_networkx_nodes(g, pos, nodelist=c, node_color=colors[color_index], node_size=10)
            plt.savefig(i['name'] + "-community.pdf")
            plt.clf()

