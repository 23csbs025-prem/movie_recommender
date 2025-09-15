import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

st.title("🎥 Movie Recommendation System")

# Function to fetch poster from TMDB
def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"] if "TMDB_API_KEY" in st.secrets else None
    if api_key:
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "poster_path" in data and data["poster_path"]:
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            else:
                return "https://via.placeholder.com/200x300?text=No+Poster+Available"
        
        except:
            # Silent fallback for network/API errors
            return "https://via.placeholder.com/200x300?text=No+Poster+Available"
    
    # If no API key
    return "https://via.placeholder.com/200x300?text=No+Poster+Available"

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Dropdown
selected_movie_name = st.selectbox("Select your Favourite movie:", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
