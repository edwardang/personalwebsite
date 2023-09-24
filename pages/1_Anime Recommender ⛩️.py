import streamlit as st
import time
import numpy as np
import pandas as pd

from streamlit_gsheets import GSheetsConnection
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Edward Ang",
    page_icon=f"assets/logo.png",
)

def create_vectorized_matrix(df):
    '''
    Includes all feature engineering in here
    '''
    cv = CountVectorizer(max_features = 13500,stop_words="english")
    vectors = cv.fit_transform(df["Tags"]).toarray()
    return pd.DataFrame(vectors)

def Recommender(user_input, df, bag_of_words, output_amt = 10):

    # Get index of animes enjoyed
    animes_enjoyed_index = df[df['Name'].isin(user_input)].index
    
    # Get mean of all animes user input from bag of words matrix
    user_prof = bag_of_words.iloc[animes_enjoyed_index,:].mean(axis = 0).values.reshape((1,bag_of_words.shape[1]))
    
    # Drop the animes user input so we don't recommend the same ones
    df_subset = df.drop(animes_enjoyed_index)
    bow_subset = bag_of_words.drop(animes_enjoyed_index)

    # Create similarity array with respect to other animes.
    similarity_array = cosine_similarity(user_prof, bow_subset)

    # Reshape and add similarity score to main df
    similarity_df = pd.DataFrame(similarity_array.T, index=bow_subset.index, columns=["similarity_score"])
    df['similarity_score'] = similarity_df['similarity_score']

    # Return sorted df
    return df.sort_values(by = 'similarity_score', ascending = False).head(output_amt)

def get_hot_animes():
    import requests
    from bs4 import BeautifulSoup

    html_string = requests.get("https://myanimelist.net/topanime.php?type=airing").content

    soup = BeautifulSoup(html_string, "html.parser")
    s = soup.find_all(attrs={"class":"top-ranking-table"})

    g = s[0].find_all('tr')[1:6]
    data = []

    # first get data on just this page, and then alter if you want you can start to scape the information

    for table_row in g:
        hover_tag = table_row.find_all(attrs={"class":"hoverinfo_trigger"})
        data.append({'title' : hover_tag[1].contents[0],
        'image' : hover_tag[0].find_all('img')[0]['data-srcset'].split(',')[1].strip().split(' ')[0],
        'rating': table_row.select('span[class*="text on score-label"]')[0].contents[0],
        'link': hover_tag[0]['href']
        })
    return pd.DataFrame(data)

@st.cache_data(ttl=200)
def run_query():
    data = conn.read(worksheet = "Anime Recommendation", usecols=list(range(1,5)))
    return pd.DataFrame(data)



conn = st.experimental_connection("gsheets", type=GSheetsConnection)
df = run_query()
bag_of_words = create_vectorized_matrix(df)


hot_animes = get_hot_animes()
with st.expander('Hot Animes Right Now 🔥 (via myanimelist.net)'):
    col1, col2, col3, col4, col5 = st.columns(5)
    col_lst = [col1, col2, col3, col4, col5]
    for index, row in hot_animes.iterrows():
        with col_lst[index]:
            st.subheader(str(index + 1), '. ')
            st.write(f"[{row['title']}]({row['link']})")
            st.image(row['image'],width=100)
            

st.title("""
Anime Recommendation System
 """)

st.text("")

user_input = st.multiselect(label="Select Animes You Like", options=df['Name'])

st.text("")
st.text("")

buffer1, col1, buffer2 = st.columns([1.45, 1, 1])

is_clicked = col1.button(label="Recommend")

if is_clicked:
    dataframe = Recommender(user_input, df, bag_of_words)
    st.write(dataframe)



