import os
import sys
sys.path.insert(1, os.getcwd())

import streamlit as st
from ml.utils import connector
import requests
import json

url = "http://127.0.0.1:8000/get-recommendation"
headers = {'Content-type': 'application/json'}


conn = connector.connect_to_db()

def display_info_form():
    userId = st.text_input("Enter your ID:")
    query = st.text_input("Enter your query:")
    empty_col = st.columns([3, 1, 3])
    with empty_col[1]:
        submit_button = st.button("Find")
    return userId, query, submit_button

def display_recommendation(title, data):
    with st.container():
        st.header(title)
        st.divider()
        for i in range(min(5, len(data['genres']))):
            st.markdown(f":red[Title]: {data['title'][i]}")
            st.markdown(f":red[Genres]: {data['genres'][i]}")
            st.divider()

def main():
    st.title("Welcome!")
    userId, query, submit_button = display_info_form()
    if submit_button:
        checked = connector.check_existence(conn, userId)
        if checked:
            data_to_send = {"userId": f"{userId}", "query": f"{query}"}
            r = requests.post(url, data=json.dumps(data_to_send), headers=headers)
            data = r.json()
            recommendation = data['recommendation']
            top_movies = data['top_movies']
            col1, col2 = st.columns(2)
            with col1:
                display_recommendation("Recommendations", recommendation)
            with col2:
                display_recommendation("Your Top Movies", top_movies)

        else:
            st.write("Your ID is not available")
        
if __name__ == "__main__":
    main()
