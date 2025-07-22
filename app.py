import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# Load external CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")
# Page config
st.set_page_config(page_title="Movie Recommender", layout="centered", page_icon="🎬")

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------------ Load Data ------------------------
movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------------ Recommendation Function ------------------------
def recommend(movie):
    if movie not in movies['title'].values:
        st.error("Movie not found in the database.")
        return []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []

    for i in distances:
        if i[0] >= len(movies):
            continue  # Skip out-of-bounds index
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

# ------------------------ Streamlit App ------------------------
st.set_page_config(layout="centered", page_title="Movie Recommender", page_icon="🎬")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "About"],
        icons=["house", "info-circle"],
        default_index=0
    )

# ------------------------ Home Page ------------------------
if selected == "Home":
    st.title("🎬 Movie Recommendation System")
    selected_movie = st.selectbox("Select a movie you like", movies['title'].values)

    if st.button("Recommend"):
        movie_names = recommend(selected_movie)

        if movie_names:
            st.subheader("Top 5 Recommendations:")
            for idx, name in enumerate(movie_names, start=1):
                st.markdown(f"**{idx}. {name}**")
        else:
            st.warning("No recommendations found.")

# ------------------------ About Page ------------------------
elif selected == "About":
    st.title("About this App")
    st.markdown("""
    This Movie Recommender System uses **cosine similarity** to suggest similar movies based on your choice.

    **Technologies Used**:
    - Python
    - Pandas
    - Scikit-learn
    - Streamlit

    **Author**: Aritra Das
    """)
