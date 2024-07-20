from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DRAWINGS_FILE = 'data/drawings.json'
SETTINGS_FILE = 'data/settings.json'
CONFIG_FILE = 'data/config.json'

def load_drawings():
    if os.path.exists(DRAWINGS_FILE):
        with open(DRAWINGS_FILE, 'r') as file:
            return json.load(file)
    return []

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return []

def hex_to_rgba(hex, alpha=0.6):
    hex = hex.lstrip('#')
    return 'rgba({}, {}, {}, {})'.format(
        int(hex[0:2], 16),
        int(hex[2:4], 16),
        int(hex[4:6], 16),
        alpha
    )

def rgba_to_hex(rgba):
    rgba = rgba.strip('rgba()').split(',')
    r = int(rgba[0])
    g = int(rgba[1])
    b = int(rgba[2])
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

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
    return {'selected_templates': ["", ""], 'apiUrls': {}, 'colors': {}}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file)

@app.route('/')
def home():
    drawings = load_drawings()
    settings = load_settings()
    config=load_config()
    selected_templates = settings.get('selected_templates', ["", ""])
    return render_template('index.html', drawings=drawings, selected_templates=selected_templates, config=config)

@app.route('/draw')
def draw():
    settings = load_settings()
    color=settings.get('colors', {})
    rgba_colors = {color: hex_to_rgba(hex, 0.5) for color, hex in color.items()}
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
    prev=load_settings()
    selected_templates = [data.get('template1', ""), data.get('template2', "")]
    settings = {'selected_templates': selected_templates, 'apiUrls': data.get('apiUrls', {}),'colors' :data.get('colors', {}) }

    #for pColorMap in prev['colors']:
     #   for pColor in (prev['colors'][pColorMap]):
      #      if pColor not in data['colors'][pColorMap]:
       #         data['colors'][pColorMap].append(pColor)

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

@app.route('/clear_drawings', methods=['POST'])
def clear_drawings():
    save_drawings([{'name': "None", 'rectangles': [], 'imageSource': ""}])


@app.route('/api_request/<color>', methods=['POST'])
def api_request(color):
    settings = load_settings()
    rgba=(settings.get('colors'))
    color_as_hex=(dict((v,k) for k,v in rgba.items())[rgba_to_hex(color)])
    api_urls = settings.get('apiUrls', {})
    api_url = api_urls.get(color_as_hex)
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
