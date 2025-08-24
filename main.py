from flask import Flask, request, jsonify, render_template
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

def rate_limit(max_requests=60, per_seconds=60):
    """Simple in-memory rate limiting decorator."""
    request_counts = {}

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
            now = time.time()

            # Clean old entries
            cutoff = now - per_seconds
            request_counts[client_ip] = [t for t in request_counts.get(client_ip, []) if t > cutoff]

            # Check rate limit
            if len(request_counts.get(client_ip, [])) >= max_requests:
                return jsonify({
                    'success': False,
                    'error': 'Rate limit exceeded. Please wait before making more requests.',
                    'retry_after': per_seconds
                }), 429

            # Add current request
            request_counts.setdefault(client_ip, []).append(now)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def find_available_port(start_port=5001):
    """Find an available port starting from start_port"""
    import socket
    for port in range(start_port, start_port + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    return None

def get_enhanced_phrase_characteristics(phrase):
    """Extract comprehensive characteristics from the phrase for unique generation"""
    if not phrase:
        return {}

    phrase_hash = hashlib.sha256(phrase.encode()).hexdigest()

    return {
        'length': len(phrase),
        'word_count': len(phrase.split()),
        'char_sum': sum(ord(c) for c in phrase),
        'vowel_count': sum(1 for c in phrase.lower() if c in 'aeiou'),
        'consonant_count': sum(1 for c in phrase.lower() if c.isalpha() and c not in 'aeiou'),
        'unique_chars': len(set(phrase.lower())),
        'hash_seed': int(phrase_hash[:8], 16),
        'char_positions': [ord(c) * (i + 1) for i, c in enumerate(phrase)],
        'char_sum_weighted': sum(ord(c) * (i + 1) for i, c in enumerate(phrase)),
        'middle_char_value': ord(phrase[len(phrase)//2]) if phrase else 77,
        'word_lengths': [len(word) for word in phrase.split()],
        'pattern_score': sum(phrase.count(c) for c in set(phrase.lower())),
        'emotional_words': sum(1 for word in phrase.lower().split() if word in [
            'love', 'peace', 'power', 'strength', 'healing', 'money', 'success', 'joy',
            'happiness', 'protection', 'wisdom', 'clarity', 'abundance', 'prosperity'
        ])
    }

def apply_optimized_vibe_effects(img, vibe, phrase):
    """Apply vibe-specific effects optimized for performance"""
    characteristics = get_enhanced_phrase_characteristics(phrase)

    if vibe == 'mystical':
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
        img = img.filter(ImageFilter.GaussianBlur(0.5))
    elif vibe == 'cosmic':
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.4)
        img = img.filter(ImageFilter.EDGE_ENHANCE)
    elif vibe == 'elemental':
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)
    elif vibe == 'crystal':
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
    elif vibe == 'shadow':
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.8)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.3)
    elif vibe == 'light':
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.4)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.9)

    return img

def generate_unique_sigil(phrase, vibe='mystical'):
    """Generate a truly unique sigil based on phrase characteristics"""
    characteristics = get_enhanced_phrase_characteristics(phrase)

    # Create deterministic randomness from phrase
    np.random.seed(characteristics['hash_seed'] % (2**32))

    # Create base image
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Generate sacred geometry based on phrase
    center_x, center_y = size // 2, size // 2

    # Draw sacred circles
    num_circles = min(max(characteristics['word_count'], 3), 7)
    for i in range(num_circles):
        radius = 50 + (i * 30) + (characteristics['char_sum'] % 100)
        angle_offset = (characteristics['char_sum_weighted'] * i) % 360

        circle_x = center_x + int(radius * 0.3 * np.cos(np.radians(angle_offset)))
        circle_y = center_y + int(radius * 0.3 * np.sin(np.radians(angle_offset)))

        draw.ellipse([circle_x - radius//4, circle_y - radius//4,
                     circle_x + radius//4, circle_y + radius//4],
                     outline=(255, 255, 255, 180), width=2)

    # Draw connecting lines based on phrase structure
    for i, pos in enumerate(characteristics['char_positions'][:8]):
        angle = (pos * 137.5) % 360  # Golden angle
        line_length = 100 + (pos % 150)

        x1 = center_x
        y1 = center_y
        x2 = center_x + int(line_length * np.cos(np.radians(angle)))
        y2 = center_y + int(line_length * np.sin(np.radians(angle)))

        draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 150), width=2)

    # Add mystical symbols
    symbol_count = characteristics['unique_chars'] % 5 + 3
    for i in range(symbol_count):
        angle = (characteristics['char_sum'] * i * 51.4) % 360
        distance = 120 + (i * 40)

        sym_x = center_x + int(distance * np.cos(np.radians(angle)))
        sym_y = center_y + int(distance * np.sin(np.radians(angle)))

        # Draw small mystical symbols
        symbol_size = 15 + (characteristics['vowel_count'] % 10)
        draw.ellipse([sym_x - symbol_size, sym_y - symbol_size,
                     sym_x + symbol_size, sym_y + symbol_size],
                     fill=(255, 255, 255, 200))

    # Apply vibe effects
    img = apply_optimized_vibe_effects(img, vibe, phrase)

    return img

@app.route('/')
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
        else:
            raise