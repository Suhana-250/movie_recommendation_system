import streamlit as st
import pickle
import pandas as pd
import requests

# Page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .title {
        font-size:40px;
        font-weight:bold;
        text-align:center;
        color: #FF4B4B;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size:18px;
        font-weight:500;
        text-align:center;
        margin-bottom: 20px;
    }
    .movie-title {
        font-size:16px;
        font-weight:600;
        text-align:center;
        margin-top:10px;
    }
    </style>
""", unsafe_allow_html=True)

# Function to fetch movie poster from TMDB
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=1d2163ed9d53db8fbec1e87a8aaf154a&language=en-US'
    )
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path", "")
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# Recommendation function
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open("movie_list.pkl", "rb"))  # Ensure this file exists
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Title and subtitle
st.markdown('<div class="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find your next favorite movie based on what you already love 🍿</div>', unsafe_allow_html=True)

# Movie selector
selected_movie_name = st.selectbox("Select a movie to get similar recommendations:", movies["title"].values)

# Recommend button
if st.button("Recommend 🎥"):
    with st.spinner("Fetching recommendations..."):
        recommended_movies, recommended_movies_posters = recommend(selected_movie_name)

        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.image(recommended_movies_posters[idx], use_column_width=True)
                st.markdown(f'<div class="movie-title">{recommended_movies[idx]}</div>', unsafe_allow_html=True)
