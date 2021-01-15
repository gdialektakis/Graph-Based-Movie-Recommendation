import networkx as nx
from collections import deque

def run(G):
    initial_nodes = ['RocknRolla', 'The League of Extraordinary Gentlemen', 'David Hemmings', 'Comedy']

    for node in G.nodes:
        nx.set_node_attributes(G, {node: []}, 'parents')

    # Enqueue all initial nodes
    queue = deque([node for node in initial_nodes])
    initial_energy = 10
    # initial_nodes.reverse()

    for node in initial_nodes:
        # Set the energy of each initial node to some constant
        # the key is 'node' (id of node)
        nx.set_node_attributes(G, {node: [initial_energy]}, 'energy')

    recommendations = []
    k = 10
    while len(queue) > 0 and k > 0:
        # take the first element of the queue
        current = queue.popleft()
        current_attr = G.nodes(data=True)[current]

        if current_attr['node_type'] == 'movie' and \
                len(current_attr['parents']) == len(initial_nodes) and \
                current not in recommendations:
            recommendations.append({current, current_attr['energy']})
            k -= 1

        # find all neighbors of current node using BFS
        successors = dict(nx.bfs_successors(G, current, 1))
        neighbors = successors[current]
        for neighbor in neighbors:
            if neighbor not in initial_nodes:
                parent_energy = G.nodes[current]['energy'][0]
                n = float(len(neighbors))
                # When a node is visited its energy increases by value E = Ep/n
                neighbor_energy = 0
                try:
                    neighbor_energy = G.nodes[neighbor]['energy'][0]
                except KeyError:
                    pass

                neighbor_energy = neighbor_energy + (parent_energy/n)
                nx.set_node_attributes(G, {neighbor: [neighbor_energy]}, 'energy')

                # TODO: check BFS so that neighbors are added into the queue and the way parents are inserted
                neighbor_attr = G.nodes(data=True)[neighbor]
                parents = neighbor_attr['parents']
                parents.append(current)
                nx.set_node_attributes(G, {neighbor: [parents]}, 'parents')

                if neighbor not in queue:
                    queue.append(neighbor)

    # sort recommendations by their energy
    recommendations.sort(key=lambda x: x[1])
    recommendations.reverse()
    print(recommendations)