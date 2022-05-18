"""
Author: Francisco Medel Molinero
Description of the script: This script creates a graph based on a csv file and gives us information like general statistics, communities, centralities, and different ways to visualize the data
Input of the function: data in csv format
Output of the function: centralities.png, communities.png, components.png, Graph.gexf and Subgraph.gexf
"""

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import csv
import scipy as sp
from itertools import islice

#Function to read a file and convert the data
def read_file(file):
    # input text
    text = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            text.append(row)
    return text

#This function creates a graph
def CreateGraph(data):
    Graph=nx.Graph()
    pelis_actores = {}
    for index, line in enumerate(data):
        # Node per actor creation
        Graph.add_node(data[index][2])

        # if the film isn't in the dictionary, we add the film and the actor
        if data[index][1] not in pelis_actores:
            pelis_actores[data[index][1]] = [[data[index][2]]]
        # if not, we add the actor to the actor's list of the film
        else:
            pelis_actores[data[index][1]].append([data[index][2]])
        pelis_actores[data[index][1]] = [''.join(ele) for ele in pelis_actores[data[index][1]]]

        # if films[1] not in film_actors:
        #   film_actors[films[1]] = film_actors[films[1]].append(films[2])
    for film, actorList in pelis_actores.items():
        for actor1 in actorList:
            for actor2 in actorList:
                if actor1 != actor2:
                    Graph.add_edge(actor1, actor2)
    return Graph

#This function shows the number of nodes, edges, density and the components  of a graph
def GeneralStatistics(G):
    num_nodes=len(G.nodes())
    num_edges=len(G.edges())
    density= num_edges / (num_nodes * (num_nodes - 1) / 2)
    components=nx.number_connected_components(G)
    print("Number of Nodes: " + str(num_nodes))
    print("Number of edges: " + str(num_edges))
    print("Density: " + str(density))
    print("Components: " + str(components))

#Function to get the first n items
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

#This function gets top 10 centralities
def TopCentralities(G):
    degree_centr=nx.degree_centrality(G)
    eigenvector_centr=nx.eigenvector_centrality(G)
    degree_sorted=dict(sorted(degree_centr.items(), key=lambda item: item[1], reverse=True))
    eigenvector_sorted=dict(sorted(eigenvector_centr.items(), key=lambda item: item[1], reverse=True))
    top_degree_centr=take(10, degree_sorted.items())
    top_eigenvector_centr=take(10, eigenvector_sorted.items())
    print("top 10 key players using degree centrality: "+ str(top_degree_centr))
    print("top 10 key players using eigenvector centrality: "+ str(top_eigenvector_centr))

#This function gets top 10 communities
def TopCommunities(G):
    communities = {node: cid + 1 for cid, community in enumerate(nx.algorithms.community.k_clique_communities(G, 3)) for
                   node in community}
    communities_sorted = dict(sorted(communities.items(), key=lambda item: item[1], reverse=True))
    top_communities = take(10, communities_sorted.items())
    print("top 10 communities: " + str(top_communities))

#This function helps us to visualize centralities and communities of the graph
def Visualize(G):
    # Communities
    communities = {node: cid + 1 for cid, community in enumerate(nx.algorithms.community.k_clique_communities(G, 3)) for
                   node in community}

    pos = graphviz_layout(G, prog="fdp")
    nx.draw(G, pos,
            labels={v: str(v) for v in G},
            cmap=plt.get_cmap("rainbow"),
            node_color=[communities[v] if v in communities else 0 for v in G])
    plt.savefig("communities.png")
    plt.show()

    #Centralities
    pos = graphviz_layout(G, prog="fdp")
    centralities = [ nx.degree_centrality,nx.closeness_centrality,
 nx.betweenness_centrality]
    region = 220
    for centrality in centralities:
        region += 1
        plt.subplot(region)
        plt.title(centrality.__name__)
        nx.draw(G, pos, labels={v: str(v) for v in G},
                cmap=plt.get_cmap("bwr"), node_color=[centrality(G)[k] for k in centrality(G)])
    plt.savefig("centralities.png")
    plt.show()
    #Components
    plt.clf()
    pos = graphviz_layout(G)
    nx.draw(G, pos, with_labels=False, node_size=10)
    plt.savefig("components.png")
    plt.show()

#This function creates a graph based on the data
def CreateSubgraph(data):
    subGraph=nx.Graph()
    pelis_actores = {}
    for index, line in enumerate(data):
        if len(data[index][2])==8:
            # Node per actor creation
            subGraph.add_node(data[index][2])

            # if the film isn't in the dictionary, we add the film and the actor
            if data[index][1] not in pelis_actores:
                pelis_actores[data[index][1]] = [[data[index][2]]]
            # if not, we add the actor to the actor's list of the film
            else:
                pelis_actores[data[index][1]].append([data[index][2]])
            pelis_actores[data[index][1]] = [''.join(ele) for ele in pelis_actores[data[index][1]]]

        # if films[1] not in film_actors:
        #   film_actors[films[1]] = film_actors[films[1]].append(films[2])
    for film, actorList in pelis_actores.items():
        for actor1 in actorList:
            for actor2 in actorList:
                if actor1 != actor2:
                    subGraph.add_edge(actor1, actor2)
    return subGraph

#Main function
def SocialNetworkAnalysis(file):
    #Load the data
    data=read_file(file)

    #Graph creation
    G = CreateGraph(data)

    #Social Network Analysis
    GeneralStatistics(G)

    #Centralities
    TopCentralities(G)

    #Communities
    TopCommunities(G)

    #Visualization
    #We create a subgraph for the visualization, this graph only contains films with 8 of actors
    subGraph=CreateSubgraph(data)
    Visualize(subGraph)

    # write graph and subgraph to GEXF
    nx.write_gexf(G, "Graph.gexf")
    nx.write_gexf(subGraph, "Subgraph.gexf")

file='casts.csv'
SocialNetworkAnalysis(file)