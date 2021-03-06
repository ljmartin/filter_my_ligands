"""Home page shown when the user enters the application"""
import streamlit as st
import pandas as pd

from rdkit import Chem
from rdkit.Chem import Draw


def write(sesh=None):
    """Used to write the page in the app.py file"""
    with st.spinner("Loading About ..."):

        st.markdown(
            """## Upload data file
Some markdown goes here. 
""",
            unsafe_allow_html=True,
        )

    st.set_option('deprecation.showfileUploaderEncoding', False)

    if st.button('load test file'):
        sesh.df = pd.read_csv('https://raw.githubusercontent.com/ljmartin/filter_my_ligands/master/docking_sample.csv')
        st.write(sesh.df)
        sesh.df['mols'] = [Chem.MolFromSmiles(i) for i in sesh.df['smiles']]
        st.write('made mols ✅')
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        uploaded_data = pd.read_csv(uploaded_file)
        st.write('Data sample:')
        st.write(uploaded_data.head())
        st.write('uploaded csv ✅')
        sesh.df = uploaded_data

        if st.button('Turn into rdkit molecules'):
            sesh.df['mols'] = [Chem.MolFromSmiles(i) for i in sesh.df['smiles']]
            st.write('made mols ✅')
            mols = [i for i in sesh.df['mols']]
#            img =Draw.MolsToGridImage(mols, useSVG=True )
#            st.write(img)
            st.image( Draw.MolsToGridImage(mols[:10] ) )
