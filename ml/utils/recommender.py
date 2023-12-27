import os
import sys
sys.path.insert(1, os.getcwd())

import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import tensorflow_recommenders as tfrs
import tensorflow as tf
from tensorflow import keras
from ml.utils import connector


class personalisedSearcher:
    def __init__(self):
        self.scann = tf.keras.models.load_model("ml/model/embedding")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L12-v2")
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L12-v2")
        self.recommender = keras.models.load_model('ml/model/CF')

        self.conn = connector.connect_to_db()
        
    def get_user_encodings(self):
        # user_ids = self.ratings["userId"].unique().tolist()
        user_ids = connector.get_id(self.conn, 'userId')
        user2user_encoded = {x[0]: i for i, x in enumerate(user_ids)}
        userencoded2user = {i: x[0] for i, x in enumerate(user_ids)}
        
        return user2user_encoded, userencoded2user

    def get_movie_encodings(self):
        # movie_ids = self.ratings["movieId"].unique().tolist()
        movie_ids = connector.get_id(self.conn, 'movieId')
        movie2movie_encoded = {x[0]: i for i, x in enumerate(movie_ids)}
        movie_encoded2movie = {i: x[0] for i, x in enumerate(movie_ids)}
        
        return movie2movie_encoded, movie_encoded2movie
    
        
    def get_candidate_movies(self, query):
        encoded_input = self.tokenizer(query, 
                                  padding=True, 
                                  truncation=True, 
                                  max_length=64, 
                                  return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        query_embeddings = model_output.pooler_output
        query_embeddings = torch.nn.functional.normalize(query_embeddings)
        test_case = self.scann(np.array(query_embeddings))
        test_case_idx = test_case[1].numpy()[0]
        res = connector.retrieve_movies(self.conn, 'idx', test_case_idx)
        return res
    
    def filter_candidates(self, user_id, query):
        # movies_watched_by_user = self.ratings[self.ratings.userId == user_id]
        movies_watched_by_user = connector.get_ratings(self.conn, user_id)
        candidates = self.get_candidate_movies(query)
        print(len(candidates))
        print("*************"*2)
        movies_not_watched = candidates[
            ~candidates["movieId"].isin(movies_watched_by_user.movieId.values)
        ]["movieId"]
        movie2movie_encoded, _ = self.get_movie_encodings()
        movies_not_watched = list(set(movies_not_watched).
                                  intersection(set(movie2movie_encoded.keys())))
        movies_not_watched = [[movie2movie_encoded.get(x)] for x in movies_not_watched]
        user2user_encoded, _ = self.get_user_encodings()
        user_encoder = user2user_encoded.get(user_id)
        movie_array = np.hstack(([[user_encoder]] * len(movies_not_watched), movies_not_watched))
        return movie_array, movies_not_watched, movies_watched_by_user
    
    def personalised_search(self, user_id, query):
        movie_array, movies_not_watched, movies_watched_by_user = self.filter_candidates(user_id, query)
        scored_items = self.recommender.predict(movie_array).flatten()
        top_rated = scored_items.argsort()[-10:][::-1]
        _, movie_encoded2movie = self.get_movie_encodings()
        recommended_movie_ids = [movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_rated]
        top_movies_user = (
            movies_watched_by_user.sort_values(by="rating", ascending=False)
            .head(5)
            .movieId.values
        )
        return recommended_movie_ids, top_movies_user