import numpy as np
import pickle
import pandas as pd

#Função para carregar os artefatos em memoria
def load_artifacts():
  cosine_sim = np.load('artifacts/cosine_sim.npy')

  with open("artifacts/ids_tmdb.pkl", "rb") as f:
    ids_tmdb = pickle.load(f)

  with open("artifacts/indices.pkl", "rb") as f:
    indices = pickle.load(f)
  
  movies_info = pd.read_parquet("artifacts/movies_info.parquet")
  
  return cosine_sim, ids_tmdb, indices, movies_info

