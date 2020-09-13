"""Home page shown when the user enters the application"""
import streamlit as st

def write(sesh):
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Home ..."):
        st.write(
            """
# Home page

This app helps you cluster and filter a list of ligands from virtual screening.
Follow the buttons in the panel on the left hand side:
- First you will need to upload a CSV with, at minimum, a column with the 
SMILES codes of the molecules. 
- Second step is to featurize with some fingerprint, i.e. Morgan or MACCS keys
- Third step is to choose a clustering algorithm 
- Fourth set sliders



    """
        )


