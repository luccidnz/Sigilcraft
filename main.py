
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

class AdvancedTextAnalyzer:
    """Analyzes text to extract unique characteristics for sigil generation"""
    
    def __init__(self, text):
        self.text = text.lower().strip()
        self.analysis = self._analyze_text()
    
    def _analyze_text(self):
        """Perform comprehensive text analysis"""
        analysis = {}
        
        # Basic metrics
        analysis['length'] = len(self.text)
        analysis['word_count'] = len(self.text.split())
        analysis['unique_chars'] = len(set(self.text.replace(' ', '')))
        
        # Character frequency analysis
        char_freq = {}
        for char in self.text:
            if char.isalpha():
                char_freq[char] = char_freq.get(char, 0) + 1
        analysis['char_frequencies'] = char_freq
        
        # Vowel/Consonant analysis
        vowels = 'aeiou'
        analysis['vowel_count'] = sum(1 for c in self.text if c in vowels)
        analysis['consonant_count'] = sum(1 for c in self.text if c.isalpha() and c not in vowels)
        analysis['vowel_ratio'] = analysis['vowel_count'] / max(analysis['length'], 1)
        
        # Phonetic characteristics
        analysis['phonetic_weight'] = self._calculate_phonetic_weight()
        analysis['syllable_count'] = self._estimate_syllables()
        
        # Numerological analysis
        analysis['letter_sum'] = sum(ord(c.lower()) - ord('a') + 1 for c in self.text if c.isalpha())
        analysis['numerology'] = (analysis['letter_sum'] % 9) + 1
        
        # Semantic energy mapping
        analysis['semantic_energy'] = self._map_semantic_energy()
        
        # Geometric characteristics
        analysis['geometric_complexity'] = self._calculate_geometric_complexity()
        
        # Sacred number derivations
        analysis['sacred_ratios'] = self._derive_sacred_ratios()
        
        return analysis
    
    def _calculate_phonetic_weight(self):
        """Calculate phonetic weight based on sound characteristics"""
        weight_map = {
            'a': 1.0, 'e': 0.8, 'i': 0.6, 'o': 1.2, 'u': 0.9,
            'b': 2.1, 'c': 1.8, 'd': 2.0, 'f': 1.5, 'g': 2.2,
            'h': 0.5, 'j': 1.7, 'k': 2.3, 'l': 1.1, 'm': 1.9,
            'n': 1.3, 'p': 2.4, 'q': 2.8, 'r': 1.4, 's': 1.6,
            't': 1.8, 'v': 2.0, 'w': 1.2, 'x': 2.9, 'y': 0.7, 'z': 2.5
        }
        
        total_weight = 0
        for char in self.text:
            if char in weight_map:
                total_weight += weight_map[char]
        
        return total_weight / max(len(self.text), 1)
    
    def _estimate_syllables(self):
        """Estimate syllable count for rhythmic patterns"""
        vowel_groups = 0
        prev_was_vowel = False
        
        for char in self.text.lower():
            if char in 'aeiou':
                if not prev_was_vowel:
                    vowel_groups += 1
                prev_was_vowel = True
            else:
                prev_was_vowel = False
        
        return max(vowel_groups, 1)
    
    def _map_semantic_energy(self):
        """Map words to semantic energy categories"""
        energy_words = {
            'fire': ['fire', 'flame', 'burn', 'heat', 'passion', 'anger', 'energy', 'power'],
            'water': ['water', 'flow', 'stream', 'ocean', 'calm', 'peace', 'healing', 'emotion'],
            'earth': ['earth', 'ground', 'stable', 'solid', 'home', 'security', 'growth', 'money'],
            'air': ['air', 'wind', 'thought', 'mind', 'freedom', 'communication', 'travel', 'ideas'],
            'light': ['light', 'bright', 'sun', 'clarity', 'truth', 'divine', 'pure', 'good'],
            'shadow': ['dark', 'shadow', 'mystery', 'hidden', 'secret', 'deep', 'transform', 'change'],
            'love': ['love', 'heart', 'romance', 'relationship', 'care', 'affection', 'bond', 'soul'],
            'wisdom': ['wisdom', 'knowledge', 'learn', 'understand', 'know', 'study', 'truth', 'insight']
        }
        
        text_words = self.text.split()
        energy_scores = {category: 0 for category in energy_words}
        
        for word in text_words:
            for category, keywords in energy_words.items():
                for keyword in keywords:
                    if keyword in word or word in keyword:
                        energy_scores[category] += 1
        
        return energy_scores
    
    def _calculate_geometric_complexity(self):
        """Calculate how geometrically complex the sigil should be"""
        complexity = 0
        
        # Base complexity on text characteristics
        complexity += self.analysis['unique_chars'] * 0.1
        complexity += self.analysis['word_count'] * 0.15
        complexity += self.analysis['phonetic_weight'] * 0.2
        
        # Add randomness based on text hash
        text_hash = hashlib.md5(self.text.encode()).hexdigest()
        hash_complexity = sum(int(c, 16) for c in text_hash[:8]) / (16 * 8)
        complexity += hash_complexity
        
        return min(max(complexity, 0.3), 1.0)  # Clamp between 0.3 and 1.0
    
    def _derive_sacred_ratios(self):
        """Derive sacred geometric ratios from text"""
        ratios = {}
        
        # Golden ratio variations
        phi = 1.618033988749895
        ratios['phi_variation'] = phi + (self.analysis['letter_sum'] % 100) / 1000
        
        # Fibonacci-based ratios
        fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        text_index = self.analysis['letter_sum'] % len(fib_sequence)
        ratios['fibonacci_ratio'] = fib_sequence[text_index] / 55.0
        
        # Sacred number ratios
        ratios['sacred_seven'] = (self.analysis['letter_sum'] % 7) / 7.0
        ratios['sacred_twelve'] = (self.analysis['letter_sum'] % 12) / 12.0
        
        return ratios

class QuantumSigilGenerator:
    """Advanced sigil generator using quantum-inspired algorithms"""
    
    def __init__(self, text, vibe='mystical'):
        self.text = text
        self.vibe = vibe
        self.analyzer = AdvancedTextAnalyzer(text)
        self.size = 1024
        self.center = self.size // 2
        
        # Create deterministic seed from text
        self.seed = int(hashlib.sha256(f"{text}-{vibe}".encode()).hexdigest()[:8], 16)
        np.random.seed(self.seed)
        random.seed(self.seed)
        
        # Initialize vibe configuration
        self.vibe_config = self._get_vibe_config()
        
    def generate(self):
        """Generate the complete sigil"""
        # Create base image with transparency
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        
        # Create multiple layers for complex composition
        layers = {
            'foundation': self._create_foundation_layer(),
            'core_structure': self._create_core_structure_layer(),
            'text_encoding': self._create_text_encoding_layer(),
            'energy_field': self._create_energy_field_layer(),
            'sacred_geometry': self._create_sacred_geometry_layer(),
            'quantum_patterns': self._create_quantum_patterns_layer(),
            'finishing_effects': self._create_finishing_effects_layer()
        }
        
        # Composite layers with advanced blending
        for layer_name, layer in layers.items():
            if layer:
                img = self._composite_layer(img, layer, layer_name)
        
        # Apply post-processing effects
        img = self._apply_post_processing(img)
        
        # Final optimization
        img = img.resize((768, 768), Image.Resampling.LANCZOS)
        
        return img
    
    def _get_vibe_config(self):
        """Get comprehensive vibe configuration"""
        configs = {
            'mystical': {
                'primary_colors': [(138, 43, 226, 200), (148, 0, 211, 180), (123, 104, 238, 160)],
                'accent_colors': [(255, 215, 0, 120), (255, 255, 255, 80)],
                'energy_type': 'spiral',
                'complexity_modifier': 1.2,
                'glow_intensity': 0.8,
                'sacred_symbols': ['moon', 'star', 'spiral'],
                'pattern_style': 'flowing'
            },
            'cosmic': {
                'primary_colors': [(25, 25, 112, 200), (72, 61, 139, 180), (0, 0, 139, 160)],
                'accent_colors': [(255, 255, 255, 150), (0, 255, 255, 100)],
                'energy_type': 'radial',
                'complexity_modifier': 1.5,
                'glow_intensity': 1.0,
                'sacred_symbols': ['star', 'galaxy', 'planet'],
                'pattern_style': 'geometric'
            },
            'elemental': {
                'primary_colors': [(139, 69, 19, 200), (160, 82, 45, 180), (205, 133, 63, 160)],
                'accent_colors': [(255, 140, 0, 120), (34, 139, 34, 100)],
                'energy_type': 'organic',
                'complexity_modifier': 0.9,
                'glow_intensity': 0.6,
                'sacred_symbols': ['tree', 'flame', 'wave'],
                'pattern_style': 'natural'
            },
            'crystal': {
                'primary_colors': [(176, 224, 230, 200), (173, 216, 230, 180), (135, 206, 235, 160)],
                'accent_colors': [(255, 255, 255, 180), (192, 192, 192, 120)],
                'energy_type': 'crystalline',
                'complexity_modifier': 1.8,
                'glow_intensity': 0.9,
                'sacred_symbols': ['crystal', 'prism', 'facet'],
                'pattern_style': 'fractal'
            },
            'shadow': {
                'primary_colors': [(47, 47, 47, 200), (69, 69, 69, 180), (105, 105, 105, 160)],
                'accent_colors': [(128, 0, 128, 150), (139, 0, 0, 120)],
                'energy_type': 'flowing',
                'complexity_modifier': 0.7,
                'glow_intensity': 0.4,
                'sacred_symbols': ['void', 'smoke', 'mirror'],
                'pattern_style': 'ethereal'
            },
            'light': {
                'primary_colors': [(255, 248, 220, 200), (255, 250, 205, 180), (255, 255, 240, 160)],
                'accent_colors': [(255, 215, 0, 180), (255, 255, 255, 200)],
                'energy_type': 'radiant',
                'complexity_modifier': 1.1,
                'glow_intensity': 1.2,
                'sacred_symbols': ['sun', 'ray', 'halo'],
                'pattern_style': 'luminous'
            }
        }
        return configs.get(self.vibe, configs['mystical'])
    
    def _create_foundation_layer(self):
        """Create the foundational energy field"""
        layer = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        
        # Create energy ripples based on text characteristics
        ripple_count = 3 + (self.analyzer.analysis['numerology'] % 5)
        
        for i in range(ripple_count):
            radius = 100 + i * 80 + (self.analyzer.analysis['letter_sum'] % 50)
            alpha = max(20, 80 - i * 15)
            
            color_index = (i + self.analyzer.analysis['letter_sum']) % len(self.vibe_config['primary_colors'])
            color = (*self.vibe_config['primary_colors'][color_index][:3], alpha)
            
            # Add text-based distortion
            distortion = self.analyzer.analysis['phonetic_weight'] * 20
            
            for angle in range(0, 360, 10):
                angle_rad = math.radians(angle)
                distorted_radius = radius + math.sin(angle_rad * 3) * distortion
                
                x = self.center + int(distorted_radius * math.cos(angle_rad))
                y = self.center + int(distorted_radius * math.sin(angle_rad))
                
                if 0 <= x < self.size and 0 <= y < self.size:
                    draw.ellipse([x-3, y-3, x+3, y+3], fill=color)
        
        return layer
    
    def _create_core_structure_layer(self):
        """Create the core geometric structure based on text analysis"""
        layer = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        
        # Primary polygon based on text characteristics
        sides = 3 + (self.analyzer.analysis['numerology'] % 9)
        radius = 150 + (self.analyzer.analysis['unique_chars'] * 10)
        
        # Calculate polygon points with text-based rotation
        rotation = self.analyzer.analysis['sacred_ratios']['phi_variation'] * 180
        points = []
        
        for i in range(sides):
            angle = (2 * math.pi * i / sides) + math.radians(rotation)
            x = self.center + int(radius * math.cos(angle))
            y = self.center + int(radius * math.sin(angle))
            points.append((x, y))
        
        # Draw the primary structure
        if len(points) > 2:
            color = (*self.vibe_config['primary_colors'][0][:3], 180)
            draw.polygon(points, outline=color, width=4)
            
            # Add inner connections based on text patterns
            connection_pattern = self.analyzer.analysis['char_frequencies']
            char_values = list(connection_pattern.values()) if connection_pattern else [1, 2, 3]
            
            for i in range(len(points)):
                for j in range(i + 2, len(points)):
                    if j < len(points):
                        connection_strength = char_values[j % len(char_values)]
                        if connection_strength > 1:  # Only draw stronger connections
                            inner_color = (*self.vibe_config['accent_colors'][0][:3], 
                                         100 + connection_strength * 20)
                            draw.line([points[i], points[j]], fill=inner_color, width=2)
        
        return layer
    
    def _create_text_encoding_layer(self):
        """Encode the text directly into visual elements"""
        layer = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        
        # Convert each character to a unique visual element
        char_positions = self._calculate_character_positions()
        
        for i, char in enumerate(self.text.replace(' ', '')):
            if char.isalpha():
                char_value = ord(char.lower()) - ord('a')
                
                if i < len(char_positions):
                    x, y = char_positions[i]
                    
                    # Create character-specific symbol
                    symbol_type = char_value % 6
                    symbol_size = 15 + (char_value % 4) * 8
                    
                    color_index = char_value % len(self.vibe_config['primary_colors'])
                    color = (*self.vibe_config['primary_colors'][color_index][:3], 200)
                    
                    if symbol_type == 0:  # Sacred circle
                        draw.ellipse([x-symbol_size, y-symbol_size, x+symbol_size, y+symbol_size], 
                                   outline=color, width=3)
                        # Add inner dot
                        draw.ellipse([x-3, y-3, x+3, y+3], fill=color)
                        
                    elif symbol_type == 1:  # Triangle
                        points = [
                            (x, y - symbol_size),
                            (x - symbol_size, y + symbol_size//2),
                            (x + symbol_size, y + symbol_size//2)
                        ]
                        draw.polygon(points, outline=color, width=3)
                        
                    elif symbol_type == 2:  # Diamond
                        points = [
                            (x, y - symbol_size),
                            (x + symbol_size, y),
                            (x, y + symbol_size),
                            (x - symbol_size, y)
                        ]
                        draw.polygon(points, outline=color, width=3)
                        
                    elif symbol_type == 3:  # Cross
                        draw.line([x - symbol_size, y, x + symbol_size, y], fill=color, width=4)
                        draw.line([x, y - symbol_size, x, y + symbol_size], fill=color, width=4)
                        
                    elif symbol_type == 4:  # Star
                        self._draw_star(draw, x, y, symbol_size, color)
                        
                    else:  # Spiral
                        self._draw_spiral(draw, x, y, symbol_size, color, char_value)
        
        return layer
    
    def _calculate_character_positions(self):
        """Calculate positions for character encoding based on text flow"""
        positions = []
        
        # Create a flowing pattern based on text characteristics
        flow_type = self.analyzer.analysis['semantic_energy']
        dominant_energy = max(flow_type, key=flow_type.get) if flow_type else 'neutral'
        
        char_count = len(self.text.replace(' ', ''))
        
        if dominant_energy in ['fire', 'light']:
            # Radial outward pattern
            for i in range(char_count):
                angle = (2 * math.pi * i / char_count) + math.radians(self.analyzer.analysis['phonetic_weight'] * 30)
                radius = 80 + (i / char_count) * 120
                x = self.center + int(radius * math.cos(angle))
                y = self.center + int(radius * math.sin(angle))
                positions.append((x, y))
                
        elif dominant_energy in ['water', 'air']:
            # Spiral pattern
            for i in range(char_count):
                progress = i / max(char_count - 1, 1)
                angle = progress * 4 * math.pi
                radius = 60 + progress * 140
                x = self.center + int(radius * math.cos(angle))
                y = self.center + int(radius * math.sin(angle))
                positions.append((x, y))
                
        else:
            # Geometric grid pattern
            grid_size = int(math.ceil(math.sqrt(char_count)))
            cell_size = 200 // max(grid_size, 1)
            
            for i in range(char_count):
                row = i // grid_size
                col = i % grid_size
                
                # Center the grid
                start_x = self.center - (grid_size * cell_size) // 2
                start_y = self.center - (grid_size * cell_size) // 2
                
                x = start_x + col * cell_size + cell_size // 2
                y = start_y + row * cell_size + cell_size // 2
                positions.append((x, y))
        
        return positions
    
    def _draw_star(self, draw, x, y, size, color):
        """Draw a star symbol"""
        points = []
        for i in range(10):  # 5-pointed star = 10 points
            angle = (i * math.pi / 5)
            radius = size if i % 2 == 0 else size // 2
            px = x + int(radius * math.cos(angle))
            py = y + int(radius * math.sin(angle))
            points.append((px, py))
        
        if len(points) > 2:
            draw.polygon(points, outline=color, width=2)
    
    def _draw_spiral(self, draw, x, y, size, color, char_value):
        """Draw a spiral symbol"""
        points = []
        for i in range(20):
            progress = i / 19.0
            angle = progress * 3 * math.pi + (char_value * 0.2)
            radius = progress * size
            px = x + int(radius * math.cos(angle))
            py = y + int(radius * math.sin(angle))
            points.append((px, py))
        
        for i in range(len(points) - 1):
            alpha = int(255 * (1 - i / len(points)))
            spiral_color = (*color[:3], alpha)
            draw.line([points[i], points[i + 1]], fill=spiral_color, width=2)
    
    def _create_energy_field_layer(self):
        """Create dynamic energy field based on text semantics"""
        layer = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        
        # Generate energy streams based on semantic analysis
        energy_map = self.analyzer.analysis['semantic_energy']
        
        for energy_type, strength in energy_map.items():
            if strength > 0:
                self._draw_energy_stream(draw, energy_type, strength)
        
        return layer
    
    def _draw_energy_stream(self, draw, energy_type, strength):
        """Draw specific energy stream based on type"""
        stream_count = min(strength * 3, 15)
        
        energy_patterns = {
            'fire': self._draw_fire_energy,
            'water': self._draw_water_energy,
            'earth': self._draw_earth_energy,
            'air': self._draw_air_energy,
            'light': self._draw_light_energy,
            'shadow': self._draw_shadow_energy,
            'love': self._draw_love_energy,
            'wisdom': self._draw_wisdom_energy
        }
        
        if energy_type in energy_patterns:
            energy_patterns[energy_type](draw, stream_count)
    
    def _draw_fire_energy(self, draw, count):
        """Draw fire energy patterns"""
        for _ in range(count):
            # Create flame-like tendrils
            start_angle = random.uniform(0, 2 * math.pi)
            points = [(self.center, self.center)]
            
            for step in range(25):
                last_x, last_y = points[-1]
                
                # Flames rise and flicker
                angle = start_angle + math.sin(step * 0.3) * 0.5
                distance = step * 8 + random.randint(-5, 5)
                
                new_x = last_x + int(distance * math.cos(angle))
                new_y = last_y - step * 4 + random.randint(-3, 3)  # Rise upward
                
                points.append((new_x, new_y))
            
            # Draw flame trail
            for i in range(len(points) - 1):
                alpha = int(200 * (1 - i / len(points)))
                color = (255, 100 + i * 3, 0, alpha)
                draw.line([points[i], points[i + 1]], fill=color, width=3)
    
    def _draw_water_energy(self, draw, count):
        """Draw water energy patterns"""
        for _ in range(count):
            # Create flowing wave patterns
            wave_y = self.center + random.randint(-100, 100)
            points = []
            
            for x in range(0, self.size, 10):
                wave_amplitude = 30 + self.analyzer.analysis['vowel_ratio'] * 50
                y = wave_y + int(wave_amplitude * math.sin(x * 0.02 + random.uniform(0, math.pi)))
                points.append((x, y))
            
            # Draw flowing lines
            for i in range(len(points) - 1):
                alpha = 150 - abs(i - len(points)//2) * 2
                alpha = max(20, alpha)
                color = (0, 150, 255, alpha)
                draw.line([points[i], points[i + 1]], fill=color, width=2)
    
    def _draw_earth_energy(self, draw, count):
        """Draw earth energy patterns"""
        for _ in range(count):
            # Create root-like branching patterns
            start_x = self.center + random.randint(-50, 50)
            start_y = self.center
            
            self._draw_branch(draw, start_x, start_y, 
                            math.pi / 2, 80, 4, (101, 67, 33, 180))
    
    def _draw_branch(self, draw, x, y, angle, length, depth, color):
        """Recursive branch drawing for earth energy"""
        if depth <= 0 or length < 10:
            return
        
        end_x = x + int(length * math.cos(angle))
        end_y = y + int(length * math.sin(angle))
        
        alpha = color[3] if len(color) > 3 else 180
        branch_color = (*color[:3], max(alpha - depth * 30, 50))
        
        draw.line([x, y, end_x, end_y], fill=branch_color, width=depth)
        
        # Create sub-branches
        if depth > 1:
            new_length = length * 0.7
            self._draw_branch(draw, end_x, end_y, angle - 0.5, new_length, depth - 1, color)
            self._draw_branch(draw, end_x, end_y, angle + 0.5, new_length, depth - 1, color)
    
    def _draw_air_energy(self, draw, count):
        """Draw air energy patterns"""
        for _ in range(count):
            # Create swirling wind patterns
            center_x = self.center + random.randint(-100, 100)
            center_y = self.center + random.randint(-100, 100)
            
            for i in range(30):
                progress = i / 29.0
                angle = progress * 4 * math.pi
                radius = progress * 80
                
                x = center_x + int(radius * math.cos(angle))
                y = center_y + int(radius * math.sin(angle))
                
                if 0 <= x < self.size and 0 <= y < self.size:
                    alpha = int(150 * (1 - progress))
                    color = (200, 200, 255, alpha)
                    size = max(1, int(5 * (1 - progress)))
                    draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
    
    def _draw_light_energy(self, draw, count):
        """Draw light energy patterns"""
        for i in range(count * 2):
            # Create radial light beams
            angle = (2 * math.pi * i / (count * 2))
            
            for distance in range(0, 200, 10):
                x = self.center + int(distance * math.cos(angle))
                y = self.center + int(distance * math.sin(angle))
                
                if 0 <= x < self.size and 0 <= y < self.size:
                    alpha = max(20, 200 - distance)
                    color = (255, 255, 200, alpha)
                    draw.ellipse([x-2, y-2, x+2, y+2], fill=color)
    
    def _draw_shadow_energy(self, draw, count):
        """Draw shadow energy patterns"""
        for _ in range(count):
            # Create dark flowing tendrils
            start_x = random.randint(0, self.size)
            start_y = random.randint(0, self.size)
            
            points = [(start_x, start_y)]
            
            for step in range(20):
                last_x, last_y = points[-1]
                angle = random.uniform(0, 2 * math.pi)
                distance = random.randint(10, 30)
                
                new_x = last_x + int(distance * math.cos(angle))
                new_y = last_y + int(distance * math.sin(angle))
                
                new_x = max(0, min(self.size, new_x))
                new_y = max(0, min(self.size, new_y))
                
                points.append((new_x, new_y))
            
            # Draw shadow trail
            for i in range(len(points) - 1):
                alpha = int(120 * (1 - i / len(points)))
                color = (40, 40, 40, alpha)
                width = max(1, 5 - i // 4)
                draw.line([points[i], points[i + 1]], fill=color, width=width)
    
    def _draw_love_energy(self, draw, count):
        """Draw love energy patterns"""
        for _ in range(count):
            # Create heart-shaped energy flows
            center_x = self.center + random.randint(-50, 50)
            center_y = self.center + random.randint(-50, 50)
            
            # Heart shape using parametric equations
            for t in range(0, 628, 10):  # 0 to 2π * 100
                t_rad = t / 100.0
                
                # Heart equation
                x = 16 * (math.sin(t_rad) ** 3)
                y = -(13 * math.cos(t_rad) - 5 * math.cos(2 * t_rad) - 
                      2 * math.cos(3 * t_rad) - math.cos(4 * t_rad))
                
                # Scale and position
                heart_x = center_x + int(x * 3)
                heart_y = center_y + int(y * 3)
                
                if 0 <= heart_x < self.size and 0 <= heart_y < self.size:
                    alpha = 150
                    color = (255, 100, 150, alpha)
                    draw.ellipse([heart_x-2, heart_y-2, heart_x+2, heart_y+2], fill=color)
    
    def _draw_wisdom_energy(self, draw, count):
        """Draw wisdom energy patterns"""
        for _ in range(count):
            # Create mandala-like patterns
            center_x = self.center + random.randint(-80, 80)
            center_y = self.center + random.randint(-80, 80)
            
            layers = 5
            for layer in range(layers):
                radius = 20 + layer * 15
                points_count = 6 + layer * 2
                
                for i in range(points_count):
                    angle = (2 * math.pi * i / points_count)
                    x = center_x + int(radius * math.cos(angle))
                    y = center_y + int(radius * math.sin(angle))
                    
                    alpha = 150 - layer * 20
                    color = (150, 100, 255, alpha)
                    size = 4 - layer
                    
                    if size > 0:
                        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
    
    def _create_sacred_geometry_layer(self):
        """Create sacred geometry based on text-derived ratios"""
        layer = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        
        # Use sacred ratios derived from text
        ratios = self.analyzer.analysis['sacred_ratios']
        
        # Golden spiral
        self._draw_golden_spiral(draw, ratios['phi_variation'])
        
        # Fibonacci rectangles
        self._draw_fibonacci_rectangles(draw, ratios['fibonacci_ratio'])
        
        # Sacred polygons
        self._draw_sacred_polygons(draw, ratios)
        
        return layer
    
    def _draw_golden_spiral(self, draw, phi_variation):
        """Draw golden spiral based on text characteristics"""
        # Calculate spiral parameters
        a = 5 * phi_variation
        b = 0.306 * phi_variation
        
        points = []
        for i in range(200):
            t = i * 0.1
            r = a * math.exp(b * t)
            
            x = self.center + int(r * math.cos(t))
            y = self.center + int(r * math.sin(t))
            
            if 0 <= x < self.size and 0 <= y < self.size:
                points.append((x, y))
        
        # Draw spiral
        for i in range(len(points) - 1):
            alpha = int(200 * (1 - i / len(points)))
            color = (*self.vibe_config['accent_colors'][0][:3], alpha)
            draw.line([points[i], points[i + 1]], fill=color, width=2)
    
    def _draw_fibonacci_rectangles(self, draw, ratio):
        """Draw Fibonacci rectangle sequence"""
        fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21]
        
        x, y = self.center - 100, self.center - 100
        
        for i, fib_num in enumerate(fib_sequence[:6]):
            size = int(fib_num * 15 * ratio)
            
            alpha = 150 - i * 20
            color = (*self.vibe_config['primary_colors'][i % len(self.vibe_config['primary_colors'])][:3], alpha)
            
            draw.rectangle([x, y, x + size, y + size], outline=color, width=2)
            
            # Move to next position in spiral pattern
            if i % 4 == 0:
                x += size
            elif i % 4 == 1:
                y += size
            elif i % 4 == 2:
                x -= size
            else:
                y -= size
    
    def _draw_sacred_polygons(self, draw, ratios):
        """Draw sacred polygons based on text ratios"""
        polygon_types = [3, 4, 5, 6, 7, 8, 12]
        
        for i, sides in enumerate(polygon_types):
            if i >= 3:  # Limit to prevent overcrowding
                break
                
            radius = 60 + i * 40
            rotation = ratios['sacred_seven'] * 360 + i * 45
            
            points = []
            for j in range(sides):
                angle = (2 * math.pi * j / sides) + math.radians(rotation)
                x = self.center + int(radius * math.cos(angle))
                y = self.center + int(radius * math.sin(angle))
                points.append((x, y))
            
            alpha = 120 - i * 30
            color = (*self.vibe_config['primary_colors'][i % len(self.vibe_config['primary_colors'])][:3], alpha)
            
            if len(points) > 2:
                draw.polygon(points, outline=color, width=2)
    
    def _create_quantum_patterns_layer(self):
        """Create quantum-inspired interference patterns"""
        layer = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        
        # Create interference patterns based on text frequency analysis
        char_freqs = list(self.analyzer.analysis['char_frequencies'].values())
        if not char_freqs:
            char_freqs = [1, 2, 3]
        
        # Quantum wave interference
        for i, freq in enumerate(char_freqs[:5]):  # Limit to 5 frequencies
            self._draw_wave_interference(draw, freq, i)
        
        return layer
    
    def _draw_wave_interference(self, draw, frequency, index):
        """Draw wave interference patterns"""
        wavelength = 30 + frequency * 10
        amplitude = 20 + frequency * 5
        
        # Create wave center based on index
        angle = (2 * math.pi * index / 5)
        center_x = self.center + int(80 * math.cos(angle))
        center_y = self.center + int(80 * math.sin(angle))
        
        # Draw concentric waves
        for radius in range(10, 200, 15):
            points = []
            
            for theta in range(0, 360, 5):
                theta_rad = math.radians(theta)
                
                # Wave equation with interference
                wave_radius = radius + amplitude * math.sin(radius / wavelength)
                
                x = center_x + int(wave_radius * math.cos(theta_rad))
                y = center_y + int(wave_radius * math.sin(theta_rad))
                
                if 0 <= x < self.size and 0 <= y < self.size:
                    points.append((x, y))
            
            # Draw wave circle
            alpha = max(20, 100 - radius // 3)
            color = (*self.vibe_config['accent_colors'][0][:3], alpha)
            
            for i in range(len(points) - 1):
                draw.line([points[i], points[i + 1]], fill=color, width=1)
    
    def _create_finishing_effects_layer(self):
        """Create final finishing effects and details"""
        layer = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        
        # Add text-specific details
        complexity = self.analyzer.analysis['geometric_complexity']
        
        if complexity > 0.7:
            self._add_detail_flourishes(draw)
        
        if self.analyzer.analysis['vowel_ratio'] > 0.3:
            self._add_flowing_accents(draw)
        
        if self.analyzer.analysis['numerology'] in [3, 7, 9]:
            self._add_sacred_markers(draw)
        
        return layer
    
    def _add_detail_flourishes(self, draw):
        """Add detailed flourishes for complex texts"""
        for _ in range(10):
            x = random.randint(100, self.size - 100)
            y = random.randint(100, self.size - 100)
            
            # Small decorative elements
            size = random.randint(5, 15)
            symbol_type = random.randint(0, 2)
            
            color = (*self.vibe_config['accent_colors'][0][:3], 120)
            
            if symbol_type == 0:
                # Decorative dots
                draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=color)
            elif symbol_type == 1:
                # Small crosses
                draw.line([x-size//2, y, x+size//2, y], fill=color, width=2)
                draw.line([x, y-size//2, x, y+size//2], fill=color, width=2)
            else:
                # Tiny spirals
                self._draw_spiral(draw, x, y, size//2, color, 1)
    
    def _add_flowing_accents(self, draw):
        """Add flowing accents for vowel-heavy texts"""
        for _ in range(5):
            # Create flowing curved lines
            start_x = random.randint(50, self.size - 50)
            start_y = random.randint(50, self.size - 50)
            
            points = [(start_x, start_y)]
            
            for i in range(15):
                last_x, last_y = points[-1]
                angle = i * 0.3 + random.uniform(-0.2, 0.2)
                distance = 15 + random.randint(-5, 5)
                
                new_x = last_x + int(distance * math.cos(angle))
                new_y = last_y + int(distance * math.sin(angle))
                
                points.append((new_x, new_y))
            
            # Draw flowing line
            for i in range(len(points) - 1):
                alpha = int(150 * (1 - i / len(points)))
                color = (*self.vibe_config['accent_colors'][0][:3], alpha)
                draw.line([points[i], points[i + 1]], fill=color, width=2)
    
    def _add_sacred_markers(self, draw):
        """Add sacred markers for numerologically significant texts"""
        # Add markers at sacred positions
        sacred_positions = [
            (self.center, 50),  # North
            (self.center, self.size - 50),  # South
            (50, self.center),  # West
            (self.size - 50, self.center)  # East
        ]
        
        for x, y in sacred_positions:
            color = (*self.vibe_config['primary_colors'][0][:3], 180)
            
            # Draw sacred marker
            draw.ellipse([x-8, y-8, x+8, y+8], fill=color)
            draw.ellipse([x-12, y-12, x+12, y+12], outline=color, width=2)
            
            # Add radiating lines
            for angle in range(0, 360, 45):
                angle_rad = math.radians(angle)
                end_x = x + int(20 * math.cos(angle_rad))
                end_y = y + int(20 * math.sin(angle_rad))
                draw.line([x, y, end_x, end_y], fill=color, width=1)
    
    def _composite_layer(self, base_img, layer, layer_name):
        """Composite layer with appropriate blending"""
        if layer:
            return Image.alpha_composite(base_img, layer)
        return base_img
    
    def _apply_post_processing(self, img):
        """Apply final post-processing effects"""
        # Apply vibe-specific effects
        if self.vibe == 'mystical':
            img = self._add_mystical_glow(img)
        elif self.vibe == 'cosmic':
            img = self._add_cosmic_starfield(img)
        elif self.vibe == 'crystal':
            img = self._add_crystal_refraction(img)
        elif self.vibe == 'shadow':
            img = self._add_shadow_wisps(img)
        elif self.vibe == 'light':
            img = self._add_divine_radiance(img)
        elif self.vibe == 'elemental':
            img = self._add_elemental_texture(img)
        
        # Final enhancement
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        return img
    
    def _add_mystical_glow(self, img):
        """Add mystical glow effect"""
        glow = img.copy()
        glow = glow.filter(ImageFilter.GaussianBlur(radius=8))
        
        # Enhance the glow
        enhancer = ImageEnhance.Brightness(glow)
        glow = enhancer.enhance(1.5)
        
        # Blend with original
        return Image.blend(img.convert('RGBA'), glow, 0.3)
    
    def _add_cosmic_starfield(self, img):
        """Add cosmic starfield background"""
        draw = ImageDraw.Draw(img)
        
        for _ in range(100):
            x = random.randint(0, img.width)
            y = random.randint(0, img.height)
            brightness = random.randint(100, 255)
            size = random.choice([1, 1, 1, 2, 2, 3])
            
            color = (brightness, brightness, brightness, random.randint(100, 200))
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
        
        return img
    
    def _add_crystal_refraction(self, img):
        """Add crystal refraction effects"""
        # Create prismatic light effects
        draw = ImageDraw.Draw(img)
        
        for i in range(8):
            angle = (360 / 8) * i
            angle_rad = math.radians(angle)
            
            # Rainbow colors
            colors = [
                (255, 0, 0, 100), (255, 127, 0, 100), (255, 255, 0, 100),
                (0, 255, 0, 100), (0, 0, 255, 100), (75, 0, 130, 100),
                (148, 0, 211, 100)
            ]
            
            color = colors[i % len(colors)]
            
            start_x = self.center + int(60 * math.cos(angle_rad))
            start_y = self.center + int(60 * math.sin(angle_rad))
            end_x = self.center + int(150 * math.cos(angle_rad))
            end_y = self.center + int(150 * math.sin(angle_rad))
            
            draw.line([start_x, start_y, end_x, end_y], fill=color, width=3)
        
        return img
    
    def _add_shadow_wisps(self, img):
        """Add shadow wisp effects"""
        draw = ImageDraw.Draw(img)
        
        for _ in range(15):
            # Create shadow tendrils
            start_x = random.randint(0, img.width)
            start_y = random.randint(img.height//2, img.height)
            
            points = [(start_x, start_y)]
            
            for step in range(20):
                last_x, last_y = points[-1]
                new_x = last_x + random.randint(-10, 10)
                new_y = last_y - random.randint(5, 15)
                
                new_x = max(0, min(img.width, new_x))
                new_y = max(0, min(img.height, new_y))
                
                points.append((new_x, new_y))
            
            # Draw shadow trail
            for i in range(len(points) - 1):
                alpha = int(100 * (1 - i / len(points)))
                color = (50, 50, 50, alpha)
                width = max(1, 6 - i//3)
                draw.line([points[i], points[i + 1]], fill=color, width=width)
        
        return img
    
    def _add_divine_radiance(self, img):
        """Add divine radiance effects"""
        draw = ImageDraw.Draw(img)
        
        # Divine rays
        for i in range(12):
            angle = (2 * math.pi / 12) * i
            
            for distance in range(0, 200, 8):
                x = self.center + int(distance * math.cos(angle))
                y = self.center + int(distance * math.sin(angle))
                
                if 0 <= x < img.width and 0 <= y < img.height:
                    alpha = max(20, 180 - distance)
                    color = (255, 215, 0, alpha)
                    size = max(1, 4 - distance//50)
                    draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
        
        return img
    
    def _add_elemental_texture(self, img):
        """Add natural elemental texture"""
        draw = ImageDraw.Draw(img)
        
        # Add organic flowing lines
        for _ in range(20):
            start_x = random.randint(0, img.width)
            start_y = random.randint(0, img.height)
            
            points = [(start_x, start_y)]
            
            for step in range(15):
                last_x, last_y = points[-1]
                angle = random.uniform(0, 2 * math.pi)
                distance = random.randint(10, 25)
                
                new_x = last_x + int(distance * math.cos(angle))
                new_y = last_y + int(distance * math.sin(angle))
                
                new_x = max(0, min(img.width, new_x))
                new_y = max(0, min(img.height, new_y))
                
                points.append((new_x, new_y))
            
            # Draw organic line
            for i in range(len(points) - 1):
                alpha = int(120 * (1 - i / len(points)))
                color = (139, 69, 19, alpha)
                draw.line([points[i], points[i + 1]], fill=color, width=2)
        
        return img

def generate_artistic_sigil(phrase, vibe='mystical'):
    """Generate a truly unique and text-responsive sigil"""
    generator = QuantumSigilGenerator(phrase, vibe)
    return generator.generate()

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'Flask backend running',
        'message': 'Revolutionary Text-Responsive Sigil Generator',
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light'],
        'version': '15.0 - Quantum Text-Responsive Revolution'
    })

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify server is working"""
    return jsonify({
        'status': 'ok',
        'message': 'Revolutionary sigil server operational',
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light'],
        'version': '15.0'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'server': 'online',
        'version': 'Quantum Revolution 15.0',
        'timestamp': str(datetime.now())
    })

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint with detailed information"""
    return jsonify({
        'status': 'operational',
        'server': 'Revolutionary Text-Responsive Sigil Generator',
        'version': '15.0',
        'features': [
            'Deep text analysis & semantic mapping',
            'Character-specific visual encoding', 
            'Quantum-inspired pattern generation',
            'Sacred geometry derived from text ratios',
            'Energy field visualization based on word semantics',
            'Multi-layered composition with advanced blending',
            'Truly unique results for each text input'
        ],
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light'],
        'endpoints': ['/generate', '/test', '/health', '/status']
    })

@app.route('/generate', methods=['POST'])
@handle_errors
def generate_sigil():
    """Generate a revolutionary text-responsive sigil"""
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

        print(f"🚀 Generating revolutionary sigil for: '{phrase}' with vibe: {vibe}")

        # Generate the revolutionary text-responsive sigil
        sigil_img = generate_artistic_sigil(phrase, vibe)

        # Convert to base64
        buffer = io.BytesIO()
        sigil_img.save(buffer, format='PNG', optimize=True, quality=95)
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        image_data_url = f"data:image/png;base64,{image_base64}"

        print(f"✅ Revolutionary sigil generated successfully (15x Enhanced)")

        return jsonify({
            'success': True,
            'image': image_data_url,
            'phrase': phrase,
            'vibe': vibe,
            'version': 'Quantum Revolution 15.0',
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

    print(f"🚀 Starting Revolutionary Text-Responsive Sigil Generator on port {port}...")

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
