
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
import os
import io
import base64
import hashlib
from datetime import datetime
import secrets
import math
import string
import random
import traceback
import time
from functools import wraps
import socket

app = Flask(__name__)
CORS(app, origins=["*"])

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('sigil_generator.log')
    ]
)
app.logger.setLevel(logging.INFO)

def handle_errors(f):
    """Decorator to handle exceptions and return JSON error responses."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error in {f.__name__}: {str(e)}")
            app.logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                'success': False,
                'error': 'Internal server error occurred',
                'timestamp': str(datetime.now())
            }), 500
    return decorated_function

def find_available_port(start_port=5001):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + 10):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

def phrase_to_seed(phrase):
    """Convert phrase to deterministic seed"""
    return hashlib.sha256(phrase.encode()).hexdigest()

def generate_unique_sigil(phrase, vibe='mystical'):
    """Generate a truly unique sigil based on phrase and vibe"""
    # Create deterministic seed from phrase
    seed_string = f"{phrase.lower().strip()}-{vibe}"
    seed = int(hashlib.sha256(seed_string.encode()).hexdigest()[:8], 16)
    np.random.seed(seed)
    random.seed(seed)
    
    # Image dimensions
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Get vibe-specific colors and styles
    colors = get_vibe_colors(vibe)
    
    # Generate phrase-specific characteristics
    num_elements = len(phrase) % 8 + 3
    complexity = (hash(phrase) % 5) + 1
    
    # Generate geometric elements based on phrase
    center_x, center_y = size // 2, size // 2
    
    # Draw background sacred geometry
    draw_sacred_geometry(draw, size, colors, seed)
    
    # Generate unique symbol based on phrase characters
    symbol_elements = generate_symbol_elements(phrase, size, colors)
    
    for element in symbol_elements:
        if element['type'] == 'circle':
            draw.ellipse(element['coords'], outline=element['color'], width=element['width'])
        elif element['type'] == 'line':
            draw.line(element['coords'], fill=element['color'], width=element['width'])
        elif element['type'] == 'polygon':
            draw.polygon(element['coords'], outline=element['color'], width=element['width'])
    
    # Apply vibe-specific effects
    img = apply_vibe_effects(img, vibe)
    
    return img

def get_vibe_colors(vibe):
    """Get color palette for each vibe"""
    palettes = {
        'mystical': [(138, 43, 226), (75, 0, 130), (148, 0, 211)],
        'cosmic': [(25, 25, 112), (72, 61, 139), (123, 104, 238)],
        'elemental': [(139, 69, 19), (160, 82, 45), (205, 133, 63)],
        'crystal': [(176, 224, 230), (173, 216, 230), (135, 206, 235)],
        'shadow': [(47, 47, 47), (69, 69, 69), (105, 105, 105)],
        'light': [(255, 248, 220), (255, 250, 205), (255, 255, 240)]
    }
    return palettes.get(vibe, palettes['mystical'])

def draw_sacred_geometry(draw, size, colors, seed):
    """Draw background sacred geometry patterns"""
    center = size // 2
    
    # Draw concentric circles
    for i in range(3):
        radius = (i + 1) * size // 8
        color = colors[i % len(colors)]
        draw.ellipse([center - radius, center - radius, center + radius, center + radius], 
                    outline=color, width=2)
    
    # Draw radial lines
    num_lines = (seed % 8) + 6
    for i in range(num_lines):
        angle = (2 * math.pi * i) / num_lines
        x1 = center + int(size // 4 * math.cos(angle))
        y1 = center + int(size // 4 * math.sin(angle))
        x2 = center + int(size // 3 * math.cos(angle))
        y2 = center + int(size // 3 * math.sin(angle))
        draw.line([x1, y1, x2, y2], fill=colors[1], width=2)

def generate_symbol_elements(phrase, size, colors):
    """Generate unique symbol elements based on phrase"""
    elements = []
    center = size // 2
    
    # Convert phrase to numeric values
    for i, char in enumerate(phrase.lower()):
        if char.isalpha():
            char_val = ord(char) - ord('a')
            
            # Generate circles
            radius = (char_val % 20) + 10
            angle = (char_val * i * 15) % 360
            x = center + int((size // 6) * math.cos(math.radians(angle)))
            y = center + int((size // 6) * math.sin(math.radians(angle)))
            
            elements.append({
                'type': 'circle',
                'coords': [x - radius, y - radius, x + radius, y + radius],
                'color': colors[char_val % len(colors)],
                'width': 2
            })
            
            # Generate connecting lines
            if i > 0:
                prev_char_val = ord(phrase.lower()[i-1]) - ord('a') if phrase.lower()[i-1].isalpha() else 0
                prev_angle = (prev_char_val * (i-1) * 15) % 360
                prev_x = center + int((size // 6) * math.cos(math.radians(prev_angle)))
                prev_y = center + int((size // 6) * math.sin(math.radians(prev_angle)))
                
                elements.append({
                    'type': 'line',
                    'coords': [prev_x, prev_y, x, y],
                    'color': colors[(char_val + prev_char_val) % len(colors)],
                    'width': 1
                })
    
    return elements

def apply_vibe_effects(img, vibe):
    """Apply vibe-specific visual effects"""
    if vibe == 'cosmic':
        # Add starfield effect
        img = add_stars(img)
    elif vibe == 'mystical':
        # Add glow effect
        img = add_glow(img)
    elif vibe == 'crystal':
        # Add crystalline effect
        img = add_crystal_effect(img)
    elif vibe == 'shadow':
        # Add shadow effect
        img = add_shadow_effect(img)
    elif vibe == 'light':
        # Add light rays
        img = add_light_rays(img)
    
    return img

def add_stars(img):
    """Add starfield effect for cosmic vibe"""
    draw = ImageDraw.Draw(img)
    for _ in range(30):
        x = random.randint(0, img.width)
        y = random.randint(0, img.height)
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(255, 255, 255, 180))
    return img

def add_glow(img):
    """Add glow effect for mystical vibe"""
    # Create a copy for glow
    glow = img.copy()
    glow = glow.filter(ImageFilter.GaussianBlur(radius=3))
    
    # Enhance the glow
    enhancer = ImageEnhance.Brightness(glow)
    glow = enhancer.enhance(1.5)
    
    # Composite with original
    img = Image.alpha_composite(glow, img)
    return img

def add_crystal_effect(img):
    """Add crystalline effect"""
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    return img

def add_shadow_effect(img):
    """Add shadow effect"""
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.8)
    return img

def add_light_rays(img):
    """Add light rays effect"""
    draw = ImageDraw.Draw(img)
    center = img.width // 2, img.height // 2
    
    for i in range(8):
        angle = i * 45
        x1 = center[0] + int(img.width // 3 * math.cos(math.radians(angle)))
        y1 = center[1] + int(img.height // 3 * math.sin(math.radians(angle)))
        x2 = center[0] + int(img.width // 2 * math.cos(math.radians(angle)))
        y2 = center[1] + int(img.height // 2 * math.sin(math.radians(angle)))
        
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255, 100), width=1)
    
    return img

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'Flask backend running',
        'message': 'Sigil generation service active',
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light']
    })

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify server is working"""
    return jsonify({
        'status': 'ok',
        'message': 'Server is working',
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light']
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'server': 'online',
        'timestamp': str(datetime.now())
    })

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint with detailed information"""
    return jsonify({
        'status': 'operational',
        'server': 'Flask Sigil Generator',
        'version': '5.0',
        'features': ['SHA256-based unique generation', 'Phrase-specific characteristics', 'Truly unique results'],
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light'],
        'endpoints': ['/generate', '/test', '/health', '/status']
    })

@app.route('/generate', methods=['POST'])
@handle_errors
def generate_sigil():
    """Generate a unique sigil based on phrase and vibe"""
    try:
        data = request.get_json()
        phrase = data.get('phrase', '').strip()
        vibe = data.get('vibe', 'mystical').strip()

        if not phrase:
            return jsonify({
                'success': False,
                'error': 'Phrase is required'
            }), 400

        if len(phrase) > 200:
            return jsonify({
                'success': False,
                'error': 'Phrase too long (max 200 characters)'
            }), 400

        print(f"🎨 Generating sigil for: '{phrase}' with vibe: {vibe}")

        # Generate the sigil
        sigil_img = generate_unique_sigil(phrase, vibe)

        # Convert to base64
        buffer = io.BytesIO()
        sigil_img.save(buffer, format='PNG')
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        image_data_url = f"data:image/png;base64,{image_base64}"

        print(f"✅ Sigil generated successfully")

        return jsonify({
            'success': True,
            'image': image_data_url,
            'phrase': phrase,
            'vibe': vibe,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Generation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Generation failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = find_available_port()
    if not port:
        print("❌ No available ports found in range 5001-5010")
        exit(1)

    print(f"🚀 Starting Flask sigil generation server on port {port}...")

    # Use production WSGI server
    try:
        from waitress import serve
        print("✅ Using Waitress production server...")
        serve(app, host="0.0.0.0", port=port,
              threads=8,
              connection_limit=200,
              cleanup_interval=30,
              channel_timeout=300)
    except ImportError:
        print("⚠️  Waitress not available, using Flask dev server...")
        app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} still in use, trying Flask dev server...")
            try:
                app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
            except OSError:
                port = find_available_port(port + 1)
                if port:
                    print(f"🔄 Retrying on port {port}...")
                    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
                else:
                    print("❌ Could not find available port")
                    exit(1)
