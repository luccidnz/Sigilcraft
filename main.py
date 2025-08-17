
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from datetime import datetime
import string
import math
import io
import base64
import random
import numpy as np
import hashlib

app = Flask(__name__)


def create_sigil(phrase, vibe="mystical", size=400):
    """Create a highly varied sigil with dramatic differences for each unique input"""
    print(f"🎨 Creating sigil for: '{phrase}' with vibe: '{vibe}' at size: {size}")
    
    original_phrase = phrase.strip()
    if not original_phrase:
        return None, "Please enter text with at least one character"

    # Create comprehensive hash for maximum uniqueness
    phrase_hash = hashlib.sha256(original_phrase.encode()).hexdigest()
    vibe_hash = hashlib.sha256(vibe.encode()).hexdigest()
    combined_hash = hashlib.sha256((original_phrase + vibe + str(len(original_phrase))).encode()).hexdigest()
    
    # Generate multiple seeds from different parts of the hash
    text_seed = int(phrase_hash[:8], 16) % 2147483647
    vibe_seed = int(vibe_hash[:8], 16) % 2147483647
    combined_seed = int(combined_hash[:8], 16) % 2147483647
    pattern_seed = int(phrase_hash[8:16], 16) % 2147483647
    color_seed = int(phrase_hash[16:24], 16) % 2147483647
    
    print(f"🌱 Using seeds - Text: {text_seed}, Vibe: {vibe_seed}, Combined: {combined_seed}")
    print(f"🎨 Pattern: {pattern_seed}, Color: {color_seed}")

    # Create image with black background
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    center = (size // 2, size // 2)

    # Generate vibe-specific sigil with phrase-specific variations
    if vibe == 'mystical':
        create_mystical_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
    elif vibe == 'cosmic':
        create_cosmic_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
    elif vibe == 'elemental':
        create_elemental_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
    elif vibe == 'crystal':
        create_crystal_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
    elif vibe == 'shadow':
        create_shadow_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
    elif vibe == 'light':
        create_light_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
    else:
        create_mystical_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)

    print("🎨 Applying final enhancements...")
    img = apply_vibe_effects(img, vibe, original_phrase)

    print("💾 Converting to base64...")
    try:
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG', quality=95, optimize=True)
        img_buffer.seek(0)
        img_data = img_buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode()
        
        print(f"✅ Image created successfully: {len(img_base64)} characters")
        return img_base64, None
        
    except Exception as e:
        print(f"❌ Error converting image: {str(e)}")
        return None, f"Error creating image: {str(e)}"


def get_phrase_characteristics(phrase):
    """Extract unique characteristics from the phrase for variation"""
    characteristics = {
        'length': len(phrase),
        'word_count': len(phrase.split()),
        'vowel_count': sum(1 for c in phrase.lower() if c in 'aeiou'),
        'consonant_count': sum(1 for c in phrase.lower() if c.isalpha() and c not in 'aeiou'),
        'numeric_count': sum(1 for c in phrase if c.isdigit()),
        'special_count': sum(1 for c in phrase if not c.isalnum() and not c.isspace()),
        'ascii_sum': sum(ord(c) for c in phrase),
        'unique_chars': len(set(phrase.lower())),
        'first_char_value': ord(phrase[0]) if phrase else 0,
        'last_char_value': ord(phrase[-1]) if phrase else 0
    }
    return characteristics


def create_mystical_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create flowing, ethereal mystical sigil with phrase-specific variations"""
    random.seed(combined_seed)
    char_data = get_phrase_characteristics(phrase)
    
    # Mystical colors with phrase-based variations
    base_colors = [(150, 60, 220), (255, 100, 255), (120, 200, 255), (200, 150, 255), (180, 120, 255)]
    colors = []
    for i, color in enumerate(base_colors):
        variation = (char_data['ascii_sum'] + i * 50) % 100
        new_color = (
            min(255, max(0, color[0] + variation - 50)),
            min(255, max(0, color[1] + variation - 50)),
            min(255, max(0, color[2] + variation - 50))
        )
        colors.append(new_color)
    
    # Create flowing energy streams based on phrase characteristics
    stream_count = 8 + char_data['length'] + char_data['word_count']
    for stream in range(stream_count):
        random.seed(pattern_seed + stream + char_data['ascii_sum'])
        start_angle = (char_data['first_char_value'] + stream * 30) % 360
        stream_length = 80 + (char_data['length'] * 10) + random.randint(0, size//3)
        
        # Create unique flow pattern based on phrase
        points = []
        current_x, current_y = center
        current_angle = start_angle
        
        for step in range(25 + char_data['unique_chars']):
            # Phrase-influenced angle changes
            angle_influence = (ord(phrase[step % len(phrase)]) - 32) if phrase else 0
            current_angle += random.uniform(-30, 30) + (angle_influence % 20 - 10)
            step_size = stream_length / (25 + char_data['unique_chars'])
            current_x += step_size * math.cos(math.radians(current_angle))
            current_y += step_size * math.sin(math.radians(current_angle))
            points.append((current_x, current_y))
        
        # Draw flowing line with phrase-influenced properties
        color = colors[stream % len(colors)]
        width = 2 + (char_data['vowel_count'] % 4)
        
        for i in range(len(points) - 1):
            try:
                alpha = 120 + (char_data['consonant_count'] * 5) % 135
                draw.line([points[i], points[i + 1]], fill=(*color, alpha), width=width)
            except:
                pass
    
    # Add mystical symbols based on phrase content
    create_mystical_symbols(draw, center, size, phrase, colors, text_seed, char_data)
    
    # Add ethereal particles with phrase variation
    particle_count = 30 + char_data['length'] * 3 + char_data['special_count'] * 5
    for i in range(particle_count):
        random.seed(color_seed + i + char_data['ascii_sum'])
        x = random.randint(0, size)
        y = random.randint(0, size)
        radius = 2 + (char_data['numeric_count'] % 6) + random.randint(0, 4)
        color = colors[i % len(colors)]
        alpha = 60 + (char_data['unique_chars'] * 10) % 120
        
        try:
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(*color, alpha))
        except:
            pass


def create_cosmic_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create stellar, galactic cosmic sigil with phrase-specific variations"""
    random.seed(combined_seed)
    char_data = get_phrase_characteristics(phrase)
    
    # Cosmic colors with phrase variations
    base_colors = [(20, 20, 80), (100, 150, 255), (200, 100, 255), (255, 200, 100), (50, 255, 200)]
    colors = []
    for i, color in enumerate(base_colors):
        variation = (char_data['ascii_sum'] + i * 75) % 120
        new_color = (
            min(255, max(20, color[0] + variation - 60)),
            min(255, max(20, color[1] + variation - 60)),
            min(255, max(20, color[2] + variation - 60))
        )
        colors.append(new_color)
    
    # Create star field with phrase-based density
    star_count = 150 + char_data['length'] * 8 + char_data['word_count'] * 20
    for star in range(star_count):
        random.seed(pattern_seed + star + char_data['first_char_value'])
        x = random.randint(0, size)
        y = random.randint(0, size)
        brightness = 80 + (char_data['vowel_count'] * 20) % 175 + random.randint(0, 50)
        star_size = 1 + (char_data['consonant_count'] % 4) + random.randint(0, 2)
        
        try:
            draw.ellipse([x-star_size, y-star_size, x+star_size, y+star_size], 
                        fill=(brightness, brightness, brightness, 200))
        except:
            pass
    
    # Create galactic spiral with phrase characteristics
    spiral_count = 2 + (char_data['word_count'] % 4)
    for spiral in range(spiral_count):
        random.seed(combined_seed + spiral + char_data['last_char_value'])
        start_radius = size // 12 + (char_data['length'] % 20)
        
        points = []
        angle_step = 3 + (char_data['unique_chars'] % 8)
        for angle in range(0, 720 + char_data['length'] * 20, angle_step):
            radius = start_radius + (angle / 720) * (size // 4 + char_data['numeric_count'] * 5)
            actual_angle = angle + spiral * 120 + char_data['ascii_sum'] % 180
            x = center[0] + radius * math.cos(math.radians(actual_angle))
            y = center[1] + radius * math.sin(math.radians(actual_angle))
            points.append((x, y))
        
        # Draw spiral arms with phrase-influenced properties
        color = colors[spiral % len(colors)]
        width = 3 + (char_data['special_count'] % 3)
        alpha = 120 + (char_data['vowel_count'] * 15) % 120
        
        for i in range(len(points) - 1):
            try:
                draw.line([points[i], points[i + 1]], fill=(*color, alpha), width=width)
            except:
                pass
    
    # Add constellation based on phrase
    create_constellation(draw, center, size, phrase, colors, text_seed, char_data)
    
    # Add nebula clouds with phrase variation
    create_nebula_effect(img, colors, combined_seed, char_data)


def create_elemental_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create elemental sigil with phrase-specific elemental patterns"""
    random.seed(combined_seed)
    char_data = get_phrase_characteristics(phrase)
    
    # Elemental colors with phrase variations
    base_colors = [(255, 100, 50), (50, 255, 100), (100, 150, 255), (200, 150, 100), (255, 200, 50)]
    colors = []
    for i, color in enumerate(base_colors):
        variation = (char_data['ascii_sum'] + i * 60) % 100
        new_color = (
            min(255, max(50, color[0] + variation - 50)),
            min(255, max(50, color[1] + variation - 50)),
            min(255, max(50, color[2] + variation - 50))
        )
        colors.append(new_color)
    
    # Determine dominant element from phrase characteristics
    element_value = (char_data['ascii_sum'] + char_data['length'] + char_data['word_count']) % 4
    
    if element_value == 0:  # Fire
        create_fire_pattern(draw, center, size, phrase, colors, text_seed, char_data)
    elif element_value == 1:  # Water
        create_water_pattern(draw, center, size, phrase, colors, text_seed, char_data)
    elif element_value == 2:  # Earth
        create_earth_pattern(draw, center, size, phrase, colors, text_seed, char_data)
    else:  # Air
        create_air_pattern(draw, center, size, phrase, colors, text_seed, char_data)
    
    # Add elemental symbols
    create_elemental_symbols(draw, center, size, phrase, colors, combined_seed, char_data)


def create_crystal_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create geometric crystal sigil with phrase-specific patterns"""
    random.seed(combined_seed)
    char_data = get_phrase_characteristics(phrase)
    
    # Crystal colors with phrase variations
    base_colors = [(200, 255, 255), (150, 200, 255), (255, 200, 255), (200, 255, 200), (255, 255, 200)]
    colors = []
    for i, color in enumerate(base_colors):
        variation = (char_data['ascii_sum'] + i * 40) % 80
        new_color = (
            min(255, max(150, color[0] + variation - 40)),
            min(255, max(150, color[1] + variation - 40)),
            min(255, max(150, color[2] + variation - 40))
        )
        colors.append(new_color)
    
    # Create crystal lattice structure based on phrase
    lattice_points = []
    grid_size = 4 + char_data['word_count'] + (char_data['length'] % 6)
    
    for i in range(grid_size):
        for j in range(grid_size):
            x_offset = (char_data['first_char_value'] % 20 - 10) / 100
            y_offset = (char_data['last_char_value'] % 20 - 10) / 100
            x = (i / (grid_size - 1)) * size * 0.8 + size * 0.1 + x_offset * size
            y = (j / (grid_size - 1)) * size * 0.8 + size * 0.1 + y_offset * size
            lattice_points.append((x, y))
    
    # Connect lattice points in phrase-influenced patterns
    random.seed(pattern_seed + char_data['ascii_sum'])
    for i, point in enumerate(lattice_points):
        connections = 2 + (char_data['unique_chars'] % 4)
        for conn in range(connections):
            target_idx = (i + conn * char_data['consonant_count'] + char_data['vowel_count']) % len(lattice_points)
            target_point = lattice_points[target_idx]
            
            color = colors[(i + char_data['numeric_count']) % len(colors)]
            width = 1 + (char_data['special_count'] % 3)
            alpha = 100 + (char_data['length'] * 5) % 120
            
            try:
                draw.line([point, target_point], fill=(*color, alpha), width=width)
            except:
                pass
    
    # Add crystal facets with phrase variation
    create_crystal_facets(draw, center, size, phrase, colors, combined_seed, char_data)
    
    # Add geometric patterns
    create_geometric_patterns(draw, center, size, phrase, colors, text_seed, char_data)


def create_shadow_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create dark, mysterious shadow sigil with phrase-specific variations"""
    random.seed(combined_seed)
    char_data = get_phrase_characteristics(phrase)
    
    # Shadow colors with phrase variations
    base_colors = [(80, 20, 80), (120, 60, 120), (60, 20, 60), (100, 40, 100), (40, 40, 80)]
    colors = []
    for i, color in enumerate(base_colors):
        variation = (char_data['ascii_sum'] + i * 30) % 60
        new_color = (
            min(150, max(20, color[0] + variation - 30)),
            min(150, max(20, color[1] + variation - 30)),
            min(150, max(20, color[2] + variation - 30))
        )
        colors.append(new_color)
    
    # Create shadow tendrils with phrase characteristics
    tendril_count = 8 + char_data['length'] + char_data['consonant_count']
    for tendril in range(tendril_count):
        random.seed(pattern_seed + tendril + char_data['ascii_sum'])
        start_angle = (char_data['first_char_value'] + tendril * 25) % 360
        
        points = []
        current_x, current_y = center
        
        steps = 20 + char_data['word_count'] * 3
        for step in range(steps):
            distance = step * (size // 40 + char_data['unique_chars'])
            angle_influence = (ord(phrase[step % len(phrase)]) - 32) if phrase else 0
            angle_variation = random.uniform(-45, 45) + (angle_influence % 30 - 15)
            actual_angle = start_angle + angle_variation
            
            x = current_x + distance * math.cos(math.radians(actual_angle))
            y = current_y + distance * math.sin(math.radians(actual_angle))
            points.append((x, y))
            
            current_x, current_y = x, y
        
        # Draw tendril with phrase-influenced properties
        color = colors[tendril % len(colors)]
        for i in range(len(points) - 1):
            thickness = max(1, 6 + char_data['numeric_count'] - i // 2)
            alpha = 140 + (char_data['special_count'] * 10) % 100
            try:
                draw.line([points[i], points[i + 1]], fill=(*color, alpha), width=thickness)
            except:
                pass
    
    # Add shadow runes
    create_shadow_runes(draw, center, size, phrase, colors, text_seed, char_data)
    
    # Add void spaces
    create_void_effect(draw, center, size, phrase, combined_seed, char_data)


def create_light_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create radiant, healing light sigil with phrase-specific variations"""
    random.seed(combined_seed)
    char_data = get_phrase_characteristics(phrase)
    
    # Light colors with phrase variations
    base_colors = [(255, 255, 200), (255, 200, 150), (200, 255, 200), (255, 220, 255), (255, 255, 150)]
    colors = []
    for i, color in enumerate(base_colors):
        variation = (char_data['ascii_sum'] + i * 25) % 50
        new_color = (
            min(255, max(200, color[0] + variation - 25)),
            min(255, max(200, color[1] + variation - 25)),
            min(255, max(200, color[2] + variation - 25))
        )
        colors.append(new_color)
    
    # Create radial light beams with phrase characteristics
    beam_count = 12 + char_data['length'] + char_data['vowel_count'] * 2
    for beam in range(beam_count):
        angle = (360 / beam_count) * beam + (char_data['first_char_value'] % 45)
        beam_length = size // 3 + char_data['word_count'] * 10
        
        # Create beam gradient with phrase influence
        intensity_levels = 8 + char_data['unique_chars'] % 6
        for intensity in range(intensity_levels):
            current_length = beam_length * (intensity + 1) / intensity_levels
            x = center[0] + current_length * math.cos(math.radians(angle))
            y = center[1] + current_length * math.sin(math.radians(angle))
            
            alpha = 200 - intensity * 15 + (char_data['consonant_count'] % 20)
            color = colors[beam % len(colors)]
            width = max(1, 5 + char_data['numeric_count'] - intensity // 2)
            
            try:
                draw.line([center, (x, y)], fill=(*color, alpha), width=width)
            except:
                pass
    
    # Add light orbs with phrase variation
    create_light_orbs(draw, center, size, phrase, colors, text_seed, char_data)
    
    # Add healing symbols
    create_healing_symbols(draw, center, size, phrase, colors, combined_seed, char_data)
    
    # Add radiance effect
    create_radiance_effect(img, center, size, colors, char_data)


# Updated helper functions with phrase characteristics
def create_mystical_symbols(draw, center, size, phrase, colors, seed, char_data):
    """Create flowing mystical symbols based on phrase content"""
    random.seed(seed + char_data['ascii_sum'])
    
    # Use actual characters from phrase for symbol placement
    for i, char in enumerate(phrase):
        if char.isalnum():
            angle = (360 / len([c for c in phrase if c.isalnum()])) * i + ord(char)
            distance = size // 5 + (char_data['length'] * 2) + (ord(char) % 50)
            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))
            
            # Create character-specific glyph
            glyph_size = 15 + (ord(char) % 20) + char_data['word_count']
            color = colors[(ord(char) + i) % len(colors)]
            
            # Draw complex symbol based on character
            symbol_parts = 3 + (ord(char) % 6)
            for symbol_part in range(symbol_parts):
                part_angle = angle + symbol_part * (360 / symbol_parts) + char_data['first_char_value']
                inner_x = x + glyph_size * math.cos(math.radians(part_angle))
                inner_y = y + glyph_size * math.sin(math.radians(part_angle))
                
                try:
                    width = 2 + (char_data['special_count'] % 3)
                    draw.line([(x, y), (inner_x, inner_y)], fill=(*color, 200), width=width)
                    radius = 2 + (ord(char) % 4)
                    draw.ellipse([inner_x-radius, inner_y-radius, inner_x+radius, inner_y+radius], 
                               fill=(*color, 255))
                except:
                    pass


def create_constellation(draw, center, size, phrase, colors, seed, char_data):
    """Create constellation pattern based on phrase content"""
    random.seed(seed + char_data['ascii_sum'])
    
    # Create star positions based on each character in phrase
    star_positions = []
    for i, char in enumerate(phrase):
        if char.isalnum():
            char_value = ord(char)
            angle = (360 / len([c for c in phrase if c.isalnum()])) * i + char_value * 5
            distance = (size // 8) + (char_value % 80) + char_data['word_count'] * 10
            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))
            star_positions.append((x, y, char_value))
    
    # Connect stars based on character relationships
    for i in range(len(star_positions)):
        for j in range(i + 1, len(star_positions)):
            char_diff = abs(star_positions[i][2] - star_positions[j][2])
            if char_diff % 3 == 0 or (i + j) % 4 == char_data['length'] % 4:
                color = colors[(char_diff + i + j) % len(colors)]
                try:
                    alpha = 100 + (char_diff % 120)
                    draw.line([star_positions[i][:2], star_positions[j][:2]], 
                             fill=(*color, alpha), width=2)
                except:
                    pass
        
        # Draw bright star based on character
        pos = star_positions[i][:2]
        char_val = star_positions[i][2]
        color = colors[(char_val + char_data['numeric_count']) % len(colors)]
        radius = 4 + (char_val % 6)
        try:
            draw.ellipse([pos[0]-radius, pos[1]-radius, pos[0]+radius, pos[1]+radius], 
                        fill=(*color, 255))
        except:
            pass


# Additional helper functions with char_data parameter
def create_fire_pattern(draw, center, size, phrase, colors, seed, char_data):
    """Create fire elemental pattern with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    flame_count = 6 + char_data['length'] + char_data['consonant_count']
    for flame in range(flame_count):
        base_x = center[0] + random.randint(-size//5, size//5) + (char_data['first_char_value'] % 40 - 20)
        base_y = center[1] + size//4 + (char_data['word_count'] * 10)
        
        flame_height = size//4 + char_data['vowel_count'] * 15 + random.randint(0, size//6)
        flame_points = []
        
        for height in range(0, flame_height, 8):
            flicker = random.randint(-25, 25) + (char_data['last_char_value'] % 20 - 10)
            x = base_x + flicker
            y = base_y - height
            flame_points.append((x, y))
        
        # Draw flame with phrase-influenced properties
        color = colors[(flame + char_data['numeric_count']) % len(colors)]
        for i in range(len(flame_points) - 1):
            width = max(1, 7 + char_data['special_count'] - i // 2)
            alpha = max(100, 255 - i * 8 + char_data['unique_chars'])
            try:
                draw.line([flame_points[i], flame_points[i + 1]], 
                         fill=(*color, alpha), width=width)
            except:
                pass


def create_water_pattern(draw, center, size, phrase, colors, seed, char_data):
    """Create water elemental pattern with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    wave_count = 4 + char_data['word_count']
    for wave in range(wave_count):
        y_offset = center[1] - size//4 + wave * (size//8) + (char_data['first_char_value'] % 30 - 15)
        
        wave_points = []
        for x in range(0, size, 8):
            wave_influence = char_data['ascii_sum'] / 1000
            wave_height = (25 + char_data['vowel_count']) * math.sin((x + wave * 40 + char_data['last_char_value']) * (0.02 + wave_influence))
            y = y_offset + wave_height
            wave_points.append((x, y))
        
        # Draw wave with phrase properties
        color = colors[(wave + char_data['consonant_count']) % len(colors)]
        width = 2 + (char_data['numeric_count'] % 4)
        alpha = 130 + (char_data['special_count'] * 15) % 100
        
        for i in range(len(wave_points) - 1):
            try:
                draw.line([wave_points[i], wave_points[i + 1]], 
                         fill=(*color, alpha), width=width)
            except:
                pass


def create_earth_pattern(draw, center, size, phrase, colors, seed, char_data):
    """Create earth elemental pattern with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    rock_count = 8 + char_data['length'] + char_data['consonant_count']
    for rock in range(rock_count):
        x = random.randint(size//8, size - size//8) + (char_data['first_char_value'] % 20 - 10)
        y = random.randint(size//8, size - size//8) + (char_data['last_char_value'] % 20 - 10)
        rock_size = 12 + char_data['word_count'] * 5 + random.randint(0, 25) + (char_data['vowel_count'] % 15)
        
        # Draw rock as polygon with phrase influence
        points = []
        sides = 6 + (char_data['unique_chars'] % 4)
        for angle in range(0, 360, 360//sides):
            variation = random.randint(-8, 8) + (char_data['numeric_count'] % 10 - 5)
            radius = rock_size + variation
            px = x + radius * math.cos(math.radians(angle + char_data['special_count'] * 10))
            py = y + radius * math.sin(math.radians(angle + char_data['special_count'] * 10))
            points.append((px, py))
        
        color = colors[(rock + char_data['ascii_sum']) % len(colors)]
        alpha = 160 + (char_data['length'] * 5) % 80
        try:
            draw.polygon(points, fill=(*color, alpha))
        except:
            pass


def create_air_pattern(draw, center, size, phrase, colors, seed, char_data):
    """Create air elemental pattern with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    spiral_count = 3 + char_data['word_count']
    for spiral in range(spiral_count):
        spiral_center_x = center[0] + random.randint(-size//5, size//5) + (char_data['first_char_value'] % 30 - 15)
        spiral_center_y = center[1] + random.randint(-size//5, size//5) + (char_data['last_char_value'] % 30 - 15)
        
        spiral_points = []
        angle_step = 12 + (char_data['unique_chars'] % 8)
        max_angle = 540 + char_data['length'] * 10 + char_data['vowel_count'] * 20
        
        for angle in range(0, max_angle, angle_step):
            radius = (angle / max_angle) * (size // 6 + char_data['consonant_count'] * 3)
            actual_angle = angle + char_data['ascii_sum'] % 180
            x = spiral_center_x + radius * math.cos(math.radians(actual_angle))
            y = spiral_center_y + radius * math.sin(math.radians(actual_angle))
            spiral_points.append((x, y))
        
        # Draw spiral with phrase properties
        color = colors[(spiral + char_data['numeric_count']) % len(colors)]
        width = 2 + (char_data['special_count'] % 3)
        alpha = 120 + (char_data['word_count'] * 15) % 100
        
        for i in range(len(spiral_points) - 1):
            try:
                draw.line([spiral_points[i], spiral_points[i + 1]], 
                         fill=(*color, alpha), width=width)
            except:
                pass


def create_elemental_symbols(draw, center, size, phrase, colors, seed, char_data):
    """Create elemental symbols with phrase characteristics"""
    symbols = ['▲', '▼', '◆', '○']
    symbol_count = 4 + (char_data['word_count'] % 3)
    
    for i in range(symbol_count):
        angle = (360 / symbol_count) * i + char_data['first_char_value']
        distance = size // 4 + char_data['length'] * 3
        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))
        
        symbol_type = (i + char_data['ascii_sum']) % 4
        color = colors[(i + char_data['last_char_value']) % len(colors)]
        symbol_size = 12 + char_data['vowel_count'] + (char_data['unique_chars'] % 8)
        alpha = 180 + (char_data['consonant_count'] * 10) % 75
        
        # Draw elemental symbol based on type
        if symbol_type == 0:  # Fire triangle
            points = [(x, y-symbol_size), (x-symbol_size, y+symbol_size//2), (x+symbol_size, y+symbol_size//2)]
        elif symbol_type == 1:  # Water triangle
            points = [(x, y+symbol_size), (x-symbol_size, y-symbol_size//2), (x+symbol_size, y-symbol_size//2)]
        elif symbol_type == 2:  # Earth diamond
            points = [(x, y-symbol_size), (x+symbol_size, y), (x, y+symbol_size), (x-symbol_size, y)]
        else:  # Air circle
            try:
                width = 2 + (char_data['numeric_count'] % 3)
                draw.ellipse([x-symbol_size, y-symbol_size, x+symbol_size, y+symbol_size], 
                           outline=(*color, alpha), width=width)
                continue
            except:
                continue
        
        try:
            draw.polygon(points, fill=(*color, alpha))
        except:
            pass


def create_crystal_facets(draw, center, size, phrase, colors, seed, char_data):
    """Create crystal facet patterns with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    facet_count = 4 + char_data['length'] + char_data['word_count'] * 2
    for facet in range(facet_count):
        # Create triangular facets based on phrase
        angle = (char_data['first_char_value'] + facet * 30) % 360
        distance = random.randint(size//8, size//3) + (char_data['vowel_count'] * 5)
        
        facet_x = center[0] + distance * math.cos(math.radians(angle))
        facet_y = center[1] + distance * math.sin(math.radians(angle))
        
        facet_size = 15 + char_data['consonant_count'] + random.randint(0, 30) + (char_data['unique_chars'] % 15)
        
        # Create facet as triangle with phrase influence
        points = []
        for i in range(3):
            point_angle = angle + i * 120 + char_data['last_char_value']
            px = facet_x + facet_size * math.cos(math.radians(point_angle))
            py = facet_y + facet_size * math.sin(math.radians(point_angle))
            points.append((px, py))
        
        color = colors[(facet + char_data['numeric_count']) % len(colors)]
        alpha = 140 + (char_data['special_count'] * 10) % 100
        outline_alpha = 200 + (char_data['word_count'] * 15) % 55
        
        try:
            draw.polygon(points, fill=(*color, alpha), outline=(*color, outline_alpha))
        except:
            pass


def create_geometric_patterns(draw, center, size, phrase, colors, seed, char_data):
    """Create geometric patterns with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    grid_size = 4 + (char_data['word_count'] % 3)
    for i in range(grid_size):
        for j in range(grid_size):
            x = size * 0.2 + i * size * (0.6 / (grid_size - 1)) + (char_data['first_char_value'] % 20 - 10)
            y = size * 0.2 + j * size * (0.6 / (grid_size - 1)) + (char_data['last_char_value'] % 20 - 10)
            
            pattern_type = (i + j + char_data['ascii_sum']) % 4
            color = colors[(i + j + char_data['numeric_count']) % len(colors)]
            pattern_size = 8 + char_data['unique_chars'] + (char_data['vowel_count'] % 6)
            alpha = 180 + (char_data['consonant_count'] * 5) % 70
            width = 2 + (char_data['special_count'] % 2)
            
            try:
                if pattern_type == 0:  # Square
                    draw.rectangle([x-pattern_size, y-pattern_size, x+pattern_size, y+pattern_size], 
                                 outline=(*color, alpha), width=width)
                elif pattern_type == 1:  # Circle
                    draw.ellipse([x-pattern_size, y-pattern_size, x+pattern_size, y+pattern_size], 
                               outline=(*color, alpha), width=width)
                elif pattern_type == 2:  # Triangle
                    points = [(x, y-pattern_size), (x-pattern_size, y+pattern_size//2), (x+pattern_size, y+pattern_size//2)]
                    draw.polygon(points, outline=(*color, alpha))
                else:  # Diamond
                    points = [(x, y-pattern_size), (x+pattern_size, y), (x, y+pattern_size), (x-pattern_size, y)]
                    draw.polygon(points, outline=(*color, alpha))
            except:
                pass


def create_shadow_runes(draw, center, size, phrase, colors, seed, char_data):
    """Create dark runic symbols with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    # Create runes based on actual characters in phrase
    for i, char in enumerate(phrase):
        if char.isalnum():
            angle = (360 / len([c for c in phrase if c.isalnum()])) * i + ord(char) * 3
            distance = size // 6 + char_data['word_count'] * 8
            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))
            
            # Create complex rune based on character
            rune_complexity = 3 + (ord(char) % 6) + char_data['consonant_count'] % 4
            color = colors[(ord(char) + i + char_data['vowel_count']) % len(colors)]
            
            for rune_line in range(rune_complexity):
                line_angle = angle + rune_line * 45 + char_data['first_char_value']
                line_length = 12 + (ord(char) % 12) + char_data['unique_chars']
                
                start_x = x + (line_length // 2) * math.cos(math.radians(line_angle))
                start_y = y + (line_length // 2) * math.sin(math.radians(line_angle))
                end_x = x - (line_length // 2) * math.cos(math.radians(line_angle))
                end_y = y - (line_length // 2) * math.sin(math.radians(line_angle))
                
                width = 2 + (char_data['numeric_count'] % 3)
                alpha = 200 + (char_data['special_count'] * 10) % 55
                
                try:
                    draw.line([(start_x, start_y), (end_x, end_y)], 
                             fill=(*color, alpha), width=width)
                except:
                    pass


def create_void_effect(draw, center, size, phrase, seed, char_data):
    """Create void spaces in shadow sigil with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    void_count = 2 + char_data['word_count'] + (char_data['length'] % 4)
    for void in range(void_count):
        void_x = random.randint(size//6, size - size//6) + (char_data['first_char_value'] % 30 - 15)
        void_y = random.randint(size//6, size - size//6) + (char_data['last_char_value'] % 30 - 15)
        void_radius = 8 + char_data['vowel_count'] * 2 + random.randint(0, 20) + (char_data['consonant_count'] % 10)
        
        # Create void with phrase-influenced properties
        outline_alpha = 150 + (char_data['unique_chars'] * 8) % 100
        
        try:
            draw.ellipse([void_x-void_radius, void_y-void_radius, 
                         void_x+void_radius, void_y+void_radius], 
                        fill=(0, 0, 0, 255), outline=(40, 40, 40, outline_alpha))
        except:
            pass


def create_light_orbs(draw, center, size, phrase, colors, seed, char_data):
    """Create radiant light orbs with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    orb_count = 6 + char_data['length'] + char_data['vowel_count'] * 2
    for orb in range(orb_count):
        orb_x = random.randint(size//8, size - size//8) + (char_data['first_char_value'] % 25 - 12)
        orb_y = random.randint(size//8, size - size//8) + (char_data['last_char_value'] % 25 - 12)
        orb_radius = 6 + char_data['word_count'] * 3 + random.randint(0, 15) + (char_data['consonant_count'] % 12)
        
        color = colors[(orb + char_data['numeric_count']) % len(colors)]
        
        # Create orb with gradient effect and phrase influence
        gradient_steps = 3 + (char_data['unique_chars'] % 4)
        for radius_step in range(orb_radius, 0, -max(1, orb_radius // gradient_steps)):
            alpha = int(255 * (radius_step / orb_radius) * 0.7) + (char_data['special_count'] % 30)
            alpha = min(255, max(50, alpha))
            try:
                draw.ellipse([orb_x-radius_step, orb_y-radius_step, 
                             orb_x+radius_step, orb_y+radius_step], 
                            fill=(*color, alpha))
            except:
                pass


def create_healing_symbols(draw, center, size, phrase, colors, seed, char_data):
    """Create healing light symbols with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    symbol_count = 3 + char_data['word_count'] + (char_data['length'] % 5)
    for i in range(symbol_count):
        angle = (360 / symbol_count) * i + char_data['first_char_value'] + char_data['last_char_value']
        distance = size // 5 + char_data['vowel_count'] * 8
        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))
        
        color = colors[(i + char_data['consonant_count']) % len(colors)]
        cross_size = 12 + char_data['unique_chars'] + (char_data['numeric_count'] % 8)
        width = 3 + (char_data['special_count'] % 3)
        alpha = 200 + (char_data['word_count'] * 10) % 55
        
        # Draw healing cross with phrase influence
        try:
            # Vertical line
            draw.line([(x, y-cross_size), (x, y+cross_size)], 
                     fill=(*color, alpha), width=width)
            # Horizontal line
            draw.line([(x-cross_size, y), (x+cross_size, y)], 
                     fill=(*color, alpha), width=width)
        except:
            pass


def create_radiance_effect(img, center, size, colors, char_data):
    """Create radiance effect for light sigil with phrase characteristics"""
    # Create radial gradient overlay based on phrase
    for y in range(size):
        for x in range(size):
            distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            max_distance = size / 2
            
            if distance < max_distance:
                intensity = 1 - (distance / max_distance)
                intensity_boost = char_data['vowel_count'] * 0.1 + char_data['word_count'] * 0.05
                intensity = min(1.0, intensity + intensity_boost)
                
                current_pixel = img.getpixel((x, y))
                
                # Add golden radiance with phrase influence
                if len(current_pixel) == 4:  # RGBA
                    r, g, b, a = current_pixel
                    radiance_boost = int(intensity * (25 + char_data['unique_chars']))
                    new_r = min(255, r + radiance_boost)
                    new_g = min(255, g + radiance_boost)
                    new_b = min(255, b + radiance_boost // 2)
                    img.putpixel((x, y), (new_r, new_g, new_b, a))


def create_nebula_effect(img, colors, seed, char_data):
    """Create nebula cloud effect for cosmic sigil with phrase characteristics"""
    random.seed(seed + char_data['ascii_sum'])
    
    cloud_count = 3 + char_data['word_count'] + (char_data['length'] % 4)
    for cloud in range(cloud_count):
        cloud_x = random.randint(0, img.width) + (char_data['first_char_value'] % 40 - 20)
        cloud_y = random.randint(0, img.height) + (char_data['last_char_value'] % 40 - 20)
        cloud_size = 40 + char_data['vowel_count'] * 8 + random.randint(0, 80) + (char_data['consonant_count'] % 30)
        color = colors[(cloud + char_data['numeric_count']) % len(colors)]
        
        for radius in range(cloud_size, 0, -max(1, cloud_size // 10)):
            alpha = int(80 * (radius / cloud_size)) + (char_data['unique_chars'] % 20)
            alpha = min(120, max(20, alpha))
            
            # Create soft circular gradient with phrase influence
            angle_step = 8 + (char_data['special_count'] % 6)
            for angle in range(0, 360, angle_step):
                x = cloud_x + radius * math.cos(math.radians(angle + char_data['ascii_sum'] % 180))
                y = cloud_y + radius * math.sin(math.radians(angle + char_data['ascii_sum'] % 180))
                
                if 0 <= x < img.width and 0 <= y < img.height:
                    current_pixel = img.getpixel((int(x), int(y)))
                    if len(current_pixel) == 4:
                        r, g, b, a = current_pixel
                        blend_r = min(255, r + color[0] * alpha // 255)
                        blend_g = min(255, g + color[1] * alpha // 255)
                        blend_b = min(255, b + color[2] * alpha // 255)
                        img.putpixel((int(x), int(y)), (blend_r, blend_g, blend_b, a))


def apply_vibe_effects(img, vibe, phrase):
    """Apply final vibe-specific effects with phrase characteristics"""
    char_data = get_phrase_characteristics(phrase)
    
    try:
        if vibe == 'shadow':
            # Very dark and mysterious with phrase influence
            brightness_factor = 0.5 + (char_data['consonant_count'] * 0.02)
            contrast_factor = 1.6 + (char_data['unique_chars'] * 0.05)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
        elif vibe == 'light':
            # Very bright and radiant with phrase influence
            brightness_factor = 1.3 + (char_data['vowel_count'] * 0.02)
            color_factor = 1.2 + (char_data['word_count'] * 0.03)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(color_factor)
        elif vibe == 'cosmic':
            # Deep space contrast with phrase influence
            contrast_factor = 1.4 + (char_data['length'] * 0.01)
            color_factor = 1.5 + (char_data['numeric_count'] * 0.1)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(color_factor)
        elif vibe == 'crystal':
            # Sharp and brilliant with phrase influence
            sharpness_factor = 1.8 + (char_data['consonant_count'] * 0.05)
            brightness_factor = 1.1 + (char_data['special_count'] * 0.05)
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness_factor)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
        elif vibe == 'elemental':
            # Natural and vivid with phrase influence
            color_factor = 1.4 + (char_data['vowel_count'] * 0.03)
            contrast_factor = 1.2 + (char_data['word_count'] * 0.02)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(color_factor)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
        else:  # mystical
            # Ethereal and flowing with phrase influence
            color_factor = 1.3 + (char_data['unique_chars'] * 0.02)
            brightness_factor = 1.05 + (char_data['length'] * 0.005)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(color_factor)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
    except Exception as e:
        print(f"Post-processing warning: {e}")
    
    return img


@app.route('/')
def index():
    return render_template('index.html')

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
def generate():
    try:
        print("=== GENERATE REQUEST RECEIVED ===")
        
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Request must be JSON'}), 400
            
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
            
        phrase = data.get('phrase', '').strip()
        vibe = data.get('vibe', 'mystical').strip().lower()

        print(f"Received phrase: '{phrase}' with vibe: '{vibe}'")

        if not phrase:
            return jsonify({'success': False, 'error': 'Please enter your intent or desire'})
            
        if len(phrase) > 200:
            return jsonify({'success': False, 'error': 'Phrase too long (max 200 characters)'})

        valid_vibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light']
        if vibe not in valid_vibes:
            vibe = 'mystical'

        print(f"✅ GENERATING SIGIL: '{phrase}' with vibe: '{vibe}'")
        
        try:
            img_base64, error = create_sigil(phrase, vibe, size=400)
            
            if error:
                return jsonify({'success': False, 'error': error})

            if not img_base64:
                return jsonify({'success': False, 'error': 'Failed to generate sigil image'})
                
            print(f"✅ SIGIL GENERATED SUCCESSFULLY")
                
        except Exception as generation_error:
            print(f"GENERATION ERROR: {str(generation_error)}")
            return jsonify({'success': False, 'error': 'Sigil generation failed. Please try again.'})

        response_data = {
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'phrase': phrase,
            'vibe': vibe,
            'timestamp': str(datetime.now())
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"CRITICAL ERROR in generate endpoint: {str(e)}")
        return jsonify({'success': False, 'error': f'Server error: Please try again'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
