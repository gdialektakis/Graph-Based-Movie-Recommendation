import networkx as nx
from collections import deque


def run(G):
    initial_nodes = ['RocknRolla', 'The League of Extraordinary Gentlemen', 'David Hemmings', 'Comedy']

    # Enqueue all initial nodes
    queue = deque([node for node in initial_nodes])
    color = 1
    for node in initial_nodes:
        # Add color to the initial nodes
        # the key is 'node' (id of node)
        nx.set_node_attributes(G, {node: [color]}, 'colors')
        color += 1


    # Stop when you have K nodes (movie) that have all the colors
    recommendations = []
    k = 10
    while len(queue) > 0 and k > 0:
        # dequeue a node and visit it
        current = queue.popleft()
        current_attr = G.nodes(data=True)[current]

        if current_attr['node_type'] == 'movie' and \
                len(current_attr['colors']) == len(initial_nodes) and \
                current not in recommendations:
            recommendations.append(current)
            k -= 1

        successors = dict(nx.bfs_successors(G, current, 1))
        neighbors = successors[current]
        for neighbor in neighbors:
            if neighbor not in initial_nodes:
                starting_node_color = G.nodes[current]['colors'][0]
                neighbor_color_list = G.nodes[neighbor]['colors']
                colors = [color for color in neighbor_color_list]
                if starting_node_color not in neighbor_color_list:
                    queue.append(neighbor)
                    colors.append(starting_node_color)
                    colors.reverse()
                    nx.set_node_attributes(G, {neighbor: colors}, 'colors')

    print(recommendations)