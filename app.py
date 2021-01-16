from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
import pandas as pd
import graph
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/EnergySpreading', methods=['GET'])
def fetchEnergySpreading():
   category = request.args.get('category', type = str)
   user_id = int(request.args.get('userId', type = str))
   ratio = int(request.args.get('ratio', type = str))
   try:
        data = graph.graph(1, user_id, category, ratio)
        return data
   except: 
       return jsonify({'error':'error'}) 
    

@app.route('/UnionColors', methods=['GET'])
def fetchUnionColors():
   category = request.args.get('category', type = str)
   user_id = int(request.args.get('userId', type = str))
   ratio = int(request.args.get('ratio', type = str))
   try:
        data = graph.graph(0, user_id, category, ratio)
        return data
   except: 
       return jsonify({'error':'error'})  

@app.route('/movies', methods=['GET'])
def fetchMovies():
    filename = os.path.join('movie_genres.csv')
    df = pd.read_csv(filename, delimiter=',')
    data_list = list(set(df['genre'].values.tolist()))
    return jsonify(data_list)

@app.route('/userId', methods=['GET'])
def fetchUserId():
    filename = os.path.join('user_ratings.csv')
    df = pd.read_csv(filename, delimiter=';')
    data_list = list(set(df['userID'].values.tolist()))
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=False)