import streamlit as st


st.set_page_config(page_title='SCR Analysis Overview', 
                    page_icon= '📊', 
                    layout='centered', 
                    initial_sidebar_state='expanded')

#title block
st.title ('Analysing Trends in Publications on Sickle Cell Retinopathy')

st.markdown(
        """
        **👈 Select a page from the dropdown on the left** to see some the results!
        """)

#Some background
st.header("Rationale")
st.write("""Sickle cell retinopathy, a critical ocular manifestation of sickle cell disease, represents a significant health concern with potentially severe consequences for affected individuals. Despite its importance, the research landscape surrounding sickle cell retinopathy remains relatively limited, with a paucity of comprehensive studies exploring its full scope and impact. Moreover, the countries that bear the highest burden of sickle cell disease and, consequently, are most affected by sickle cell retinopathy, often face considerable challenges in contributing significantly to the research in this area. To shed light on this crucial issue and address the disparities in research representation, this app introduces a comprehensive analysis aimed at examining the trends in publications on sickle cell retinopathy.""")

st.header("Method")
st.markdown("""
## Publication Search
The keywords **Sickle cell retinopathy** were entered into the Scopus search engine and all results from 1954 to July 2023 were downloaded.

## Analysis
The results were analysed using python scripts.

### Methods Used
* Descriptive and Inferential Statistics
* Natural Language Processing
* Data Visualization


### Python Packages Used

- **General Purpose:** `os, request`, and many more.
- **Data Manipulation:** Packages used for handling and importing dataset such as `pandas, numpy, jupyter, pycountry` and others.
- **Data Visualization:** Include packages which were used to plot graphs in the analysis or for understanding the ML modelling such as `plotly, seaborn, matplotlib` and others.
- **NLP:** `spacy, displacy`, etc.

            """)