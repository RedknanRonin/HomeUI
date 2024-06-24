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

def hex_to_rgba(hex, alpha=0.6):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return 'rgba({}, {}, {}, {})'.format(
        int(hex[0:2], 16),
        int(hex[2:4], 16),
        int(hex[4:6], 16),
        alpha
    )

def save_drawings(drawings):
    if os.path.exists(DRAWINGS_FILE):
        with open(DRAWINGS_FILE, 'w') as file:
            json.dump(drawings, file)
    return []

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
            return settings
    return {'selected_templates': ["", ""], 'apiUrls': {}}

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
    settings = load_settings()
    color=settings.get('colors', {})
    rgba_colors = {color: hex_to_rgba(hex, 0.5) for color, hex in color.items()}
    print(rgba_colors)
    return render_template('draw.html',colors=rgba_colors.values())

@app.route('/settings')
def settings():
    drawings = load_drawings()
    settings = load_settings()  # Load the settings
    selected_templates = settings.get('selected_templates', ["", ""])  # Get the selected templates
    return render_template('settings.html', drawings=drawings, settings=settings, selected_templates=selected_templates)



@app.route('/save', methods=['POST'])
def save():
    data = request.json
    name = data.get('name')
    rectangles = data.get('rectangles', [])
    image=data.get('imageSource')
    drawings = load_drawings()
    drawings.append({'name': name, 'rectangles': rectangles, 'imageSource': image})
    save_drawings(drawings)
    return jsonify(status='success')

@app.route('/save_settings', methods=['POST'])
def save_settings_route():
    data = request.json
    selected_templates = [data.get('template1', ""), data.get('template2', "")]
    settings = {'selected_templates': selected_templates, 'apiUrls': data.get('apiUrls', {}),'colors' :data.get('colors', {}) }
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


@app.route('/api_request/<color>', methods=['POST'])
def api_request(color):
    print(color)
    settings = load_settings()
    api_urls = settings.get('apiUrls', {})
    api_url = api_urls.get(color)
    if not api_url:
        return jsonify(status='error', message='API URL not found for color'), 404

    data = request.json
    response = request.post(api_url, json=data)
    if response.status_code == 200:
        return jsonify(status='success')
    else:
        return jsonify(status='error', message='Failed to send API request'), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
