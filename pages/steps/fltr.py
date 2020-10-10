"""Home page shown when the user enters the application"""
import streamlit as st
import numpy as np
import io

from rdkit import Chem
from rdkit.Chem import Draw

def get_labels(dendrogram: np.ndarray, cluster: dict, sort_clusters: bool, return_dendrogram: bool):
    """Returns the labels from clusters."""
    n = dendrogram.shape[0] + 1
    n_clusters = len(cluster)
    clusters = list(cluster.values())
    index = None
    if sort_clusters:
        sizes = np.array([len(nodes) for nodes in clusters])
        index = np.argsort(-sizes)
        clusters = [clusters[i] for i in index]

    labels = np.zeros(n, dtype=int)
    for label, nodes in enumerate(clusters):
        labels[nodes] = label

    if return_dendrogram:
        indices_clusters = np.array(list(cluster.keys()))
        if sort_clusters:
            indices_clusters = indices_clusters[index]
        index_new = np.zeros(2 * n - 1, int)
        index_new[np.array(indices_clusters)] = np.arange(n_clusters)
        index_new[- n_clusters + 1:] = np.arange(n_clusters, 2 * n_clusters - 1)
        dendrogram_new = dendrogram[- n_clusters + 1:].copy()
        dendrogram_new[:, 0] = index_new[dendrogram_new[:, 0].astype(int)]
        dendrogram_new[:, 1] = index_new[dendrogram_new[:, 1].astype(int)]
        return labels, dendrogram_new
    else:
        return labels

def cut_straight(dendrogram, n_clusters=None, threshold=None,
                 sort_clusters = True, return_dendrogram = False):

    n = dendrogram.shape[0] + 1

    cluster = {i: [i] for i in range(n)}
    if n_clusters is None:
        if threshold is None:
            n_clusters = 2
        else:
            n_clusters = n

    cut = np.sort(dendrogram[:, 2])[n - n_clusters]
    if threshold is not None:
        cut = max(cut, threshold)
    for t in range(n - 1):
        i = int(dendrogram[t][0])
        j = int(dendrogram[t][1])
        if dendrogram[t][2] < cut and i in cluster and j in cluster:
            cluster[n + t] = cluster.pop(i) + cluster.pop(j)

    return get_labels(dendrogram, cluster, sort_clusters, return_dendrogram)

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


    threshold = st.slider('threshold', min_value=0.0, max_value=1.0, value=0.5)
    
    out = cut_straight(sesh.clusters, threshold=threshold)
    sesh.df['cluster'] = out
    st.write(sesh.df)

    subsample = sesh.df.sort_values(by='dockscore').drop_duplicates(subset='cluster', keep='first')
    st.write(len(subsample))
    st.write(subsample)
    if st.button('Display'):

        st.image( Draw.MolsToGridImage( list(subsample['mols'])[:50], molsPerRow=6, useSVG=True ) )
