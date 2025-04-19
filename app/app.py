from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory weather log store
weather_logs = []

@app.route('/weather', methods=['POST'])
def log_weather():
    data = request.get_json()
    city = data.get('city')
    temperature = data.get('temperature')
    description = data.get('description', '')
    date = data.get('date') or datetime.now().strftime('%Y-%m-%d')

    if not city or temperature is None:
        return jsonify({'error': 'Missing required fields: city and temperature'}), 400

    entry = {
        'city': city.lower(),
        'temperature': temperature,
        'description': description,
        'date': date
    }
    weather_logs.append(entry)
    return jsonify({'message': 'Weather logged successfully', 'entry': entry}), 201

@app.route('/weather/<city>', methods=['GET'])
def get_weather_by_city(city):
    city = city.lower()
    city_logs = [log for log in weather_logs if log['city'] == city]
    return jsonify(city_logs), 200

@app.route('/weather', methods=['GET'])
def get_all_weather():
    return jsonify(weather_logs), 200

@app.route('/ping')
def ping():
    return "pong pong ding dong"

@app.route('/status')
def status():
    return jsonify({"status": "OK Good"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
