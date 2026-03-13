from backend.load_data import load_artifacts
from dotenv import load_dotenv
import httpx
import asyncio
import os

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

#Faz a recomendação para determinado id e retorna os ids recomendados
def recommendation(id, cosine_sim, ids_tmdb, indices, n=10):
  idx = indices[id]
  movie_indices = cosine_sim[idx][:n]
  return ids_tmdb[movie_indices].tolist()
  




#Requisição de um filme
async def get_movie(client, tmdb_id):
  url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"

  headers = {
        "accept": "application/json",
        "Authorization": TMDB_API_KEY
    }
  
  params = {
    "language": "pt-BR"
  }

  r = await client.get(url, headers= headers, params=params)

  return r.json()


#Requisição asincrona em paralelo para retornar os filmes mais rápido de uma vez
async def get_movies(tmdb_ids):

  async with httpx.AsyncClient() as client:

    tasks = [
      get_movie(client, movie_id)
      for movie_id in tmdb_ids
    ]

    movies = await asyncio.gather(*tasks)

    return movies
