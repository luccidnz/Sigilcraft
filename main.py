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
app = Flask(__name__, static_folder='public', static_url_path='')
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
                'colors': [(180, 100, 180), (200, 80, 200), (160, 120, 160), (220, 150, 220), (140, 90, 140), (190, 130, 190), (170, 110, 170)],
                'base_patterns': ['void_portal', 'shadow_tendrils', 'dark_sigil', 'obscured_geometry'],
                'stroke_multiplier': 2.0,
                'complexity_bias': 'hidden',
                'geometry_type': 'jagged',
                'energy_flow': 'consuming',
                'symbol_density': 'sparse',
                'glow_intensity': 0.6,
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
                'colors': [(150, 100, 200), (120, 80, 180), (180, 120, 220), (200, 150, 250), (160, 90, 190), (140, 70, 170), (190, 140, 230)],
                'base_patterns': ['infinite_spiral', 'dimensional_portal', 'void_geometry', 'recursive_depth'],
                'stroke_multiplier': 1.8,
                'complexity_bias': 'infinite',
                'geometry_type': 'impossible',
                'energy_flow': 'recursive',
                'symbol_density': 'deep',
                'glow_intensity': 0.7,
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
        """Create base pattern with maximum contrast and visibility for all vibes"""
        center = (size // 2, size // 2)

        # Create base geometry with ultra-high contrast
        for i in range(min(12, len(phrase))):
            char = phrase[i] if i < len(phrase) else phrase[i % len(phrase)]
            angle = (ord(char) * 13 + i * 30) % 360
            radius = (size // 8) + (ord(char) % (size // 15))

            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))

            # ULTRA-ENHANCED color processing for maximum visibility
            base_color = style['colors'][i % len(style['colors'])]
            
            # Ensure EVERY color has minimum brightness and maximum contrast
            enhanced_color = []
            for c in base_color:
                # Force minimum brightness of 120, maximum boost of 2.2x
                boosted = min(255, max(120, int(c * 2.2)))
                enhanced_color.append(boosted)
            enhanced_color = tuple(enhanced_color)
            
            # Much larger symbols and thicker strokes for ALL vibes
            size_factor = max(12, ord(char) % 25)  # Even larger symbols
            stroke_width = max(6, int(style['stroke_multiplier'] * 8))  # Much thicker strokes

            try:
                # Draw character-based symbol with maximum visibility
                if ord(char) % 3 == 0:
                    # Filled circle with thick outline
                    draw.ellipse([x-size_factor, y-size_factor, x+size_factor, y+size_factor],
                               fill=enhanced_color, outline=enhanced_color, width=stroke_width)
                    # Add bright center highlight
                    highlight_color = tuple(min(255, c + 60) for c in enhanced_color)
                    inner_size = max(3, size_factor // 3)
                    draw.ellipse([x-inner_size, y-inner_size, x+inner_size, y+inner_size],
                               fill=highlight_color)
                elif ord(char) % 3 == 1:
                    # Thick crossing lines
                    draw.line([(x-size_factor, y-size_factor), (x+size_factor, y+size_factor)],
                             fill=enhanced_color, width=stroke_width)
                    draw.line([(x-size_factor, y+size_factor), (x+size_factor, y-size_factor)],
                             fill=enhanced_color, width=stroke_width)
                    # Add center dot
                    draw.ellipse([x-3, y-3, x+3, y+3], fill=enhanced_color)
                else:
                    # Filled polygon with outline
                    points = []
                    for j in range(6):
                        px = x + size_factor * math.cos(math.radians(j * 60))
                        py = y + size_factor * math.sin(math.radians(j * 60))
                        points.append((px, py))
                    if len(points) >= 3:
                        draw.polygon(points, fill=enhanced_color, outline=enhanced_color, width=stroke_width)
            except:
                pass

    def _create_text_pattern(self, draw: ImageDraw, phrase: str, style: Dict, size: int):
        """Create high-contrast text pattern with enhanced visibility"""
        center = (size // 2, size // 2)
        words = phrase.split()

        for i, word in enumerate(words[:8]):
            word_energy = sum(ord(c) for c in word.lower())
            angle = (word_energy * 7 + i * 45) % 360
            distance = (size // 5) + (len(word) * size // 30)  # Better spacing

            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))

            # MAXIMUM contrast enhancement for all vibes
            base_color = style['colors'][(word_energy + i) % len(style['colors'])]
            # Force ultra-high contrast with minimum brightness of 140
            enhanced_color = []
            for c in base_color:
                boosted = min(255, max(140, int(c * 2.5)))
                enhanced_color.append(boosted)
            enhanced_color = tuple(enhanced_color)

            # Create word-specific pattern with maximum visibility
            try:
                stroke_width = max(5, int(style['stroke_multiplier'] * 4))  # Much thicker strokes
                connector_width = max(4, int(style['stroke_multiplier'] * 2))

                if len(word) <= 3:
                    # Larger triangle with high contrast
                    points = []
                    triangle_size = size // 25  # Bigger
                    for j in range(3):
                        px = x + triangle_size * math.cos(math.radians(j * 120))
                        py = y + triangle_size * math.sin(math.radians(j * 120))
                        points.append((px, py))
                    draw.polygon(points, fill=enhanced_color, outline=enhanced_color, width=stroke_width)
                    
                elif len(word) <= 6:
                    # Larger square with high contrast
                    s = size // 30  # Bigger
                    draw.rectangle([x-s, y-s, x+s, y+s], fill=enhanced_color, outline=enhanced_color, width=stroke_width)
                    
                else:
                    # Larger hexagon with high contrast
                    points = []
                    hex_size = size // 20  # Bigger
                    for j in range(6):
                        px = x + hex_size * math.cos(math.radians(j * 60))
                        py = y + hex_size * math.sin(math.radians(j * 60))
                        points.append((px, py))
                    draw.polygon(points, fill=enhanced_color, outline=enhanced_color, width=stroke_width)

                # Enhanced connector line with glow effect
                draw.line([center, (x, y)], fill=enhanced_color, width=connector_width)
                # Add subtle glow to connector
                glow_color = tuple(min(255, c + 40) for c in enhanced_color)
                draw.line([center, (x, y)], fill=glow_color, width=max(1, connector_width // 2))
                
            except:
                pass

    def _create_vibe_pattern(self, draw: ImageDraw, phrase: str, vibe: str, style: Dict, size: int):
        """Create high-contrast vibe-specific resonance patterns"""
        center = (size // 2, size // 2)
        phrase_seed = sum(ord(c) for c in phrase.lower())

        if vibe == 'cosmic':
            # ULTRA-enhanced star pattern with forced maximum contrast
            for i in range(8):
                angle = i * 45
                radius = size // 3
                x = center[0] + radius * math.cos(math.radians(angle))
                y = center[1] + radius * math.sin(math.radians(angle))

                base_color = style['colors'][i % len(style['colors'])]
                # Force ultra-bright cosmic colors
                enhanced_color = []
                for c in base_color:
                    boosted = min(255, max(160, int(c * 3.0)))
                    enhanced_color.append(boosted)
                enhanced_color = tuple(enhanced_color)
                
                try:
                    # Thick star rays with glow
                    draw.line([center, (x, y)], fill=enhanced_color, width=8)
                    # Bright star points
                    star_size = size // 40
                    draw.ellipse([x-star_size, y-star_size, x+star_size, y+star_size], 
                               fill=enhanced_color, outline=enhanced_color, width=3)
                    # Add center highlight
                    highlight = tuple(min(255, c + 80) for c in enhanced_color)
                    draw.ellipse([x-star_size//2, y-star_size//2, x+star_size//2, y+star_size//2], fill=highlight)
                except:
                    pass

        elif vibe == 'elemental':
            # Enhanced natural flow pattern
            for i in range(6):
                start_angle = i * 60
                prev_pos = None
                for j in range(7):  # More segments
                    angle = start_angle + (j * 8)
                    radius = (size // 6) + (j * size // 30)
                    x = center[0] + radius * math.cos(math.radians(angle))
                    y = center[1] + radius * math.sin(math.radians(angle))

                    if prev_pos:
                        base_color = style['colors'][(i + j) % len(style['colors'])]
                        # Force ultra-bright elemental colors
                        enhanced_color = []
                        for c in base_color:
                            boosted = min(255, max(150, int(c * 2.8)))
                            enhanced_color.append(boosted)
                        enhanced_color = tuple(enhanced_color)
                        try:
                            draw.line([prev_pos, (x, y)], fill=enhanced_color, width=6)
                            # Add connection nodes
                            node_size = 4
                            draw.ellipse([x-node_size, y-node_size, x+node_size, y+node_size], fill=enhanced_color)
                        except:
                            pass
                    prev_pos = (x, y)

        elif vibe == 'crystal':
            # FIXED: Enhanced prismatic crystal lattice pattern
            for layer in range(5):  # More layers for complexity
                layer_radius = (size // 8) + (layer * size // 12)
                sides = 6 + (layer * 2)
                rotation = layer * 15 + (phrase_seed % 45)  # Phrase-specific rotation

                points = []
                for i in range(sides):
                    angle = (360 / sides) * i + rotation
                    x = center[0] + layer_radius * math.cos(math.radians(angle))
                    y = center[1] + layer_radius * math.sin(math.radians(angle))
                    points.append((x, y))

                base_color = style['colors'][layer % len(style['colors'])]
                # Force ultra-bright crystal colors with prismatic effect
                enhanced_color = []
                for c in base_color:
                    boosted = min(255, max(180, int(c * 3.5)))
                    enhanced_color.append(boosted)
                enhanced_color = tuple(enhanced_color)
                
                try:
                    if len(points) >= 3:
                        # Bright filled polygon for crystal facets
                        fill_color = tuple(max(60, c // 2) for c in enhanced_color)
                        draw.polygon(points, fill=fill_color, outline=enhanced_color, width=6)
                        
                        # Add crystalline inner structure
                        if layer > 0:
                            for i in range(0, len(points), 2):
                                if i + 2 < len(points):
                                    draw.line([points[i], points[i+2]], fill=enhanced_color, width=3)
                        
                        # Add crystal vertices
                        for point in points:
                            vertex_size = 6
                            draw.ellipse([point[0]-vertex_size, point[1]-vertex_size, 
                                        point[0]+vertex_size, point[1]+vertex_size], 
                                       fill=enhanced_color)
                except:
                    pass

        elif vibe == 'shadow':
            # FIXED: Enhanced shadow tendrils and void portals
            # Create multiple shadow layers with varying opacity and jagged patterns
            for ring in range(6):
                ring_radius = (size // 12) + (ring * size // 15)
                tendril_count = 5 + (ring * 2)
                
                for i in range(tendril_count):
                    # Create jagged, irregular shadow tendrils
                    base_angle = (360 / tendril_count) * i + (phrase_seed % 360)
                    angle_variation = 15 + (phrase_seed % 20)
                    
                    # Multiple segments for each tendril
                    prev_point = center
                    for segment in range(4 + ring):
                        angle = base_angle + random.randint(-angle_variation, angle_variation)
                        segment_radius = ring_radius + (segment * size // 40)
                        
                        # Add jagged variations
                        jagged_offset = random.randint(-size//60, size//60)
                        x = center[0] + (segment_radius + jagged_offset) * math.cos(math.radians(angle))
                        y = center[1] + (segment_radius + jagged_offset) * math.sin(math.radians(angle))
                        
                        base_color = style['colors'][(ring + i) % len(style['colors'])]
                        # Force much brighter shadow colors for visibility
                        enhanced_color = []
                        for c in base_color:
                            boosted = min(255, max(160, int(c * 3.2)))
                            enhanced_color.append(boosted)
                        enhanced_color = tuple(enhanced_color)
                        
                        try:
                            # Thick shadow tendrils
                            stroke_width = max(4, 8 - ring)
                            draw.line([prev_point, (x, y)], fill=enhanced_color, width=stroke_width)
                            
                            # Shadow nodes
                            node_size = max(3, 8 - ring)
                            draw.ellipse([x-node_size, y-node_size, x+node_size, y+node_size], 
                                       fill=enhanced_color, outline=enhanced_color, width=2)
                        except:
                            pass
                        prev_point = (x, y)

        elif vibe == 'storm':
            # FIXED: Enhanced chaotic lightning and electric storm patterns
            storm_center_x, storm_center_y = center
            
            # Create multiple storm systems
            for storm_sys in range(3):
                # Offset storm centers for chaos
                offset_x = random.randint(-size//6, size//6)
                offset_y = random.randint(-size//6, size//6)
                storm_x = storm_center_x + offset_x
                storm_y = storm_center_y + offset_y
                
                # Lightning branches from each storm center
                for branch in range(8 + storm_sys * 3):
                    base_angle = (phrase_seed * 7 + branch * 35) % 360
                    
                    # Create chaotic lightning path
                    current_x, current_y = storm_x, storm_y
                    
                    for segment in range(6 + random.randint(0, 4)):
                        # Chaotic angle variations for lightning
                        angle_chaos = random.randint(-45, 45)
                        angle = base_angle + angle_chaos + (segment * random.randint(-15, 15))
                        
                        # Variable segment length for chaos
                        segment_length = size // 20 + random.randint(-size//40, size//40)
                        
                        next_x = current_x + segment_length * math.cos(math.radians(angle))
                        next_y = current_y + segment_length * math.sin(math.radians(angle))
                        
                        base_color = style['colors'][(storm_sys + branch + segment) % len(style['colors'])]
                        # Force ultra-bright electric colors
                        enhanced_color = []
                        for c in base_color:
                            boosted = min(255, max(180, int(c * 3.8)))
                            enhanced_color.append(boosted)
                        enhanced_color = tuple(enhanced_color)
                        
                        try:
                            # Thick electric bolts with random width variation
                            bolt_width = random.randint(3, 8)
                            draw.line([(current_x, current_y), (next_x, next_y)], 
                                     fill=enhanced_color, width=bolt_width)
                            
                            # Electric charge points
                            charge_size = random.randint(4, 10)
                            draw.ellipse([next_x-charge_size, next_y-charge_size, 
                                        next_x+charge_size, next_y+charge_size], 
                                       fill=enhanced_color)
                            
                            # Random secondary bolts for more chaos
                            if random.random() < 0.4:
                                side_angle = angle + random.randint(-90, 90)
                                side_length = segment_length // 2
                                side_x = next_x + side_length * math.cos(math.radians(side_angle))
                                side_y = next_y + side_length * math.sin(math.radians(side_angle))
                                draw.line([(next_x, next_y), (side_x, side_y)], 
                                         fill=enhanced_color, width=max(2, bolt_width//2))
                        except:
                            pass
                        
                        current_x, current_y = next_x, next_y

        elif vibe == 'void':
            # FIXED: Enhanced recursive void geometry and dimensional portals
            # Create multiple void spirals with recursive depth
            for void_layer in range(7):
                layer_radius = (size // 15) + (void_layer * size // 20)
                spiral_segments = 12 + (void_layer * 4)
                
                # Create recursive spiral patterns
                for segment in range(spiral_segments):
                    # Recursive angle calculation for infinite feel
                    base_angle = (segment * 360 / spiral_segments) + (void_layer * 23)
                    recursive_angle = base_angle + (phrase_seed % 180) + (segment * void_layer * 3)
                    
                    # Recursive radius with depth illusion
                    recursive_radius = layer_radius * (1 + math.sin(math.radians(segment * 15)) * 0.3)
                    
                    x = center[0] + recursive_radius * math.cos(math.radians(recursive_angle))
                    y = center[1] + recursive_radius * math.sin(math.radians(recursive_angle))
                    
                    # Calculate next point for continuous spiral
                    next_segment = (segment + 1) % spiral_segments
                    next_angle = (next_segment * 360 / spiral_segments) + (void_layer * 23)
                    next_recursive_angle = next_angle + (phrase_seed % 180) + (next_segment * void_layer * 3)
                    next_radius = layer_radius * (1 + math.sin(math.radians(next_segment * 15)) * 0.3)
                    
                    next_x = center[0] + next_radius * math.cos(math.radians(next_recursive_angle))
                    next_y = center[1] + next_radius * math.sin(math.radians(next_recursive_angle))
                    
                    base_color = style['colors'][(void_layer + segment) % len(style['colors'])]
                    # Force much brighter void colors with depth
                    enhanced_color = []
                    for c in base_color:
                        depth_factor = 2.8 + (void_layer * 0.3)
                        boosted = min(255, max(150, int(c * depth_factor)))
                        enhanced_color.append(boosted)
                    enhanced_color = tuple(enhanced_color)
                    
                    try:
                        # Void spiral lines with varying thickness
                        line_width = max(2, 6 - (void_layer // 2))
                        draw.line([(x, y), (next_x, next_y)], fill=enhanced_color, width=line_width)
                        
                        # Void portals (dimensional dots)
                        portal_size = max(2, 8 - void_layer)
                        draw.ellipse([x-portal_size, y-portal_size, x+portal_size, y+portal_size], 
                                   fill=enhanced_color, outline=enhanced_color, width=2)
                        
                        # Inner recursive connections to center for infinite depth
                        if void_layer > 0 and segment % 3 == 0:
                            inner_factor = 0.6
                            inner_x = center[0] + (x - center[0]) * inner_factor
                            inner_y = center[1] + (y - center[1]) * inner_factor
                            draw.line([(x, y), (inner_x, inner_y)], fill=enhanced_color, width=max(1, line_width//2))
                    except:
                        pass

        elif vibe == 'light':
            # FIXED: Enhanced radiant light pattern with proper rays and luminous geometry
            # Create multiple light ray systems
            for ray_system in range(4):
                system_angle_offset = ray_system * 45 + (phrase_seed % 90)
                
                # Create radiant light rays from center
                for ray in range(12):
                    ray_angle = (360 / 12) * ray + system_angle_offset
                    
                    # Create multi-segment light rays
                    for segment in range(6):
                        start_radius = (size // 15) + (segment * size // 20)
                        end_radius = start_radius + (size // 25)
                        
                        # Ray start point
                        start_x = center[0] + start_radius * math.cos(math.radians(ray_angle))
                        start_y = center[1] + start_radius * math.sin(math.radians(ray_angle))
                        
                        # Ray end point
                        end_x = center[0] + end_radius * math.cos(math.radians(ray_angle))
                        end_y = center[1] + end_radius * math.sin(math.radians(ray_angle))
                        
                        base_color = style['colors'][(ray_system + ray + segment) % len(style['colors'])]
                        # Force ultra-bright light colors
                        enhanced_color = []
                        for c in base_color:
                            boosted = min(255, max(200, int(c * 4.0)))
                            enhanced_color.append(boosted)
                        enhanced_color = tuple(enhanced_color)
                        
                        try:
                            # Bright light ray segments
                            ray_width = max(3, 8 - segment)
                            draw.line([(start_x, start_y), (end_x, end_y)], fill=enhanced_color, width=ray_width)
                            
                            # Luminous points at ray ends
                            light_size = max(4, 10 - segment)
                            draw.ellipse([end_x-light_size, end_y-light_size, end_x+light_size, end_y+light_size], 
                                       fill=enhanced_color)
                            
                            # Add brilliant center highlight
                            highlight_size = max(2, light_size // 2)
                            ultra_bright = tuple(min(255, c) for c in enhanced_color)
                            draw.ellipse([end_x-highlight_size, end_y-highlight_size, 
                                        end_x+highlight_size, end_y+highlight_size], fill=ultra_bright)
                        except:
                            pass
                            
                # Create divine mandala center
                for mandala_ring in range(3):
                    ring_radius = (size // 30) + (mandala_ring * size // 40)
                    ring_points = 8 + (mandala_ring * 4)
                    
                    for point in range(ring_points):
                        point_angle = (360 / ring_points) * point + (mandala_ring * 30)
                        x = center[0] + ring_radius * math.cos(math.radians(point_angle))
                        y = center[1] + ring_radius * math.sin(math.radians(point_angle))
                        
                        base_color = style['colors'][(mandala_ring + point) % len(style['colors'])]
                        enhanced_color = []
                        for c in base_color:
                            boosted = min(255, max(220, int(c * 4.5)))
                            enhanced_color.append(boosted)
                        enhanced_color = tuple(enhanced_color)
                        
                        try:
                            mandala_size = max(6, 12 - mandala_ring * 2)
                            draw.ellipse([x-mandala_size, y-mandala_size, x+mandala_size, y+mandala_size], 
                                       fill=enhanced_color, outline=enhanced_color, width=2)
                        except:
                            pass

        else:
            # Enhanced mystical pattern (fallback for other vibes)
            for ring in range(5):  # More rings
                ring_radius = (size // 10) + (ring * size // 18)
                segments = 8 + (ring * 2)

                for i in range(segments):
                    angle = (360 / segments) * i + (ring * 15)
                    x = center[0] + ring_radius * math.cos(math.radians(angle))
                    y = center[1] + ring_radius * math.sin(math.radians(angle))

                    base_color = style['colors'][(ring + i) % len(style['colors'])]
                    # Force ultra-bright mystical colors
                    enhanced_color = []
                    for c in base_color:
                        boosted = min(255, max(140, int(c * 2.7)))
                        enhanced_color.append(boosted)
                    enhanced_color = tuple(enhanced_color)
                    symbol_size = max(8, size // 50)  # Even larger symbols

                    try:
                        # Bright filled circles with outlines
                        draw.ellipse([x-symbol_size, y-symbol_size, x+symbol_size, y+symbol_size],
                                   fill=enhanced_color, outline=enhanced_color, width=2)
                        # Add bright center
                        center_size = max(2, symbol_size // 2)
                        highlight = tuple(min(255, c + 60) for c in enhanced_color)
                        draw.ellipse([x-center_size, y-center_size, x+center_size, y+center_size], fill=highlight)
                    except:
                        pass

    def _apply_enhanced_effects(self, img: Image.Image, style: Dict, phrase: str) -> Image.Image:
        """Apply maximum contrast and sharpness effects"""
        result = img.copy()
        
        # Apply sharpening filter first
        result = result.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=3))
        
        # MAXIMUM contrast for all vibes
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(3.0)  # Ultra-high contrast
        
        # MAXIMUM color saturation
        enhancer = ImageEnhance.Color(result)
        result = enhancer.enhance(2.8)  # Ultra-vibrant colors
        
        # MAXIMUM brightness for perfect visibility
        enhancer = ImageEnhance.Brightness(result)
        result = enhancer.enhance(1.5)
        
        # Apply controlled glow only if specified
        if style.get('glow_intensity', 0) > 0:
            glow_layers = []
            for layer in range(2):  # Fewer, more controlled glow layers
                blur_radius = (layer + 1) * 1.5
                glow = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                
                enhancer = ImageEnhance.Brightness(glow)
                intensity = min(2.5, style['glow_intensity'] * 1.5) * (0.6 ** layer)
                glow = enhancer.enhance(intensity)
                glow_layers.append(glow)
            
            # Composite glow layers
            for glow in glow_layers:
                result = Image.alpha_composite(result, glow)
        
        return result

    def _apply_ultra_effects(self, img: Image.Image, style: Dict, phrase: str) -> Image.Image:
        """Apply ultra-revolutionary visual effects with maximum quality"""
        base_img = img.copy()
        
        # Apply multiple sharpening passes for ultra-crisp results
        base_img = base_img.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=2))
        base_img = base_img.filter(ImageFilter.UnsharpMask(radius=3, percent=100, threshold=1))
        
        # Ultra-enhanced contrast
        enhancer = ImageEnhance.Contrast(base_img)
        base_img = enhancer.enhance(2.8)  # Maximum contrast
        
        # Ultra-enhanced color saturation
        enhancer = ImageEnhance.Color(base_img)
        base_img = enhancer.enhance(2.5)  # Maximum saturation
        
        # Enhanced brightness for perfect visibility
        enhancer = ImageEnhance.Brightness(base_img)
        base_img = enhancer.enhance(1.4)
        
        # Controlled ultra glow effect
        if style.get('glow_intensity', 0) > 0:
            glow_radii = [0.8, 1.5, 3, 5]  # More precise glow radii
            for radius in glow_radii:
                glow = img.filter(ImageFilter.GaussianBlur(radius=radius))
                enhancer = ImageEnhance.Brightness(glow)
                intensity = min(3.0, style['glow_intensity'] * 2.0) * (0.4 ** (radius / 3))
                glow = enhancer.enhance(intensity)
                base_img = Image.alpha_composite(base_img, glow)
        
        # Final detail enhancement
        base_img = base_img.filter(ImageFilter.DETAIL)
        
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
def serve_frontend():
    """Serve the frontend index.html"""
    try:
        return send_from_directory('public', 'index.html')
    except Exception as e:
        logger.error(f"❌ Error serving frontend: {e}")
        return f"Sigilcraft Frontend Error: {e}", 500

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

    # Use Replit's PORT environment variable
    port = int(os.environ.get('PORT', 5000))
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