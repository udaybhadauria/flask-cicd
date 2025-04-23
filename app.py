from dotenv import load_dotenv
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import jwt
import os
import secrets
from functools import wraps

load_dotenv()  # Load variables from .env into os.environ

app = Flask(__name__)
#app.config['SECRET_KEY'] = ''  # Change this in production
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', secrets.token_urlsafe(32))

# In-memory weather log store
weather_logs = []

# JWT decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # JWT passed in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated

# Login route
@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    username = auth.get('username')
    password = auth.get('password')

    if username == 'admin' and password == 'admin123':
        token = jwt.encode({
            'user': username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'}), 401

# Protected: Log weather
@app.route('/weather', methods=['POST'])
@token_required
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

# Public: Get weather for city
@app.route('/weather/<city>', methods=['GET'])
def get_weather_by_city(city):
    city = city.lower()
    city_logs = [log for log in weather_logs if log['city'] == city]
    return jsonify(city_logs), 200

# Public: Get all weather logs
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
    app.run(host='0.0.0.0', port=5876, ssl_context=('/home/pi/flask-cicd/cert.pem', '/home/pi/flask-cicd/key.pem'), debug=True)
    #app.run(host='0.0.0.0', port=5876, ssl_context=('cert.pem', 'key.pem'), debug=True)
