import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import scanpy as sc
import matplotlib.pyplot as plt
import os
import sys
from sklearn.metrics.cluster import adjusted_rand_score
import SR_DGN
os.environ['R_HOME'] = '/home/dell/anaconda3/envs/stpython/lib/R'

adata = sc.read('Data/Mouse_olfactory_bulb/adata.h5ad')
adata.var_names_make_unique()
# adata.obsm['spatial'][:, 0] *= -1
sc.pp.highly_variable_genes(adata, flavor="seurat_v3", n_top_genes=3000)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.scale(adata, zero_center=False, max_value=10)

SR_DGN.Cal_Spatial_Net(adata, rad_cutoff=70)
SR_DGN.Stats_Spatial_Net(adata)
adata = SR_DGN.train(adata)
sc.pp.neighbors(adata, use_rep='SR-DGN')
sc.tl.umap(adata)
adata = SR_DGN.mclust_R(adata, used_obsm='SR-DGN', num_cluster=7)
