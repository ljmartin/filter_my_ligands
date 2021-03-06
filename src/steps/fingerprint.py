"""Home page shown when the user enters the application"""
import streamlit as st
import pandas as pd
import numpy as np

from rdkit.Chem import rdFingerprintGenerator


def write_fingerprints(sesh):

    
    option = st.selectbox('What fingerprint?',
                          ('choose one', 'Morgan',))
    
    if option in ['Morgan', 'MACCS']:
        if st.button('Generate fingerprints'):
            pbar = st.progress(0)
            gen_mo = rdFingerprintGenerator.GetMorganGenerator(512)
            for count, mol in enumerate(sesh.df['mols']):
                fp = rdFingerprintGenerator
                sesh.fp.append(gen_mo.GetFingerprint(mol))
                pbar.progress(int((count+1)/len(sesh.df)*100))
            sesh.fp = np.array(sesh.fp)

def write(sesh):
    """Used to write the page in the app.py file"""
    st.markdown(
            """## Add featurization
Some markdown goes here. 
""",
            unsafe_allow_html=True,
        )

    if len(sesh.fp) == 0:
        write_fingerprints(sesh)
    
    else:
        st.write('Fingerprints already generated. Regenerate?')
        if st.button('Regenerate fingerprints'):
            sesh.fp = []
            write_fingerprints(sesh)
            
