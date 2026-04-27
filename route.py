from flask import Flask, render_template,redirect,  url_for, abort, request, jsonify
from Db_manager import get_all_observations, get_observations_by_id, insert_weather, update_weather, delete_weather
from Db import get_weather
import requests

app = Flask(__name__)

@app.route('/')
def home():
    results = get_all_observations()
    return render_template('index.html', observations=results)

@app.route('/about')
def about():
    return 'this is the about page.'

@app.route('/ingest', methods=['POST'])
def ingest():

    city = request.args.get("city")
    country = request.args.get("country")

    result = get_weather(city, country)

    insert_weather(
        result.city,
        result.country,
        result.temperature,
        0,
        result.observation_time
    )
    return jsonify({
        "city": result.city,
        "country": result.country,
        "temperature": result.temperature
    }), 201

@app.route('/observations', methods=['GET'] )
def observations():
    results = get_all_observations(id)
    return jsonify(results)

@app.route('/observations/<int:id>', methods=['GET'])
def get_observation():

    result = get_observations_by_id(id)

    if not result:
        abort(404)

    return jsonify(result)

@app.route('/observations/<int:id>', methods=['DELETE'])
def delete_observations(id):
    delete_weather(id)
    return jsonify({"deleted": id})

@app.route('/observations/<int:id>', methods=['PUT'])
def update_observations(id):

    data = request.get_json()

    update_weather(id, data["temperature"], data["humidity"])


    return jsonify({
        "id": id,
        "temperature": data["temperature"],
        "humidity": data["humidity"]
    })

if __name__ == "__main__":
    app.run(debug=True)
