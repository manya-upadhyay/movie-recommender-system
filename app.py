import pickle
import joblib
import gdown
import streamlit as st
import os
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750.png?text=No+Poster"

# 🎯 Google Drive File for similarity.pkl
FILE_ID = "1K98mZEzjE0dIvb2-HerUZTPcJerY3-iE"
URL = f"https://drive.google.com/uc?id={FILE_ID}"
OUTPUT_FILE = "similarity_compressed.pkl"

# ✅ Download file if not exists
if not os.path.exists(OUTPUT_FILE):
    with st.spinner("📥 Downloading similarity file... please wait ⏳"):
        try:
            gdown.download(URL, OUTPUT_FILE, quiet=False)
        except Exception as e:
            st.error("❌ Failed to download similarity file. Please check Google Drive link or permissions.")
            st.stop()

def fetch_poster(movie_id):
    """
    Fetch movie poster from TMDB API with retry & timeout handling.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return PLACEHOLDER_POSTER
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return PLACEHOLDER_POSTER


def recommend(movie):
    recommended_movie_names = []
    recommended_movie_posters = []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i, _ in movie_list:
        movie_id = movies.iloc[i].movie_id
        recommended_movie_names.append(movies.iloc[i].title)
        poster_url = fetch_poster(movie_id)
        recommended_movie_posters.append(poster_url)
        time.sleep(0.2)  # avoid hitting API rate limits

    return recommended_movie_names, recommended_movie_posters


# Streamlit UI
st.header('🎬 Movie Recommender System')

# ✅ Load Data
movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = joblib.load("similarity_compressed.pkl")  # only load compressed file

# 🎯 Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)  # updated method

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])














