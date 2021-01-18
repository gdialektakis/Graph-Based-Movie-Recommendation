import networkx as nx
from collections import deque


def run(G, initial_nodes, top_k=10):
    # the number of recommendations we want to receive from the system
    k = top_k

    for node in G.nodes:
        # attribute parents holds a list of adjacent nodes to each node sorted by the the order they visited the node
        nx.set_node_attributes(G, {node: []}, 'parents')
        # spread energy is the energy the node received only from the first time and
        # it's the one that it can spread to other nodes
        nx.set_node_attributes(G, {node: 0}, 'spread_energy')
        nx.set_node_attributes(G, {node: 0}, 'energy')

    # Enqueue all initial nodes
    queue = deque([node for node in initial_nodes])
    initial_energy = 10
    for node in initial_nodes:
        # Set the energy of each initial node to some constant
        # the key is 'node' (id of node)
        nx.set_node_attributes(G, {node: initial_energy}, 'spread_energy')

    recommendations = []
    while len(queue) > 0 and k > 0:
        # take the first element of the queue
        current = queue.popleft()
        current_attr = G.nodes(data=True)[current]

        # append the current node to recommendations if it's been visited by all initial nodes
        if current_attr['node_type'] == 'movie' and \
                len(current_attr['parents']) == len(initial_nodes) and \
                current not in recommendations and current not in initial_nodes:
            recommendations.append([current, current_attr['energy']])
            k -= 1

        # find all neighbors of current node using BFS
        successors = dict(nx.bfs_successors(G, current, 1))
        neighbors = successors[current]
        for neighbor in neighbors:
            if neighbor not in initial_nodes:
                parent_energy = G.nodes[current]['spread_energy']
                n = float(len(neighbors))
                neighbor_energy = 0
                try:
                    neighbor_energy = G.nodes[neighbor]['energy']
                except KeyError:
                    pass

                # When a node is visited its energy increases by value E = Ep/n
                # where Ep is the energy of its parent and n is the number of neighbors its parent has
                neighbor_energy = neighbor_energy + (parent_energy / n)
                nx.set_node_attributes(G, {neighbor: neighbor_energy}, 'energy')

                # if it's the first time this node receives energy, then save it to spread_energy attribute as
                # it can later spread only this energy
                if G.nodes(data=True)[neighbor]['spread_energy'] == 0:
                    nx.set_node_attributes(G, {neighbor: neighbor_energy}, 'spread_energy')

                neighbor_attr = G.nodes(data=True)[neighbor]
                parents = neighbor_attr['parents']
                parents.append(current)
                # store the node's parent
                nx.set_node_attributes(G, {neighbor: parents}, 'parents')

                if neighbor not in queue:
                    queue.append(neighbor)

    # sort recommendations by their energy and return the top k with the most energy
    recommendations.sort(key=lambda x: x[1])
    recommendations.reverse()
    return recommendations
