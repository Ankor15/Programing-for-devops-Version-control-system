from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import redis

app = Flask(__name__)

# Konfigurasi database PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@db:5432/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Konfigurasi Redis
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/')
def hello_world():
    return 'Hello, World! Aplikasi dengan database PostgreSQL dan Redis.'

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!"}), 201

@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'username': user.username, 'email': user.email} for user in users])

@app.route('/set_cache/<key>/<value>', methods=['GET'])
def set_cache(key, value):
    cache.set(key, value)
    return jsonify({"message": f"Cache set for {key} with value {value}."})

@app.route('/get_cache/<key>', methods=['GET'])
def get_cache(key):
    value = cache.get(key)
    if value:
        return jsonify({"key": key, "value": value.decode('utf-8')})
    else:
        return jsonify({"message": "Key not found in cache."}), 404

if __name__ == '__main__':
    db.create_all()  # Membuat tabel jika belum ada
    app.run(debug=True)
