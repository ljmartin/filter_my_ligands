from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdFingerprintGenerator

import src.steps.home
import src.steps.upload
import src.steps.cluster
import src.steps.fingerprint
import src.steps.filter

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
    0: src.steps.home,
    1: src.steps.upload,
    2: src.steps.fingerprint,
    3: src.steps.cluster,
    4: src.steps.filter
}

sesh = SessionState.get(file_uploaded=False, mols=[], fp = [], csv=None, curr_page = 0)

def write_current_page():
    st.write('curr page:', sesh.curr_page)
    PAGES[sesh.curr_page].write(sesh)


def main():
    """Main function of the App"""
    st.sidebar.title("Start here:")
    st.sidebar.title('Re-run')
    st.sidebar.write(f'Current page? its: {sesh.curr_page}')
    st.sidebar.info('_note_ This will forget all loaded data and start from a blank slate')
    if st.sidebar.button('Refresh'):
        st.curr_page=0
    

    st.title('Navigation')
    st.markdown('Click Next to go to the next page')
    if st.button('Back:'):
        sesh.curr_page = max(0, sesh.curr_page-1)
    if st.button('Next page:'):
        sesh.curr_page+=1
    st.markdown('----------------------------------')
    

    PAGES[sesh.curr_page].write(sesh)
        

#    if st.sidebar.button('Page one'):
#        sesh.curr_page = 0
#        #PAGES[0].write(sesh)


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
    
