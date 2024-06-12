from flask import Flask, render_template, request, jsonify
import json
import os
import uuid

app = Flask(__name__)
DATA_FILE = 'data/drawings.json'

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

def load_drawings():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_drawings(drawings):
    with open(DATA_FILE, 'w') as f:
        json.dump(drawings, f)

@app.route('/')
def home():
    drawings = load_drawings()
    # Display the last two drawings
    recent_drawings = drawings[-2:]
    return render_template('index.html', drawings=recent_drawings)

@app.route('/draw')
def draw():
    return render_template('draw.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    drawing_id = str(uuid.uuid4())
    data['id'] = drawing_id
    drawings = load_drawings()
    drawings.append(data)
    save_drawings(drawings)
    return jsonify(status='success', id=drawing_id)

@app.route('/load', methods=['GET'])
def load():
    drawings = load_drawings()
    return jsonify(drawings)

@app.route('/lights')
def lights():
    return render_template("lights.html")


if __name__ == '__main__':
    app.run(debug=True)
