"""Home page shown when the user enters the application"""
import streamlit as st
import pandas as pd

from rdkit import Chem
from rdkit.Chem import Draw
from IPython.display import SVG
 
def write(sesh=None):
    """Used to write the page in the app.py file"""

    if sesh.predicted_uploaded:
        st.write('bhahaha')
    st.markdown(
            """## Upload data file
Here you can upload two CSV files, each containing a `smiles` column. 
After uploading, click 'Turn into RDKit molecules' to generate `mol` objects.
Invalid SMILES codes will be removed. 

"""
    )
    st.set_option('deprecation.showfileUploaderEncoding', False)

    ###
    # Upload the CSV containing the predicted smiles:
    ###
    st.write('### Upload predicted smiles:')
    predicted_file = st.file_uploader("", type="csv")
    if predicted_file is not None:
        predicted_data = pd.read_csv(predicted_file)        
        result_string = 'Uploaded `predicted` mols csv ✅. '
        if 'smiles' in predicted_data.columns:
            result_string += 'File contains `smiles` column ✅. '
        else:
            result_string += 'X no `smiles` column present. Please upload new CSV containing column labelled `smiles`'
        st.write(result_string)
        st.write('First line:')
        st.write(predicted_data.iloc[:1])
        sesh.df_predicted = predicted_data

    ###
    # Upload the CSV containing the predicted smiles:
    ###
    st.write('### Upload smiles of known molecules:')
    known_file = st.file_uploader(" ", type="csv")
    if known_file is not None:
        known_data = pd.read_csv(known_file)
        result_string = 'Uploaded `known` mols csv ✅. '
        if 'smiles' in known_data.columns:
            result_string += 'File contains `smiles` column ✅. '
        else:
            result_string += 'X no `smiles` column present. Please upload new CSV containing column labelled `smiles`'
        st.write(result_string)
        st.write('First line:')
        st.write(known_data.iloc[:1])
        sesh.df_known = known_data


    ###
    # If successful, turn them into mol objects (and add the mol objects to the df)
    ###
    if not sesh.predicted_uploaded and not sesh.known_uploaded:
        st.write('Wating on file uploads to make the `mol` objects...')
    if sesh.df_predicted is not None and sesh.df_known is not None:
        if st.button('Turn into rdkit molecules'):
            st.write(sesh.df_predicted is not None)
            #progress bar for making `mol` objects:
            #(should progress to 100 only when both sets of smiles are complete)
            pbar = st.progress(0)
            tot_smiles = len(sesh.df_predicted) + len(sesh.df_known)
            processed_smiles = 0

            predicted_mols = list()
            bad_mols = list()
            for smi in sesh.df_predicted['smiles']:
                try:
                    mol = Chem.MolFromSmiles(smi)
                except:
                    st.write(f'Warning: molecule failed to parse. SMILES code was: {smi} and index {count}. This entry will get removed.')
                    bad_mols.append(count)
                    
                predicted_mols.append(mol)
                processed_smiles+=1
                pbar.progress( int (processed_smiles / tot_smiles * 100 ) )
            sesh.df_predicted = sesh.df_predicted.drop(bad_mols)
            sesh.predicted_mols = predicted_mols

            known_mols = list()
            bad_mols = list()
            for count, smi in enumerate(sesh.df_known['smiles']):
                try:
                    mol = Chem.MolFromSmiles(smi)
                except:
                    st.write(f'Warning: molecule failed to parse. SMILES code was: {smi} and index {count}. This entry will get removed.')
                    bad_mols.append(count)
                    
                known_mols.append(mol)
                processed_smiles+=1
                pbar.progress( int( processed_smiles / tot_smiles * 100 ) )

            sesh.df_known = sesh.df_known.drop(bad_mols)
            sesh.known_mols = known_mols
            

            #sesh.df['mols'] = [Chem.MolFromSmiles(i) for i in sesh.df['smiles']]
            st.write('✅ made mols, first ten:')
            #mols = [i for i in sesh.df['mols']]
            #img = Draw.MolsToGridImage(mols[:10], molsPerRow=5,)

            #st.image(img)
            #st.image( Draw.MolsToGridImage(mols[:10], molsPerRow=5, useSVG=True ) )


    step_one = '✅' if sesh.df_predicted is not None else '❌'
    step_two = '✅' if sesh.df_known is not None else '❌'
    step_three = '✅' if (len(sesh.known_mols)>0) and (len(sesh.predicted_mols)>0) else '❌'
    step_four = '✅ Proceed to next step' if step_three==step_two==step_one=='✅' else ''
    st.markdown("""Progress:
- %s Upload csv containing smiles for predicted molecules from some virtual screen (i.e. docking)
- %s Upload csv containing smiles for molecules already known to be active at the
target. These will be used to filter the predictions.
- %s Turn both of these into rdkit molecule objects.
- %s 
----------------------------------------------""" % (step_one, step_two, step_three, step_four)
                )
