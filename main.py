
from flask import Flask, request, jsonify
try:
    from flask_cors import CORS
except ImportError:
    print("⚠️  flask-cors not installed, using basic CORS headers")
    CORS = None
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
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

# Configure CORS properly
if CORS:
    CORS(app, origins=["*"], allow_headers=["Content-Type", "Authorization", "X-Pro-Key"])
else:
    # Fallback CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Pro-Key')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

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
            error_msg = str(e)
            app.logger.error(f"Error in {f.__name__}: {error_msg}")
            app.logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                'success': False,
                'error': f'Generation failed: {error_msg}',
                'details': error_msg,
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

def generate_artistic_sigil(phrase, vibe='mystical'):
    """Generate a truly artistic and unique sigil with advanced algorithms"""
    # Create deterministic seed from phrase
    seed_string = f"{phrase.lower().strip()}-{vibe}"
    seed = int(hashlib.sha256(seed_string.encode()).hexdigest()[:8], 16)
    np.random.seed(seed)
    random.seed(seed)
    
    # High resolution for better quality
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # Create multiple drawing layers for complex composition
    base_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    geometry_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    energy_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    effect_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # Get vibe-specific artistic parameters
    vibe_config = get_vibe_artistic_config(vibe)
    
    # Generate phrase-specific characteristics for artistic variation
    phrase_energy = calculate_phrase_energy(phrase)
    
    # Layer 1: Mystical Background Patterns
    draw_mystical_background(ImageDraw.Draw(base_layer), size, vibe_config, phrase_energy)
    
    # Layer 2: Sacred Geometry Core
    draw_advanced_sacred_geometry(ImageDraw.Draw(geometry_layer), size, vibe_config, phrase_energy)
    
    # Layer 3: Phrase-Based Symbol System
    draw_phrase_symbols(ImageDraw.Draw(energy_layer), phrase, size, vibe_config)
    
    # Layer 4: Artistic Effects and Flourishes
    draw_artistic_effects(ImageDraw.Draw(effect_layer), size, vibe_config, phrase_energy)
    
    # Composite all layers with advanced blending
    img = Image.alpha_composite(img, base_layer)
    img = Image.alpha_composite(img, geometry_layer)
    img = Image.alpha_composite(img, energy_layer)
    img = Image.alpha_composite(img, effect_layer)
    
    # Apply vibe-specific post-processing
    img = apply_artistic_post_processing(img, vibe, phrase_energy)
    
    # Add final artistic touches
    img = add_mystical_aura(img, vibe_config)
    
    # Resize to optimal display size while maintaining quality
    img = img.resize((768, 768), Image.Resampling.LANCZOS)
    
    return img

def get_vibe_artistic_config(vibe):
    """Get comprehensive artistic configuration for each vibe"""
    configs = {
        'mystical': {
            'primary_colors': [(138, 43, 226, 200), (148, 0, 211, 180), (123, 104, 238, 160)],
            'accent_colors': [(255, 215, 0, 120), (255, 255, 255, 80)],
            'patterns': ['spirals', 'mandalas', 'runes'],
            'complexity': 0.8,
            'glow_intensity': 0.7,
            'sacred_symbols': ['pentagram', 'moon_phases', 'eye_of_horus'],
            'energy_flow': 'spiral',
            'texture': 'ethereal'
        },
        'cosmic': {
            'primary_colors': [(25, 25, 112, 200), (72, 61, 139, 180), (123, 104, 238, 160)],
            'accent_colors': [(255, 255, 255, 150), (0, 255, 255, 100)],
            'patterns': ['galaxies', 'constellations', 'nebulae'],
            'complexity': 0.9,
            'glow_intensity': 0.8,
            'sacred_symbols': ['star_patterns', 'planets', 'cosmic_eye'],
            'energy_flow': 'radial',
            'texture': 'starfield'
        },
        'elemental': {
            'primary_colors': [(139, 69, 19, 200), (160, 82, 45, 180), (205, 133, 63, 160)],
            'accent_colors': [(255, 140, 0, 120), (34, 139, 34, 100)],
            'patterns': ['flames', 'waves', 'crystals'],
            'complexity': 0.7,
            'glow_intensity': 0.6,
            'sacred_symbols': ['tree_of_life', 'elements', 'nature_spirits'],
            'energy_flow': 'organic',
            'texture': 'natural'
        },
        'crystal': {
            'primary_colors': [(176, 224, 230, 200), (173, 216, 230, 180), (135, 206, 235, 160)],
            'accent_colors': [(255, 255, 255, 180), (192, 192, 192, 120)],
            'patterns': ['fractals', 'prisms', 'geometric'],
            'complexity': 0.9,
            'glow_intensity': 0.9,
            'sacred_symbols': ['merkaba', 'crystal_grid', 'platonic_solids'],
            'energy_flow': 'crystalline',
            'texture': 'prismatic'
        },
        'shadow': {
            'primary_colors': [(47, 47, 47, 200), (69, 69, 69, 180), (105, 105, 105, 160)],
            'accent_colors': [(128, 0, 128, 150), (139, 0, 0, 120)],
            'patterns': ['smoke', 'shadows', 'void'],
            'complexity': 0.6,
            'glow_intensity': 0.5,
            'sacred_symbols': ['ouroboros', 'eclipse', 'void_sigils'],
            'energy_flow': 'flowing',
            'texture': 'misty'
        },
        'light': {
            'primary_colors': [(255, 248, 220, 200), (255, 250, 205, 180), (255, 255, 240, 160)],
            'accent_colors': [(255, 215, 0, 180), (255, 255, 255, 200)],
            'patterns': ['rays', 'halos', 'divine'],
            'complexity': 0.8,
            'glow_intensity': 1.0,
            'sacred_symbols': ['sun_symbols', 'angels', 'divine_geometry'],
            'energy_flow': 'radiant',
            'texture': 'luminous'
        }
    }
    return configs.get(vibe, configs['mystical'])

def calculate_phrase_energy(phrase):
    """Calculate unique energy signature from phrase for artistic variation"""
    energy = {}
    
    # Character frequency analysis
    char_freq = {}
    for char in phrase.lower():
        if char.isalpha():
            char_freq[char] = char_freq.get(char, 0) + 1
    
    # Calculate energy metrics
    energy['vowel_ratio'] = sum(1 for c in phrase.lower() if c in 'aeiou') / max(len(phrase), 1)
    energy['consonant_complexity'] = len(set(c for c in phrase.lower() if c.isalpha() and c not in 'aeiou'))
    energy['phrase_harmony'] = sum(ord(c) for c in phrase) % 360  # For rotation angles
    energy['sacred_number'] = len(phrase) % 12 + 1  # 1-12 sacred numerology
    energy['fibonacci_index'] = get_fibonacci_position(len(phrase))
    energy['golden_ratio'] = (len(phrase) * 1.618) % 360
    
    return energy

def get_fibonacci_position(n):
    """Get position in Fibonacci sequence for sacred geometry"""
    fib = [1, 1]
    while fib[-1] < n:
        fib.append(fib[-1] + fib[-2])
    return len(fib) % 8

def draw_mystical_background(draw, size, config, phrase_energy):
    """Draw complex mystical background patterns"""
    center = size // 2
    
    # Create mystical energy field
    for ring in range(5):
        radius = size // 8 + ring * size // 12
        alpha = max(30, 120 - ring * 20)
        
        # Energy rings with phrase-specific distortion
        distortion = phrase_energy['phrase_harmony'] + ring * 30
        for angle in range(0, 360, 5):
            angle_rad = math.radians(angle + distortion)
            inner_radius = radius - 5
            outer_radius = radius + 5
            
            x1 = center + int(inner_radius * math.cos(angle_rad))
            y1 = center + int(inner_radius * math.sin(angle_rad))
            x2 = center + int(outer_radius * math.cos(angle_rad))
            y2 = center + int(outer_radius * math.sin(angle_rad))
            
            color = (*config['primary_colors'][ring % len(config['primary_colors'])][:3], alpha)
            draw.line([x1, y1, x2, y2], fill=color, width=2)

def draw_advanced_sacred_geometry(draw, size, config, phrase_energy):
    """Draw complex sacred geometry patterns"""
    center = size // 2
    golden_ratio = 1.618033988749895
    
    # Sacred polygons based on phrase energy
    sides_list = [phrase_energy['sacred_number'], phrase_energy['sacred_number'] + 3, phrase_energy['sacred_number'] + 6]
    
    for i, sides in enumerate(sides_list):
        radius = size // 6 + i * size // 12
        rotation = phrase_energy['golden_ratio'] + i * 45
        
        points = []
        for j in range(sides):
            angle = (2 * math.pi * j / sides) + math.radians(rotation)
            x = center + int(radius * math.cos(angle))
            y = center + int(radius * math.sin(angle))
            points.append((x, y))
        
        # Draw sacred polygon
        if len(points) > 2:
            color = (*config['primary_colors'][i % len(config['primary_colors'])][:3], 150)
            draw.polygon(points, outline=color, width=3)
            
            # Add inner sacred connections
            for k in range(0, len(points), 2):
                for l in range(k + 2, len(points), 3):
                    if l < len(points):
                        inner_color = (*config['accent_colors'][0][:3], 80)
                        draw.line([points[k], points[l]], fill=inner_color, width=1)

def draw_phrase_symbols(draw, phrase, size, config):
    """Generate unique symbols based on phrase characteristics"""
    center = size // 2
    
    # Convert phrase to symbol elements
    for i, char in enumerate(phrase.lower()):
        if char.isalpha():
            char_value = ord(char) - ord('a')
            
            # Position based on character
            angle = (char_value * 15 + i * 25) % 360
            distance = size // 8 + (char_value % 3) * size // 12
            
            x = center + int(distance * math.cos(math.radians(angle)))
            y = center + int(distance * math.sin(math.radians(angle)))
            
            # Draw character-specific symbol
            symbol_size = 20 + (char_value % 5) * 10
            symbol_type = char_value % 4
            
            color = (*config['primary_colors'][char_value % len(config['primary_colors'])][:3], 180)
            
            if symbol_type == 0:  # Circle
                draw.ellipse([x-symbol_size//2, y-symbol_size//2, x+symbol_size//2, y+symbol_size//2], 
                           outline=color, width=3)
            elif symbol_type == 1:  # Triangle
                points = [
                    (x, y - symbol_size//2),
                    (x - symbol_size//2, y + symbol_size//2),
                    (x + symbol_size//2, y + symbol_size//2)
                ]
                draw.polygon(points, outline=color, width=3)
            elif symbol_type == 2:  # Diamond
                points = [
                    (x, y - symbol_size//2),
                    (x + symbol_size//2, y),
                    (x, y + symbol_size//2),
                    (x - symbol_size//2, y)
                ]
                draw.polygon(points, outline=color, width=3)
            else:  # Cross
                draw.line([x - symbol_size//2, y, x + symbol_size//2, y], fill=color, width=3)
                draw.line([x, y - symbol_size//2, x, y + symbol_size//2], fill=color, width=3)

def draw_artistic_effects(draw, size, config, phrase_energy):
    """Add artistic flourishes and effects"""
    center = size // 2
    
    # Energy tendrils
    num_tendrils = phrase_energy['sacred_number']
    for i in range(num_tendrils):
        start_angle = (360 / num_tendrils) * i + phrase_energy['phrase_harmony']
        
        # Create flowing tendril
        points = []
        for step in range(20):
            progress = step / 19.0
            angle = math.radians(start_angle + progress * 720)  # 2 full rotations
            distance = size // 6 + progress * size // 4
            
            # Add organic variation
            wave = math.sin(progress * math.pi * 4) * 20
            x = center + int((distance + wave) * math.cos(angle))
            y = center + int((distance + wave) * math.sin(angle))
            points.append((x, y))
        
        # Draw tendril as connected lines
        for j in range(len(points) - 1):
            alpha = int(200 * (1 - j / len(points)))
            color = (*config['accent_colors'][0][:3], alpha)
            draw.line([points[j], points[j + 1]], fill=color, width=2)

def apply_artistic_post_processing(img, vibe, phrase_energy):
    """Apply vibe-specific artistic post-processing"""
    
    if vibe == 'mystical':
        # Add ethereal glow
        img = add_ethereal_glow(img, (138, 43, 226))
        img = add_particle_effects(img, 'stars')
        
    elif vibe == 'cosmic':
        # Add cosmic effects
        img = add_starfield_background(img)
        img = add_nebula_effect(img)
        
    elif vibe == 'elemental':
        # Add natural textures
        img = add_organic_texture(img)
        img = add_energy_wisps(img, (139, 69, 19))
        
    elif vibe == 'crystal':
        # Add crystalline effects
        img = add_prismatic_effect(img)
        img = add_crystal_fractals(img)
        
    elif vibe == 'shadow':
        # Add shadow effects
        img = add_smoke_wisps(img)
        img = add_dark_energy(img)
        
    elif vibe == 'light':
        # Add divine light effects
        img = add_divine_rays(img)
        img = add_golden_particles(img)
    
    return img

def add_ethereal_glow(img, glow_color):
    """Add ethereal glow effect"""
    # Create glow layer
    glow = img.copy()
    glow = glow.filter(ImageFilter.GaussianBlur(radius=8))
    
    # Enhance the glow
    enhancer = ImageEnhance.Brightness(glow)
    glow = enhancer.enhance(1.8)
    
    # Tint with glow color
    overlay = Image.new('RGBA', glow.size, (*glow_color, 60))
    glow = Image.blend(glow.convert('RGBA'), overlay, 0.3)
    
    # Composite with original
    return Image.alpha_composite(img, glow)

def add_particle_effects(img, particle_type='stars'):
    """Add particle effects"""
    draw = ImageDraw.Draw(img)
    
    for _ in range(50):
        x = random.randint(0, img.width)
        y = random.randint(0, img.height)
        size = random.randint(2, 8)
        
        if particle_type == 'stars':
            # Draw star-like particles
            color = (255, 255, 255, random.randint(100, 200))
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=color)
            
            # Add cross pattern for star effect
            draw.line([x-size, y, x+size, y], fill=color, width=1)
            draw.line([x, y-size, x, y+size], fill=color, width=1)
    
    return img

def add_starfield_background(img):
    """Add cosmic starfield"""
    draw = ImageDraw.Draw(img)
    
    for _ in range(200):
        x = random.randint(0, img.width)
        y = random.randint(0, img.height)
        brightness = random.randint(50, 255)
        size = random.choice([1, 1, 1, 2, 2, 3])  # Mostly small stars
        
        color = (brightness, brightness, brightness, random.randint(80, 180))
        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
    
    return img

def add_nebula_effect(img):
    """Add nebula-like clouds"""
    # This would require more advanced image processing
    # For now, add cosmic color gradients
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    center_x, center_y = img.width // 2, img.height // 2
    
    for ring in range(5):
        radius = img.width // 8 + ring * img.width // 16
        alpha = max(20, 80 - ring * 15)
        
        colors = [(72, 61, 139, alpha), (123, 104, 238, alpha), (25, 25, 112, alpha)]
        color = colors[ring % len(colors)]
        
        draw.ellipse([center_x - radius, center_y - radius, 
                     center_x + radius, center_y + radius], 
                    outline=color, width=3)
    
    return Image.alpha_composite(img, overlay)

def add_organic_texture(img):
    """Add natural, organic texture"""
    # Create organic flowing patterns
    draw = ImageDraw.Draw(img)
    
    for _ in range(30):
        # Create organic flowing lines
        start_x = random.randint(0, img.width)
        start_y = random.randint(0, img.height)
        
        points = [(start_x, start_y)]
        for step in range(20):
            last_x, last_y = points[-1]
            angle = random.uniform(0, 2 * math.pi)
            distance = random.randint(5, 25)
            
            new_x = last_x + int(distance * math.cos(angle))
            new_y = last_y + int(distance * math.sin(angle))
            
            # Keep within bounds
            new_x = max(0, min(img.width, new_x))
            new_y = max(0, min(img.height, new_y))
            
            points.append((new_x, new_y))
        
        # Draw organic line
        for i in range(len(points) - 1):
            alpha = int(150 * (1 - i / len(points)))
            color = (160, 82, 45, alpha)
            draw.line([points[i], points[i + 1]], fill=color, width=2)
    
    return img

def add_energy_wisps(img, base_color):
    """Add energy wisp effects"""
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = img.width // 2, img.height // 2
    
    for _ in range(15):
        # Create wisp starting from center area
        start_angle = random.uniform(0, 2 * math.pi)
        start_distance = random.randint(50, img.width // 4)
        
        x = center_x + int(start_distance * math.cos(start_angle))
        y = center_y + int(start_distance * math.sin(start_angle))
        
        # Create wisp trail
        for step in range(25):
            progress = step / 24.0
            
            # Wisp movement with natural curve
            angle = start_angle + progress * math.pi + math.sin(progress * math.pi * 3) * 0.5
            distance = start_distance + progress * img.width // 3
            
            new_x = center_x + int(distance * math.cos(angle))
            new_y = center_y + int(distance * math.sin(angle))
            
            # Keep within bounds
            if 0 <= new_x < img.width and 0 <= new_y < img.height:
                alpha = int(180 * (1 - progress) * 0.7)
                size = max(1, int(8 * (1 - progress)))
                
                color = (*base_color, alpha)
                draw.ellipse([new_x - size, new_y - size, 
                             new_x + size, new_y + size], fill=color)
    
    return img

def add_prismatic_effect(img):
    """Add crystal prismatic effects"""
    # Create prismatic light splits
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = img.width // 2, img.height // 2
    
    # Add prismatic rays
    for i in range(12):
        angle = (360 / 12) * i
        angle_rad = math.radians(angle)
        
        # Create prismatic ray with rainbow colors
        colors = [
            (255, 0, 0, 100),    # Red
            (255, 127, 0, 100),  # Orange
            (255, 255, 0, 100),  # Yellow
            (0, 255, 0, 100),    # Green
            (0, 0, 255, 100),    # Blue
            (75, 0, 130, 100),   # Indigo
            (148, 0, 211, 100)   # Violet
        ]
        
        color = colors[i % len(colors)]
        
        # Draw prismatic ray
        for width_offset in range(-2, 3):
            start_x = center_x + int(50 * math.cos(angle_rad))
            start_y = center_y + int(50 * math.sin(angle_rad))
            end_x = center_x + int(200 * math.cos(angle_rad)) + width_offset * 5
            end_y = center_y + int(200 * math.sin(angle_rad))
            
            draw.line([start_x, start_y, end_x, end_y], fill=color, width=2)
    
    return img

def add_crystal_fractals(img):
    """Add crystalline fractal patterns"""
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = img.width // 2, img.height // 2
    
    def draw_crystal_branch(x, y, angle, length, depth):
        if depth <= 0 or length < 5:
            return
        
        # Calculate end point
        end_x = x + int(length * math.cos(angle))
        end_y = y + int(length * math.sin(angle))
        
        # Draw branch
        alpha = min(255, int(200 * (depth / 4)))
        color = (176, 224, 230, alpha)
        draw.line([x, y, end_x, end_y], fill=color, width=max(1, depth))
        
        # Draw crystal nodes
        node_size = depth * 2
        draw.ellipse([end_x - node_size, end_y - node_size, 
                     end_x + node_size, end_y + node_size], 
                    fill=(255, 255, 255, alpha // 2))
        
        # Recursive branches
        branch_angle1 = angle + math.pi / 4
        branch_angle2 = angle - math.pi / 4
        new_length = length * 0.7
        
        draw_crystal_branch(end_x, end_y, branch_angle1, new_length, depth - 1)
        draw_crystal_branch(end_x, end_y, branch_angle2, new_length, depth - 1)
    
    # Draw crystal fractal trees
    for i in range(6):
        start_angle = (2 * math.pi / 6) * i
        draw_crystal_branch(center_x, center_y, start_angle, 80, 4)
    
    return img

def add_smoke_wisps(img):
    """Add smoky shadow effects"""
    draw = ImageDraw.Draw(img)
    
    for _ in range(20):
        # Random starting point
        x = random.randint(0, img.width)
        y = random.randint(img.height // 2, img.height)
        
        # Create upward flowing smoke
        points = [(x, y)]
        
        for step in range(30):
            last_x, last_y = points[-1]
            
            # Smoke rises and disperses
            new_x = last_x + random.randint(-15, 15)
            new_y = last_y - random.randint(5, 20)
            
            # Add some horizontal drift
            new_x += int(step * 0.5 * random.choice([-1, 1]))
            
            # Keep within bounds
            new_x = max(0, min(img.width, new_x))
            new_y = max(0, min(img.height, new_y))
            
            points.append((new_x, new_y))
        
        # Draw smoke trail
        for i in range(len(points) - 1):
            progress = i / len(points)
            alpha = int(120 * (1 - progress) * 0.6)
            width = max(1, int(8 * (1 - progress)))
            
            color = (105, 105, 105, alpha)
            draw.line([points[i], points[i + 1]], fill=color, width=width)
    
    return img

def add_dark_energy(img):
    """Add dark shadow energy effects"""
    # Create dark energy vortexes
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = img.width // 2, img.height // 2
    
    for spiral in range(3):
        spiral_center_x = center_x + random.randint(-100, 100)
        spiral_center_y = center_y + random.randint(-100, 100)
        
        # Create dark energy spiral
        for i in range(50):
            progress = i / 49.0
            angle = progress * 4 * math.pi  # 2 full rotations
            radius = progress * 120
            
            x = spiral_center_x + int(radius * math.cos(angle))
            y = spiral_center_y + int(radius * math.sin(angle))
            
            if 0 <= x < img.width and 0 <= y < img.height:
                alpha = int(150 * (1 - progress) * 0.8)
                size = max(1, int(6 * (1 - progress)))
                
                color = (47, 47, 47, alpha)
                draw.ellipse([x - size, y - size, x + size, y + size], fill=color)
    
    return img

def add_divine_rays(img):
    """Add divine light rays"""
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = img.width // 2, img.height // 2
    
    # Create divine light rays emanating from center
    for i in range(16):
        angle = (2 * math.pi / 16) * i
        
        # Create light ray with varying intensity
        for distance in range(0, img.width // 2, 10):
            x = center_x + int(distance * math.cos(angle))
            y = center_y + int(distance * math.sin(angle))
            
            if 0 <= x < img.width and 0 <= y < img.height:
                # Light fades with distance
                alpha = max(20, int(200 * (1 - distance / (img.width // 2))))
                width = max(1, int(8 * (1 - distance / (img.width // 2))))
                
                # Golden divine light
                color = (255, 215, 0, alpha)
                
                # Draw ray segment
                next_x = center_x + int((distance + 10) * math.cos(angle))
                next_y = center_y + int((distance + 10) * math.sin(angle))
                
                if 0 <= next_x < img.width and 0 <= next_y < img.height:
                    draw.line([x, y, next_x, next_y], fill=color, width=width)
    
    return img

def add_golden_particles(img):
    """Add golden light particles"""
    draw = ImageDraw.Draw(img)
    
    # Add floating golden particles
    for _ in range(80):
        x = random.randint(0, img.width)
        y = random.randint(0, img.height)
        
        # Various sizes for depth
        size = random.choice([2, 3, 4, 5, 6])
        alpha = random.randint(120, 255)
        
        # Golden colors with variation
        gold_variations = [
            (255, 215, 0, alpha),
            (255, 223, 0, alpha),
            (255, 255, 224, alpha),
            (255, 248, 220, alpha)
        ]
        
        color = random.choice(gold_variations)
        
        # Draw particle with subtle glow
        draw.ellipse([x - size, y - size, x + size, y + size], fill=color)
        
        # Add subtle cross pattern for sparkle effect
        if size >= 4:
            sparkle_color = (255, 255, 255, alpha // 2)
            draw.line([x - size - 2, y, x + size + 2, y], fill=sparkle_color, width=1)
            draw.line([x, y - size - 2, x, y + size + 2], fill=sparkle_color, width=1)
    
    return img

def add_mystical_aura(img, config):
    """Add final mystical aura effect"""
    # Create soft outer glow
    glow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_layer)
    
    center_x, center_y = img.width // 2, img.height // 2
    
    # Multi-layered aura
    for ring in range(5):
        radius = img.width // 3 + ring * 30
        alpha = max(10, 50 - ring * 8)
        
        # Use primary color for aura
        aura_color = (*config['primary_colors'][0][:3], alpha)
        
        # Draw aura ring
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius],
                    outline=aura_color, width=15 - ring * 2)
    
    # Blur the aura
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=20))
    
    # Composite with main image
    return Image.alpha_composite(glow_layer, img)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'Flask backend running',
        'message': 'Enhanced artistic sigil generation service active',
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light'],
        'version': '10.0 - Artistic Mastery'
    })

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify server is working"""
    return jsonify({
        'status': 'ok',
        'message': 'Enhanced artistic server is working',
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light'],
        'version': '10.0'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'server': 'online',
        'version': 'Artistic Mastery 10.0',
        'timestamp': str(datetime.now())
    })

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint with detailed information"""
    return jsonify({
        'status': 'operational',
        'server': 'Enhanced Artistic Sigil Generator',
        'version': '10.0',
        'features': [
            'Advanced sacred geometry',
            'Vibe-specific artistic algorithms', 
            'Phrase-energy calculation',
            'Multi-layered composition',
            'Complex post-processing effects',
            'Truly unique artistic results'
        ],
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light'],
        'endpoints': ['/generate', '/test', '/health', '/status']
    })

@app.route('/generate', methods=['POST'])
@handle_errors
def generate_sigil():
    """Generate an artistic sigil based on phrase and vibe"""
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

        print(f"🎨 Generating artistic sigil for: '{phrase}' with vibe: {vibe}")

        # Generate the enhanced artistic sigil
        sigil_img = generate_artistic_sigil(phrase, vibe)

        # Convert to base64
        buffer = io.BytesIO()
        sigil_img.save(buffer, format='PNG', optimize=True, quality=95)
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        image_data_url = f"data:image/png;base64,{image_base64}"

        print(f"✅ Artistic sigil generated successfully (Enhanced 10x)")

        return jsonify({
            'success': True,
            'image': image_data_url,
            'phrase': phrase,
            'vibe': vibe,
            'version': 'Artistic Mastery 10.0',
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

    print(f"🚀 Starting Enhanced Artistic Sigil Generator on port {port}...")

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
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        print("🔄 Falling back to Flask dev server...")
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
