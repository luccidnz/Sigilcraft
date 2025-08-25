
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
app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Request-ID"],
        "supports_credentials": True
    }
})

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
        
        # Ultra-advanced text DNA analysis
        self.word_archetypes = {
            'love': {'energy': 'heart', 'geometry': 'flowing', 'density': 'warm', 'pattern': 'embrace'},
            'power': {'energy': 'force', 'geometry': 'angular', 'density': 'intense', 'pattern': 'domination'},
            'peace': {'energy': 'calm', 'geometry': 'circular', 'density': 'gentle', 'pattern': 'harmony'},
            'money': {'energy': 'magnetic', 'geometry': 'crystalline', 'density': 'abundant', 'pattern': 'attraction'},
            'health': {'energy': 'vital', 'geometry': 'organic', 'density': 'flowing', 'pattern': 'renewal'},
            'protection': {'energy': 'shield', 'geometry': 'barrier', 'density': 'strong', 'pattern': 'defensive'},
            'wisdom': {'energy': 'ancient', 'geometry': 'spiral', 'density': 'deep', 'pattern': 'knowing'},
            'success': {'energy': 'ascending', 'geometry': 'upward', 'density': 'expanding', 'pattern': 'achievement'},
            'abundance': {'energy': 'overflowing', 'geometry': 'radiating', 'density': 'rich', 'pattern': 'prosperity'},
            'light': {'energy': 'radiant', 'geometry': 'burst', 'density': 'bright', 'pattern': 'illumination'},
            'shadow': {'energy': 'hidden', 'geometry': 'veiled', 'density': 'mysterious', 'pattern': 'concealment'},
            'dream': {'energy': 'ethereal', 'geometry': 'fluid', 'density': 'soft', 'pattern': 'vision'},
            'magic': {'energy': 'mystical', 'geometry': 'arcane', 'density': 'enchanted', 'pattern': 'manifestation'},
            'fire': {'energy': 'passionate', 'geometry': 'dancing', 'density': 'fierce', 'pattern': 'transformation'},
            'water': {'energy': 'flowing', 'geometry': 'wave', 'density': 'fluid', 'pattern': 'emotion'},
            'earth': {'energy': 'grounded', 'geometry': 'stable', 'density': 'solid', 'pattern': 'foundation'},
            'air': {'energy': 'free', 'geometry': 'swirling', 'density': 'light', 'pattern': 'thought'},
            'consciousness': {'energy': 'aware', 'geometry': 'infinite', 'density': 'expansive', 'pattern': 'awakening'},
            'manifestation': {'energy': 'creative', 'geometry': 'forming', 'density': 'materializing', 'pattern': 'creation'}
        }
        
        # Character energy mappings with expanded meanings
        self.char_energies = {
            'a': {'flow': 'open', 'intensity': 'gentle', 'direction': 'expanding'},
            'b': {'flow': 'blocked', 'intensity': 'strong', 'direction': 'contained'},
            'c': {'flow': 'curved', 'intensity': 'moderate', 'direction': 'enclosing'},
            'd': {'flow': 'decisive', 'intensity': 'firm', 'direction': 'forward'},
            'e': {'flow': 'ethereal', 'intensity': 'light', 'direction': 'upward'},
            'f': {'flow': 'fierce', 'intensity': 'intense', 'direction': 'cutting'},
            'g': {'flow': 'grounded', 'intensity': 'stable', 'direction': 'downward'},
            'h': {'flow': 'hidden', 'intensity': 'mysterious', 'direction': 'inward'},
            'i': {'flow': 'intense', 'intensity': 'focused', 'direction': 'piercing'},
            'j': {'flow': 'joyful', 'intensity': 'vibrant', 'direction': 'dancing'},
            'k': {'flow': 'kinetic', 'intensity': 'sharp', 'direction': 'striking'},
            'l': {'flow': 'flowing', 'intensity': 'smooth', 'direction': 'liquid'},
            'm': {'flow': 'mothering', 'intensity': 'nurturing', 'direction': 'embracing'},
            'n': {'flow': 'neutral', 'intensity': 'balanced', 'direction': 'centering'},
            'o': {'flow': 'open', 'intensity': 'complete', 'direction': 'circular'},
            'p': {'flow': 'powerful', 'intensity': 'strong', 'direction': 'projecting'},
            'q': {'flow': 'questioning', 'intensity': 'seeking', 'direction': 'spiraling'},
            'r': {'flow': 'rough', 'intensity': 'turbulent', 'direction': 'rolling'},
            's': {'flow': 'serpentine', 'intensity': 'sinuous', 'direction': 'winding'},
            't': {'flow': 'tall', 'intensity': 'structured', 'direction': 'vertical'},
            'u': {'flow': 'unified', 'intensity': 'harmonious', 'direction': 'joining'},
            'v': {'flow': 'victorious', 'intensity': 'triumphant', 'direction': 'ascending'},
            'w': {'flow': 'wavy', 'intensity': 'undulating', 'direction': 'oscillating'},
            'x': {'flow': 'crossing', 'intensity': 'intersecting', 'direction': 'multiplying'},
            'y': {'flow': 'yearning', 'intensity': 'reaching', 'direction': 'striving'},
            'z': {'flow': 'zigzag', 'intensity': 'electric', 'direction': 'energetic'}
        }
    
    def generate_sigil(self, phrase: str, vibe: str = 'mystical', advanced: bool = False) -> str:
        """Generate ultra-unique sigils with extreme text responsiveness"""
        try:
            logger.info(f"🎨 Generating ultra-revolutionary sigil: '{phrase}' with vibe: {vibe}")
            
            # Ultra-deep text DNA analysis
            text_dna = self._ultra_analyze_text_dna(phrase)
            
            # Get style configuration
            style = self.vibe_styles.get(vibe, self.vibe_styles['mystical'])
            
            # Create ultra high-resolution canvas
            canvas_size = 2048 if advanced else self.size
            img = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Generate ultra-unique seed with phrase specificity
            seed = self._generate_ultra_unique_seed(phrase, vibe, text_dna)
            random.seed(seed)
            np.random.seed(seed % (2**32 - 1))
            
            # Multi-layer revolutionary generation
            self._create_text_essence_field(draw, text_dna, style, canvas_size, phrase)
            self._create_phrase_geometry(draw, phrase, text_dna, style, canvas_size)
            self._create_word_manifestations(draw, phrase, text_dna, style, canvas_size)
            self._create_character_symphony(draw, phrase, text_dna, style, canvas_size)
            self._create_vibe_resonance(draw, phrase, vibe, style, canvas_size, text_dna)
            self._create_unique_signature(draw, phrase, vibe, style, canvas_size, text_dna)
            
            # Apply revolutionary effects
            if advanced:
                img = self._apply_ultra_effects(img, style, text_dna, phrase)
            else:
                img = self._apply_enhanced_effects(img, style, text_dna, phrase)
            
            # Convert to base64
            return self._image_to_base64(img)
            
        except Exception as e:
            logger.error(f"❌ Ultra-revolutionary sigil generation failed: {e}")
            raise
    
    def _ultra_analyze_text_dna(self, phrase: str) -> Dict:
        """Ultra-advanced text analysis creating unique DNA signatures"""
        clean_phrase = ''.join(c.lower() for c in phrase if c.isalnum() or c.isspace())
        words = clean_phrase.split()
        all_chars = ''.join(clean_phrase.split())
        
        # Character frequency with position weighting
        char_freq_weighted = {}
        for i, char in enumerate(all_chars):
            weight = 1 + (i / len(all_chars))  # Position importance
            char_freq_weighted[char] = char_freq_weighted.get(char, 0) + weight
        
        # Phonetic analysis
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        vowel_positions = [i for i, c in enumerate(all_chars) if c in vowels]
        consonant_positions = [i for i, c in enumerate(all_chars) if c in consonants]
        
        # Word relationship analysis
        word_relationships = []
        for i, word1 in enumerate(words):
            for j, word2 in enumerate(words[i+1:], i+1):
                similarity = len(set(word1) & set(word2)) / len(set(word1) | set(word2)) if set(word1) | set(word2) else 0
                word_relationships.append((i, j, similarity))
        
        # Semantic depth analysis
        semantic_layers = []
        for word in words:
            for archetype, properties in self.word_archetypes.items():
                if archetype in word.lower() or any(part in archetype for part in word.lower().split()):
                    semantic_layers.append({
                        'word': word,
                        'archetype': archetype,
                        'properties': properties
                    })
        
        # Character energy flow analysis
        energy_flow_pattern = []
        for char in all_chars:
            if char in self.char_energies:
                energy_flow_pattern.append(self.char_energies[char])
        
        # Mathematical signatures with advanced calculations
        phrase_hash_md5 = hashlib.md5(phrase.encode()).hexdigest()
        phrase_hash_sha1 = hashlib.sha1(phrase.encode()).hexdigest()
        phrase_hash_sha256 = hashlib.sha256(phrase.encode()).hexdigest()
        
        # Complexity and uniqueness scores
        uniqueness_score = len(set(all_chars)) / len(all_chars) if all_chars else 0
        complexity_score = (len(words) * len(set(all_chars)) * len(semantic_layers)) / max(1, len(all_chars))
        
        return {
            'char_freq_weighted': char_freq_weighted,
            'vowel_positions': vowel_positions,
            'consonant_positions': consonant_positions,
            'word_relationships': word_relationships,
            'semantic_layers': semantic_layers,
            'energy_flow_pattern': energy_flow_pattern,
            'phrase_hash_md5': phrase_hash_md5,
            'phrase_hash_sha1': phrase_hash_sha1,
            'phrase_hash_sha256': phrase_hash_sha256,
            'uniqueness_score': uniqueness_score,
            'complexity_score': complexity_score,
            'word_count': len(words),
            'char_count': len(all_chars),
            'unique_chars': len(set(all_chars)),
            'phrase_length': len(phrase)
        }
    
    def _generate_ultra_unique_seed(self, phrase: str, vibe: str, text_dna: Dict) -> int:
        """Generate ultra-unique seed incorporating all text characteristics"""
        # Multiple hash layers with text-specific data
        base_data = f"{phrase}|{vibe}|{text_dna['uniqueness_score']:.6f}|{text_dna['complexity_score']:.6f}"
        
        # Add semantic layer data
        semantic_signature = ''.join([layer['archetype'] for layer in text_dna['semantic_layers']])
        
        # Add energy flow signature
        energy_signature = ''.join([str(hash(str(e))) for e in text_dna['energy_flow_pattern']])
        
        # Combine all data
        combined_data = f"{base_data}|{semantic_signature}|{energy_signature}|{text_dna['phrase_hash_sha256']}"
        
        # Generate final unique hash
        final_hash = hashlib.sha512(combined_data.encode()).hexdigest()
        return int(final_hash[:16], 16) % (2**31)
    
    def _create_text_essence_field(self, draw: ImageDraw, text_dna: Dict, style: Dict, size: int, phrase: str):
        """Create the foundational energy field based on text essence"""
        center = (size // 2, size // 2)
        
        # Create unique field based on text characteristics
        for i, (char, weight) in enumerate(text_dna['char_freq_weighted'].items()):
            if i >= 12:  # Limit for performance
                break
                
            char_energy = self.char_energies.get(char, {'flow': 'neutral', 'intensity': 'moderate', 'direction': 'centered'})
            
            # Position based on character energy and phrase position
            angle_base = (ord(char) * 23 + hash(phrase) % 360) % 360
            radius_base = (size // 8) + (weight * size // 60)
            
            # Create energy rings with character-specific properties
            ring_count = max(1, int(weight))
            for ring in range(ring_count):
                radius = radius_base + (ring * size // 100)
                segments = max(6, int(weight * 4) + ring)
                
                # Direction-based angle modification
                direction_modifier = {'inward': -15, 'outward': 15, 'circular': 0}.get(char_energy['direction'][:7], 0)
                
                for segment in range(segments):
                    angle = angle_base + (360 / segments) * segment + direction_modifier
                    
                    # Intensity affects stroke width and color
                    intensity_factor = {'gentle': 0.5, 'moderate': 1.0, 'strong': 1.5, 'intense': 2.0}.get(char_energy['intensity'], 1.0)
                    stroke_width = max(1, int(style['stroke_multiplier'] * intensity_factor * 3))
                    
                    # Color selection based on character and position
                    color_index = (ord(char) + ring + segment) % len(style['colors'])
                    base_color = style['colors'][color_index]
                    
                    # Flow affects the drawing pattern
                    if char_energy['flow'] == 'curved':
                        self._draw_curved_arc(draw, center, radius, angle, stroke_width, base_color, size)
                    elif char_energy['flow'] == 'angular':
                        self._draw_angular_pattern(draw, center, radius, angle, stroke_width, base_color, size)
                    else:
                        self._draw_flowing_line(draw, center, radius, angle, stroke_width, base_color, size)
    
    def _create_phrase_geometry(self, draw: ImageDraw, phrase: str, text_dna: Dict, style: Dict, size: int):
        """Create geometric patterns based on phrase structure"""
        center = (size // 2, size // 2)
        words = phrase.lower().split()
        
        # Create unique geometry for each word based on its semantic properties
        for i, word in enumerate(words[:8]):  # Limit for performance
            word_semantic = None
            for layer in text_dna['semantic_layers']:
                if layer['word'].lower() == word:
                    word_semantic = layer['properties']
                    break
            
            if not word_semantic:
                # Default properties for non-semantic words
                word_semantic = {
                    'energy': 'neutral',
                    'geometry': 'circular',
                    'density': 'moderate',
                    'pattern': 'simple'
                }
            
            # Position based on word characteristics and phrase position
            word_hash = hash(word + phrase)
            angle = (word_hash * 47 + i * 45) % 360
            distance = (len(word) * size // 25) + (size // 6) + (i * size // 40)
            
            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))
            
            # Create word-specific geometric pattern
            pattern_size = max(size // 60, len(word) * size // 120)
            color = style['colors'][(word_hash + i) % len(style['colors'])]
            
            if word_semantic['geometry'] == 'flowing':
                self._draw_flowing_mandala(draw, (x, y), pattern_size, word, color, style)
            elif word_semantic['geometry'] == 'angular':
                self._draw_angular_crystal(draw, (x, y), pattern_size, word, color, style)
            elif word_semantic['geometry'] == 'spiral':
                self._draw_semantic_spiral(draw, (x, y), pattern_size, word, color, style)
            elif word_semantic['geometry'] == 'radiating':
                self._draw_radiant_burst(draw, (x, y), pattern_size, word, color, style)
            else:
                self._draw_unique_symbol(draw, (x, y), pattern_size, word, color, style, word_semantic)
    
    def _create_word_manifestations(self, draw: ImageDraw, phrase: str, text_dna: Dict, style: Dict, size: int):
        """Create specific manifestations for each word"""
        center = (size // 2, size // 2)
        words = phrase.split()
        
        for i, word in enumerate(words[:6]):
            # Find semantic properties
            semantic_props = None
            for layer in text_dna['semantic_layers']:
                if layer['word'].lower() == word.lower():
                    semantic_props = layer
                    break
            
            if semantic_props:
                # Create archetype-specific manifestation
                archetype = semantic_props['archetype']
                properties = semantic_props['properties']
                
                # Position based on word energy
                word_energy = sum(ord(c) for c in word.lower())
                angle = (word_energy * 31 + i * 60) % 360
                radius = (size // 4) + ((word_energy % 100) * size // 300)
                
                x = center[0] + radius * math.cos(math.radians(angle))
                y = center[1] + radius * math.sin(math.radians(angle))
                
                # Draw archetype-specific pattern
                if archetype == 'love':
                    self._draw_love_manifestation(draw, (x, y), size // 50, style, word)
                elif archetype == 'power':
                    self._draw_power_manifestation(draw, (x, y), size // 50, style, word)
                elif archetype == 'abundance':
                    self._draw_abundance_manifestation(draw, (x, y), size // 50, style, word)
                elif archetype == 'consciousness':
                    self._draw_consciousness_manifestation(draw, (x, y), size // 50, style, word)
                else:
                    self._draw_generic_manifestation(draw, (x, y), size // 50, style, word, archetype)
    
    def _create_character_symphony(self, draw: ImageDraw, phrase: str, text_dna: Dict, style: Dict, size: int):
        """Create a symphony of individual character energies"""
        center = (size // 2, size // 2)
        all_chars = ''.join(c.lower() for c in phrase if c.isalpha())
        
        # Create character-specific energy patterns
        for i, char in enumerate(all_chars[:20]):  # Limit for performance
            char_energy = self.char_energies.get(char, {'flow': 'neutral', 'intensity': 'moderate', 'direction': 'centered'})
            
            # Position in expanding spiral based on character position in phrase
            spiral_angle = i * 23  # Golden angle for natural spiral
            spiral_radius = (size // 12) + (i * size // 80)
            
            # Modify based on character energy
            if char_energy['direction'] == 'upward':
                spiral_radius *= 0.8
                spiral_angle -= 30
            elif char_energy['direction'] == 'downward':
                spiral_radius *= 1.2
                spiral_angle += 30
            elif char_energy['direction'] == 'inward':
                spiral_radius *= 0.6
            elif char_energy['direction'] == 'outward':
                spiral_radius *= 1.4
            
            x = center[0] + spiral_radius * math.cos(math.radians(spiral_angle))
            y = center[1] + spiral_radius * math.sin(math.radians(spiral_angle))
            
            # Draw character-specific symbol
            symbol_size = max(3, size // 120)
            color = style['colors'][(ord(char) + i) % len(style['colors'])]
            
            # Symbol shape based on character properties
            if char_energy['flow'] == 'flowing':
                self._draw_flowing_symbol(draw, (x, y), symbol_size, color, char)
            elif char_energy['flow'] == 'angular':
                self._draw_angular_symbol(draw, (x, y), symbol_size, color, char)
            elif char_energy['flow'] == 'curved':
                self._draw_curved_symbol(draw, (x, y), symbol_size, color, char)
            else:
                self._draw_basic_symbol(draw, (x, y), symbol_size, color, char, char_energy)
    
    def _create_vibe_resonance(self, draw: ImageDraw, phrase: str, vibe: str, style: Dict, size: int, text_dna: Dict):
        """Create vibe-specific resonance patterns that interact with text"""
        center = (size // 2, size // 2)
        
        # Get vibe-specific parameters
        geometry_type = style['geometry_type']
        energy_flow = style['energy_flow']
        pattern_scale = style['pattern_scale']
        
        # Create base resonance pattern
        if geometry_type == 'stellar':
            self._create_stellar_resonance(draw, center, style, size, phrase, text_dna)
        elif geometry_type == 'natural':
            self._create_natural_resonance(draw, center, style, size, phrase, text_dna)
        elif geometry_type == 'angular':
            self._create_crystal_resonance(draw, center, style, size, phrase, text_dna)
        elif geometry_type == 'curved':
            self._create_mystic_resonance(draw, center, style, size, phrase, text_dna)
        elif geometry_type == 'radial':
            self._create_radial_resonance(draw, center, style, size, phrase, text_dna)
        elif geometry_type == 'electric':
            self._create_electric_resonance(draw, center, style, size, phrase, text_dna)
        elif geometry_type == 'jagged':
            self._create_shadow_resonance(draw, center, style, size, phrase, text_dna)
        elif geometry_type == 'impossible':
            self._create_void_resonance(draw, center, style, size, phrase, text_dna)
    
    def _create_unique_signature(self, draw: ImageDraw, phrase: str, vibe: str, style: Dict, size: int, text_dna: Dict):
        """Create a unique signature that makes each sigil completely distinct"""
        center = (size // 2, size // 2)
        
        # Create phrase-specific signature pattern
        signature_hash = hashlib.sha256((phrase + vibe).encode()).hexdigest()
        signature_data = [int(signature_hash[i:i+2], 16) for i in range(0, min(20, len(signature_hash)), 2)]
        
        # Draw signature pattern in center
        signature_radius = size // 20
        for i, data_byte in enumerate(signature_data):
            angle = (i * 36) + (data_byte % 360)  # 10 points max
            radius = signature_radius + (data_byte % 30)
            
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            
            # Connect to center with unique pattern
            color = style['colors'][data_byte % len(style['colors'])]
            width = max(1, (data_byte % 5) + 1)
            
            # Create signature connection
            if data_byte % 3 == 0:
                draw.line([center, (x, y)], fill=color, width=width)
            elif data_byte % 3 == 1:
                # Curved connection
                mid_x = center[0] + (x - center[0]) // 2 + ((data_byte % 40) - 20)
                mid_y = center[1] + (y - center[1]) // 2 + ((data_byte % 40) - 20)
                draw.line([center, (mid_x, mid_y)], fill=color, width=width)
                draw.line([(mid_x, mid_y), (x, y)], fill=color, width=width)
            else:
                # Dot pattern
                dot_size = max(2, data_byte % 8)
                draw.ellipse([x-dot_size, y-dot_size, x+dot_size, y+dot_size], fill=color)
    
    # Helper drawing methods for specific patterns
    def _draw_curved_arc(self, draw: ImageDraw, center: Tuple[int, int], radius: int, angle: float, width: int, color: Tuple[int, int, int], size: int):
        """Draw curved arc pattern"""
        start_angle = angle - 15
        end_angle = angle + 15
        bbox = [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius]
        try:
            draw.arc(bbox, start_angle, end_angle, fill=color, width=width)
        except:
            pass
    
    def _draw_angular_pattern(self, draw: ImageDraw, center: Tuple[int, int], radius: int, angle: float, width: int, color: Tuple[int, int, int], size: int):
        """Draw angular pattern"""
        points = []
        for i in range(3):  # Triangle
            point_angle = angle + (i * 120)
            x = center[0] + radius * math.cos(math.radians(point_angle))
            y = center[1] + radius * math.sin(math.radians(point_angle))
            points.append((x, y))
        
        if len(points) >= 3:
            try:
                for i in range(len(points)):
                    next_i = (i + 1) % len(points)
                    draw.line([points[i], points[next_i]], fill=color, width=width)
            except:
                pass
    
    def _draw_flowing_line(self, draw: ImageDraw, center: Tuple[int, int], radius: int, angle: float, width: int, color: Tuple[int, int, int], size: int):
        """Draw flowing line pattern"""
        start_x = center[0] + (radius * 0.7) * math.cos(math.radians(angle))
        start_y = center[1] + (radius * 0.7) * math.sin(math.radians(angle))
        end_x = center[0] + radius * math.cos(math.radians(angle))
        end_y = center[1] + radius * math.sin(math.radians(angle))
        
        try:
            draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=width)
        except:
            pass
    
    def _draw_flowing_mandala(self, draw: ImageDraw, pos: Tuple[int, int], size: int, word: str, color: Tuple[int, int, int], style: Dict):
        """Draw flowing mandala pattern"""
        x, y = pos
        petals = max(6, len(word))
        
        for i in range(petals):
            angle = (360 / petals) * i
            petal_x = x + size * math.cos(math.radians(angle))
            petal_y = y + size * math.sin(math.radians(angle))
            
            try:
                draw.ellipse([petal_x-size//3, petal_y-size//3, petal_x+size//3, petal_y+size//3], 
                           outline=color, width=2)
            except:
                pass
    
    def _draw_angular_crystal(self, draw: ImageDraw, pos: Tuple[int, int], size: int, word: str, color: Tuple[int, int, int], style: Dict):
        """Draw angular crystal pattern"""
        x, y = pos
        sides = max(3, min(8, len(word)))
        
        points = []
        for i in range(sides):
            angle = (360 / sides) * i
            px = x + size * math.cos(math.radians(angle))
            py = y + size * math.sin(math.radians(angle))
            points.append((px, py))
        
        if len(points) >= 3:
            try:
                draw.polygon(points, outline=color, width=2)
                # Connect center to all points
                for point in points:
                    draw.line([(x, y), point], fill=color, width=1)
            except:
                pass
    
    def _draw_semantic_spiral(self, draw: ImageDraw, pos: Tuple[int, int], size: int, word: str, color: Tuple[int, int, int], style: Dict):
        """Draw semantic spiral pattern"""
        x, y = pos
        
        points = []
        for i in range(20):
            angle = i * 18  # 18 degrees per step
            radius = (size // 4) + (i * size // 40)
            px = x + radius * math.cos(math.radians(angle))
            py = y + radius * math.sin(math.radians(angle))
            points.append((px, py))
        
        # Connect points to form spiral
        for i in range(len(points) - 1):
            try:
                draw.line([points[i], points[i + 1]], fill=color, width=2)
            except:
                pass
    
    def _draw_radiant_burst(self, draw: ImageDraw, pos: Tuple[int, int], size: int, word: str, color: Tuple[int, int, int], style: Dict):
        """Draw radiant burst pattern"""
        x, y = pos
        rays = max(8, len(word) * 2)
        
        for i in range(rays):
            angle = (360 / rays) * i
            end_x = x + size * math.cos(math.radians(angle))
            end_y = y + size * math.sin(math.radians(angle))
            
            try:
                draw.line([(x, y), (end_x, end_y)], fill=color, width=2)
            except:
                pass
    
    def _draw_unique_symbol(self, draw: ImageDraw, pos: Tuple[int, int], size: int, word: str, color: Tuple[int, int, int], style: Dict, semantic: Dict):
        """Draw unique symbol based on semantic properties"""
        x, y = pos
        
        # Create symbol based on semantic properties
        if semantic['pattern'] == 'embrace':
            # Heart-like pattern
            try:
                draw.arc([x-size, y-size//2, x, y+size//2], 0, 180, fill=color, width=2)
                draw.arc([x, y-size//2, x+size, y+size//2], 0, 180, fill=color, width=2)
                draw.line([(x-size, y), (x, y+size)], fill=color, width=2)
                draw.line([(x+size, y), (x, y+size)], fill=color, width=2)
            except:
                pass
        elif semantic['pattern'] == 'domination':
            # Lightning bolt
            points = [(x, y-size), (x+size//2, y), (x-size//2, y), (x, y+size)]
            for i in range(len(points)-1):
                try:
                    draw.line([points[i], points[i+1]], fill=color, width=3)
                except:
                    pass
        else:
            # Default unique pattern
            try:
                draw.ellipse([x-size, y-size, x+size, y+size], outline=color, width=2)
                draw.line([(x-size, y), (x+size, y)], fill=color, width=2)
                draw.line([(x, y-size), (x, y+size)], fill=color, width=2)
            except:
                pass
    
    # Manifestation drawing methods
    def _draw_love_manifestation(self, draw: ImageDraw, pos: Tuple[int, int], size: int, style: Dict, word: str):
        """Draw love-specific manifestation"""
        x, y = pos
        color = random.choice(style['colors'])
        
        # Multiple heart patterns
        for offset in range(3):
            heart_size = size + (offset * size // 4)
            alpha_offset = offset * 50
            
            try:
                # Heart shape using arcs and lines
                draw.arc([x-heart_size, y-heart_size//2, x, y+heart_size//2], 0, 180, fill=color, width=2)
                draw.arc([x, y-heart_size//2, x+heart_size, y+heart_size//2], 0, 180, fill=color, width=2)
                draw.line([(x-heart_size, y), (x, y+heart_size)], fill=color, width=2)
                draw.line([(x+heart_size, y), (x, y+heart_size)], fill=color, width=2)
            except:
                pass
    
    def _draw_power_manifestation(self, draw: ImageDraw, pos: Tuple[int, int], size: int, style: Dict, word: str):
        """Draw power-specific manifestation"""
        x, y = pos
        color = random.choice(style['colors'])
        
        # Power symbol with radiating lines
        for i in range(8):
            angle = i * 45
            end_x = x + size * 2 * math.cos(math.radians(angle))
            end_y = y + size * 2 * math.sin(math.radians(angle))
            
            try:
                draw.line([(x, y), (end_x, end_y)], fill=color, width=3)
            except:
                pass
        
        # Central power core
        try:
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=color)
        except:
            pass
    
    def _draw_abundance_manifestation(self, draw: ImageDraw, pos: Tuple[int, int], size: int, style: Dict, word: str):
        """Draw abundance-specific manifestation"""
        x, y = pos
        color = random.choice(style['colors'])
        
        # Expanding circles representing abundance
        for i in range(5):
            radius = size * (i + 1) // 2
            try:
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], outline=color, width=2)
            except:
                pass
        
        # Radiating abundance lines
        for i in range(12):
            angle = i * 30
            end_x = x + size * 1.5 * math.cos(math.radians(angle))
            end_y = y + size * 1.5 * math.sin(math.radians(angle))
            
            try:
                draw.line([(x, y), (end_x, end_y)], fill=color, width=1)
            except:
                pass
    
    def _draw_consciousness_manifestation(self, draw: ImageDraw, pos: Tuple[int, int], size: int, style: Dict, word: str):
        """Draw consciousness-specific manifestation"""
        x, y = pos
        color = random.choice(style['colors'])
        
        # Consciousness eye symbol
        try:
            # Outer eye shape
            draw.ellipse([x-size*2, y-size, x+size*2, y+size], outline=color, width=3)
            # Inner iris
            draw.ellipse([x-size, y-size, x+size, y+size], outline=color, width=2)
            # Pupil
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=color)
            
            # Third eye rays
            for i in range(6):
                angle = -90 + (i * 30) - 75  # Above the eye
                ray_length = size * 3
                end_x = x + ray_length * math.cos(math.radians(angle))
                end_y = y + ray_length * math.sin(math.radians(angle))
                draw.line([(x, y-size), (end_x, end_y)], fill=color, width=2)
        except:
            pass
    
    def _draw_generic_manifestation(self, draw: ImageDraw, pos: Tuple[int, int], size: int, style: Dict, word: str, archetype: str):
        """Draw generic manifestation for other archetypes"""
        x, y = pos
        color = random.choice(style['colors'])
        
        # Create unique pattern based on archetype hash
        archetype_hash = hash(archetype + word)
        pattern_type = archetype_hash % 4
        
        if pattern_type == 0:
            # Spiral pattern
            points = []
            for i in range(15):
                angle = i * 24
                radius = (size // 4) + (i * size // 30)
                px = x + radius * math.cos(math.radians(angle))
                py = y + radius * math.sin(math.radians(angle))
                points.append((px, py))
            
            for i in range(len(points) - 1):
                try:
                    draw.line([points[i], points[i + 1]], fill=color, width=2)
                except:
                    pass
                
        elif pattern_type == 1:
            # Star pattern
            points = []
            for i in range(10):
                angle = i * 36
                radius = size * 2 if i % 2 == 0 else size
                px = x + radius * math.cos(math.radians(angle))
                py = y + radius * math.sin(math.radians(angle))
                points.append((px, py))
            
            if len(points) >= 3:
                try:
                    draw.polygon(points, outline=color, width=2)
                except:
                    pass
                    
        elif pattern_type == 2:
            # Grid pattern
            grid_size = size // 2
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) <= 2:  # Diamond shape
                        px = x + i * grid_size
                        py = y + j * grid_size
                        try:
                            draw.ellipse([px-grid_size//4, py-grid_size//4, 
                                        px+grid_size//4, py+grid_size//4], 
                                       fill=color)
                        except:
                            pass
        else:
            # Cross pattern with variations
            try:
                draw.line([(x-size*2, y), (x+size*2, y)], fill=color, width=3)
                draw.line([(x, y-size*2), (x, y+size*2)], fill=color, width=3)
                # Add diagonals for uniqueness
                draw.line([(x-size, y-size), (x+size, y+size)], fill=color, width=2)
                draw.line([(x-size, y+size), (x+size, y-size)], fill=color, width=2)
            except:
                pass
    
    # Symbol drawing methods for character symphony
    def _draw_flowing_symbol(self, draw: ImageDraw, pos: Tuple[int, int], size: int, color: Tuple[int, int, int], char: str):
        """Draw flowing symbol for character"""
        x, y = pos
        try:
            # Flowing wave pattern
            points = []
            for i in range(8):
                angle = i * 45
                radius = size + (i % 2) * size // 2
                px = x + radius * math.cos(math.radians(angle))
                py = y + radius * math.sin(math.radians(angle))
                points.append((px, py))
            
            for i in range(len(points) - 1):
                draw.line([points[i], points[i + 1]], fill=color, width=1)
        except:
            pass
    
    def _draw_angular_symbol(self, draw: ImageDraw, pos: Tuple[int, int], size: int, color: Tuple[int, int, int], char: str):
        """Draw angular symbol for character"""
        x, y = pos
        try:
            # Angular diamond
            points = [(x, y-size), (x+size, y), (x, y+size), (x-size, y)]
            draw.polygon(points, outline=color, width=1)
        except:
            pass
    
    def _draw_curved_symbol(self, draw: ImageDraw, pos: Tuple[int, int], size: int, color: Tuple[int, int, int], char: str):
        """Draw curved symbol for character"""
        x, y = pos
        try:
            # Curved arc pattern
            draw.arc([x-size, y-size, x+size, y+size], 0, 180, fill=color, width=2)
            draw.arc([x-size, y-size, x+size, y+size], 180, 360, fill=color, width=1)
        except:
            pass
    
    def _draw_basic_symbol(self, draw: ImageDraw, pos: Tuple[int, int], size: int, color: Tuple[int, int, int], char: str, energy: Dict):
        """Draw basic symbol based on character energy"""
        x, y = pos
        try:
            if energy['intensity'] == 'gentle':
                draw.ellipse([x-size, y-size, x+size, y+size], outline=color, width=1)
            elif energy['intensity'] == 'strong':
                draw.rectangle([x-size, y-size, x+size, y+size], outline=color, width=2)
            else:
                # Triangle
                points = [(x, y-size), (x-size, y+size), (x+size, y+size)]
                draw.polygon(points, outline=color, width=1)
        except:
            pass
    
    # Vibe-specific resonance methods
    def _create_stellar_resonance(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str, text_dna: Dict):
        """Create stellar/cosmic resonance pattern"""
        # Create constellation based on phrase
        stars = min(15, len(phrase.split()) * 3)
        
        for i in range(stars):
            angle = (i * 23.5) % 360  # Golden angle variation
            radius = (size // 6) + ((i * size // 50) % (size // 3))
            
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            
            # Star brightness based on text characteristics
            brightness = max(3, (text_dna['complexity_score'] * (i + 1)) % 12)
            color = style['colors'][i % len(style['colors'])]
            
            try:
                # Draw star
                self._draw_star(draw, (x, y), brightness, color, 2)
                
                # Connect to nearby stars
                for j in range(max(0, i-2), min(stars, i+3)):
                    if j != i and abs(j - i) <= 2:
                        other_angle = (j * 23.5) % 360
                        other_radius = (size // 6) + ((j * size // 50) % (size // 3))
                        other_x = center[0] + other_radius * math.cos(math.radians(other_angle))
                        other_y = center[1] + other_radius * math.sin(math.radians(other_angle))
                        
                        # Connect with faint line
                        draw.line([(x, y), (other_x, other_y)], fill=color, width=1)
            except:
                pass
    
    def _create_natural_resonance(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str, text_dna: Dict):
        """Create natural/elemental resonance pattern"""
        # Create organic flowing patterns
        branches = max(4, len(phrase.split()) * 2)
        
        for branch in range(branches):
            # Start from center and grow organically
            current_x, current_y = center
            branch_angle = (branch * 360 / branches) + (hash(phrase) % 90)
            
            # Create branching path
            path_points = [(current_x, current_y)]
            
            for step in range(8):
                # Natural growth with some randomness
                step_length = size // 20 + (step * size // 60)
                angle_variation = (hash(phrase + str(branch + step)) % 60) - 30
                current_angle = branch_angle + angle_variation
                
                current_x += step_length * math.cos(math.radians(current_angle))
                current_y += step_length * math.sin(math.radians(current_angle))
                path_points.append((current_x, current_y))
                
                # Occasionally branch
                if step % 3 == 0 and step > 0:
                    # Create sub-branch
                    sub_angle = current_angle + (45 if step % 2 else -45)
                    sub_length = step_length // 2
                    sub_x = current_x + sub_length * math.cos(math.radians(sub_angle))
                    sub_y = current_y + sub_length * math.sin(math.radians(sub_angle))
                    
                    color = style['colors'][(branch + step) % len(style['colors'])]
                    try:
                        draw.line([(current_x, current_y), (sub_x, sub_y)], fill=color, width=2)
                    except:
                        pass
            
            # Draw main branch
            color = style['colors'][branch % len(style['colors'])]
            for i in range(len(path_points) - 1):
                try:
                    width = max(1, 4 - (i // 3))  # Taper the branch
                    draw.line([path_points[i], path_points[i + 1]], fill=color, width=width)
                except:
                    pass
    
    def _create_crystal_resonance(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str, text_dna: Dict):
        """Create crystal/angular resonance pattern"""
        # Create crystalline structure
        facets = max(6, len(phrase) // 3)
        
        for layer in range(3):
            layer_radius = (size // 8) + (layer * size // 12)
            layer_facets = facets + (layer * 2)
            
            # Create faceted ring
            points = []
            for i in range(layer_facets):
                angle = (360 / layer_facets) * i + (layer * 15)
                x = center[0] + layer_radius * math.cos(math.radians(angle))
                y = center[1] + layer_radius * math.sin(math.radians(angle))
                points.append((x, y))
            
            # Connect facets
            color = style['colors'][layer % len(style['colors'])]
            if len(points) >= 3:
                try:
                    # Draw faceted outline
                    draw.polygon(points, outline=color, width=2)
                    
                    # Connect to center
                    for point in points[::2]:  # Every other point
                        draw.line([center, point], fill=color, width=1)
                except:
                    pass
    
    def _create_mystic_resonance(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str, text_dna: Dict):
        """Create mystical/curved resonance pattern"""
        # Create sacred geometry patterns
        rings = max(3, len(phrase.split()))
        
        for ring in range(rings):
            ring_radius = (size // 10) + (ring * size // 15)
            petals = 6 + (ring * 2)
            
            # Create petal pattern
            for petal in range(petals):
                angle = (360 / petals) * petal + (ring * 7.5)
                
                # Petal center
                petal_x = center[0] + ring_radius * math.cos(math.radians(angle))
                petal_y = center[1] + ring_radius * math.sin(math.radians(angle))
                
                # Petal size
                petal_radius = max(size // 40, ring_radius // 6)
                
                color = style['colors'][(ring + petal) % len(style['colors'])]
                
                try:
                    # Draw petal as circle
                    draw.ellipse([petal_x - petal_radius, petal_y - petal_radius,
                                petal_x + petal_radius, petal_y + petal_radius],
                               outline=color, width=2)
                    
                    # Connect to center with curved line (approximate with segments)
                    segments = 5
                    for seg in range(segments):
                        t = seg / segments
                        # Bezier curve approximation
                        curve_x = center[0] * (1-t) + petal_x * t + (ring * 10 * math.sin(t * math.pi))
                        curve_y = center[1] * (1-t) + petal_y * t
                        
                        if seg > 0:
                            draw.line([(prev_curve_x, prev_curve_y), (curve_x, curve_y)], 
                                    fill=color, width=1)
                        prev_curve_x, prev_curve_y = curve_x, curve_y
                except:
                    pass
    
    def _create_radial_resonance(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str, text_dna: Dict):
        """Create radial/light resonance pattern"""
        # Create radiating light pattern
        rays = max(12, len(phrase) * 2)
        
        for ray in range(rays):
            angle = (360 / rays) * ray + (hash(phrase) % 45)
            
            # Multiple ray segments for light effect
            for segment in range(4):
                start_radius = (segment * size // 12) + (size // 20)
                end_radius = start_radius + (size // 15)
                
                start_x = center[0] + start_radius * math.cos(math.radians(angle))
                start_y = center[1] + start_radius * math.sin(math.radians(angle))
                end_x = center[0] + end_radius * math.cos(math.radians(angle))
                end_y = center[1] + end_radius * math.sin(math.radians(angle))
                
                # Brightness fades with distance
                color_index = (ray + segment) % len(style['colors'])
                color = style['colors'][color_index]
                width = max(1, 4 - segment)
                
                try:
                    draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=width)
                except:
                    pass
            
            # Add ray sparkles
            for sparkle in range(3):
                sparkle_radius = (size // 8) + (sparkle * size // 12)
                sparkle_x = center[0] + sparkle_radius * math.cos(math.radians(angle))
                sparkle_y = center[1] + sparkle_radius * math.sin(math.radians(angle))
                sparkle_size = max(2, 6 - sparkle * 2)
                
                color = style['colors'][sparkle % len(style['colors'])]
                
                try:
                    # Draw sparkle as small star
                    self._draw_star(draw, (sparkle_x, sparkle_y), sparkle_size, color, 1)
                except:
                    pass
    
    def _create_electric_resonance(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str, text_dna: Dict):
        """Create electric/storm resonance pattern"""
        # Create lightning-like patterns
        bolts = max(6, len(phrase.split()) * 2)
        
        for bolt in range(bolts):
            # Start point around center
            start_angle = (bolt * 360 / bolts) + (hash(phrase + str(bolt)) % 60)
            start_radius = size // 20
            start_x = center[0] + start_radius * math.cos(math.radians(start_angle))
            start_y = center[1] + start_radius * math.sin(math.radians(start_angle))
            
            # Create jagged lightning path
            current_x, current_y = start_x, start_y
            current_angle = start_angle
            
            lightning_points = [(current_x, current_y)]
            
            for step in range(8):
                step_length = size // 25 + (step * size // 60)
                
                # Random direction change for jagged effect
                angle_change = ((hash(phrase + str(bolt) + str(step)) % 90) - 45)
                current_angle += angle_change
                
                current_x += step_length * math.cos(math.radians(current_angle))
                current_y += step_length * math.sin(math.radians(current_angle))
                lightning_points.append((current_x, current_y))
            
            # Draw lightning bolt
            color = style['colors'][bolt % len(style['colors'])]
            for i in range(len(lightning_points) - 1):
                try:
                    width = max(2, 5 - (i // 3))  # Taper the bolt
                    draw.line([lightning_points[i], lightning_points[i + 1]], fill=color, width=width)
                except:
                    pass
            
            # Add electric nodes
            for i in range(0, len(lightning_points), 2):
                node_x, node_y = lightning_points[i]
                node_size = max(2, 6 - (i // 3))
                
                try:
                    draw.ellipse([node_x - node_size, node_y - node_size,
                                node_x + node_size, node_y + node_size], fill=color)
                except:
                    pass
    
    def _create_shadow_resonance(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str, text_dna: Dict):
        """Create shadow/jagged resonance pattern"""
        # Create shadow tendrils
        tendrils = max(5, len(phrase.split()) * 2)
        
        for tendril in range(tendrils):
            # Shadow tendrils grow outward in jagged patterns
            start_angle = (tendril * 360 / tendrils) + (hash(phrase) % 72)
            
            current_x, current_y = center
            current_angle = start_angle
            shadow_points = [center]
            
            for step in range(6):
                step_length = (size // 12) + (step * size // 30)
                
                # Jagged shadow growth
                angle_variation = ((hash(phrase + str(tendril) + str(step)) % 120) - 60)
                current_angle += angle_variation
                
                current_x += step_length * math.cos(math.radians(current_angle))
                current_y += step_length * math.sin(math.radians(current_angle))
                shadow_points.append((current_x, current_y))
                
                # Shadow branches
                if step % 2 == 1:
                    branch_angle = current_angle + (90 if step % 4 == 1 else -90)
                    branch_length = step_length // 2
                    branch_x = current_x + branch_length * math.cos(math.radians(branch_angle))
                    branch_y = current_y + branch_length * math.sin(math.radians(branch_angle))
                    
                    color = style['colors'][(tendril + step) % len(style['colors'])]
                    try:
                        draw.line([(current_x, current_y), (branch_x, branch_y)], fill=color, width=3)
                    except:
                        pass
            
            # Draw main tendril
            color = style['colors'][tendril % len(style['colors'])]
            for i in range(len(shadow_points) - 1):
                try:
                    width = max(2, 5 - (i // 2))
                    draw.line([shadow_points[i], shadow_points[i + 1]], fill=color, width=width)
                except:
                    pass
    
    def _create_void_resonance(self, draw: ImageDraw, center: Tuple[int, int], style: Dict, size: int, phrase: str, text_dna: Dict):
        """Create void/impossible resonance pattern"""
        # Create recursive spiral patterns
        spirals = max(3, len(phrase.split()))
        
        for spiral_index in range(spirals):
            spiral_offset = spiral_index * 120 + (hash(phrase) % 90)
            
            # Create impossible geometry - spirals that fold in on themselves
            spiral_points = []
            
            for i in range(30):
                # Multi-dimensional spiral calculation
                base_angle = (i * 12) + spiral_offset
                base_radius = (size // 15) + (i * size // 100)
                
                # Add void distortion
                distortion = math.sin(i / 5) * (size // 30)
                final_radius = base_radius + distortion
                
                # Recursive angle modification
                recursive_angle = base_angle + (math.sin(i / 3) * 45)
                
                x = center[0] + final_radius * math.cos(math.radians(recursive_angle))
                y = center[1] + final_radius * math.sin(math.radians(recursive_angle))
                spiral_points.append((x, y))
            
            # Draw void spiral
            color = style['colors'][spiral_index % len(style['colors'])]
            
            for i in range(len(spiral_points) - 1):
                try:
                    # Fading line width for depth effect
                    width = max(1, 4 - (i // 10))
                    draw.line([spiral_points[i], spiral_points[i + 1]], fill=color, width=width)
                except:
                    pass
            
            # Add dimensional portals
            for portal in range(5):
                portal_pos = spiral_points[portal * 6] if portal * 6 < len(spiral_points) else spiral_points[-1]
                portal_size = max(3, 8 - portal)
                
                try:
                    # Portal as concentric circles
                    for ring in range(3):
                        ring_radius = portal_size + (ring * portal_size // 2)
                        draw.ellipse([portal_pos[0] - ring_radius, portal_pos[1] - ring_radius,
                                    portal_pos[0] + ring_radius, portal_pos[1] + ring_radius],
                                   outline=color, width=1)
                except:
                    pass
    
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
        
        if len(points) >= 3:
            try:
                for i in range(len(points)):
                    next_i = (i + 1) % len(points)
                    draw.line([points[i], points[next_i]], fill=color, width=width)
            except:
                pass
    
    def _apply_enhanced_effects(self, img: Image.Image, style: Dict, text_dna: Dict, phrase: str) -> Image.Image:
        """Apply enhanced visual effects based on text characteristics"""
        if style.get('glow_intensity', 0) > 0:
            # Multi-layer glow based on phrase characteristics
            glow_layers = min(6, max(3, int(text_dna['complexity_score'])))
            
            result = img.copy()
            for layer in range(glow_layers):
                blur_radius = (layer + 1) * 2
                glow = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                
                enhancer = ImageEnhance.Brightness(glow)
                intensity = style['glow_intensity'] * (0.7 ** layer)
                glow = enhancer.enhance(intensity)
                
                result = Image.alpha_composite(result, glow)
            
            return result
        
        return img
    
    def _apply_ultra_effects(self, img: Image.Image, style: Dict, text_dna: Dict, phrase: str) -> Image.Image:
        """Apply ultra-revolutionary visual effects for advanced generation"""
        base_img = img.copy()
        
        # Advanced multi-effect processing
        effects = ['glow', 'contrast', 'saturation', 'sharpness', 'brightness']
        
        for effect in effects:
            if effect == 'glow' and style.get('glow_intensity', 0) > 0:
                # Ultra-sophisticated multi-radius glow
                glow_radii = [1, 2, 4, 6, 10, 15]
                for radius in glow_radii:
                    glow = base_img.filter(ImageFilter.GaussianBlur(radius=radius))
                    enhancer = ImageEnhance.Brightness(glow)
                    intensity = style['glow_intensity'] * (0.5 ** (radius / 5))
                    glow = enhancer.enhance(intensity)
                    base_img = Image.alpha_composite(base_img, glow)
            
            elif effect == 'contrast':
                enhancer = ImageEnhance.Contrast(base_img)
                contrast_factor = 1.0 + (text_dna['complexity_score'] / 15)
                base_img = enhancer.enhance(contrast_factor)
            
            elif effect == 'saturation':
                enhancer = ImageEnhance.Color(base_img)
                saturation_factor = 1.0 + (text_dna['uniqueness_score'] * 0.5)
                base_img = enhancer.enhance(saturation_factor)
            
            elif effect == 'sharpness':
                enhancer = ImageEnhance.Sharpness(base_img)
                sharpness_factor = 1.0 + (len(text_dna['semantic_layers']) / 10)
                base_img = enhancer.enhance(sharpness_factor)
                
            elif effect == 'brightness':
                enhancer = ImageEnhance.Brightness(base_img)
                brightness_factor = 1.0 + (len(phrase.split()) / 50)
                base_img = enhancer.enhance(brightness_factor)
        
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

@app.route('/')
def serve_index():
    """Serve the main application"""
    try:
        return app.send_static_file('index.html')
    except:
        return jsonify({
            'success': False,
            'error': 'Frontend not found',
            'message': 'Please ensure static files are properly served'
        }), 404

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    try:
        return app.send_static_file(path)
    except:
        # Fallback to index.html for client-side routing
        try:
            return app.send_static_file('index.html')
        except:
            return jsonify({
                'success': False,
                'error': f'File not found: {path}'
            }), 404

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'sigilcraft-ultra-revolutionary-backend',
        'version': '4.0.0',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'ultra_revolutionary_generation': True,
            'extreme_text_responsiveness': True,
            'ultra_unique_signatures': True,
            'vibe_specific_resonance': True,
            'semantic_manifestation': True,
            'character_symphony': True
        }
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
                'version': '4.0.0',
                'ultra_revolutionary': True
            },
            'message': f'Ultra-unique text-responsive sigil manifested for: "{phrase}"'
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
    """Get list of available energy vibes with enhanced descriptions"""
    vibes = list(generator.vibe_styles.keys())
    
    return jsonify({
        'success': True,
        'vibes': vibes,
        'count': len(vibes),
        'descriptions': {
            'mystical': 'Ancient wisdom & sacred geometry with curved flowing energy',
            'cosmic': 'Universal stellar connection with radiant burst patterns',
            'elemental': 'Natural organic forces with flowing growth patterns',
            'crystal': 'Prismatic clarity with angular geometric precision',
            'shadow': 'Hidden mysterious power with jagged consuming energy',
            'light': 'Pure divine radiance with emanating luminous patterns',
            'storm': 'Raw electric chaos with explosive lightning energy',
            'void': 'Infinite recursive potential with impossible geometry'
        },
        'features': {
            'ultra_text_responsive': True,
            'extreme_semantic_analysis': True,
            'character_symphony_generation': True,
            'vibe_specific_resonance': True,
            'unique_signature_creation': True
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
    print("🔮 Starting Ultra-Revolutionary Sigilcraft Python Backend...")
    print(f"📦 PIL/Pillow version: {Image.__version__}")
    print(f"🔢 NumPy available: {'✅' if 'numpy' in sys.modules or 'np' in globals() else '❌'}")
    print("🎨 Ultra-revolutionary text-responsive sigil generation ready!")
    print("✨ Features: Extreme text analysis, character symphony, vibe resonance")
    
    # Get port from environment or default to 5001 (Flask backend)
    port = int(os.getenv('FLASK_PORT', 5001))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting server on port {port}")
    print(f"🔧 Debug mode: {'ON' if debug_mode else 'OFF'}")
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug_mode,
            threaded=True,
            use_reloader=False  # Prevent double startup in production
        )
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown gracefully")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)
