from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdFingerprintGenerator

import SessionState
import streamlit as st
import pandas as pd
import numpy as np
import io

st.title('Molecule filtering')
st.sidebar.title('Molecule filtering')

st.write('\nFirst step: upload a CSV. It can have multiple columns, but please include one column labelled `smiles` containing the SMILES codes\n')

sesh = SessionState.get(file_uploaded=False, mols=[])

st.set_option('deprecation.showfileUploaderEncoding', False)
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    sesh.file_uploaded=True
    uploaded_data = pd.read_csv(uploaded_file)

    
@st.cache
def fingerprint_molecules(mols):
    fps = [rdFingerprintGenerator.GetMorganGenerator().GetFingerprint(mol) for mol in mols]
    return fps
    
st.sidebar.title('bah')

if sesh.file_uploaded:
    st.sidebar.markdown('# Hi')
    
    if st.button('Show molecules'):
        mols = [Chem.MolFromSmiles(i) for i in uploaded_data['smiles']]
        sesh.mols=mols
        st.image(Draw.MolsToGridImage(mols, molsPerRow=5))

    if st.button('Fingerprint molecules'):
        
        fps = fingerprint_molecules(sesh.mols)
    
