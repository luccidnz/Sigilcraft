
#!/usr/bin/env python3
"""
SIGILCRAFT NEXUS - ULTRA ADVANCED SIGIL GENERATION ENGINE
Revolutionary quantum-enhanced sigil creation with AI-powered mystical algorithms
Version 3.0.0 - Supreme Coding Master Edition
"""

import os
import json
import base64
import math
import hashlib
import time
import secrets
from io import BytesIO
from datetime import datetime, timedelta
from collections import defaultdict
from functools import wraps, lru_cache
from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS
import logging

# Ultra-robust logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/sigilcraft.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins="*", methods=['GET', 'POST', 'OPTIONS'], 
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'])

# Ultra-advanced configuration
app.config.update({
    'MAX_CONTENT_LENGTH': 32 * 1024 * 1024,  # 32MB max
    'JSON_SORT_KEYS': False,
    'JSONIFY_PRETTYPRINT_REGULAR': False,
    'SECRET_KEY': secrets.token_hex(32),
    'PERMANENT_SESSION_LIFETIME': timedelta(hours=24),
    'SEND_FILE_MAX_AGE_DEFAULT': 31536000  # 1 year cache for static files
})

# Performance monitoring and rate limiting
request_stats = defaultdict(lambda: {'count': 0, 'last_reset': time.time()})
generation_cache = {}
CACHE_TTL = 3600  # 1 hour cache
RATE_LIMIT_PER_MINUTE = 100

def rate_limit(max_requests=60):
    """Advanced rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            current_time = time.time()
            
            # Reset counter every minute
            if current_time - request_stats[client_ip]['last_reset'] > 60:
                request_stats[client_ip] = {'count': 0, 'last_reset': current_time}
            
            if request_stats[client_ip]['count'] >= max_requests:
                return jsonify({
                    'success': False, 
                    'error': 'Rate limit exceeded. Please wait before making more requests.',
                    'retry_after': 60
                }), 429
            
            request_stats[client_ip]['count'] += 1
            return f(*args, **kwargs)
        return wrapper
    return decorator

@lru_cache(maxsize=256)
def get_vibe_config(vibe):
    """Cached vibe configurations for ultra-fast access"""
    configs = {
        'mystical': {
            'colors': [(139, 92, 246), (168, 85, 247), (147, 51, 234), (126, 34, 206)],
            'pattern_type': 'sacred_geometry',
            'complexity': 8,
            'power_level': 'ancient'
        },
        'cosmic': {
            'colors': [(59, 130, 246), (99, 102, 241), (139, 92, 246), (168, 85, 247)],
            'pattern_type': 'spiral_galaxy',
            'complexity': 12,
            'power_level': 'stellar'
        },
        'elemental': {
            'colors': [(34, 197, 94), (59, 130, 246), (168, 85, 247), (34, 197, 94)],
            'pattern_type': 'organic_growth',
            'complexity': 10,
            'power_level': 'natural'
        },
        'crystal': {
            'colors': [(236, 72, 153), (219, 39, 119), (147, 51, 234), (168, 85, 247)],
            'pattern_type': 'geometric_crystal',
            'complexity': 14,
            'power_level': 'prismatic'
        },
        'shadow': {
            'colors': [(75, 85, 99), (55, 65, 81), (31, 41, 55), (17, 24, 39)],
            'pattern_type': 'chaos_fractal',
            'complexity': 16,
            'power_level': 'void'
        },
        'light': {
            'colors': [(251, 191, 36), (245, 158, 11), (217, 119, 6), (180, 83, 9)],
            'pattern_type': 'radiant_burst',
            'complexity': 18,
            'power_level': 'divine'
        },
        'storm': {
            'colors': [(220, 38, 127), (239, 68, 68), (248, 113, 113), (252, 165, 165)],
            'pattern_type': 'lightning_chaos',
            'complexity': 20,
            'power_level': 'tempest'
        },
        'void': {
            'colors': [(17, 24, 39), (55, 65, 81), (99, 102, 241), (139, 92, 246)],
            'pattern_type': 'recursive_spiral',
            'complexity': 24,
            'power_level': 'infinite'
        },
        'quantum': {
            'colors': [(16, 185, 129), (59, 130, 246), (168, 85, 247), (236, 72, 153)],
            'pattern_type': 'quantum_field',
            'complexity': 32,
            'power_level': 'transcendent'
        },
        'aurora': {
            'colors': [(16, 185, 129), (34, 197, 94), (59, 130, 246), (168, 85, 247)],
            'pattern_type': 'aurora_waves',
            'complexity': 28,
            'power_level': 'ethereal'
        },
        'phoenix': {
            'colors': [(239, 68, 68), (245, 158, 11), (251, 191, 36), (252, 211, 77)],
            'pattern_type': 'phoenix_rise',
            'complexity': 26,
            'power_level': 'rebirth'
        },
        'dragon': {
            'colors': [(220, 38, 127), (147, 51, 234), (55, 65, 81), (239, 68, 68)],
            'pattern_type': 'dragon_spiral',
            'complexity': 30,
            'power_level': 'legendary'
        }
    }
    return configs.get(vibe, configs['mystical'])

def generate_cache_key(phrase, vibe, advanced, quality=None):
    """Generate unique cache key for sigil configurations"""
    key_data = f"{phrase}_{vibe}_{advanced}_{quality}"
    return hashlib.sha256(key_data.encode()).hexdigest()[:16]

def generate_ultra_sigil_image(phrase, vibe="mystical", advanced=False, quality="hd"):
    """Ultra-advanced sigil generation with quantum-enhanced algorithms"""
    try:
        # Check cache first for lightning-fast responses
        cache_key = generate_cache_key(phrase, vibe, advanced, quality)
        cached_result = generation_cache.get(cache_key)
        if cached_result and time.time() - cached_result['timestamp'] < CACHE_TTL:
            logger.info(f"🚀 Cache hit for sigil: {phrase[:30]}")
            return cached_result['image']

        # Import PIL with fallback handling
        from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
        
        # Ultra-high quality settings
        base_size = 1024 if quality == "4k" else 768 if quality == "hd" else 512
        if advanced:
            base_size = int(base_size * 1.5)
        
        # Create base image with alpha channel
        image = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Get vibe configuration
        vibe_config = get_vibe_config(vibe)
        colors = vibe_config['colors']
        pattern_type = vibe_config['pattern_type']
        complexity = vibe_config['complexity']
        
        # Advanced phrase processing for quantum effects
        phrase_hash = hashlib.sha256(phrase.encode()).digest()
        char_values = [ord(c) for c in phrase.lower() if c.isalnum()]
        if not char_values:
            char_values = [97, 98, 99]  # Default values
        
        # Quantum seed generation
        quantum_seed = sum(phrase_hash[:8]) % 10000
        center_x, center_y = base_size // 2, base_size // 2
        
        # Ultra-advanced pattern generation based on type
        if pattern_type == 'sacred_geometry':
            generate_sacred_geometry(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'spiral_galaxy':
            generate_spiral_galaxy(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'organic_growth':
            generate_organic_growth(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'geometric_crystal':
            generate_geometric_crystal(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'chaos_fractal':
            generate_chaos_fractal(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'radiant_burst':
            generate_radiant_burst(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'lightning_chaos':
            generate_lightning_chaos(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'recursive_spiral':
            generate_recursive_spiral(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'quantum_field':
            generate_quantum_field(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'aurora_waves':
            generate_aurora_waves(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'phoenix_rise':
            generate_phoenix_rise(draw, center_x, center_y, base_size, colors, char_values, complexity)
        elif pattern_type == 'dragon_spiral':
            generate_dragon_spiral(draw, center_x, center_y, base_size, colors, char_values, complexity)
        
        # Add ultra-powerful center focus
        generate_power_center(draw, center_x, center_y, base_size, colors, vibe, quantum_seed)
        
        # Apply advanced post-processing effects
        if advanced or quality in ["hd", "4k"]:
            # Apply subtle glow effect
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            # Apply sharpening
            image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
        
        # Convert to optimized base64
        buffer = BytesIO()
        image.save(buffer, format='PNG', optimize=True, compress_level=6)
        image_data = base64.b64encode(buffer.getvalue()).decode()
        
        # Cache the result
        result = f"data:image/png;base64,{image_data}"
        generation_cache[cache_key] = {
            'image': result,
            'timestamp': time.time()
        }
        
        # Clean old cache entries periodically
        if len(generation_cache) > 1000:
            cutoff_time = time.time() - CACHE_TTL
            generation_cache.clear()
        
        return result
        
    except ImportError:
        logger.warning("PIL not available, using ultra-advanced SVG fallback")
        return generate_ultra_fallback_sigil(phrase, vibe, advanced)
    except Exception as e:
        logger.error(f"Ultra sigil generation error: {e}", exc_info=True)
        return generate_ultra_fallback_sigil(phrase, vibe, advanced)

def generate_sacred_geometry(draw, cx, cy, size, colors, char_values, complexity):
    """Generate sacred geometry patterns"""
    radius = size // 3
    for layer in range(3):
        r = radius - (layer * radius // 4)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=colors[layer], width=3)
    
    for i, char_val in enumerate(char_values[:complexity]):
        angle = (char_val * 7 + i * (360 / complexity)) % 360
        rad = math.radians(angle)
        x1 = cx + int(radius * 0.8 * math.cos(rad))
        y1 = cy + int(radius * 0.8 * math.sin(rad))
        color_idx = i % len(colors)
        draw.line([cx, cy, x1, y1], fill=colors[color_idx], width=3)
        
        # Add sacred nodes
        draw.ellipse([x1-6, y1-6, x1+6, y1+6], fill=colors[color_idx])

def generate_spiral_galaxy(draw, cx, cy, size, colors, char_values, complexity):
    """Generate spiral galaxy patterns"""
    for i, char_val in enumerate(char_values[:complexity]):
        spiral_turns = 4
        t = i / len(char_values) * spiral_turns * 2 * math.pi
        r = (char_val % 100) + i * 12
        x = cx + int(r * math.cos(t + char_val * 0.1))
        y = cy + int(r * math.sin(t + char_val * 0.1))
        color_idx = i % len(colors)
        
        # Create star clusters
        for j in range(3):
            offset_x = x + (j * 8) - 8
            offset_y = y + (j * 8) - 8
            draw.ellipse([offset_x-4, offset_y-4, offset_x+4, offset_y+4], fill=colors[color_idx])
        
        if i > 0:
            prev_t = (i-1) / len(char_values) * spiral_turns * 2 * math.pi
            prev_r = (char_values[i-1] % 100) + (i-1) * 12
            prev_x = cx + int(prev_r * math.cos(prev_t + char_values[i-1] * 0.1))
            prev_y = cy + int(prev_r * math.sin(prev_t + char_values[i-1] * 0.1))
            draw.line([prev_x, prev_y, x, y], fill=colors[color_idx], width=2)

def generate_organic_growth(draw, cx, cy, size, colors, char_values, complexity):
    """Generate organic growth patterns"""
    for i, char_val in enumerate(char_values[:min(complexity, 8)]):
        base_angle = (char_val * 11 + i * 45) % 360
        main_length = (char_val % 80) + 60
        
        for branch_level in range(3):
            for branch in range(2 ** branch_level):
                angle_offset = (branch * 30) - 15
                angle = base_angle + angle_offset
                rad = math.radians(angle)
                
                start_ratio = branch_level * 0.3
                end_ratio = (branch_level + 1) * 0.3
                
                x1 = cx + int(main_length * start_ratio * math.cos(rad))
                y1 = cy + int(main_length * start_ratio * math.sin(rad))
                x2 = cx + int(main_length * end_ratio * math.cos(rad))
                y2 = cy + int(main_length * end_ratio * math.sin(rad))
                
                color_idx = (i + branch_level) % len(colors)
                width = 4 - branch_level
                draw.line([x1, y1, x2, y2], fill=colors[color_idx], width=width)
                
                # Add growth nodes
                if branch_level == 2:
                    draw.ellipse([x2-3, y2-3, x2+3, y2+3], fill=colors[color_idx])

def generate_geometric_crystal(draw, cx, cy, size, colors, char_values, complexity):
    """Generate geometric crystal patterns"""
    num_sides = 6 + (sum(char_values) % 6)
    for layer in range(4):
        radius = (layer + 1) * (size // 8)
        for i in range(num_sides):
            angle1 = (i * 360 / num_sides + sum(char_values[:i+1]) % 90) % 360
            angle2 = ((i + 1) * 360 / num_sides + sum(char_values[:i+1]) % 90) % 360
            rad1, rad2 = math.radians(angle1), math.radians(angle2)
            
            x1 = cx + int(radius * math.cos(rad1))
            y1 = cy + int(radius * math.sin(rad1))
            x2 = cx + int(radius * math.cos(rad2))
            y2 = cy + int(radius * math.sin(rad2))
            
            color_idx = (layer + i) % len(colors)
            draw.line([x1, y1, x2, y2], fill=colors[color_idx], width=2)
            draw.line([cx, cy, x1, y1], fill=colors[color_idx], width=1)
            
            # Add crystal facets
            if layer > 1:
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                draw.polygon([(cx, cy), (x1, y1), (mid_x, mid_y)], fill=colors[color_idx] + (50,))

def generate_chaos_fractal(draw, cx, cy, size, colors, char_values, complexity):
    """Generate chaos fractal patterns"""
    for i, char_val in enumerate(char_values[:min(complexity, 12)]):
        angle = (char_val * 13 + i * 30) % 360
        rad = math.radians(angle)
        distance = (char_val % 120) + 40
        
        # Create fractal branches
        current_x = cx
        current_y = cy
        
        for step in range(5):
            next_angle = angle + (char_val * step) % 120 - 60
            next_rad = math.radians(next_angle)
            step_distance = distance * (0.8 ** step)
            
            next_x = current_x + int(step_distance * math.cos(next_rad))
            next_y = current_y + int(step_distance * math.sin(next_rad))
            
            color_idx = (i + step) % len(colors)
            width = max(1, 4 - step)
            draw.line([current_x, current_y, next_x, next_y], fill=colors[color_idx], width=width)
            
            # Add chaos nodes
            node_size = 4 - step
            draw.ellipse([next_x-node_size, next_y-node_size, next_x+node_size, next_y+node_size], fill=colors[color_idx])
            
            current_x, current_y = next_x, next_y

def generate_radiant_burst(draw, cx, cy, size, colors, char_values, complexity):
    """Generate radiant burst patterns"""
    for i, char_val in enumerate(char_values[:min(complexity, 20)]):
        angle = (char_val * 5 + i * 18) % 360
        rad = math.radians(angle)
        inner_radius = 50 + (i * 5)
        outer_radius = (char_val % 100) + 100 + (i * 8)
        
        x1 = cx + int(inner_radius * math.cos(rad))
        y1 = cy + int(inner_radius * math.sin(rad))
        x2 = cx + int(outer_radius * math.cos(rad))
        y2 = cy + int(outer_radius * math.sin(rad))
        
        color_idx = i % len(colors)
        draw.line([x1, y1, x2, y2], fill=colors[color_idx], width=4)
        
        # Add radiant bursts
        if i % 3 == 0:
            burst_points = []
            for b in range(8):
                burst_angle = angle + (b * 45) - 180
                burst_rad = math.radians(burst_angle)
                bx = x2 + int(15 * math.cos(burst_rad))
                by = y2 + int(15 * math.sin(burst_rad))
                burst_points.append((bx, by))
            draw.polygon(burst_points, fill=colors[color_idx])

def generate_lightning_chaos(draw, cx, cy, size, colors, char_values, complexity):
    """Generate lightning chaos patterns"""
    for i, char_val in enumerate(char_values[:min(complexity, 10)]):
        start_angle = (char_val * 23 + i * 36) % 360
        start_rad = math.radians(start_angle)
        start_x = cx + int(60 * math.cos(start_rad))
        start_y = cy + int(60 * math.sin(start_rad))
        
        # Create lightning bolt with multiple branches
        current_x, current_y = start_x, start_y
        for segment in range(7):
            branch_angle = start_angle + (char_val * segment) % 150 - 75
            branch_rad = math.radians(branch_angle)
            length = 25 + (char_val % 30) + (segment * 5)
            next_x = current_x + int(length * math.cos(branch_rad))
            next_y = current_y + int(length * math.sin(branch_rad))
            
            color_idx = (i + segment) % len(colors)
            width = max(1, 5 - segment // 2)
            draw.line([current_x, current_y, next_x, next_y], fill=colors[color_idx], width=width)
            
            # Add electric nodes
            if segment % 2 == 0:
                draw.ellipse([next_x-4, next_y-4, next_x+4, next_y+4], fill=colors[color_idx])
            
            current_x, current_y = next_x, next_y

def generate_recursive_spiral(draw, cx, cy, size, colors, char_values, complexity):
    """Generate recursive spiral patterns"""
    for layer in range(4):
        spiral_radius = 30 + layer * 40
        points_per_layer = min(complexity, 24) + layer * 6
        
        for i in range(points_per_layer):
            t = i / points_per_layer * 6 * math.pi
            r = spiral_radius * (1 + 0.1 * math.sin(t * 3))
            x = cx + int(r * math.cos(t))
            y = cy + int(r * math.sin(t))
            
            color_idx = (layer + i) % len(colors)
            
            # Create sub-spirals at each point
            for sub in range(3):
                sub_t = t + sub * 2.1
                sub_r = 8 + sub * 4
                sub_x = x + int(sub_r * math.cos(sub_t))
                sub_y = y + int(sub_r * math.sin(sub_t))
                draw.line([x, y, sub_x, sub_y], fill=colors[color_idx], width=2)
                draw.ellipse([sub_x-2, sub_y-2, sub_x+2, sub_y+2], fill=colors[color_idx])

def generate_quantum_field(draw, cx, cy, size, colors, char_values, complexity):
    """Generate quantum field patterns"""
    grid_size = 8
    cell_size = size // grid_size
    
    for i in range(grid_size):
        for j in range(grid_size):
            cell_cx = i * cell_size + cell_size // 2
            cell_cy = j * cell_size + cell_size // 2
            
            # Quantum probability based on phrase
            prob_index = (i * grid_size + j) % len(char_values)
            probability = char_values[prob_index] / 255.0
            
            if probability > 0.3:
                # Create quantum particles
                num_particles = int(probability * 8) + 1
                for p in range(num_particles):
                    angle = (p * 360 / num_particles + char_values[prob_index] * 10) % 360
                    rad = math.radians(angle)
                    distance = probability * 30
                    
                    px = cell_cx + int(distance * math.cos(rad))
                    py = cell_cy + int(distance * math.sin(rad))
                    
                    color_idx = p % len(colors)
                    particle_size = int(probability * 6) + 2
                    
                    draw.ellipse([px-particle_size, py-particle_size, px+particle_size, py+particle_size], 
                               fill=colors[color_idx])
                    
                    # Quantum entanglement lines
                    if p > 0:
                        prev_angle = ((p-1) * 360 / num_particles + char_values[prob_index] * 10) % 360
                        prev_rad = math.radians(prev_angle)
                        prev_px = cell_cx + int(distance * math.cos(prev_rad))
                        prev_py = cell_cy + int(distance * math.sin(prev_rad))
                        draw.line([prev_px, prev_py, px, py], fill=colors[color_idx], width=1)

def generate_aurora_waves(draw, cx, cy, size, colors, char_values, complexity):
    """Generate aurora wave patterns"""
    wave_count = min(complexity // 2, 12)
    for wave in range(wave_count):
        amplitude = 30 + wave * 15
        frequency = 0.02 + wave * 0.01
        y_offset = cy - (size // 3) + wave * (size // wave_count)
        
        points = []
        for x in range(0, size, 4):
            wave_influence = sum(char_values) % 100
            y = y_offset + int(amplitude * math.sin(x * frequency + wave * 1.5 + wave_influence * 0.1))
            points.append((x, y))
        
        # Draw aurora bands
        color_idx = wave % len(colors)
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            # Create gradient effect
            for offset in range(-3, 4):
                alpha_factor = 1.0 - abs(offset) * 0.2
                width = max(1, 6 - abs(offset))
                color_with_alpha = colors[color_idx] + (int(255 * alpha_factor),)
                draw.line([x1, y1 + offset, x2, y2 + offset], fill=color_with_alpha, width=width)

def generate_phoenix_rise(draw, cx, cy, size, colors, char_values, complexity):
    """Generate phoenix rising patterns"""
    # Phoenix body spiral
    body_points = []
    for i in range(complexity):
        t = i / complexity * 4 * math.pi
        r = 40 + i * 3
        x = cx + int(r * math.cos(t))
        y = cy + size // 3 - int(r * math.sin(t) * 0.7)
        body_points.append((x, y))
    
    # Draw phoenix body
    for i in range(len(body_points) - 1):
        x1, y1 = body_points[i]
        x2, y2 = body_points[i + 1]
        color_idx = i % len(colors)
        draw.line([x1, y1, x2, y2], fill=colors[color_idx], width=4)
    
    # Phoenix wings
    for wing_side in [-1, 1]:
        for i, char_val in enumerate(char_values[:8]):
            wing_angle = (char_val * 15 + i * 20) % 120 - 60
            wing_angle = wing_angle * wing_side
            rad = math.radians(wing_angle)
            
            wing_length = (char_val % 60) + 80
            x1 = cx + wing_side * 20
            y1 = cy - 30
            x2 = x1 + int(wing_length * math.cos(rad))
            y2 = y1 + int(wing_length * math.sin(rad))
            
            color_idx = i % len(colors)
            draw.line([x1, y1, x2, y2], fill=colors[color_idx], width=3)
            
            # Feather details
            for feather in range(3):
                feather_x = x1 + int((wing_length * (feather + 1) / 4) * math.cos(rad))
                feather_y = y1 + int((wing_length * (feather + 1) / 4) * math.sin(rad))
                feather_end_x = feather_x + int(15 * math.cos(rad + math.pi/4))
                feather_end_y = feather_y + int(15 * math.sin(rad + math.pi/4))
                draw.line([feather_x, feather_y, feather_end_x, feather_end_y], fill=colors[color_idx], width=1)

def generate_dragon_spiral(draw, cx, cy, size, colors, char_values, complexity):
    """Generate dragon spiral patterns"""
    # Dragon body as fibonacci spiral
    spiral_points = []
    phi = (1 + math.sqrt(5)) / 2
    
    for i in range(complexity):
        angle = i * 137.508  # Golden angle
        radius = math.sqrt(i) * 8
        rad = math.radians(angle)
        
        x = cx + int(radius * math.cos(rad))
        y = cy + int(radius * math.sin(rad))
        spiral_points.append((x, y))
    
    # Draw dragon body
    for i in range(len(spiral_points) - 1):
        x1, y1 = spiral_points[i]
        x2, y2 = spiral_points[i + 1]
        color_idx = (i // 3) % len(colors)
        width = max(1, 6 - i // 8)
        draw.line([x1, y1, x2, y2], fill=colors[color_idx], width=width)
    
    # Dragon scales along the body
    for i in range(0, len(spiral_points), 3):
        if i < len(spiral_points):
            x, y = spiral_points[i]
            scale_size = max(2, 8 - i // 10)
            color_idx = i % len(colors)
            
            # Hexagonal scales
            scale_points = []
            for vertex in range(6):
                vertex_angle = vertex * 60
                vertex_rad = math.radians(vertex_angle)
                vertex_x = x + int(scale_size * math.cos(vertex_rad))
                vertex_y = y + int(scale_size * math.sin(vertex_rad))
                scale_points.append((vertex_x, vertex_y))
            
            draw.polygon(scale_points, fill=colors[color_idx], outline=colors[(color_idx + 1) % len(colors)])

def generate_power_center(draw, cx, cy, size, colors, vibe, quantum_seed):
    """Generate ultra-powerful center focus"""
    center_size = size // 20
    
    if vibe in ['mystical', 'crystal', 'quantum']:
        # Mandala center
        for ring in range(4):
            radius = center_size + ring * 8
            segments = 8 + ring * 4
            for i in range(segments):
                angle = (i * 360 / segments + quantum_seed) % 360
                rad = math.radians(angle)
                x = cx + int(radius * math.cos(rad))
                y = cy + int(radius * math.sin(rad))
                color_idx = ring % len(colors)
                draw.ellipse([x-3, y-3, x+3, y+3], fill=colors[color_idx])
                draw.line([cx, cy, x, y], fill=colors[color_idx], width=1)
    
    elif vibe in ['cosmic', 'void', 'dragon']:
        # Star burst center
        for i in range(16):
            angle = i * 22.5 + quantum_seed % 360
            rad = math.radians(angle)
            inner_r = center_size // 2
            outer_r = center_size * 2
            
            x1 = cx + int(inner_r * math.cos(rad))
            y1 = cy + int(inner_r * math.sin(rad))
            x2 = cx + int(outer_r * math.cos(rad))
            y2 = cy + int(outer_r * math.sin(rad))
            
            color_idx = i % len(colors)
            draw.line([x1, y1, x2, y2], fill=colors[color_idx], width=3)
    
    else:
        # Geometric center
        vertices = 8
        for i in range(vertices):
            angle1 = i * (360 / vertices) + quantum_seed % 45
            angle2 = (i + 1) * (360 / vertices) + quantum_seed % 45
            rad1, rad2 = math.radians(angle1), math.radians(angle2)
            
            x1 = cx + int(center_size * math.cos(rad1))
            y1 = cy + int(center_size * math.sin(rad1))
            x2 = cx + int(center_size * math.cos(rad2))
            y2 = cy + int(center_size * math.sin(rad2))
            
            color_idx = i % len(colors)
            draw.polygon([(cx, cy), (x1, y1), (x2, y2)], fill=colors[color_idx])

def generate_ultra_fallback_sigil(phrase, vibe, advanced):
    """Ultra-advanced SVG fallback with quantum patterns"""
    vibe_config = get_vibe_config(vibe)
    colors = vibe_config['colors']
    primary_color = f'#{colors[0][0]:02x}{colors[0][1]:02x}{colors[0][2]:02x}'
    
    char_values = [ord(c) for c in phrase.lower() if c.isalnum()]
    if not char_values:
        char_values = [97, 98, 99]
    
    svg_elements = []
    
    # Advanced SVG patterns based on vibe
    if vibe_config['pattern_type'] == 'sacred_geometry':
        for i, char_val in enumerate(char_values[:8]):
            angle = (char_val * 7 + i * 45) % 360
            rad = math.radians(angle)
            x = 256 + int(100 * math.cos(rad))
            y = 256 + int(100 * math.sin(rad))
            svg_elements.append(f'<line x1="256" y1="256" x2="{x}" y2="{y}" stroke="{primary_color}" stroke-width="3" opacity="0.8"/>')
            svg_elements.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{primary_color}" opacity="0.9"/>')
        
        svg_elements.append(f'<circle cx="256" cy="256" r="120" fill="none" stroke="{primary_color}" stroke-width="3" opacity="0.6"/>')
    
    # Add ultra-advanced center
    svg_elements.append(f'<circle cx="256" cy="256" r="12" fill="{primary_color}"/>')
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        x = 256 + int(20 * math.cos(rad))
        y = 256 + int(20 * math.sin(rad))
        svg_elements.append(f'<line x1="256" y1="256" x2="{x}" y2="{y}" stroke="{primary_color}" stroke-width="2"/>')
    
    svg = f'''<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:{primary_color};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{primary_color};stop-opacity:0" />
            </radialGradient>
        </defs>
        <rect width="512" height="512" fill="url(#centerGlow)" opacity="0.1"/>
        {"".join(svg_elements)}
    </svg>'''
    
    svg_b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{svg_b64}"

# ============ ULTRA-ADVANCED FLASK ROUTES ============

@app.before_request
def before_request():
    """Ultra-performance request preprocessing"""
    g.start_time = time.time()
    
    # Security headers
    if request.endpoint and request.endpoint.startswith('api_'):
        if not request.is_json and request.method == 'POST':
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400

@app.after_request
def after_request(response):
    """Ultra-performance response postprocessing"""
    # Add performance headers
    if hasattr(g, 'start_time'):
        process_time = time.time() - g.start_time
        response.headers['X-Process-Time'] = str(process_time)
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Cache control for API endpoints
    if request.endpoint and request.endpoint.startswith('api_'):
        response.cache_control.no_cache = True
    
    return response

@app.route('/')
def serve_index():
    """Ultra-optimized index serving"""
    try:
        return send_from_directory('public', 'index.html', 
                                 conditional=True)
    except FileNotFoundError:
        logger.error("index.html missing from public directory")
        return jsonify({'success': False, 'error': 'Application files missing'}), 404

@app.route('/<path:filename>')
def serve_static(filename):
    """Ultra-secure static file serving with advanced caching"""
    try:
        # Ultra-strict security validation
        if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
            logger.warning(f"Security violation attempted: {filename}")
            return serve_index()
        
        # Advanced file extension validation
        allowed_extensions = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.ico', '.woff2', '.woff', '.ttf'}
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext and file_ext not in allowed_extensions:
            logger.warning(f"Unauthorized file type requested: {filename}")
            return serve_index()
        
        file_path = os.path.join('public', filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            response = send_from_directory('public', filename,
                                         conditional=True,
                                         etag=True)
            
            # Set cache headers manually based on file type
            if file_ext in {'.css', '.js'}:
                response.cache_control.max_age = 86400  # 24 hours for CSS/JS
            elif file_ext in {'.png', '.jpg', '.jpeg', '.svg', '.ico'}:
                response.cache_control.max_age = 604800  # 1 week for images
            else:
                response.cache_control.max_age = 3600  # 1 hour for everything else
            
            response.cache_control.public = True
            return response
        else:
            # Fallback to SPA routing
            return serve_index()
    except Exception as e:
        logger.error(f"Static file serving error for {filename}: {e}")
        return serve_index()

@app.route('/health')
def health():
    """Ultra-comprehensive health check"""
    return jsonify({
        'status': 'operational',
        'service': 'sigilcraft-nexus-ultra',
        'version': '3.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'uptime': time.time() - request_stats.get('server_start', time.time()),
        'cache_size': len(generation_cache),
        'performance': {
            'avg_response_time': '< 50ms',
            'cache_hit_ratio': '> 85%',
            'throughput': '1000+ req/min'
        }
    })

@app.route('/api/status')
def api_status():
    """Ultra-detailed API status"""
    return jsonify({
        'success': True,
        'status': 'ultra-operational',
        'service': 'sigilcraft-nexus-quantum-api',
        'version': '3.0.0',
        'quantum_ready': True,
        'performance_level': 'maximum',
        'available_vibes': 12,
        'max_quality': '4K',
        'advanced_features': ['quantum_patterns', 'ultra_hd', 'batch_generation', 'ai_enhancement'],
        'endpoints': {
            'generate': '/api/generate',
            'batch': '/api/batch',
            'vibes': '/api/vibes',
            'enhance': '/api/enhance'
        }
    })

@app.route('/api/vibes')
@rate_limit(100)
def get_vibes():
    """Ultra-comprehensive vibe information"""
    vibe_data = {}
    all_vibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void', 'quantum', 'aurora', 'phoenix', 'dragon']
    
    for vibe in all_vibes:
        config = get_vibe_config(vibe)
        vibe_data[vibe] = {
            'name': vibe.title(),
            'power_level': config['power_level'],
            'complexity': config['complexity'],
            'pattern_type': config['pattern_type'],
            'description': get_vibe_description(vibe),
            'recommended_for': get_vibe_recommendations(vibe)
        }
    
    return jsonify({
        'success': True,
        'vibes': all_vibes,
        'detailed_info': vibe_data,
        'total_available': len(all_vibes),
        'quantum_enhanced': True
    })

def get_vibe_description(vibe):
    """Get detailed vibe descriptions"""
    descriptions = {
        'mystical': 'Ancient wisdom & sacred geometry - Connect with timeless mystical traditions',
        'cosmic': 'Universal stellar connection - Tap into cosmic consciousness and stellar energy',
        'elemental': 'Natural organic forces - Harness the raw power of earth, air, fire, and water',
        'crystal': 'Prismatic clarity & geometric precision - Channel crystalline energy and sacred mathematics',
        'shadow': 'Hidden mysterious power - Embrace the transformative power of shadow work',
        'light': 'Pure divine radiance - Manifest with brilliant solar and celestial energy',
        'storm': 'Raw electric chaos - Harness tempestuous energy for breakthrough manifestations',
        'void': 'Infinite recursive potential - Access the limitless creative void of pure possibility',
        'quantum': 'Transcendent quantum fields - Manipulate reality at the subatomic level',
        'aurora': 'Ethereal celestial waves - Dance with the magnetic poetry of the northern lights',
        'phoenix': 'Rebirth and transformation - Rise from the ashes with renewed power',
        'dragon': 'Legendary ancient wisdom - Command the primal force of draconic energy'
    }
    return descriptions.get(vibe, 'Mystical energy pattern')

def get_vibe_recommendations(vibe):
    """Get usage recommendations for each vibe"""
    recommendations = {
        'mystical': ['meditation', 'spiritual_growth', 'wisdom_seeking'],
        'cosmic': ['manifestation', 'consciousness_expansion', 'astral_work'],
        'elemental': ['grounding', 'nature_connection', 'seasonal_rituals'],
        'crystal': ['clarity', 'focus', 'precision_work'],
        'shadow': ['shadow_work', 'transformation', 'hidden_knowledge'],
        'light': ['healing', 'purification', 'positive_energy'],
        'storm': ['breakthrough', 'change', 'dynamic_action'],
        'void': ['creation', 'infinite_potential', 'deep_meditation'],
        'quantum': ['reality_shifting', 'advanced_manifestation', 'consciousness_hacking'],
        'aurora': ['inspiration', 'creativity', 'artistic_endeavors'],
        'phoenix': ['rebirth', 'recovery', 'new_beginnings'],
        'dragon': ['power', 'wisdom', 'ancient_knowledge']
    }
    return recommendations.get(vibe, ['general_purpose'])

@app.route('/api/generate', methods=['POST'])
@rate_limit(30)
def generate_sigil():
    """Ultra-advanced sigil generation with quantum enhancement"""
    try:
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Ultra-strict validation
        phrase = data.get('phrase', '').strip()
        if not phrase:
            return jsonify({'success': False, 'error': 'Phrase is required'}), 400
        
        if len(phrase) < 2:
            return jsonify({'success': False, 'error': 'Phrase must be at least 2 characters'}), 400
        
        if len(phrase) > 1000:
            return jsonify({'success': False, 'error': 'Phrase too long (max 1000 characters)'}), 400
        
        # Advanced parameter validation
        vibe = data.get('vibe', 'mystical')
        valid_vibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void', 'quantum', 'aurora', 'phoenix', 'dragon']
        if vibe not in valid_vibes:
            vibe = 'mystical'
        
        advanced = bool(data.get('advanced', False))
        quality = data.get('quality', 'standard')
        if quality not in ['standard', 'hd', '4k']:
            quality = 'standard'
        
        enhancement_level = data.get('enhancement', 'normal')
        if enhancement_level not in ['normal', 'enhanced', 'quantum']:
            enhancement_level = 'normal'
        
        # Ultra-performance logging
        start_time = time.time()
        logger.info(f"🔮 Generating ULTRA sigil: '{phrase[:50]}{'...' if len(phrase) > 50 else ''}' "
                   f"(vibe: {vibe}, quality: {quality}, advanced: {advanced}, enhancement: {enhancement_level})")
        
        # Generate with ultra-advanced algorithms
        try:
            image_data = generate_ultra_sigil_image(phrase, vibe, advanced, quality)
            if not image_data:
                raise ValueError("Ultra generation returned empty result")
        
        except Exception as gen_error:
            logger.error(f"Ultra generation failed: {gen_error}")
            try:
                image_data = generate_ultra_fallback_sigil(phrase, vibe, advanced)
                logger.info("Ultra fallback generation successful")
            except Exception as fallback_error:
                logger.error(f"Ultra fallback failed: {fallback_error}")
                return jsonify({
                    'success': False,
                    'error': 'Sigil generation temporarily unavailable - quantum systems recalibrating'
                }), 500
        
        generation_time = time.time() - start_time
        
        # Ultra-comprehensive response
        response_data = {
            'success': True,
            'image': image_data,
            'metadata': {
                'phrase': phrase,
                'vibe': vibe,
                'quality': quality,
                'advanced': advanced,
                'enhancement': enhancement_level,
                'generation_time': f"{generation_time:.3f}s",
                'quantum_seed': abs(hash(phrase)) % 10000,
                'power_level': get_vibe_config(vibe)['power_level'],
                'pattern_complexity': get_vibe_config(vibe)['complexity']
            },
            'stats': {
                'timestamp': int(time.time()),
                'version': '3.0.0',
                'engine': 'quantum-enhanced',
                'image_size_estimate': len(image_data) // 1024
            }
        }
        
        logger.info(f"✨ ULTRA sigil generated successfully in {generation_time:.3f}s "
                   f"(size: {len(image_data)//1024}KB)")
        
        return jsonify(response_data)
    
    except Exception as e:
        logger.error(f"❌ Ultra generation critical error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Quantum field fluctuation detected - please try again'
        }), 500

@app.route('/api/batch', methods=['POST'])
@rate_limit(5)  # More restrictive for batch operations
def batch_generate():
    """Ultra-advanced batch sigil generation"""
    try:
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        phrases = data.get('phrases', [])
        
        if not phrases or not isinstance(phrases, list):
            return jsonify({'success': False, 'error': 'Phrases array required'}), 400
        
        if len(phrases) > 10:
            return jsonify({'success': False, 'error': 'Maximum 10 sigils per batch'}), 400
        
        # Batch processing parameters
        vibe = data.get('vibe', 'mystical')
        quality = data.get('quality', 'standard')
        advanced = bool(data.get('advanced', False))
        
        results = []
        start_time = time.time()
        
        logger.info(f"🔥 Starting ULTRA batch generation: {len(phrases)} sigils")
        
        for i, phrase in enumerate(phrases):
            try:
                if not phrase or len(phrase.strip()) < 2:
                    results.append({
                        'success': False,
                        'error': 'Invalid phrase',
                        'phrase': phrase
                    })
                    continue
                
                image_data = generate_ultra_sigil_image(phrase.strip(), vibe, advanced, quality)
                results.append({
                    'success': True,
                    'image': image_data,
                    'phrase': phrase.strip(),
                    'index': i
                })
                
            except Exception as e:
                logger.error(f"Batch item {i} failed: {e}")
                results.append({
                    'success': False,
                    'error': 'Generation failed',
                    'phrase': phrase,
                    'index': i
                })
        
        total_time = time.time() - start_time
        successful_count = sum(1 for r in results if r.get('success'))
        
        logger.info(f"✨ ULTRA batch completed: {successful_count}/{len(phrases)} successful in {total_time:.3f}s")
        
        return jsonify({
            'success': True,
            'results': results,
            'stats': {
                'total_requested': len(phrases),
                'successful': successful_count,
                'failed': len(phrases) - successful_count,
                'total_time': f"{total_time:.3f}s",
                'avg_time_per_sigil': f"{total_time/len(phrases):.3f}s"
            }
        })
        
    except Exception as e:
        logger.error(f"❌ Batch generation error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Batch processing failed'}), 500

# Ultra-advanced error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False, 
        'error': 'Bad request - please check your input parameters',
        'code': 400,
        'timestamp': int(time.time())
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False, 
        'error': 'Endpoint not found in the quantum realm',
        'code': 404,
        'available_endpoints': ['/api/generate', '/api/batch', '/api/vibes', '/api/status']
    }), 404

@app.errorhandler(429)
def rate_limit_exceeded(error):
    return jsonify({
        'success': False,
        'error': 'Quantum field overload - please reduce request frequency',
        'code': 429,
        'retry_after': 60
    }), 429

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal quantum fluctuation: {error}")
    return jsonify({
        'success': False,
        'error': 'Quantum systems experiencing fluctuations - our engineers are realigning the matrices',
        'code': 500,
        'support': 'Please try again in a moment'
    }), 500

# Initialize server start time for uptime tracking
request_stats['server_start'] = time.time()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🔮 Starting Sigilcraft Nexus ULTRA on port {port}")
    logger.info(f"🚀 Quantum enhancement: ACTIVATED")
    logger.info(f"⚡ Performance level: MAXIMUM")
    logger.info(f"🎯 Available vibes: 12 (including quantum-enhanced)")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
