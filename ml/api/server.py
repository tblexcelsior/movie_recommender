import os
import sys
sys.path.insert(1, os.getcwd())
from ml.utils.recommender import personalisedSearcher
from ml.utils import connector
from flask import Flask, request

ps = personalisedSearcher()
app = Flask(__name__)

@app.route("/get-recommendation", methods=["GET", "POST"])
def get_recommendation():
    if request.method == "POST":
        req_data = request.get_json()
        user_id = int(req_data['userId'])
        query = req_data['query']
        recommendations, movies_watched_by_user = ps.personalised_search(user_id = user_id, query=query)
        recommended_movies = connector.retrieve_movies(ps.conn, 'movieId', recommendations)
        top_movies = connector.retrieve_movies(ps.conn, 'movieId', movies_watched_by_user)
    return {"recommendation": recommended_movies.to_dict('list'),
            "top_movies": top_movies.to_dict('list')}
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=False, port=8000)