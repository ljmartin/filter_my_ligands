"""Home page shown when the user enters the application"""
import streamlit as st
from fastcluster import linkage

# pylint: disable=line-too-long
def write(sesh):
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Cluster ..."):

        st.markdown(
            """## Cluster
Here you can use create a single-linkage dendrogram to use for clustering.
""",
            unsafe_allow_html=True,
        )

    if st.button('Cluster!'):
        sesh.clusters = linkage(sesh.fp, method='single', metric='dice')
        st.write('Dendrogram calculated ✅')
    st.write(sesh.df)
    if st.button('Show clusters'):
        st.write(sesh.clusters)
