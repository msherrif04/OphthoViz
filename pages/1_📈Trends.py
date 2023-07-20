import streamlit as st
from streamlit_extras import add_vertical_space as avs

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='SCR Trends', 
                    page_icon= '📊', 
                    layout='centered', 
                    initial_sidebar_state='expanded')

#title block
st.title ('Trends in publications on Sickle Cell Retinopathy Over the Years')

#----------------------------
#------Choropleth Map------------
#------------------------------

# Choropleth map showing publication frequency 
st.subheader("""Sickle cell retinopathy publication frequency between 1954 and 2023.""")

#loading the data
df_country_map = pd.read_csv('data/processed/map_data.csv')

#creating the choropleth map
choropleth_fig = go.Figure(data=go.Choropleth(
    locations = df_country_map['code'],
    z = df_country_map['count'],
    text = df_country_map['countries'],
    colorscale = 'blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=1,
    colorbar_title = 'Number of SCR Publications',
))

choropleth_fig.update_layout(
    title_text='Sickle cell retinopathy publication frequency',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='world map',
        showarrow = False
    )]
)

#rendering the choropleth map
st.plotly_chart(choropleth_fig, theme='streamlit',use_container_width=True)
st.markdown("""
            Looks like North America contributes the most publications on sickle cell retinopathy, followed by Europe with Africa contributing the least to research on sickle cell retinopathy. 
            """)

#----------------------------
#------Publication count charts------------
#------------------------------
st.header('Number of Publications from each country')
avs.add_vertical_space(2)

col_1, col_2= st.columns(
    (1,1)
)
df_publication_count = pd.read_csv('data/processed/publication_count.csv', index_col=0)
df_publication_count = df_publication_count[['countries']].replace(r"^ +| +$", r"", regex=True)
df_publication_count['Number of Publications'] = 1
df_publication_count = df_publication_count.groupby(['countries'])['Number of Publications'].sum().reset_index(name='Number of Publications')
df_publication_count = df_publication_count.sort_values(by='Number of Publications', ascending=False).reset_index(drop=True)



with col_1:

    st.dataframe(df_publication_count, use_container_width = True, column_config = {'_index':None, 'countries':'Country'})
    

with col_2:

    top_10_countries = df_publication_count.head(10)
    pub_count_plot = px.bar(top_10_countries, x='countries', y='Number of Publications', title='20 most prolific countries from 1954 - 2023')
    
    st.plotly_chart(pub_count_plot, theme='streamlit', use_container_width= True)
    

#---------------------------
#-------compare two countries
#---------------------------
