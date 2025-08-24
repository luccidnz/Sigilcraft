
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import random
import math
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
CORS(app)

def create_sigil(phrase, vibe='mystical'):
    """Generate a revolutionary sigil based on phrase and vibe"""
    
    # Create canvas
    size = 400
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define vibe colors and styles
    vibe_styles = {
        'mystical': {'colors': [(138, 43, 226), (75, 0, 130), (148, 0, 211)], 'stroke': 3},
        'cosmic': {'colors': [(0, 100, 200), (100, 0, 200), (200, 0, 100)], 'stroke': 2},
        'elemental': {'colors': [(34, 139, 34), (255, 140, 0), (30, 144, 255)], 'stroke': 4},
        'crystal': {'colors': [(255, 20, 147), (0, 255, 255), (255, 215, 0)], 'stroke': 2},
        'shadow': {'colors': [(64, 64, 64), (128, 0, 128), (105, 105, 105)], 'stroke': 5},
        'light': {'colors': [(255, 255, 0), (255, 215, 0), (255, 255, 255)], 'stroke': 2}
    }
    
    style = vibe_styles.get(vibe, vibe_styles['mystical'])
    colors = style['colors']
    stroke_width = style['stroke']
    
    # Convert phrase to unique pattern
    phrase_clean = ''.join(c.lower() for c in phrase if c.isalnum())
    center_x, center_y = size // 2, size // 2
    
    # Generate sigil geometry based on phrase
    random.seed(sum(ord(c) for c in phrase_clean))
    
    # Create multiple layers of geometric patterns
    for layer in range(3):
        color = colors[layer % len(colors)]
        
        # Generate points based on phrase characters
        points = []
        for i, char in enumerate(phrase_clean[:12]):  # Limit to 12 chars for complexity
            angle = (ord(char) * 29 + i * 30) % 360
            radius = 50 + (ord(char) % 100) + layer * 30
            
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            points.append((x, y))
        
        # Draw connecting lines between points
        if len(points) > 1:
            for i in range(len(points)):
                start = points[i]
                end = points[(i + len(phrase_clean) // 3 + 1) % len(points)]
                draw.line([start, end], fill=color, width=stroke_width)
        
        # Add sacred geometry circles
        for i, point in enumerate(points[:6]):
            radius = 10 + (i * 8)
            draw.ellipse([point[0]-radius, point[1]-radius, 
                         point[0]+radius, point[1]+radius], 
                        outline=color, width=stroke_width//2)
    
    # Add central focus point
    central_color = colors[0]
    draw.ellipse([center_x-15, center_y-15, center_x+15, center_y+15], 
                fill=central_color, outline=colors[1], width=3)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

@app.route('/generate', methods=['POST'])
def generate_sigil():
    try:
        data = request.get_json()
        phrase = data.get('phrase', '').strip()
        vibe = data.get('vibe', 'mystical')
        
        if not phrase:
            return jsonify({'success': False, 'error': 'Phrase is required'}), 400
        
        # Generate the sigil
        sigil_image = create_sigil(phrase, vibe)
        
        return jsonify({
            'success': True,
            'image': sigil_image,
            'phrase': phrase,
            'vibe': vibe,
            'message': f'Revolutionary sigil generated for: "{phrase}"'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'sigilcraft-backend'})

if __name__ == '__main__':
    print("🔮 Starting Sigilcraft Flask Backend...")
    app.run(host='0.0.0.0', port=5001, debug=True)
