
#!/usr/bin/env python3
"""
SIGILCRAFT: REVOLUTIONARY SIGIL GENERATOR
Enhanced Python Flask Backend with Advanced Algorithms
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

# Flask and web dependencies
from flask import Flask, request, jsonify
from flask_cors import CORS

# Image processing
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import numpy as np
except ImportError as e:
    print(f"❌ Missing required packages: {e}")
    print("📦 Please install: pip install pillow numpy")
    sys.exit(1)

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

# ===== ENHANCED SIGIL GENERATOR CLASS =====
class AdvancedSigilGenerator:
    """Advanced sigil generation with multiple algorithms and styles"""
    
    def __init__(self):
        self.size = 512
        self.center = (self.size // 2, self.size // 2)
        
        # Enhanced vibe configurations
        self.vibe_styles = {
            'mystical': {
                'colors': [(138, 43, 226), (75, 0, 130), (148, 0, 211), (186, 85, 211)],
                'stroke_width': 3,
                'glow_intensity': 0.6,
                'complexity': 'medium',
                'sacred_geometry': True
            },
            'cosmic': {
                'colors': [(0, 100, 200), (100, 0, 200), (200, 0, 100), (0, 255, 255)],
                'stroke_width': 2,
                'glow_intensity': 0.8,
                'complexity': 'high',
                'stellar_patterns': True
            },
            'elemental': {
                'colors': [(34, 139, 34), (255, 140, 0), (30, 144, 255), (139, 69, 19)],
                'stroke_width': 4,
                'glow_intensity': 0.5,
                'complexity': 'medium',
                'natural_flow': True
            },
            'crystal': {
                'colors': [(255, 20, 147), (0, 255, 255), (255, 215, 0), (255, 105, 180)],
                'stroke_width': 2,
                'glow_intensity': 0.9,
                'complexity': 'high',
                'geometric_precision': True
            },
            'shadow': {
                'colors': [(64, 64, 64), (128, 0, 128), (105, 105, 105), (169, 169, 169)],
                'stroke_width': 5,
                'glow_intensity': 0.3,
                'complexity': 'low',
                'dark_energy': True
            },
            'light': {
                'colors': [(255, 255, 0), (255, 215, 0), (255, 255, 255), (255, 250, 205)],
                'stroke_width': 2,
                'glow_intensity': 1.0,
                'complexity': 'medium',
                'radiant_energy': True
            },
            'storm': {
                'colors': [(75, 0, 130), (255, 255, 0), (0, 0, 139), (220, 20, 60)],
                'stroke_width': 3,
                'glow_intensity': 0.7,
                'complexity': 'high',
                'chaotic_energy': True
            },
            'void': {
                'colors': [(25, 25, 112), (0, 0, 0), (72, 61, 139), (106, 90, 205)],
                'stroke_width': 4,
                'glow_intensity': 0.4,
                'complexity': 'minimal',
                'infinite_depth': True
            }
        }
    
    def generate_sigil(self, phrase: str, vibe: str = 'mystical', advanced: bool = False) -> str:
        """Generate an advanced sigil based on phrase and vibe"""
        try:
            logger.info(f"🎨 Generating sigil: '{phrase}' with vibe: {vibe}")
            
            # Get style configuration
            style = self.vibe_styles.get(vibe, self.vibe_styles['mystical'])
            
            # Create high-resolution canvas
            canvas_size = 1024 if advanced else self.size
            img = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Generate seed from phrase for reproducibility
            seed = self._generate_seed(phrase)
            random.seed(seed)
            np.random.seed(seed % (2**32 - 1))
            
            # Create base sigil structure
            self._create_base_structure(draw, phrase, style, canvas_size)
            
            # Add vibe-specific elements
            self._add_vibe_elements(draw, phrase, vibe, style, canvas_size)
            
            # Apply post-processing effects
            if advanced:
                img = self._apply_advanced_effects(img, style)
            else:
                img = self._apply_basic_effects(img, style)
            
            # Convert to base64
            return self._image_to_base64(img)
            
        except Exception as e:
            logger.error(f"❌ Sigil generation failed: {e}")
            raise
    
    def _generate_seed(self, phrase: str) -> int:
        """Generate a consistent seed from phrase"""
        return int(hashlib.md5(phrase.encode()).hexdigest(), 16) % (2**31)
    
    def _create_base_structure(self, draw: ImageDraw, phrase: str, style: Dict, size: int):
        """Create the base geometric structure of the sigil"""
        center = (size // 2, size // 2)
        colors = style['colors']
        stroke = style['stroke_width']
        
        # Convert phrase to geometric pattern
        phrase_clean = ''.join(c.lower() for c in phrase if c.isalnum())
        
        # Generate sacred geometry based on phrase
        for i, char in enumerate(phrase_clean):
            char_value = ord(char)
            angle = (char_value * 23 + i * 37) % 360
            radius = (char_value % 100) + 50
            
            # Scale for canvas size
            radius = radius * size // 512
            
            # Calculate position
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            
            # Draw connecting lines
            if i > 0:
                prev_char = ord(phrase_clean[i-1])
                prev_angle = (prev_char * 23 + (i-1) * 37) % 360
                prev_radius = (prev_char % 100) + 50
                prev_radius = prev_radius * size // 512
                
                prev_x = center[0] + prev_radius * math.cos(math.radians(prev_angle))
                prev_y = center[1] + prev_radius * math.sin(math.radians(prev_angle))
                
                color = colors[i % len(colors)]
                draw.line([(prev_x, prev_y), (x, y)], fill=color, width=stroke)
            
            # Draw nodes
            node_size = stroke * 2
            color = colors[i % len(colors)]
            draw.ellipse([x-node_size, y-node_size, x+node_size, y+node_size], 
                        fill=color, outline=color)
    
    def _add_vibe_elements(self, draw: ImageDraw, phrase: str, vibe: str, style: Dict, size: int):
        """Add vibe-specific visual elements"""
        center = (size // 2, size // 2)
        colors = style['colors']
        
        if vibe == 'mystical' or style.get('sacred_geometry'):
            self._add_sacred_geometry(draw, center, colors, size)
        elif vibe == 'cosmic' or style.get('stellar_patterns'):
            self._add_stellar_patterns(draw, center, colors, size)
        elif vibe == 'elemental' or style.get('natural_flow'):
            self._add_natural_elements(draw, phrase, center, colors, size)
        elif vibe == 'crystal' or style.get('geometric_precision'):
            self._add_crystalline_structure(draw, center, colors, size)
        elif vibe == 'shadow' or style.get('dark_energy'):
            self._add_shadow_elements(draw, center, colors, size)
        elif vibe == 'light' or style.get('radiant_energy'):
            self._add_light_rays(draw, center, colors, size)
        elif vibe == 'storm' or style.get('chaotic_energy'):
            self._add_storm_patterns(draw, center, colors, size)
        elif vibe == 'void' or style.get('infinite_depth'):
            self._add_void_patterns(draw, center, colors, size)
    
    def _add_sacred_geometry(self, draw: ImageDraw, center: Tuple[int, int], colors: List[Tuple[int, int, int]], size: int):
        """Add sacred geometric patterns"""
        # Flower of Life pattern
        radius = size // 8
        for i in range(6):
            angle = i * 60
            x = center[0] + radius * math.cos(math.radians(angle)) // 2
            y = center[1] + radius * math.sin(math.radians(angle)) // 2
            
            color = colors[i % len(colors)]
            draw.ellipse([x-radius//3, y-radius//3, x+radius//3, y+radius//3], 
                        outline=color, width=2)
    
    def _add_stellar_patterns(self, draw: ImageDraw, center: Tuple[int, int], colors: List[Tuple[int, int, int]], size: int):
        """Add cosmic stellar patterns"""
        # Draw constellation-like patterns
        for i in range(8):
            angle = i * 45
            radius = size // 4
            
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            
            # Draw star
            star_points = []
            for j in range(8):
                star_angle = angle + j * 45
                star_radius = radius // 6 if j % 2 == 0 else radius // 12
                star_x = x + star_radius * math.cos(math.radians(star_angle))
                star_y = y + star_radius * math.sin(math.radians(star_angle))
                star_points.append((star_x, star_y))
            
            if len(star_points) > 2:
                color = colors[i % len(colors)]
                draw.polygon(star_points, outline=color)
    
    def _add_natural_elements(self, draw: ImageDraw, phrase: str, center: Tuple[int, int], colors: List[Tuple[int, int, int]], size: int):
        """Add natural, flowing elements"""
        # Create organic, flowing lines
        phrase_sum = sum(ord(c) for c in phrase)
        
        for i in range(4):
            points = []
            base_angle = (phrase_sum + i * 90) % 360
            
            for j in range(20):
                angle = base_angle + j * 18 + random.randint(-10, 10)
                radius = (size // 6) + (j * size // 200) + random.randint(-20, 20)
                
                x = center[0] + radius * math.cos(math.radians(angle))
                y = center[1] + radius * math.sin(math.radians(angle))
                points.append((x, y))
            
            if len(points) > 1:
                color = colors[i % len(colors)]
                for k in range(len(points) - 1):
                    draw.line([points[k], points[k + 1]], fill=color, width=3)
    
    def _add_crystalline_structure(self, draw: ImageDraw, center: Tuple[int, int], colors: List[Tuple[int, int, int]], size: int):
        """Add crystal-like geometric structures"""
        # Draw crystalline facets
        for i in range(6):
            angle = i * 60
            outer_radius = size // 3
            inner_radius = size // 6
            
            # Outer points
            outer_x = center[0] + outer_radius * math.cos(math.radians(angle))
            outer_y = center[1] + outer_radius * math.sin(math.radians(angle))
            
            # Inner points
            inner_x = center[0] + inner_radius * math.cos(math.radians(angle + 30))
            inner_y = center[1] + inner_radius * math.sin(math.radians(angle + 30))
            
            # Draw facet
            color = colors[i % len(colors)]
            draw.line([center, (outer_x, outer_y)], fill=color, width=2)
            draw.line([center, (inner_x, inner_y)], fill=color, width=1)
            draw.line([(outer_x, outer_y), (inner_x, inner_y)], fill=color, width=1)
    
    def _add_shadow_elements(self, draw: ImageDraw, center: Tuple[int, int], colors: List[Tuple[int, int, int]], size: int):
        """Add shadow and dark energy elements"""
        # Create shadowy, angular patterns
        for i in range(3):
            angle = i * 120
            points = []
            
            for j in range(5):
                sub_angle = angle + j * 20 - 40
                radius = size // 4 + random.randint(-20, 20)
                
                x = center[0] + radius * math.cos(math.radians(sub_angle))
                y = center[1] + radius * math.sin(math.radians(sub_angle))
                points.append((x, y))
            
            if len(points) > 2:
                color = colors[i % len(colors)]
                draw.polygon(points, outline=color, width=3)
    
    def _add_light_rays(self, draw: ImageDraw, center: Tuple[int, int], colors: List[Tuple[int, int, int]], size: int):
        """Add radiant light ray patterns"""
        # Draw radiating light beams
        for i in range(12):
            angle = i * 30
            inner_radius = size // 8
            outer_radius = size // 3
            
            inner_x = center[0] + inner_radius * math.cos(math.radians(angle))
            inner_y = center[1] + inner_radius * math.sin(math.radians(angle))
            
            outer_x = center[0] + outer_radius * math.cos(math.radians(angle))
            outer_y = center[1] + outer_radius * math.sin(math.radians(angle))
            
            color = colors[i % len(colors)]
            width = 3 if i % 3 == 0 else 1
            draw.line([(inner_x, inner_y), (outer_x, outer_y)], fill=color, width=width)
    
    def _add_storm_patterns(self, draw: ImageDraw, center: Tuple[int, int], colors: List[Tuple[int, int, int]], size: int):
        """Add chaotic storm-like patterns"""
        # Create lightning-like jagged lines
        for i in range(5):
            start_angle = i * 72
            points = [center]
            
            current_angle = start_angle
            current_radius = 0
            
            while current_radius < size // 3:
                current_angle += random.randint(-45, 45)
                current_radius += random.randint(20, 60)
                
                x = center[0] + current_radius * math.cos(math.radians(current_angle))
                y = center[1] + current_radius * math.sin(math.radians(current_angle))
                points.append((x, y))
            
            # Draw jagged line
            color = colors[i % len(colors)]
            for j in range(len(points) - 1):
                draw.line([points[j], points[j + 1]], fill=color, width=2)
    
    def _add_void_patterns(self, draw: ImageDraw, center: Tuple[int, int], colors: List[Tuple[int, int, int]], size: int):
        """Add void/infinite depth patterns"""
        # Create concentric patterns that suggest depth
        for i in range(5):
            radius = (i + 1) * size // 12
            color = colors[i % len(colors)]
            
            # Draw concentric circles with gaps
            for angle in range(0, 360, 45):
                arc_start = angle
                arc_end = angle + 30
                
                bbox = [center[0] - radius, center[1] - radius, 
                       center[0] + radius, center[1] + radius]
                draw.arc(bbox, arc_start, arc_end, fill=color, width=2)
    
    def _apply_basic_effects(self, img: Image.Image, style: Dict) -> Image.Image:
        """Apply basic visual effects"""
        # Add subtle glow effect
        if style.get('glow_intensity', 0) > 0:
            # Create glow layer
            glow = img.filter(ImageFilter.GaussianBlur(radius=3))
            enhancer = ImageEnhance.Brightness(glow)
            glow = enhancer.enhance(style['glow_intensity'])
            
            # Composite with original
            result = Image.alpha_composite(glow, img)
            return result
        
        return img
    
    def _apply_advanced_effects(self, img: Image.Image, style: Dict) -> Image.Image:
        """Apply advanced visual effects for pro users"""
        # Multiple glow layers
        if style.get('glow_intensity', 0) > 0:
            # Inner glow
            inner_glow = img.filter(ImageFilter.GaussianBlur(radius=2))
            inner_enhancer = ImageEnhance.Brightness(inner_glow)
            inner_glow = inner_enhancer.enhance(style['glow_intensity'] * 0.8)
            
            # Outer glow
            outer_glow = img.filter(ImageFilter.GaussianBlur(radius=6))
            outer_enhancer = ImageEnhance.Brightness(outer_glow)
            outer_glow = outer_enhancer.enhance(style['glow_intensity'] * 0.4)
            
            # Composite layers
            result = Image.alpha_composite(outer_glow, inner_glow)
            result = Image.alpha_composite(result, img)
            
            # Enhance contrast
            contrast_enhancer = ImageEnhance.Contrast(result)
            result = contrast_enhancer.enhance(1.2)
            
            return result
        
        return img
    
    def _image_to_base64(self, img: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffer = BytesIO()
        
        # Resize if needed for web delivery
        if img.size[0] > 512:
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
        
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

# ===== FLASK ROUTES =====

# Initialize generator
generator = AdvancedSigilGenerator()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'sigilcraft-python-backend',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'advanced_generation': True,
            'multiple_vibes': True,
            'high_resolution': True,
            'sacred_geometry': True
        }
    })

@app.route('/generate', methods=['POST'])
def generate_sigil():
    """Enhanced sigil generation endpoint"""
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
        
        # Generate sigil
        logger.info(f"🎨 Generating sigil: '{phrase}' ({vibe}) [Advanced: {advanced}]")
        
        sigil_image = generator.generate_sigil(phrase, vibe, advanced)
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Sigil generated in {duration:.2f}s")
        
        return jsonify({
            'success': True,
            'image': sigil_image,
            'phrase': phrase,
            'vibe': vibe,
            'advanced': advanced,
            'metadata': {
                'generation_time': duration,
                'timestamp': datetime.now().isoformat(),
                'version': '2.0.0'
            },
            'message': f'Revolutionary sigil manifested for: "{phrase}"'
        })
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"❌ Generation failed after {duration:.2f}s: {e}")
        
        return jsonify({
            'success': False,
            'error': str(e),
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/vibes', methods=['GET'])
def get_available_vibes():
    """Get list of available energy vibes"""
    vibes = list(generator.vibe_styles.keys())
    
    return jsonify({
        'success': True,
        'vibes': vibes,
        'count': len(vibes),
        'descriptions': {
            'mystical': 'Ancient wisdom & mystery',
            'cosmic': 'Universal connection',
            'elemental': 'Natural forces',
            'crystal': 'Clarity & healing',
            'shadow': 'Hidden power',
            'light': 'Pure radiance',
            'storm': 'Raw electric energy',
            'void': 'Infinite potential'
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'code': 404
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
    print("🔮 Starting Enhanced Sigilcraft Python Backend...")
    print(f"📦 PIL/Pillow version: {Image.__version__}")
    print(f"🔢 NumPy available: {'✅' if 'numpy' in sys.modules or 'np' in globals() else '❌'}")
    print("🎨 Advanced sigil generation ready!")
    
    # Get port from environment or default to 5001
    port = int(os.getenv('PORT', 5001))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting server on port {port}")
    print(f"🔧 Debug mode: {'ON' if debug_mode else 'OFF'}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        threaded=True
    )
