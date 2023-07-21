import streamlit as st
from streamlit_extras import add_vertical_space as avs

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import *




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
The research effort on sickle cell retinopathy, as indicated by the number of publications, was mainly led by the United States, accounting for over 40% of all publications with either full or partial contributions. The United Kingdom and EU members also made significant contributions to the research. Surprisingly, African countries, led by Nigeria, which was one of the top 20 most prolific contributors in research overall, had the least involvement in research efforts on sickle cell retinopathy.          """)

#----------------------------
#------Publication count charts------------
#------------------------------
st.header('How many papers did each country publish?')
avs.add_vertical_space(2)

col_1, col_2= st.columns(
    (1,1)
)
df_publication = pd.read_csv('data/processed/publication_count.csv', index_col=0)
df_publication_count = df_publication[['countries']].replace(r"^ +| +$", r"", regex=True)
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
#header
st.subheader('Compare the number of publications contributed by any two countries')
st.info(
        """
        **👇 Select 2 countries from the dropdown below** to see some the results!
        """)

#select box section
countries_list = tuple(df_publication_count['countries'].values.tolist())

row2_col1, row2_col2 = st.columns((1,1))

with row2_col1:
    country_1 = st.selectbox("select country 1", countries_list)
    
with row2_col2:
    country_2 = st.selectbox("select country 2", countries_list)



# graphs comparing two countries by year

df_publication_comp = df_publication[['countries','Year','Document Type']]
df_publication_comp['Number of Publications'] = 1
df_publication_comp = df_publication_comp.groupby(['countries','Year','Document Type'])['countries'].count().reset_index(name='counts')

comp_fig_yr = comp_country_publications_yr(df_publication_comp, country_1, country_2)

st.plotly_chart(comp_fig_yr, theme = 'streamlit', use_container_width = True)
    


#bar graph comparing two countries by decade

row4_col1, row4_col2 = st.columns((2,1))

with row4_col1:
    df_publication_comp_dc = df_publication[['countries','Period','Document Type']]
    df_publication_comp_dc['Number of Publications'] = 1
    df_publication_comp_dc = df_publication_comp_dc.groupby(['countries','Period','Document Type'])['countries'].count().reset_index(name='counts')

    comp_fig_dc = comp_country_publications_dc(df_publication_comp_dc, country_1, country_2)
    st.plotly_chart(comp_fig_dc, theme = 'streamlit', use_container_width = True)

    
    
with row4_col2:
    pub_comp_pie_fig = publication_comp_pie(df_publication_comp,country_1, country_2)
    st.plotly_chart(pub_comp_pie_fig, theme='streamlit', use_container_width = True)
    
    

#------------------------------------------------------------
#-------Funding landscape for research on sickle cell retinopathy
#----------------------------------------------------------------
st.subheader('Which countries receive the most funding to conduct research on Sickle Cell Retinopathy?')

#funding treemap
funding_df = pd.read_csv('data/processed/funding_treemap_df.csv', index_col = 0)
funding_df.dropna(inplace=True)
funding_fig = px.treemap(funding_df, path= ['countries', 'Funding Entities'], values = 'Times Funded',color='Times Funded', color_continuous_scale='Blues')
funding_fig.update_traces(root_color="lightgrey")
funding_fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
funding_fig.update_traces(marker=dict(cornerradius=5))

st.plotly_chart(funding_fig, theme='streamlit', use_container_width = True)

# funding paragraph
st.markdown("""
            The distribution of funding and sponsorship for research on sickle cell retinopathy shows a clear disparity.The majority of financial support and sponsorship in this area comes from developed countries. The National Heart, Lung and Blood Insititute has been a significant contributor, allocating vast amounts annually for sickle cell research. Additionally, private and public foundations, such as the National Eye Institute and the National Institute of Health, have played crucial roles in funding research endeavors on sickle cell retinopathy. Conversely, African countries, which bear a considerable burden of sickle cell disease and retinopathy, receive relatively limited funding and sponsorship for research. This discrepancy highlights the urgent need for increased support and collaboration to address the healthcare challenges faced by these populations and advance our understanding of sickle cell retinopathy globally.
            """)


#------------------------------------------------------------
#-------Whcih Journal has published the most papers on sickle cell retinopathy
#----------------------------------------------------------------

st.subheader("Which journal has published the most on sickle cell retinopathy?")

#journal plot
journals_df = pd.read_csv('data/processed/journals_df.csv', index_col=0)
journals_df = journals_df.groupby('Source title')['counts'].sum().reset_index(name='counts').sort_values(by='counts', ascending=False).head(30)

journals_fig = px.bar(journals_df, x='Source title', y='counts', title='Top 30 most prolific research journals', labels = {'Source title':'Publishing Journal', 'counts':'Number of papers published'}, height = 800)

    
#bar chart
st.plotly_chart(journals_fig, theme='streamlit', use_container_width=True)
#table
st.dataframe(journals_df, use_container_width = True, column_config = {'_index':None, 'Source title':'Journal', 'counts': 'No of Papers'})




#----paragraph
st.markdown("""
            The publishing landscape on sickle cell retinopathy has been enriched by several prominent scientific journals. Among them, the "American Journal of Ophthalmology" and the "British Journal of Ophthalmology" stand out as one of the leading contributors, featuring numerous papers on this topic. "Archives of Ophthalmology," another highly regarded journal, has also published a substantial number of research papers related to sickle cell retinopathy. Furthermore, the "European Journal of Ophthalmology" and the "Investigative Ophthalmology and Visual sciences" have consistently published research papers in this field. While these journals have been major contributors, it is essential to note that other ophthalmology-related journals and hematology-focused publications have also made valuable contributions to disseminating research on sickle cell retinopathy.
            """)

#------------------------------------------------------------
#-------Most common document type
#----------------------------------------------------------------
doc_type_df = pd.read_csv('data/processed/doc_type.csv', index_col=0)

doct_fig = px.treemap(doc_type_df, path=[px.Constant('all'), 'Document Type'], values='counts')
doct_fig.update_traces(root_color="lightgrey")
doct_fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
doct_fig.update_traces(marker=dict(cornerradius=5))


st.subheader('What are the most common document types research of sickle cell retinopathy is published in?')

#chart
st.plotly_chart(doct_fig, theme='streamlit')

#paragraph
st.markdown("""
            Research on sickle cell retinopathy is primarily disseminated in the form of scientific articles, reviews, and letters. These articles present in-depth studies, analyses, and findings related to the condition, contributing to the body of knowledge on this subject. Reviews offer critical summaries of existing research and highlight key developments, while letters often present concise and timely observations or comments on specific aspects of sickle cell retinopathy. While articles, reviews, and letters are the most prevalent forms of research publication, data papers and errata also play a role, albeit to a lesser extent. Data papers provide detailed information on datasets related to sickle cell retinopathy, aiding in reproducibility and further analyses by the scientific community. On the other hand, errata address and correct errors or omissions in previously published works, ensuring the accuracy and reliability of the research presented. The diversity of publication formats contributes to a comprehensive understanding of sickle cell retinopathy and facilitates ongoing advancements in the field.
            """)


#------------------------------------------------------------
#-------Most common publishing language
#----------------------------------------------------------------

lang_df = pd.read_csv('data/processed/lang_data.csv', index_col=0).sort_values(by='counts', ascending=False)

st.subheader('What is the most common language research on sickle cell retinopathy is published in?')

row6_col1,row6_spacer, row6_col2 = st.columns((1,0.1,1))

with row6_col1:
    st.dataframe(lang_df,use_container_width = True, column_config = {'_index':None, 'counts':'Number of Papers'})
    
with row6_col2:
    st.markdown("""
                English remains the most commonly used language in publications on sickle cell retinopathy. The majority of research articles, reviews, and scientific papers are published in English-language journals, making it the primary medium for disseminating knowledge and findings in this field. This prevalence of English as the dominant language in sickle cell retinopathy publications allows for global accessibility and facilitates collaboration and exchange of information among researchers and healthcare professionals worldwide. While there might be a limited number of publications in other languages, English continues to be the primary language of choice for communication and dissemination of research in the realm of sickle cell retinopathy.
                """)
