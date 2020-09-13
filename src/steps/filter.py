"""Home page shown when the user enters the application"""
import streamlit as st


# pylint: disable=line-too-long
def write(sesh):
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Cluster ..."):

        st.markdown(
            """## Cluster
Some markdown initially
""",
            unsafe_allow_html=True,
        )

    if st.button('Cluster!'):
        sesh.clusters = linkage(sesh.fp, method='single', metric='dice')
        st.write('bah')
    st.write(sesh.df)
    if st.button('Write out clusters?'):
        st.write(sesh.clusters)
