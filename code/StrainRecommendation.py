import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


URL = "https://raw.githubusercontent.com/Build-Week-Med-Cabinet-2-MP/bw-med-cabinet-2-ml/data-generation/data/CLEAN_WMS_2020_05_24.csv"


class StrainRecommendation():
  """Cannabis strain recommendation system for Build-Week-Med-Cabinet-2-MP
  
  Methods:
    __init__: Initialize StrainRecommendation class with Weedmaps Cannabis Strain Data
    knn_predict: Generate k-Nearest Neighbor Cannabis Strains from User Preferences
  """

  def __init__(self):
    """Initialize StrainRecommendation class with Weedmaps Cannabis Strain Data
    
    Args:
        None: Data is ingested behid the scenes
    
    Attributes:
        df: Weedmaps Cannabis Strain Dataset in a pandas DataFrame
        x_train: df with string label columns removed"""

    self.url = URL
    self.df = pd.read_csv(self.url)
    self.x_train = self.df.drop(columns=["name","description"])

  def knn_predict(self, user_input, k=3):
    """Generate k-Nearest Neighbor Cannabis Strains from User Preferences
    
    Args:
        user_input User Preferences for cannabis strain flavors and effects
        k: Number of cannabis strains to return, an iteger (default=3)"""

    self.user_input = user_input
    self.k = k

    self.neigh = NearestNeighbors(n_neighbors=self.k, n_jobs=-1)
    self.neigh.fit(self.x_train)
    self.distances, self.indices = self.neigh.kneighbors(self.user_input.reshape(1, -1))

    self.strains_of_interest = [list(self.df["name"].iloc[i].values) for i in list(self.indices)][0]
    self.list_of_strains =  self.df[self.df["name"].isin(self.strains_of_interest)]
    self.intermediate_df = self.list_of_strains[["name","description"]]
    self.cols = self.list_of_strains.drop(["name","description"], axis=1).columns
    self.bt = self.list_of_strains.drop(["name","description"], axis=1).apply(lambda x: x > 0)
    self.reverse_onehot = self.bt.apply(lambda x: list(cols[x.values]), axis=1)

    self.results = self.intermediate_df.copy()
    self.results["Flavors"] = self.reverse_onehot.copy().str[0:3]
    self.results["Effects"] = self.reverse_onehot.copy().str[3:6]
    return self.results

