import networkx as nx
from collections import deque


def run(G):
    initial_nodes = ['RocknRolla', 'The League of Extraordinary Gentlemen', 'David Hemmings', 'Comedy']

    # Enqueue all initial nodes
    queue = deque([node for node in initial_nodes])
    initial_energy = 1
    initial_nodes.reverse()

    for node in initial_nodes:
        # Set the energy of each initial node to some constant
        # the key is 'node' (id of node)
        nx.set_node_attributes(G, {node: [initial_energy]}, 'energy')

    recommendations = []
    # each initial node must visit 10 nodes
    # TODO: We should run this until the required number of nodes is visited from each initial node
    required_nodes = 10

    while len(queue) > 0:
        current = queue.pop()
        current_attr = G.nodes(data=True)[current]

        if current_attr['node_type'] == 'movie' and \
                len(current_attr['energy']) == len(initial_nodes) and \
                current not in recommendations:
            recommendations.append(current)
        # TODO: change BFS so that neighbors are added into the queue and remember by which node they were visited
        # find all neighbors of current node using BFS
        successors = dict(nx.bfs_successors(G, current, 1))
        neighbors = successors[current]
        for neighbor in neighbors:
            if neighbor not in initial_nodes:
                energy_parent = G.nodes[current]['energy'][0]
                n = len(neighbors)
                # When a node is visited its energy increases by value E = Ep/n

                #TODO: create attribute energy for all nodes that dont belong to initial nodes
                energy_neighbor = G.nodes[neighbor]['energy'][0] + (energy_parent/n)
                nx.set_node_attributes(G, {neighbor: [energy_neighbor]}, 'energy')

    print(recommendations)