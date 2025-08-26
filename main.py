#!/usr/bin/env python3
"""
SIGILCRAFT: ULTRA-REVOLUTIONARY SIGIL GENERATOR V4.0
Completely rewritten for maximum text-responsiveness and uniqueness
"""

import os
import sys
import base64
import random
import math
import hashlib
from io import BytesIO
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging
import string
import re
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask and web dependencies
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Image processing
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError as e:
    print(f"❌ Missing required packages: {e}")
    print("📦 Please install: pip install pillow numpy")
    NUMPY_AVAILABLE = False
    # sys.exit(1) # Removed exit to allow partial functionality if numpy is missing but other parts are used

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== FLASK APP SETUP =====
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Request-ID"],
        "supports_credentials": True
    }
})

# Ensure CORS headers on all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# ===== ULTRA-REVOLUTIONARY SIGIL GENERATOR CLASS =====
class UltraRevolutionarySigilGenerator:
    """Ultra-revolutionary sigil generation with extreme text-specific uniqueness"""

    def __init__(self):
        self.size = 1024
        self.center = (self.size // 2, self.size // 2)

        # Completely redesigned vibe configurations with extreme differentiation
        self.vibe_styles = {
            'mystical': {
                'colors': [(138, 43, 226), (75, 0, 130), (148, 0, 211), (186, 85, 211), (123, 104, 238), (221, 160, 221)],
                'base_patterns': ['pentagram', 'sacred_circle', 'ancient_rune', 'mystic_spiral'],
                'stroke_multiplier': 1.0,
                'complexity_bias': 'ancient',
                'geometry_type': 'curved',
                'energy_flow': 'inward_spiral',
                'symbol_density': 'moderate',
                'glow_intensity': 0.8,
                'pattern_scale': 1.2
            },
            'cosmic': {
                'colors': [(0, 100, 200), (100, 0, 200), (200, 0, 100), (0, 255, 255), (255, 0, 255), (138, 43, 226), (64, 224, 208)],
                'base_patterns': ['constellation', 'galaxy_spiral', 'nebula_cloud', 'star_burst'],
                'stroke_multiplier': 0.8,
                'complexity_bias': 'infinite',
                'geometry_type': 'stellar',
                'energy_flow': 'radial_burst',
                'symbol_density': 'high',
                'glow_intensity': 1.2,
                'pattern_scale': 1.8
            },
            'elemental': {
                'colors': [(34, 139, 34), (255, 140, 0), (30, 144, 255), (139, 69, 19), (255, 69, 0), (0, 128, 0), (255, 215, 0)],
                'base_patterns': ['nature_flow', 'elemental_cross', 'root_system', 'wave_pattern'],
                'stroke_multiplier': 1.5,
                'complexity_bias': 'organic',
                'geometry_type': 'natural',
                'energy_flow': 'flowing',
                'symbol_density': 'organic',
                'glow_intensity': 0.6,
                'pattern_scale': 1.1
            },
            'crystal': {
                'colors': [(255, 20, 147), (0, 255, 255), (255, 215, 0), (255, 105, 180), (64, 224, 208), (255, 255, 255), (147, 0, 211)],
                'base_patterns': ['crystal_lattice', 'prismatic', 'faceted_gem', 'refraction'],
                'stroke_multiplier': 0.6,
                'complexity_bias': 'geometric',
                'geometry_type': 'angular',
                'energy_flow': 'prismatic',
                'symbol_density': 'precise',
                'glow_intensity': 1.5,
                'pattern_scale': 0.9
            },
            'shadow': {
                'colors': [(64, 64, 64), (128, 0, 128), (105, 105, 105), (169, 169, 169), (25, 25, 25), (47, 79, 79), (72, 61, 139)],
                'base_patterns': ['void_portal', 'shadow_tendrils', 'dark_sigil', 'obscured_geometry'],
                'stroke_multiplier': 2.0,
                'complexity_bias': 'hidden',
                'geometry_type': 'jagged',
                'energy_flow': 'consuming',
                'symbol_density': 'sparse',
                'glow_intensity': 0.3,
                'pattern_scale': 1.4
            },
            'light': {
                'colors': [(255, 255, 0), (255, 215, 0), (255, 255, 255), (255, 250, 205), (255, 255, 224), (250, 250, 210), (255, 255, 240)],
                'base_patterns': ['radiant_sun', 'light_rays', 'divine_mandala', 'brilliant_star'],
                'stroke_multiplier': 0.7,
                'complexity_bias': 'illuminating',
                'geometry_type': 'radial',
                'energy_flow': 'emanating',
                'symbol_density': 'luminous',
                'glow_intensity': 2.0,
                'pattern_scale': 1.6
            },
            'storm': {
                'colors': [(75, 0, 130), (255, 255, 0), (0, 0, 139), (220, 20, 60), (255, 20, 147), (138, 43, 226), (255, 69, 0)],
                'base_patterns': ['lightning_tree', 'storm_vortex', 'electric_web', 'chaos_fractal'],
                'stroke_multiplier': 1.3,
                'complexity_bias': 'chaotic',
                'geometry_type': 'electric',
                'energy_flow': 'explosive',
                'symbol_density': 'intense',
                'glow_intensity': 1.1,
                'pattern_scale': 1.7
            },
            'void': {
                'colors': [(25, 25, 112), (0, 0, 0), (72, 61, 139), (106, 90, 205), (75, 0, 130), (25, 25, 25), (47, 79, 79)],
                'base_patterns': ['infinite_spiral', 'dimensional_portal', 'void_geometry', 'recursive_depth'],
                'stroke_multiplier': 1.8,
                'complexity_bias': 'infinite',
                'geometry_type': 'impossible',
                'energy_flow': 'recursive',
                'symbol_density': 'deep',
                'glow_intensity': 0.4,
                'pattern_scale': 2.0
            }
        }

    def generate_sigil(self, phrase: str, vibe: str = 'mystical', advanced: bool = False) -> str:
        """Generate ultra-unique sigils with extreme text responsiveness"""
        try:
            logger.info(f"🎨 Generating ultra-revolutionary sigil: '{phrase}' with vibe: {vibe}")

            # Get style configuration
            style = self.vibe_styles.get(vibe, self.vibe_styles['mystical'])

            # Create ultra high-resolution canvas
            canvas_size = 2048 if advanced else self.size
            img = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Generate ultra-unique seed with phrase specificity
            seed = self._generate_ultra_unique_seed(phrase, vibe)
            random.seed(seed)
            if NUMPY_AVAILABLE:
                np.random.seed(seed % (2**32 - 1))

            # Create sigil with multiple layers
            self._create_base_pattern(draw, phrase, style, canvas_size)
            self._create_text_pattern(draw, phrase, style, canvas_size)
            self._create_vibe_pattern(draw, phrase, vibe, style, canvas_size)

            # Apply effects
            if advanced:
                img = self._apply_ultra_effects(img, style, phrase)
            else:
                img = self._apply_enhanced_effects(img, style, phrase)

            # Convert to base64
            return self._image_to_base64(img)

        except Exception as e:
            logger.error(f"❌ Ultra-revolutionary sigil generation failed: {e}")
            raise

    def _generate_ultra_unique_seed(self, phrase: str, vibe: str) -> int:
        """Generate ultra-unique seed incorporating all text characteristics"""
        combined_data = f"{phrase}|{vibe}|{len(phrase)}|{hash(phrase)}"
        final_hash = hashlib.sha512(combined_data.encode()).hexdigest()
        return int(final_hash[:16], 16) % (2**31)

    def _create_base_pattern(self, draw: ImageDraw, phrase: str, style: Dict, size: int):
        """Create base pattern based on phrase"""
        center = (size // 2, size // 2)

        # Create base geometry
        for i in range(min(12, len(phrase))):
            char = phrase[i] if i < len(phrase) else phrase[i % len(phrase)]
            angle = (ord(char) * 13 + i * 30) % 360
            radius = (size // 10) + (ord(char) % (size // 20))

            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))

            color = style['colors'][i % len(style['colors'])]
            size_factor = max(3, ord(char) % 15)

            try:
                # Draw character-based symbol
                if ord(char) % 3 == 0:
                    draw.ellipse([x-size_factor, y-size_factor, x+size_factor, y+size_factor],
                               outline=color, width=2)
                elif ord(char) % 3 == 1:
                    draw.line([(x-size_factor, y-size_factor), (x+size_factor, y+size_factor)],
                             fill=color, width=3)
                    draw.line([(x-size_factor, y+size_factor), (x+size_factor, y-size_factor)],
                             fill=color, width=3)
                else:
                    points = []
                    for j in range(6):
                        px = x + size_factor * math.cos(math.radians(j * 60))
                        py = y + size_factor * math.sin(math.radians(j * 60))
                        points.append((px, py))
                    if len(points) >= 3:
                        draw.polygon(points, outline=color, width=2)
            except:
                pass

    def _create_text_pattern(self, draw: ImageDraw, phrase: str, style: Dict, size: int):
        """Create pattern based on text structure"""
        center = (size // 2, size // 2)
        words = phrase.split()

        for i, word in enumerate(words[:8]):
            word_energy = sum(ord(c) for c in word.lower())
            angle = (word_energy * 7 + i * 45) % 360
            distance = (size // 6) + (len(word) * size // 40)

            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))

            color = style['colors'][(word_energy + i) % len(style['colors'])]

            # Create word-specific pattern
            try:
                if len(word) <= 3:
                    # Small triangle
                    points = []
                    for j in range(3):
                        px = x + (size//40) * math.cos(math.radians(j * 120))
                        py = y + (size//40) * math.sin(math.radians(j * 120))
                        points.append((px, py))
                    draw.polygon(points, outline=color, width=2)
                elif len(word) <= 6:
                    # Medium square
                    s = size // 50
                    draw.rectangle([x-s, y-s, x+s, y+s], outline=color, width=2)
                else:
                    # Large hexagon
                    points = []
                    for j in range(6):
                        px = x + (size//35) * math.cos(math.radians(j * 60))
                        py = y + (size//35) * math.sin(math.radians(j * 60))
                        points.append((px, py))
                    draw.polygon(points, outline=color, width=2)

                # Connect to center
                draw.line([center, (x, y)], fill=color, width=1)
            except:
                pass

    def _create_vibe_pattern(self, draw: ImageDraw, phrase: str, vibe: str, style: Dict, size: int):
        """Create vibe-specific resonance patterns"""
        center = (size // 2, size // 2)

        if vibe == 'cosmic':
            # Star pattern
            for i in range(8):
                angle = i * 45
                radius = size // 4
                x = center[0] + radius * math.cos(math.radians(angle))
                y = center[1] + radius * math.sin(math.radians(angle))

                color = style['colors'][i % len(style['colors'])]
                try:
                    # Draw star rays
                    draw.line([center, (x, y)], fill=color, width=3)
                    # Add star points
                    star_size = size // 60
                    draw.ellipse([x-star_size, y-star_size, x+star_size, y+star_size], fill=color)
                except:
                    pass

        elif vibe == 'elemental':
            # Natural flow pattern
            for i in range(6):
                start_angle = i * 60
                for j in range(5):
                    angle = start_angle + (j * 10)
                    radius = (size // 8) + (j * size // 40)
                    x = center[0] + radius * math.cos(math.radians(angle))
                    y = center[1] + radius * math.sin(math.radians(angle))

                    if j > 0:
                        color = style['colors'][(i + j) % len(style['colors'])]
                        try:
                            draw.line([prev_pos, (x, y)], fill=color, width=2)
                        except:
                            pass
                    prev_pos = (x, y)

        elif vibe == 'crystal':
            # Geometric crystal pattern
            for layer in range(3):
                layer_radius = (size // 8) + (layer * size // 12)
                sides = 6 + (layer * 2)

                points = []
                for i in range(sides):
                    angle = (360 / sides) * i
                    x = center[0] + layer_radius * math.cos(math.radians(angle))
                    y = center[1] + layer_radius * math.sin(math.radians(angle))
                    points.append((x, y))

                color = style['colors'][layer % len(style['colors'])]
                try:
                    if len(points) >= 3:
                        draw.polygon(points, outline=color, width=2)
                except:
                    pass

        else:
            # Default mystical pattern
            for ring in range(4):
                ring_radius = (size // 12) + (ring * size // 20)
                segments = 8 + (ring * 2)

                for i in range(segments):
                    angle = (360 / segments) * i + (ring * 15)
                    x = center[0] + ring_radius * math.cos(math.radians(angle))
                    y = center[1] + ring_radius * math.sin(math.radians(angle))

                    color = style['colors'][(ring + i) % len(style['colors'])]
                    symbol_size = max(2, size // 80)

                    try:
                        draw.ellipse([x-symbol_size, y-symbol_size, x+symbol_size, y+symbol_size],
                                   fill=color)
                    except:
                        pass

    def _apply_enhanced_effects(self, img: Image.Image, style: Dict, phrase: str) -> Image.Image:
        """Apply enhanced visual effects"""
        if style.get('glow_intensity', 0) > 0:
            result = img.copy()
            for layer in range(3):
                blur_radius = (layer + 1) * 2
                glow = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

                enhancer = ImageEnhance.Brightness(glow)
                intensity = style['glow_intensity'] * (0.7 ** layer)
                glow = enhancer.enhance(intensity)

                result = Image.alpha_composite(result, glow)

            return result

        return img

    def _apply_ultra_effects(self, img: Image.Image, style: Dict, phrase: str) -> Image.Image:
        """Apply ultra-revolutionary visual effects for advanced generation"""
        base_img = img.copy()

        # Enhanced glow effect
        if style.get('glow_intensity', 0) > 0:
            glow_radii = [1, 2, 4, 6, 10]
            for radius in glow_radii:
                glow = base_img.filter(ImageFilter.GaussianBlur(radius=radius))
                enhancer = ImageEnhance.Brightness(glow)
                intensity = style['glow_intensity'] * (0.5 ** (radius / 5))
                glow = enhancer.enhance(intensity)
                base_img = Image.alpha_composite(base_img, glow)

        # Enhanced contrast
        enhancer = ImageEnhance.Contrast(base_img)
        base_img = enhancer.enhance(1.2)

        # Enhanced saturation
        enhancer = ImageEnhance.Color(base_img)
        base_img = enhancer.enhance(1.3)

        return base_img

    def _image_to_base64(self, img: Image.Image) -> str:
        """Convert PIL Image to base64 string with optimization"""
        buffer = BytesIO()

        # Resize for web delivery while maintaining quality
        target_size = 1024
        if img.size[0] > target_size:
            img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)

        img.save(buffer, format='PNG', optimize=True, compress_level=6)
        buffer.seek(0)

        return base64.b64encode(buffer.getvalue()).decode('utf-8')

# ===== FLASK ROUTES =====

# Initialize ultra-revolutionary generator
generator = UltraRevolutionarySigilGenerator()

@app.route('/', methods=['GET'])
def root_health():
    """Root health check endpoint"""
    logger.info("✅ Root health check accessed")
    return "OK", 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'sigilcraft-ultra-revolutionary-backend',
        'version': '4.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate', methods=['POST'])
def generate_sigil():
    """Ultra-revolutionary sigil generation endpoint"""
    start_time = datetime.now()

    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data'
            }), 400

        phrase = data.get('phrase', '').strip()
        vibe = data.get('vibe', 'mystical').lower()
        advanced = data.get('advanced', False)

        # Validation
        if not phrase:
            return jsonify({
                'success': False,
                'error': 'Phrase is required'
            }), 400

        if len(phrase) < 2:
            return jsonify({
                'success': False,
                'error': 'Phrase must be at least 2 characters long'
            }), 400

        if len(phrase) > 500:
            return jsonify({
                'success': False,
                'error': 'Phrase is too long (max 500 characters)'
            }), 400

        # Generate ultra-revolutionary sigil
        logger.info(f"🎨 Generating ultra-revolutionary sigil: '{phrase}' ({vibe}) [Advanced: {advanced}]")

        sigil_image = generator.generate_sigil(phrase, vibe, advanced)

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Ultra-revolutionary sigil generated in {duration:.2f}s")

        return jsonify({
            'success': True,
            'image': sigil_image,
            'phrase': phrase,
            'vibe': vibe,
            'advanced': advanced,
            'metadata': {
                'generation_time': duration,
                'timestamp': datetime.now().isoformat(),
                'version': '4.0.0'
            }
        })

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"❌ Ultra-revolutionary generation failed after {duration:.2f}s: {e}")

        return jsonify({
            'success': False,
            'error': str(e),
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/vibes', methods=['GET'])
def get_available_vibes():
    """Get list of available energy vibes"""
    vibes = list(generator.vibe_styles.keys())

    return jsonify({
        'success': True,
        'vibes': vibes,
        'count': len(vibes),
        'descriptions': {
            'mystical': 'Ancient wisdom & sacred geometry',
            'cosmic': 'Universal stellar connection',
            'elemental': 'Natural organic forces',
            'crystal': 'Prismatic geometric precision',
            'shadow': 'Hidden mysterious power',
            'light': 'Pure divine radiance',
            'storm': 'Raw electric chaos',
            'void': 'Infinite recursive potential'
        }
    })

@app.route('/debug/routes', methods=['GET'])
def debug_routes():
    """Debug endpoint to list all registered routes"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'path': rule.rule,
            'methods': list(rule.methods),
            'endpoint': rule.endpoint
        })
    return jsonify({
        'success': True,
        'routes': routes,
        'count': len(routes)
    })

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 - Path not found: {request.path}")
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'code': 404,
        'path': request.path
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'code': 500
    }), 500

# ===== MAIN EXECUTION =====
if __name__ == '__main__':
    print("🔮 Starting Ultra-Revolutionary Sigilcraft Python Backend...")
    print(f"📦 PIL/Pillow version: {Image.__version__}")
    print(f"🔢 NumPy available: {'✅' if NUMPY_AVAILABLE else '❌'}")
    print("🎨 Ultra-revolutionary text-responsive sigil generation ready!")

    # Get port from environment or default to 5001 (Flask backend)
    port = int(os.getenv('FLASK_PORT', '5001'))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    print(f"🚀 Starting server on port {port}")
    print(f"🔧 Debug mode: {'ON' if debug_mode else 'OFF'}")

    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug_mode,
            threaded=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown gracefully")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)