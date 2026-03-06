from flask import Flask 

app = Flask(__name__)

@app.route('/')
def home():
    return "This is the Weather tracker"

@app.route('/ingest', methods=['POST'])
def ingest():
    return "Ingest endpoint placeholder"

@app.route('/observations', methods=['GET'] )
def observations():
    return "List observations placeholder"

@app.route('/observations/<int:id>', methods=['GET'])
def get_observation(id):
    return "Single observation placeholder"

@app.route('/observations/<int:id>', methods=['DELETE'])
def delete_observations(id):
    return "Observation placeholder deleted"

@app.route('/observations/<int:id>', methods=['PUT'])
def update_observations(id):
    return "Update observation placeholder"


if __name__ == "__main__":
    app.run(debug=True)
