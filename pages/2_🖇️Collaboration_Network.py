import streamlit as st
from streamlit_extras import add_vertical_space as avs
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from utils import *

st.set_page_config(page_title='SCR Collaborations', 
                    page_icon= '📊', 
                    layout='centered', 
                    initial_sidebar_state='expanded')

#title block
st.title ('International Collaboration On Research on Sickle Cell Retinopathy')


#Number of colaborators
st.subheader("""
        How frequent has international collaboration in Sickle cell retinopathy research been?
        """)

#Number of colaborators chart
df_num_colaborating_authors = pd.read_csv('data/processed/number_of_countries.csv', index_col=0)
colab_fig = go.Figure()
colab_fig.add_trace(go.Scatter(x=df_num_colaborating_authors['Year'], y=df_num_colaborating_authors['single country'],mode='lines', name= 'single country'))
colab_fig.add_trace(go.Scatter(x=df_num_colaborating_authors['Year'], y=df_num_colaborating_authors['two countries' ],mode='lines', name= '2 countries'))
colab_fig.add_trace(go.Scatter(x=df_num_colaborating_authors['Year'], y=df_num_colaborating_authors['> 2 countries' ],mode='lines', name= '> 2 countries'))

colab_fig.update_layout(title='Number of Collaborating countries', xaxis_title='Year', yaxis_title='Number of Publications')

st.plotly_chart(colab_fig, theme='streamlit', use_container_width= True)

#results
st.markdown("""
            Internation collaboratin has been infrequent in research on sickle cell retinopathy. 80% of papers on sickle cell retinopathy had authors from a single country, 15% had authors from two countries and only 4% had authors from 3 or more countries.
            """)

#------------------------------------------------------------
#-------Collaboration network
#----------------------------------------------------------------
st.subheader('Which countries collaborate the most on sickle cell retinopathy research')
st.info("""
        ☝ Select a country to see the most common collaboratores. \n
        ✌ Hover/click on a node to see list of collaborators.
        """)

#create network
network_df = pd.read_csv('data/processed/collaborations.csv')

htmlFile = open('network.html', 'r',encoding= 'utf-8')
source_code = htmlFile.read()
components.html(source_code, height= 800, width = 800)

st.markdown("""
            Researchers in the USA were on the highest number of collaborative publications.
            """)
