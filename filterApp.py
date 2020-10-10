from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdFingerprintGenerator

from pages.steps import home, upload, cluster, fingerprint, fltr

import SessionState
import streamlit as st
import pandas as pd
import numpy as np
import io

st.beta_set_page_config(
    page_icon=":shark:",
    layout="wide",

)

PAGES = {
    "Home": home,
    "Upload Mols.": upload,
     "Fingerprint": fingerprint,
    "Cluster": cluster,
    "Filter": fltr
}

sesh = SessionState.get(predicted_uploaded=False,
                        known_uploaded=False,
                        predicted_mols=[],
                        known_mols=[],
                        df_predicted = None,
                        df_known = None,
                        fp = [], csv=None, )


def main():
    """Main function of the App"""
    st.sidebar.title("Start here:")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.write(sesh)

    st.sidebar.title('Re-run')
    st.sidebar.info('_note_ This will forget all loaded data and start from a blank slate')
    st.sidebar.button('Refresh')
    
    st.sidebar.title("About")
    st.sidebar.info(
        """
        Lewis martin. contact: 
"""
    )

if __name__=='__main__':
    main()

#    
#@st.cache
#def fingerprint_molecules(mols):
#    fps = [rdFingerprintGenerator.GetMorganGenerator().GetFingerprint(mol) for mol in mols]
#    return fps
#    
#st.sidebar.title('bah')
#
#if sesh.file_uploaded:
#    st.sidebar.markdown('# Hi')
#    
#    if st.button('Show molecules'):
#        mols = [Chem.MolFromSmiles(i) for i in uploaded_data['smiles']]
#        sesh.mols=mols
#        st.image(Draw.MolsToGridImage(mols, molsPerRow=5))
#
#    if st.button('Fingerprint molecules'):
#        
#        fps = fingerprint_molecules(sesh.mols)
    
