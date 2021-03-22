from dwave_qbsolv import QBSolv
import networkx as nx
import matplotlib.pyplot as plt

solving = True

num_colors = 2

while solving:

    v1 = -1
    v2 = 2
    v3 = 1

    # Make Networkx graph
    G = nx.Graph()
    G.add_edges_from([ 
        (1, 0),
        (2, 0),
        (2, 1),
        (3, 0),
        (3, 1),
        (3, 2),
        (4, 0),
        (4, 1),
        (4, 2), 
        (4, 3),
        (5, 0),
        (5, 1),
        (5, 2), 
        (5, 3),
        (5, 4),
    ])
    n_edges = len(G.edges)
    n_nodes = len(G.nodes)

    Q = {}

    #Basic weight for all QuBits (for right node states)
    for node in G.nodes:
        for i in range(num_colors):
            Q[(num_colors * node + i, num_colors * node + i)] = v1

    #Weights in nodes (for right node states)
    for node in G.nodes:
        for i in range(num_colors - 1):
            for j in range(num_colors - 1 - i):
                Q[(num_colors * node + i ,num_colors * node + 1 + i + j)] = v2

    # +2 for all wrong edges (has a 1 on the same place)
    for edge in G.edges:
        for i in range(num_colors):
            Q[(num_colors * edge[0] + i,num_colors * edge[1] + i)] = v3

    print("Q = " + str(Q))

    response = QBSolv().sample_qubo(Q)

    samples = list(response.samples())

    print("Solution = " + str(samples))
    print("Energy = " + str(list(response.data_vectors['energy'])))

    energy_test = v1 * n_nodes

    if response.data_vectors['energy'][0] == energy_test:
        plt.title('Successfully solved with ' + str(num_colors) + ' colors')
        solving = False
    else:
        if num_colors == 10:
            plt.title('Cannot be solved with 10 or less colors')
            solving = False
        else:
            num_colors += 1



color_name = ['#2ecc71','#3498db','#e74c3c','#f1c40f','#9b59b6','#2c3e50','#95a5a6','#e67e22','#1abc9c','#273c75']
pos = nx.circular_layout(G)

colors = []
for i in range(num_colors):
    colors.append([])

sample = samples[0]

for x, y in sample.items():
    if y == 1:
        colors[x % num_colors].append(x // num_colors)

for i in range(num_colors):
    nx.draw_networkx_nodes( G, pos, node_size=500, nodelist=colors[i], node_color=color_name[i] )

nx.draw_networkx_edges( G, pos, edgelist=G.edges(), edge_color='black')
nx.draw_networkx_labels(G, pos)


plt.show()
