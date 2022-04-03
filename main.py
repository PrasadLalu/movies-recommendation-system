import pickle
import requests
import streamlit as st

BASE_URL = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

# Load model
similarity = pickle.load(open("similarity.pkl", "rb"))

# Load movies list
movies = pickle.load(open("movies_list.pkl", "rb"))
movies_list = movies['title'].values

# Add header
st.header("Movie Recommendation System")


def fetch_movie_poster(movie_id):
    url = BASE_URL.format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend_movies(movie_title):
    index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    movies_titles = []
    movies_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        movies_titles.append(movies.iloc[i[0]].title)
        movies_posters.append(fetch_movie_poster(movie_id))
    return movies_titles, movies_posters


# Get selected movie
selected_movie = st.selectbox(
    "Type or Select a movie from the dropdown:",
    movies_list)


if st.button("Show Recommendation"):
    movies_titles, movies_posters = recommend_movies(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movies_titles[0])
        st.image(movies_posters[0])

    with col2:
        st.text(movies_titles[1])
        st.image(movies_posters[1])

    with col3:
        st.text(movies_titles[2])
        st.image(movies_posters[2])

    with col4:
        st.text(movies_titles[3])
        st.image(movies_posters[3])

    with col5:
        st.text(movies_titles[4])
        st.image(movies_posters[4])
