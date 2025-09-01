
#!/usr/bin/env python3
"""
SIGILCRAFT FLASK BACKEND
Revolutionary sigil generation API - ULTRA STABLE VERSION
"""

import os
import json
import base64
import math
from io import BytesIO
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging

# Configure robust logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins="*")

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['JSON_SORT_KEYS'] = False

def generate_sigil_image(phrase, vibe="mystical", advanced=False):
    """Generate a revolutionary sigil image"""
    try:
        # Import here to avoid issues if packages aren't available
        from PIL import Image, ImageDraw, ImageFont
        
        # Create base image
        size = 512 if advanced else 256
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Vibe color schemes
        vibe_colors = {
            'mystical': [(139, 92, 246), (168, 85, 247), (147, 51, 234)],
            'cosmic': [(59, 130, 246), (99, 102, 241), (139, 92, 246)],
            'elemental': [(34, 197, 94), (59, 130, 246), (168, 85, 247)],
            'crystal': [(236, 72, 153), (219, 39, 119), (147, 51, 234)],
            'shadow': [(75, 85, 99), (55, 65, 81), (31, 41, 55)],
            'light': [(251, 191, 36), (245, 158, 11), (217, 119, 6)],
            'storm': [(220, 38, 127), (239, 68, 68), (248, 113, 113)],
            'void': [(17, 24, 39), (55, 65, 81), (99, 102, 241)]
        }
        
        colors = vibe_colors.get(vibe, vibe_colors['mystical'])
        
        # Generate sigil based on phrase
        center_x, center_y = size // 2, size // 2
        
        # Create sacred geometry based on phrase
        char_values = [ord(c) for c in phrase.lower() if c.isalpha()]
        if not char_values:
            char_values = [97]  # Default to 'a'
            
        # Draw base circle
        radius = size // 3
        draw.ellipse([center_x - radius, center_y - radius, 
                     center_x + radius, center_y + radius], 
                    outline=colors[0], width=3)
        
        # Generate mystical patterns
        for i, char_val in enumerate(char_values[:8]):  # Limit to 8 characters
            angle = (char_val * 7 + i * 45) % 360
            rad = math.radians(angle)
            
            # Calculate points
            x1 = center_x + int(radius * 0.7 * math.cos(rad))
            y1 = center_y + int(radius * 0.7 * math.sin(rad))
            x2 = center_x + int(radius * 1.2 * math.cos(rad + math.pi/4))
            y2 = center_y + int(radius * 1.2 * math.sin(rad + math.pi/4))
            
            # Draw mystical lines
            color_idx = i % len(colors)
            draw.line([center_x, center_y, x1, y1], fill=colors[color_idx], width=2)
            
            if advanced:
                # Add sacred symbols
                symbol_size = 20
                draw.ellipse([x1-symbol_size//2, y1-symbol_size//2, 
                            x1+symbol_size//2, y1+symbol_size//2], 
                           fill=colors[color_idx])
        
        # Add central power symbol
        center_size = 15 if advanced else 10
        draw.ellipse([center_x-center_size, center_y-center_size, 
                     center_x+center_size, center_y+center_size], 
                    fill=colors[1])
        
        # Convert to base64
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        image_data = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{image_data}"
        
    except ImportError:
        # Fallback if PIL not available - generate simple SVG
        return generate_fallback_sigil(phrase, vibe)
    except Exception as e:
        logger.error(f"Error generating sigil: {e}")
        return generate_fallback_sigil(phrase, vibe)

def generate_fallback_sigil(phrase, vibe):
    """Generate a simple SVG sigil as fallback"""
    colors = {
        'mystical': '#8B5CF6',
        'cosmic': '#3B82F6',
        'elemental': '#22C55E',
        'crystal': '#EC4899',
        'shadow': '#4B5563',
        'light': '#FBBF24',
        'storm': '#DC2626',
        'void': '#6366F1'
    }
    
    color = colors.get(vibe, '#8B5CF6')
    
    # Generate pattern based on phrase
    char_values = [ord(c) for c in phrase.lower() if c.isalpha()]
    if not char_values:
        char_values = [97]
    
    svg_paths = []
    for i, char_val in enumerate(char_values[:6]):
        angle = (char_val * 7 + i * 60) % 360
        rad = math.radians(angle)
        x = 128 + int(80 * math.cos(rad))
        y = 128 + int(80 * math.sin(rad))
        svg_paths.append(f"M128,128 L{x},{y}")
    
    svg = f'''<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
        <circle cx="128" cy="128" r="100" fill="none" stroke="{color}" stroke-width="3"/>
        <path d="{' '.join(svg_paths)}" stroke="{color}" stroke-width="2" fill="none"/>
        <circle cx="128" cy="128" r="8" fill="{color}"/>
    </svg>'''
    
    svg_b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{svg_b64}"

@app.route('/')
def serve_index():
    """Serve the main index.html"""
    try:
        return send_from_directory('public', 'index.html')
    except FileNotFoundError:
        logger.error("index.html not found in public directory")
        return jsonify({'success': False, 'error': 'Application files missing'}), 404
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return jsonify({'success': False, 'error': 'Server error'}), 500

@app.route('/api/status')
def api_status():
    """Enhanced API status endpoint"""
    return jsonify({
        'success': True,
        'status': 'operational',
        'service': 'sigilcraft-api',
        'version': '2.0.1',
        'endpoints': {
            'generate': '/api/generate',
            'vibes': '/api/vibes',
            'health': '/health'
        }
    })

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from public directory with robust error handling"""
    try:
        # Security check - prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            logger.warning(f"Blocked potentially malicious path: {filename}")
            return send_from_directory('public', 'index.html')
            
        # Check if file exists in public directory
        file_path = os.path.join('public', filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory('public', filename)
        else:
            # If file not found, serve index.html for client-side routing
            logger.info(f"File not found, serving index.html for: {filename}")
            return send_from_directory('public', 'index.html')
    except Exception as e:
        logger.error(f"Error serving {filename}: {e}")
        try:
            return send_from_directory('public', 'index.html')
        except:
            return jsonify({'success': False, 'error': 'Static file error'}), 500

@app.route('/health')
def health():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'sigilcraft-backend',
        'version': '2.0.0'
    })

@app.route('/api/generate', methods=['POST'])
def generate_sigil():
    """Generate a revolutionary sigil with bulletproof error handling"""
    try:
        # Validate request data
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400
        
        # Validate phrase
        phrase = data.get('phrase', '').strip()
        if not phrase:
            return jsonify({'success': False, 'error': 'Phrase is required'}), 400
            
        if len(phrase) < 2:
            return jsonify({'success': False, 'error': 'Phrase must be at least 2 characters'}), 400
        
        if len(phrase) > 500:
            return jsonify({'success': False, 'error': 'Phrase too long (max 500 characters)'}), 400
        
        # Validate vibe
        vibe = data.get('vibe', 'mystical')
        valid_vibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void']
        if vibe not in valid_vibes:
            vibe = 'mystical'  # Default fallback
        
        advanced = bool(data.get('advanced', False))
        
        # Generate the sigil with comprehensive error handling
        logger.info(f"🔮 Generating sigil for: '{phrase[:50]}{'...' if len(phrase) > 50 else ''}' (vibe: {vibe}, advanced: {advanced})")
        
        try:
            image_data = generate_sigil_image(phrase, vibe, advanced)
            if not image_data:
                raise ValueError("Image generation returned empty result")
                
        except Exception as gen_error:
            logger.error(f"Image generation failed: {gen_error}")
            # Try fallback generation
            try:
                image_data = generate_fallback_sigil(phrase, vibe)
                logger.info("Successfully generated fallback sigil")
            except Exception as fallback_error:
                logger.error(f"Fallback generation also failed: {fallback_error}")
                return jsonify({
                    'success': False, 
                    'error': 'Sigil generation temporarily unavailable'
                }), 500
        
        response_data = {
            'success': True,
            'image': image_data,
            'phrase': phrase,
            'vibe': vibe,
            'advanced': advanced,
            'timestamp': int(__import__('time').time())
        }
        
        logger.info(f"✨ Successfully generated sigil (length: {len(image_data)} chars)")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"❌ Critical generation error: {e}", exc_info=True)
        return jsonify({
            'success': False, 
            'error': 'Internal server error during generation'
        }), 500

@app.route('/api/vibes')
def get_vibes():
    """Get available vibes"""
    return jsonify({
        'success': True,
        'vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void'],
        'descriptions': {
            'mystical': 'Ancient wisdom & sacred geometry',
            'cosmic': 'Universal stellar connection',
            'elemental': 'Natural organic forces',
            'crystal': 'Prismatic clarity',
            'shadow': 'Hidden mysterious power',
            'light': 'Pure divine radiance',
            'storm': 'Raw electric chaos',
            'void': 'Infinite recursive potential'
        }
    })

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'success': False, 'error': 'Bad request', 'code': 400}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found', 'code': 404}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'success': False, 'error': 'Method not allowed', 'code': 405}), 405

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'success': False, 'error': 'Request too large', 'code': 413}), 413

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'success': False, 'error': 'Internal server error', 'code': 500}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return jsonify({'success': False, 'error': 'Unexpected error occurred', 'code': 500}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🔮 Starting Sigilcraft Backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
