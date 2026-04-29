from flask import Flask, render_template,redirect,  url_for, abort, request, jsonify
from Db_manager import get_all_observations, get_observations_by_id, insert_weather, update_weather, delete_weather
from Db import get_weather
import requests

app = Flask(__name__)
#displays all of the weather observation from the index.html
@app.route('/')
def home():
    results = get_all_observations()
    return render_template('index.html', observations=results)

@app.route('/about')
def about():
    return 'this is the about page.'
#fetches the weather for a city
@app.route('/ingest', methods=['POST'])
def ingest():

    city = request.args.get("city")
    country = request.args.get("country")

    result = get_weather(city, country)

    insert_weather(
            result.city,
            result.country,
            result.latitude,
            result.longitude,
            result.temperature,
            result.windspeed,
            result.observation_time,
            None
    )
    return jsonify({
        "city": result.city,
        "country": result.country,
        "latitude": result.latitude,
        "longitude": result.longitude,
        "temperature": result.temperature,
        "windspeed": result.windspeed,
        "observation_time": result.observation_time,
        "notes": None
    }), 201
#returns all the weather with the observation route
@app.route('/observations', methods=['GET'] )
def observations():
    results = get_all_observations()
    return jsonify(results)
#gets the observation with id route which gives a single observation
@app.route('/observations/<int:id>', methods=['GET'])
def get_observation(id):

    result = get_observations_by_id(id)

    if not result:
        abort(404)

    return jsonify(result)
#Delete route and removes a weather observation
@app.route('/observations/<int:id>', methods=['DELETE'])
def delete_observations(id):
    delete_weather(id)
    return jsonify({"deleted": id})
#updates temperature and humidity
@app.route('/observations/<int:id>', methods=['PUT'])
def update_observations(id):

    data = request.get_json()

    update_weather(id, data["notes"])


    return jsonify({
        "id": id,
        "notes": data["notes"]
    })

if __name__ == "__main__":
    app.run(debug=True)
