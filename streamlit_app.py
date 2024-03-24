import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies=pd.DataFrame(movies_dict)
st.image('images/android-chrome-192x192.png',width=100) 
st.title('THE MOVIE HUB')


def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=47923ebeadd89dcdf414628f2121658e'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']

def fetch_overview(movie_id):
   response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=47923ebeadd89dcdf414628f2121658e'.format(movie_id))
   data=response.json()
   return data['overview']
   
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    recommended_movies_overview=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_overview.append(fetch_overview(movie_id))
    return recommended_movies,recommended_movies_posters,recommended_movies_overview

selected_movie= st.selectbox(
    'What kind of movie would you like to watch today?',
    movies['title'].values,index=None,placeholder='Select a movie...' )


if st.button('Recommend'):
    names, posters, overview=recommend(selected_movie)
    import streamlit as st
    
    for i in range (0,5):
     title_container = st.container(border=True)
     col1, col2 = st.columns([10, 20])
     with title_container:
            st.header(names[i])
            with col1:
                st.image(posters[i], width=200)
            with col2:
                st.markdown(overview[i])


