from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DRAWINGS_FILE = 'data/drawings.json'
SETTINGS_FILE = 'data/settings.json'

def load_drawings():
    if os.path.exists(DRAWINGS_FILE):
        with open(DRAWINGS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_drawings(drawings):
    if os.path.exists(DRAWINGS_FILE):
        with open(DRAWINGS_FILE, 'w') as file:
            json.dump(drawings, file)
    return []

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
            if isinstance(settings, dict):
                return settings
            return {'selected_templates': settings}
    return {'selected_templates': ["", ""]}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file)

@app.route('/')
def home():
    drawings = load_drawings()
    settings = load_settings()
    selected_templates = settings.get('selected_templates', ["", ""])
    return render_template('index.html', drawings=drawings, selected_templates=selected_templates)

@app.route('/draw')
def draw():
    return render_template('draw.html')

@app.route('/settings')
def settings():
    drawings = load_drawings()
    return render_template('settings.html', drawings=drawings)

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    name = data.get('name')
    rectangles = data.get('rectangles', [])
    drawings = load_drawings()
    drawings.append({'name': name, 'rectangles': rectangles})
    save_drawings(drawings)
    return jsonify(status='success')

@app.route('/save_settings', methods=['POST'])
def save_settings_route():
    data = request.json
    selected_templates = [data.get('template1', ""), data.get('template2', "")]
    settings = {'selected_templates': selected_templates}
    save_settings(settings)
    return jsonify(status='success')

@app.route('/load/<name>', methods=['GET'])
def load(name):
    drawings = load_drawings()
    drawing = next((d for d in drawings if d['name'] == name), None)
    if drawing:
        return jsonify(drawing)
    return jsonify(status='error', message='Drawing not found'), 404

@app.route('/templates', methods=['GET'])
def templates():
    drawings = load_drawings()
    template_names = [{'name': d['name']} for d in drawings]
    return jsonify(templates=template_names)

@app.route('/square-clicked', methods=['POST'])
def square_clicked():
    data = request.json
    # Process the data as needed
    print(f"Canvas: {data['canvas']}, Rectangle: {data['rectangle']}")
    return jsonify(status='success')

if __name__ == '__main__':
    app.run(debug=True)
