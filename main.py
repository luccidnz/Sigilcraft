
import os
os.system("pip install flask pillow")

from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import string
import math
import io
import base64

app = Flask(__name__)

def create_sigil(phrase, size=400):
    """Create a sigil image and return it as base64 encoded string"""
    phrase = phrase.upper()
    phrase = ''.join([c for c in phrase if c in string.ascii_uppercase])
    phrase = ''.join(sorted(set(phrase), key=phrase.index))
    
    if not phrase:
        return None, "Please enter text with at least one letter"

    img = Image.new('RGB', (size, size), color='black')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", max(20, size//15))
    except:
        font = ImageFont.load_default()

    radius = size * 0.35
    center = (size//2, size//2)
    angle_step = 360 / len(phrase)
    points = []

    for i, letter in enumerate(phrase):
        angle = math.radians(i * angle_step - 90)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        
        # Get text size for better centering
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        draw.text((x - text_width//2, y - text_height//2), letter, font=font, fill='white')
        points.append((x, y))

    if len(points) > 1:
        draw.line(points, fill='red', width=max(2, size//150))
    
    # Convert to base64
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    return img_base64, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    phrase = data.get('phrase', '')
    
    if not phrase.strip():
        return jsonify({'error': 'Please enter your intent or desire'})
    
    img_base64, error = create_sigil(phrase.strip())
    
    if error:
        return jsonify({'error': error})
    
    return jsonify({'image': f'data:image/png;base64,{img_base64}'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
