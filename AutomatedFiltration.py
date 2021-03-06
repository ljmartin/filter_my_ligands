from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem import Draw
from rdkit.Chem import Descriptors, FilterCatalog
from rdkit.Chem.FilterCatalog import *
from rdkit.Chem.Descriptors import qed

import sascorer 

from scipy import sparse
from scipy.spatial.distance import pdist
import numpy as np

import sknetwork
from sknetwork.hierarchy import Paris, cut_straight


class AutomatedFiltering():
    def __init__(self, df, smiles_col, rank_col):
        self.df = df
        self.smiles_col = smiles_col
        self.rank_col = rank_col

        self.df['mols'] = self._makeMols()
        self.fp = self._get_morgan()
        self.filter_columns = list()

    def _makeMols(self):
        mols = list()
        for smile in self.df[self.smiles_col]:
            mols.append(Chem.MolFromSmiles(smile))
        return mols

    def _get_morgan(self):
        gen_mo = rdFingerprintGenerator.GetMorganGenerator()
        fps = list()
        for mol in self.df['mols']:
            fp = np.array(gen_mo.GetFingerprint(mol))
            fps.append(fp)
        fps = np.array(fps)
        return sparse.csr_matrix(fps).astype('int')

    def _fast_jaccard(self,X, Y=None):
        """credit: https://stackoverflow.com/questions/32805916/compute-jaccard-distances-on-sparse-matrix"""
        if isinstance(X, np.ndarray):
            X = sparse.csr_matrix(X)
        if Y is None:
            Y = X
        else:
            if isinstance(Y, np.ndarray):
                Y = sparse.csr_matrix(Y)
        assert X.shape[1] == Y.shape[1]

        X = X.astype(bool).astype(int)
        Y = Y.astype(bool).astype(int)
        intersect = X.dot(Y.T)
        x_sum = X.sum(axis=1).A1
        y_sum = Y.sum(axis=1).A1
        xx, yy = np.meshgrid(x_sum, y_sum)
        union = ((xx + yy).T - intersect)
        return (1 - intersect / union).A
        
    def make_distance_matrix(self, kneighbors=None):
        if kneighbors == None:
            kneighbors = min(int(self.fp.shape[0]/2), 15)
        #this sparse matrix is the adjacency graph
        #using DOK matrix because it's faster to write. It is converted to CSR after. 
        wdAdj = sparse.dok_matrix((self.fp.shape[0], self.fp.shape[0]), dtype=float)

        #iterate through every row, writing adjacencies for the k-NN.
        for count, row in enumerate(self.fp):
            row_distances = self._fast_jaccard(row, self.fp)[0]
            neighbors = np.argpartition(row_distances, kneighbors)[:kneighbors]
            distances = row_distances[neighbors]
    
            for neighbourIndex, distance in zip(neighbors[1:], distances[1:]):
                wdAdj[count, neighbourIndex] += 1-distance # because similarity is 1-distance, and this a weighted adjacency
        self.knn_graph = sparse.csr_matrix(wdAdj)
        
    def _cluster(self):
        try:
            self.knn_graph
        except AttributeError:
            var_exists = False
        else:
            var_exists = True
        if not var_exists:
            self.make_distance_matrix()
        paris = Paris()
        self.dendrogram = paris.fit_transform(self.knn_graph)

    def add_synthetic_accessibility_score(self):
        """create a list holding the 'synthetic accessibility score'
        reference: https://doi.org/10.1186/1758-2946-1-8
        module code is in: https://github.com/rdkit/rdkit/tree/master/Contrib/SA_Score"""
        sa_score = [sascorer.calculateScore(i) for i in list(self.df['mols'])]
        self.df['sa_score'] = sa_score
        print(f'Synthetic accessibility score range: {min(sa_score)} -  {max(sa_score)}')

    def add_qed_score(self):
        """create a list holding the QED drug-likeness score
        reference: https://doi.org/10.1038/nchem.1243"""
        qeds = [qed(mol) for mol in self.df['mols']]
        self.df['qed_score'] = qeds
        print(f'QED score range: {min(qed)} -  {max(qed)}')

    def add_logP(self):
        """create a list holding logp"""
        logp = [Descriptors.MolLogP(m) for m in self.df['mols']]
        self.df['logp'] = logp
        print(f'logp range: {min(logp)} -  {max(logp)}')
    

       
    def filter(self, n_clusters):
        try:
            self.dendrogram
        except AttributeError:
            var_exists = False
        else:
            var_exists = True
        if not var_exists:
            self._cluster()

        self.df['cluster_id'] = cut_straight(self.dendrogram, n_clusters)

        return Draw.MolsToGridImage(self.df.drop_duplicates(subset='cluster_id', keep='first')['mols'])

