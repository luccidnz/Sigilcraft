
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
import string
import re

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

# ===== REVOLUTIONARY SIGIL GENERATOR CLASS =====
class RevolutionarySigilGenerator:
    """Revolutionary sigil generation with phrase-specific algorithms"""
    
    def __init__(self):
        self.size = 1024
        self.center = (self.size // 2, self.size // 2)
        
        # Enhanced vibe configurations
        self.vibe_styles = {
            'mystical': {
                'colors': [(138, 43, 226), (75, 0, 130), (148, 0, 211), (186, 85, 211), (123, 104, 238)],
                'stroke_width': lambda: random.randint(2, 5),
                'glow_intensity': 0.8,
                'complexity': 'high',
                'patterns': ['sacred_geometry', 'pentagram', 'spiral', 'mandala']
            },
            'cosmic': {
                'colors': [(0, 100, 200), (100, 0, 200), (200, 0, 100), (0, 255, 255), (255, 0, 255), (138, 43, 226)],
                'stroke_width': lambda: random.randint(1, 4),
                'glow_intensity': 1.0,
                'complexity': 'extreme',
                'patterns': ['constellation', 'galaxy', 'nebula', 'orbital']
            },
            'elemental': {
                'colors': [(34, 139, 34), (255, 140, 0), (30, 144, 255), (139, 69, 19), (255, 69, 0), (0, 128, 0)],
                'stroke_width': lambda: random.randint(3, 6),
                'glow_intensity': 0.6,
                'complexity': 'organic',
                'patterns': ['flowing', 'crystalline', 'root_system', 'flame']
            },
            'crystal': {
                'colors': [(255, 20, 147), (0, 255, 255), (255, 215, 0), (255, 105, 180), (64, 224, 208), (255, 255, 255)],
                'stroke_width': lambda: random.randint(1, 3),
                'glow_intensity': 1.2,
                'complexity': 'geometric',
                'patterns': ['faceted', 'prismatic', 'lattice', 'refraction']
            },
            'shadow': {
                'colors': [(64, 64, 64), (128, 0, 128), (105, 105, 105), (169, 169, 169), (0, 0, 0), (47, 79, 79)],
                'stroke_width': lambda: random.randint(4, 8),
                'glow_intensity': 0.3,
                'complexity': 'angular',
                'patterns': ['jagged', 'void', 'shadow_cast', 'broken']
            },
            'light': {
                'colors': [(255, 255, 0), (255, 215, 0), (255, 255, 255), (255, 250, 205), (255, 255, 224), (250, 250, 210)],
                'stroke_width': lambda: random.randint(1, 4),
                'glow_intensity': 1.5,
                'complexity': 'radiant',
                'patterns': ['radial', 'burst', 'prism', 'halo']
            },
            'storm': {
                'colors': [(75, 0, 130), (255, 255, 0), (0, 0, 139), (220, 20, 60), (255, 20, 147), (138, 43, 226)],
                'stroke_width': lambda: random.randint(2, 6),
                'glow_intensity': 0.9,
                'complexity': 'chaotic',
                'patterns': ['lightning', 'turbulent', 'fractal', 'electric']
            },
            'void': {
                'colors': [(25, 25, 112), (0, 0, 0), (72, 61, 139), (106, 90, 205), (75, 0, 130), (25, 25, 25)],
                'stroke_width': lambda: random.randint(3, 7),
                'glow_intensity': 0.4,
                'complexity': 'infinite',
                'patterns': ['spiral_void', 'recursive', 'portal', 'dimensional']
            }
        }
        
        # Letter-to-energy mapping for deeper text analysis
        self.letter_energies = {
            'a': 'light', 'b': 'elemental', 'c': 'crystal', 'd': 'shadow', 'e': 'light',
            'f': 'storm', 'g': 'elemental', 'h': 'mystical', 'i': 'light', 'j': 'storm',
            'k': 'shadow', 'l': 'light', 'm': 'mystical', 'n': 'void', 'o': 'cosmic',
            'p': 'mystical', 'q': 'void', 'r': 'storm', 's': 'shadow', 't': 'crystal',
            'u': 'cosmic', 'v': 'void', 'w': 'storm', 'x': 'shadow', 'y': 'light', 'z': 'void'
        }
        
        # Word semantic categories for pattern selection
        self.semantic_patterns = {
            'love': ['heart', 'flowing', 'embrace'],
            'power': ['lightning', 'angular', 'dominant'],
            'peace': ['circular', 'balanced', 'gentle'],
            'money': ['crystalline', 'abundant', 'magnetic'],
            'health': ['organic', 'flowing', 'vital'],
            'protection': ['shield', 'barrier', 'defensive'],
            'wisdom': ['spiral', 'ancient', 'deep'],
            'success': ['ascending', 'radial', 'expanding'],
            'abundance': ['flowing', 'multiplying', 'rich'],
            'light': ['radial', 'burst', 'illuminating'],
            'shadow': ['angular', 'hidden', 'mysterious'],
            'dream': ['ethereal', 'floating', 'surreal'],
            'magic': ['spiral', 'mystical', 'enchanted'],
            'fire': ['flame', 'dancing', 'passionate'],
            'water': ['flowing', 'wave', 'fluid'],
            'earth': ['grounded', 'crystalline', 'stable'],
            'air': ['swirling', 'light', 'free']
        }
    
    def generate_sigil(self, phrase: str, vibe: str = 'mystical', advanced: bool = False) -> str:
        """Generate a revolutionary sigil that's deeply responsive to text content"""
        try:
            logger.info(f"🎨 Generating revolutionary sigil: '{phrase}' with vibe: {vibe}")
            
            # Deep text analysis for unique generation
            text_dna = self._analyze_text_dna(phrase)
            
            # Get enhanced style configuration
            style = self.vibe_styles.get(vibe, self.vibe_styles['mystical'])
            
            # Create ultra high-resolution canvas
            canvas_size = 2048 if advanced else self.size
            img = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Generate unique seed from phrase for reproducibility but with uniqueness
            seed = self._generate_complex_seed(phrase, vibe)
            random.seed(seed)
            np.random.seed(seed % (2**32 - 1))
            
            # Revolutionary multi-layer generation
            self._create_base_energy_field(draw, text_dna, style, canvas_size)
            self._create_semantic_structure(draw, phrase, text_dna, style, canvas_size)
            self._create_letter_manifestation(draw, phrase, text_dna, style, canvas_size)
            self._create_phrase_resonance(draw, phrase, text_dna, style, canvas_size)
            self._add_vibe_specific_patterns(draw, phrase, vibe, style, canvas_size)
            
            # Apply revolutionary effects
            if advanced:
                img = self._apply_revolutionary_effects(img, style, text_dna)
            else:
                img = self._apply_enhanced_effects(img, style, text_dna)
            
            # Convert to base64
            return self._image_to_base64(img)
            
        except Exception as e:
            logger.error(f"❌ Revolutionary sigil generation failed: {e}")
            raise
    
    def _analyze_text_dna(self, phrase: str) -> Dict:
        """Revolutionary text analysis that creates a unique DNA signature"""
        clean_phrase = ''.join(c.lower() for c in phrase if c.isalnum() or c.isspace())
        words = clean_phrase.split()
        all_chars = ''.join(clean_phrase.split())
        
        # Character frequency analysis
        char_freq = {}
        for char in all_chars:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        # Vowel/consonant patterns
        vowels = 'aeiou'
        vowel_pattern = [1 if c in vowels else 0 for c in all_chars if c.isalpha()]
        consonant_pattern = [1 if c not in vowels else 0 for c in all_chars if c.isalpha()]
        
        # Word length distribution
        word_lengths = [len(word) for word in words]
        
        # Semantic analysis
        semantic_matches = []
        for word in words:
            for key, patterns in self.semantic_patterns.items():
                if key in word.lower() or word.lower() in key:
                    semantic_matches.extend(patterns)
        
        # Energy distribution from letters
        energy_distribution = {}
        for char in all_chars:
            if char in self.letter_energies:
                energy = self.letter_energies[char]
                energy_distribution[energy] = energy_distribution.get(energy, 0) + 1
        
        # Mathematical signatures
        phrase_sum = sum(ord(c) for c in all_chars)
        phrase_product = 1
        for c in all_chars:
            phrase_product = (phrase_product * ord(c)) % 999999
        
        # Rhythm analysis
        syllable_count = self._estimate_syllables(phrase)
        rhythm_pattern = [len(word) % 5 for word in words]
        
        return {
            'char_freq': char_freq,
            'vowel_pattern': vowel_pattern,
            'consonant_pattern': consonant_pattern,
            'word_lengths': word_lengths,
            'semantic_matches': semantic_matches,
            'energy_distribution': energy_distribution,
            'phrase_sum': phrase_sum,
            'phrase_product': phrase_product,
            'syllable_count': syllable_count,
            'rhythm_pattern': rhythm_pattern,
            'unique_chars': len(set(all_chars)),
            'total_chars': len(all_chars),
            'word_count': len(words),
            'complexity_score': self._calculate_complexity_score(phrase)
        }
    
    def _estimate_syllables(self, phrase: str) -> int:
        """Estimate syllable count for rhythm analysis"""
        vowels = 'aeiouAEIOU'
        syllables = 0
        prev_was_vowel = False
        
        for char in phrase:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllables += 1
            prev_was_vowel = is_vowel
        
        return max(1, syllables)
    
    def _calculate_complexity_score(self, phrase: str) -> float:
        """Calculate a complexity score for the phrase"""
        words = phrase.split()
        unique_chars = len(set(phrase.lower()))
        total_chars = len(phrase.replace(' ', ''))
        word_variety = len(set(words))
        
        complexity = (unique_chars / max(1, total_chars)) * word_variety * len(words)
        return min(10.0, complexity)
    
    def _generate_complex_seed(self, phrase: str, vibe: str) -> int:
        """Generate a complex seed that incorporates phrase semantics"""
        # Multiple hash layers for uniqueness
        phrase_hash = hashlib.sha256(phrase.encode()).hexdigest()
        vibe_hash = hashlib.md5(vibe.encode()).hexdigest()
        combined = phrase + vibe + phrase_hash[:8] + vibe_hash[:8]
        
        final_hash = hashlib.sha512(combined.encode()).hexdigest()
        return int(final_hash[:16], 16) % (2**31)
    
    def _create_base_energy_field(self, draw: ImageDraw, text_dna: Dict, style: Dict, size: int):
        """Create the base energy field based on text DNA"""
        center = (size // 2, size // 2)
        
        # Energy rings based on character frequency
        for i, (char, freq) in enumerate(text_dna['char_freq'].items()):
            if i >= 8:  # Limit for performance
                break
                
            radius = (size // 6) + (freq * size // 40)
            angle_offset = ord(char) * 17
            
            # Multiple concentric patterns
            for ring in range(freq):
                ring_radius = radius + (ring * size // 80)
                segments = max(6, freq * 3)
                
                for segment in range(segments):
                    angle = (360 / segments) * segment + angle_offset
                    start_angle = angle - 10
                    end_angle = angle + 10
                    
                    color = style['colors'][i % len(style['colors'])]
                    width = style['stroke_width']() if callable(style['stroke_width']) else style['stroke_width']
                    
                    bbox = [center[0] - ring_radius, center[1] - ring_radius,
                           center[0] + ring_radius, center[1] + ring_radius]
                    
                    try:
                        draw.arc(bbox, start_angle, end_angle, fill=color, width=width)
                    except:
                        continue
    
    def _create_semantic_structure(self, draw: ImageDraw, phrase: str, text_dna: Dict, style: Dict, size: int):
        """Create structure based on semantic meaning"""
        center = (size // 2, size // 2)
        words = phrase.lower().split()
        
        for i, word in enumerate(words):
            if i >= 6:  # Limit complexity
                break
                
            # Position based on word characteristics
            word_value = sum(ord(c) for c in word)
            angle = (word_value * 47) % 360
            distance = (len(word) * size // 20) + (size // 8)
            
            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))
            
            # Create word-specific pattern
            if any(semantic in word for semantic in ['love', 'heart']):
                self._draw_heart_pattern(draw, (x, y), style, size // 40)
            elif any(semantic in word for semantic in ['power', 'strength']):
                self._draw_power_pattern(draw, (x, y), style, size // 40)
            elif any(semantic in word for semantic in ['peace', 'calm']):
                self._draw_peace_pattern(draw, (x, y), style, size // 40)
            elif any(semantic in word for semantic in ['money', 'wealth', 'abundance']):
                self._draw_abundance_pattern(draw, (x, y), style, size // 40)
            else:
                self._draw_generic_semantic_pattern(draw, (x, y), word, style, size // 40)
    
    def _create_letter_manifestation(self, draw: ImageDraw, phrase: str, text_dna: Dict, style: Dict, size: int):
        """Create visual manifestation of individual letters"""
        center = (size // 2, size // 2)
        unique_chars = list(set(c.lower() for c in phrase if c.isalpha()))
        
        for i, char in enumerate(unique_chars[:12]):  # Limit to 12 for performance
            char_value = ord(char)
            
            # Position based on character properties
            angle = (char_value * 23 + i * 30) % 360
            radius = (size // 6) + ((char_value % 50) * size // 200)
            
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            
            # Create character-specific symbol
            symbol_size = max(10, size // 80)
            color = style['colors'][char_value % len(style['colors'])]
            
            # Different shapes for different characters
            if char in 'aeiou':
                # Vowels get circles
                draw.ellipse([x-symbol_size, y-symbol_size, x+symbol_size, y+symbol_size], 
                           outline=color, width=2)
            elif char in 'bcdfghjklmnpqrstvwxyz':
                # Consonants get various shapes
                if char_value % 4 == 0:
                    # Square
                    draw.rectangle([x-symbol_size, y-symbol_size, x+symbol_size, y+symbol_size], 
                                 outline=color, width=2)
                elif char_value % 4 == 1:
                    # Triangle
                    points = [(x, y-symbol_size), (x-symbol_size, y+symbol_size), (x+symbol_size, y+symbol_size)]
                    draw.polygon(points, outline=color, width=2)
                elif char_value % 4 == 2:
                    # Diamond
                    points = [(x, y-symbol_size), (x+symbol_size, y), (x, y+symbol_size), (x-symbol_size, y)]
                    draw.polygon(points, outline=color, width=2)
                else:
                    # Star
                    self._draw_star(draw, (x, y), symbol_size, color, 2)
    
    def _create_phrase_resonance(self, draw: ImageDraw, phrase: str, text_dna: Dict, style: Dict, size: int):
        """Create resonance patterns based on the entire phrase"""
        center = (size // 2, size // 2)
        
        # Phrase rhythm visualization
        rhythm = text_dna['rhythm_pattern']
        syllables = text_dna['syllable_count']
        
        # Create spiral based on phrase rhythm
        angle_step = 360 / max(1, syllables * 3)
        radius_start = size // 12
        radius_growth = size // (syllables * 4) if syllables > 0 else size // 20
        
        for i in range(syllables * 6):
            angle = i * angle_step + (text_dna['phrase_sum'] % 360)
            radius = radius_start + (i * radius_growth)
            
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            
            # Size varies with complexity
            point_size = max(2, (text_dna['complexity_score'] * 3) // (i % 5 + 1))
            color_index = (text_dna['phrase_product'] + i) % len(style['colors'])
            color = style['colors'][color_index]
            
            draw.ellipse([x-point_size, y-point_size, x+point_size, y+point_size], 
                        fill=color)
            
            # Connect to create flow
            if i > 0:
                prev_angle = (i-1) * angle_step + (text_dna['phrase_sum'] % 360)
                prev_radius = radius_start + ((i-1) * radius_growth)
                prev_x = center[0] + prev_radius * math.cos(math.radians(prev_angle))
                prev_y = center[1] + prev_radius * math.sin(math.radians(prev_angle))
                
                width = max(1, style['stroke_width']() if callable(style['stroke_width']) else style['stroke_width'] // 2)
                draw.line([(prev_x, prev_y), (x, y)], fill=color, width=width)
    
    def _add_vibe_specific_patterns(self, draw: ImageDraw, phrase: str, vibe: str, style: Dict, size: int):
        """Add vibe-specific patterns that interact with text DNA"""
        center = (size // 2, size // 2)
        patterns = style.get('patterns', ['generic'])
        
        for pattern in patterns:
            if pattern == 'sacred_geometry':
                self._add_sacred_geometry_enhanced(draw, center, style, size, phrase)
            elif pattern == 'constellation':
                self._add_constellation_enhanced(draw, center, style, size, phrase)
            elif pattern == 'flowing':
                self._add_flowing_enhanced(draw, center, style, size, phrase)
            elif pattern == 'crystalline':
                self._add_crystalline_enhanced(draw, center, style, size, phrase)
            elif pattern == 'lightning':
                self._add_lightning_enhanced(draw, center, style, size, phrase)
            elif pattern == 'spiral_void':
                self._add_spiral_void_enhanced(draw, center, style, size, phrase)
    
    def _draw_heart_pattern(self, draw: ImageDraw, pos: Tuple[int, int], style: Dict, size: int):
        """Draw a heart pattern for love-related words"""
        x, y = pos
        color = random.choice(style['colors'])
        
        # Simple heart shape using arcs and lines
        draw.arc([x-size, y-size//2, x, y+size//2], 0, 180, fill=color, width=2)
        draw.arc([x, y-size//2, x+size, y+size//2], 0, 180, fill=color, width=2)
        draw.line([(x-size, y), (x, y+size)], fill=color, width=2)
        draw.line([(x+size, y), (x, y+size)], fill=color, width=2)
    
    def _draw_power_pattern(self, draw: ImageDraw, pos: Tuple[int, int], style: Dict, size: int):
        """Draw a power pattern for strength-related words"""
        x, y = pos
        color = random.choice(style['colors'])
        
        # Lightning bolt pattern
        points = [
            (x, y-size), (x+size//2, y), (x-size//2, y),
            (x, y+size), (x-size//2, y), (x+size//2, y)
        ]
        for i in range(len(points)-1):
            draw.line([points[i], points[i+1]], fill=color, width=3)
    
    def _draw_peace_pattern(self, draw: ImageDraw, pos: Tuple[int, int], style: Dict, size: int):
        """Draw a peace pattern for calm-related words"""
        x, y = pos
        color = random.choice(style['colors'])
        
        # Concentric circles for peace
        for i in range(3):
            radius = size // (i + 1)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        outline=color, width=1)
    
    def _draw_abundance_pattern(self, draw: ImageDraw, pos: Tuple[int, int], style: Dict, size: int):
        """Draw an abundance pattern for wealth-related words"""
        x, y = pos
        color = random.choice(style['colors'])
        
        # Expanding rays for abundance
        for angle in range(0, 360, 45):
            end_x = x + size * math.cos(math.radians(angle))
            end_y = y + size * math.sin(math.radians(angle))
            draw.line([(x, y), (end_x, end_y)], fill=color, width=2)
    
    def _draw_generic_semantic_pattern(self, draw: ImageDraw, pos: Tuple[int, int], word: str, style: Dict, size: int):
        """Draw a pattern based on word characteristics"""
        x, y = pos
        color = random.choice(style['colors'])
        word_sum = sum(ord(c) for c in word)
        
        # Pattern varies by word characteristics
        if word_sum % 4 == 0:
            # Spiral
            for i in range(8):
                angle = i * 45
                radius = size * (i / 8)
                end_x = x + radius * math.cos(math.radians(angle))
                end_y = y + radius * math.sin(math.radians(angle))
                draw.line([(x, y), (end_x, end_y)], fill=color, width=1)
        elif word_sum % 4 == 1:
            # Cross
            draw.line([(x-size, y), (x+size, y)], fill=color, width=2)
            draw.line([(x, y-size), (x, y+size)], fill=color, width=2)
        elif word_sum % 4 == 2:
            # Hexagon
            points = []
            for i in range(6):
                angle = i * 60
                px = x + size * math.cos(math.radians(angle))
                py = y + size * math.sin(math.radians(angle))
                points.append((px, py))
            draw.polygon(points, outline=color, width=2)
        else:
            # Star
            self._draw_star(draw, (x, y), size, color, 2)
    
    def _draw_star(self, draw: ImageDraw, pos: Tuple[int, int], size: int, color: Tuple[int, int, int], width: int):
        """Draw a star pattern"""
        x, y = pos
        points = []
        for i in range(10):
            angle = i * 36
            radius = size if i % 2 == 0 else size // 2
            px = x + radius * math.cos(math.radians(angle))
            py = y + radius * math.sin(math.radians(angle))
            points.append((px, py))
        
        if len(points) > 2:
            draw.polygon(points, outline=color, width=width)
    
    def _add_sacred_geometry_enhanced(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str):
        """Enhanced sacred geometry based on phrase characteristics"""
        phrase_sum = sum(ord(c) for c in phrase)
        
        # Flower of Life variation based on phrase
        petals = max(6, (phrase_sum % 12) + 6)
        radius = size // 8
        
        for i in range(petals):
            angle = (360 / petals) * i + (phrase_sum % 360)
            x = center[0] + radius * math.cos(math.radians(angle)) // 2
            y = center[1] + radius * math.sin(math.radians(angle)) // 2
            
            color = style['colors'][(phrase_sum + i) % len(style['colors'])]
            petal_radius = radius // 3 + (phrase_sum % 20)
            
            draw.ellipse([x-petal_radius, y-petal_radius, x+petal_radius, y+petal_radius], 
                        outline=color, width=2)
    
    def _add_constellation_enhanced(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str):
        """Enhanced constellation pattern based on phrase"""
        words = phrase.split()
        
        # Create constellation based on word count and characteristics
        for i, word in enumerate(words[:8]):
            word_value = sum(ord(c) for c in word)
            angle = (word_value * 47) % 360
            radius = size // 4 + (len(word) * size // 60)
            
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            
            # Star size based on word importance
            star_size = max(size // 100, len(word) * size // 200)
            color = style['colors'][word_value % len(style['colors'])]
            
            self._draw_star(draw, (x, y), star_size, color, 2)
            
            # Connect stars based on word relationships
            if i > 0:
                prev_word = words[i-1]
                prev_word_value = sum(ord(c) for c in prev_word)
                prev_angle = (prev_word_value * 47) % 360
                prev_radius = size // 4 + (len(prev_word) * size // 60)
                
                prev_x = center[0] + prev_radius * math.cos(math.radians(prev_angle))
                prev_y = center[1] + prev_radius * math.sin(math.radians(prev_angle))
                
                # Connect if words have similar characteristics
                if abs(len(word) - len(prev_word)) <= 2:
                    draw.line([(prev_x, prev_y), (x, y)], fill=color, width=1)
    
    def _add_flowing_enhanced(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str):
        """Enhanced flowing pattern based on phrase rhythm"""
        phrase_chars = [c for c in phrase.lower() if c.isalpha()]
        
        if not phrase_chars:
            return
        
        # Create flowing lines based on character sequence
        points = []
        for i, char in enumerate(phrase_chars[:20]):  # Limit for performance
            char_value = ord(char)
            angle = (char_value * 23 + i * 15) % 360
            radius = (size // 8) + (i * size // 100) + ((char_value % 30) - 15)
            
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            points.append((x, y))
        
        # Draw flowing lines connecting the points
        if len(points) > 1:
            for i in range(len(points) - 1):
                color = style['colors'][i % len(style['colors'])]
                width = max(1, style['stroke_width']() if callable(style['stroke_width']) else style['stroke_width'])
                draw.line([points[i], points[i + 1]], fill=color, width=width)
                
                # Add curved variations
                if i % 3 == 0 and i < len(points) - 2:
                    mid_x = (points[i][0] + points[i + 1][0]) // 2 + random.randint(-20, 20)
                    mid_y = (points[i][1] + points[i + 1][1]) // 2 + random.randint(-20, 20)
                    draw.line([points[i], (mid_x, mid_y)], fill=color, width=width//2)
                    draw.line([(mid_x, mid_y), points[i + 1]], fill=color, width=width//2)
    
    def _add_crystalline_enhanced(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str):
        """Enhanced crystalline pattern based on phrase structure"""
        words = phrase.split()
        
        # Create crystal facets based on word structure
        for i, word in enumerate(words[:6]):
            word_value = sum(ord(c) for c in word)
            sides = max(3, len(word) % 8 + 3)
            
            angle_offset = word_value % 360
            radius = size // 6 + (len(word) * size // 40)
            
            # Create polygon for crystal facet
            points = []
            for j in range(sides):
                angle = (360 / sides) * j + angle_offset
                x = center[0] + radius * math.cos(math.radians(angle))
                y = center[1] + radius * math.sin(math.radians(angle))
                points.append((x, y))
            
            if len(points) > 2:
                color = style['colors'][word_value % len(style['colors'])]
                draw.polygon(points, outline=color, width=2)
                
                # Add internal structure
                for point in points:
                    draw.line([center, point], fill=color, width=1)
    
    def _add_lightning_enhanced(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str):
        """Enhanced lightning pattern based on phrase energy"""
        words = phrase.split()
        
        for i, word in enumerate(words[:5]):
            word_value = sum(ord(c) for c in word)
            start_angle = (word_value * 37) % 360
            
            # Create jagged lightning path
            current_x, current_y = center
            current_angle = start_angle
            distance_per_step = size // 20
            
            points = [(current_x, current_y)]
            
            for step in range(len(word)):
                # Random direction change
                angle_change = random.randint(-45, 45)
                current_angle += angle_change
                
                current_x += distance_per_step * math.cos(math.radians(current_angle))
                current_y += distance_per_step * math.sin(math.radians(current_angle))
                points.append((current_x, current_y))
            
            # Draw lightning bolt
            color = style['colors'][word_value % len(style['colors'])]
            for j in range(len(points) - 1):
                width = max(2, style['stroke_width']() if callable(style['stroke_width']) else style['stroke_width'])
                draw.line([points[j], points[j + 1]], fill=color, width=width)
    
    def _add_spiral_void_enhanced(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str):
        """Enhanced spiral void pattern based on phrase depth"""
        phrase_sum = sum(ord(c) for c in phrase)
        
        # Create multiple spirals based on phrase characteristics
        spirals = max(2, len(phrase.split()) // 2)
        
        for spiral_i in range(spirals):
            spiral_offset = (phrase_sum * (spiral_i + 1)) % 360
            
            points = []
            for i in range(50):
                angle = i * 7.2 + spiral_offset  # 7.2 degrees per step
                radius = (size // 20) + (i * size // 200)
                
                x = center[0] + radius * math.cos(math.radians(angle))
                y = center[1] + radius * math.sin(math.radians(angle))
                points.append((x, y))
            
            # Draw spiral
            if len(points) > 1:
                color = style['colors'][(phrase_sum + spiral_i) % len(style['colors'])]
                for j in range(len(points) - 1):
                    alpha = max(50, 255 - (j * 4))  # Fade as spiral goes out
                    fade_color = (*color, alpha) if len(color) == 3 else color
                    width = max(1, 4 - (j // 15))
                    draw.line([points[j], points[j + 1]], fill=color, width=width)
    
    def _apply_enhanced_effects(self, img: Image.Image, style: Dict, text_dna: Dict) -> Image.Image:
        """Apply enhanced visual effects based on text characteristics"""
        if style.get('glow_intensity', 0) > 0:
            # Multi-layer glow based on complexity
            layers = min(5, int(text_dna['complexity_score']))
            
            result = img.copy()
            for layer in range(layers):
                blur_radius = (layer + 1) * 2
                glow = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                
                enhancer = ImageEnhance.Brightness(glow)
                intensity = style['glow_intensity'] * (0.8 ** layer)
                glow = enhancer.enhance(intensity)
                
                result = Image.alpha_composite(result, glow)
            
            return result
        
        return img
    
    def _apply_revolutionary_effects(self, img: Image.Image, style: Dict, text_dna: Dict) -> Image.Image:
        """Apply revolutionary visual effects for advanced generation"""
        base_img = img.copy()
        
        # Multiple effect layers
        effects = ['glow', 'contrast', 'saturation', 'sharpness']
        
        for effect in effects:
            if effect == 'glow' and style.get('glow_intensity', 0) > 0:
                # Sophisticated multi-radius glow
                for radius in [2, 4, 8, 12]:
                    glow = base_img.filter(ImageFilter.GaussianBlur(radius=radius))
                    enhancer = ImageEnhance.Brightness(glow)
                    intensity = style['glow_intensity'] * (0.6 ** (radius / 4))
                    glow = enhancer.enhance(intensity)
                    base_img = Image.alpha_composite(base_img, glow)
            
            elif effect == 'contrast':
                enhancer = ImageEnhance.Contrast(base_img)
                contrast_factor = 1.0 + (text_dna['complexity_score'] / 20)
                base_img = enhancer.enhance(contrast_factor)
            
            elif effect == 'saturation':
                enhancer = ImageEnhance.Color(base_img)
                saturation_factor = 1.0 + (text_dna['unique_chars'] / 50)
                base_img = enhancer.enhance(saturation_factor)
            
            elif effect == 'sharpness':
                enhancer = ImageEnhance.Sharpness(base_img)
                sharpness_factor = 1.0 + (len(text_dna['semantic_matches']) / 20)
                base_img = enhancer.enhance(sharpness_factor)
        
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

# Initialize revolutionary generator
generator = RevolutionarySigilGenerator()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'sigilcraft-revolutionary-backend',
        'version': '3.0.0',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'revolutionary_generation': True,
            'text_dna_analysis': True,
            'semantic_patterns': True,
            'ultra_unique_output': True,
            'phrase_responsive': True
        }
    })

@app.route('/generate', methods=['POST'])
def generate_sigil():
    """Revolutionary sigil generation endpoint"""
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
        
        # Generate revolutionary sigil
        logger.info(f"🎨 Generating revolutionary sigil: '{phrase}' ({vibe}) [Advanced: {advanced}]")
        
        sigil_image = generator.generate_sigil(phrase, vibe, advanced)
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Revolutionary sigil generated in {duration:.2f}s")
        
        return jsonify({
            'success': True,
            'image': sigil_image,
            'phrase': phrase,
            'vibe': vibe,
            'advanced': advanced,
            'metadata': {
                'generation_time': duration,
                'timestamp': datetime.now().isoformat(),
                'version': '3.0.0',
                'revolutionary': True
            },
            'message': f'Revolutionary text-responsive sigil manifested for: "{phrase}"'
        })
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"❌ Revolutionary generation failed after {duration:.2f}s: {e}")
        
        return jsonify({
            'success': False,
            'error': str(e),
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/vibes', methods=['GET'])
def get_available_vibes():
    """Get list of available energy vibes with enhanced descriptions"""
    vibes = list(generator.vibe_styles.keys())
    
    return jsonify({
        'success': True,
        'vibes': vibes,
        'count': len(vibes),
        'descriptions': {
            'mystical': 'Ancient wisdom & sacred geometry',
            'cosmic': 'Universal connection & stellar patterns',
            'elemental': 'Natural forces & organic flow',
            'crystal': 'Clarity, healing & prismatic light',
            'shadow': 'Hidden power & angular mystery',
            'light': 'Pure radiance & illuminating energy',
            'storm': 'Raw electric chaos & lightning',
            'void': 'Infinite potential & spiral depth'
        },
        'features': {
            'text_responsive': True,
            'semantic_analysis': True,
            'unique_per_phrase': True,
            'revolutionary_algorithms': True
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
    print("🔮 Starting Revolutionary Sigilcraft Python Backend...")
    print(f"📦 PIL/Pillow version: {Image.__version__}")
    print(f"🔢 NumPy available: {'✅' if 'numpy' in sys.modules or 'np' in globals() else '❌'}")
    print("🎨 Revolutionary text-responsive sigil generation ready!")
    print("✨ Features: Deep text analysis, semantic patterns, unique algorithms")
    
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
