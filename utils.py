import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

def comp_country_publications_yr(df, country1, country2):
    comp_list=[country1, country2]
    #create dataframe with values of chosen countries
    temp_df = df[df.countries.isin(comp_list)]
    #create grouped bar graph
    fig = go.Figure()
    fig.update_layout(xaxis_title='Years', yaxis_title='Number of publications', title_text=f'{country1} VS {country2} by Year')
    
    for y in temp_df.countries.unique():
        dfy = temp_df[temp_df.countries == y]
        fig.add_bar(x = dfy.Year, y = dfy.counts, name = str(y))
    
    return(fig)


def comp_country_publications_dc(df,country1, country2):
    comp_list=[country1, country2]
    #create dataframe with values of chosen countries
    temp_df = df[df.countries.isin(comp_list)]
    #create grouped bar graph
    fig = go.Figure()
    fig.update_layout(xaxis_title='Decades', yaxis_title='Number of publications', title_text=f'{country1} VS {country2} by Decade')
    
    for y in temp_df.countries.unique():
        dfy = temp_df[temp_df.countries == y]
        fig.add_bar(x = dfy.Period, y = dfy.counts, name = str(y))
    
    return(fig)


def publication_comp_pie (df,country1, country2):
    comp_list=[country1, country2]
    temp_df = df[df.countries.isin(comp_list)]
    temp_df = temp_df.groupby(['countries'])['counts'].sum().reset_index(name='counts')
    fig = px.pie(temp_df, values = 'counts', names = 'countries', title='Share of publications', hole=.3)
    
    return (fig)

def create_network(df):
    """_summary_
    takes a dataframe, and a filename and creates a network map using pyvis and networks. It outputs an html file into the reports folder

    Args:
        df (dataframe): pandas dataframe
        filename (str): name of html file

    Returns:
        html: html file
    """
    #create a network object 
    net =  Network(notebook=True, select_menu=True, height='750px', width='100%', bgcolor='#222222', font_color='white',cdn_resources="in_line", )
    net.force_atlas_2based() # set the physics module to forceatlas
    net.show_buttons(filter_=['physics']) #show buttons to control physics of the map
    sources = df['source']
    targets = df['target']
    weights = df['value']

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        net.add_node(src, src, title=src)
        net.add_node(dst, dst, title=dst)
        net.add_edge(src, dst, value=w)

    neighbor_map = net.get_adj_list()
    edges = net.get_edges()
    nodes= net.get_nodes()

    N_nodes=len(nodes)
    N_edges=len(edges)


    weights=[[] for i in range(N_nodes)]

    #Associating weights to neighbors
    for i in range(N_nodes): #Loop through nodes
        for neighbor in neighbor_map[nodes[i]]: #and neighbors
            for j in range(N_edges): #associate weights to the edge between node and neighbor
                if (edges[j]['from']==nodes[i] and edges[j]['to']==neighbor) or \
                    (edges[j]['from']==neighbor and edges[j]['to']==nodes[i]):
                    weights[i].append(edges[j]['value'])
        

    for node,i in zip(net.nodes,range(N_nodes)):
        node['value']=len(neighbor_map[node['id']])
        node['weight']=[str(weights[i][k]) for k in range(len(weights[i]))]
        list_neighbor=list(neighbor_map[node['id']]) 
        #Concatenating neighbors and weights
        hover_str=[list_neighbor[k]+' '+ node['weight'][k] for k in range(node['value'])]
        hover_str.sort(reverse=True, key=lambda x: (int(x.split(' ')[-1]) if x[-1].isdigit() else 999, x))
        #Setting up node title for hovering 
        node['title']+=' Connections:\n ' + '\n'.join(hover_str)

    
    return (net.show('network.html'))