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
import logging
import traceback
import time
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('sigil_generator.log')
    ]
)

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error in {f.__name__}: {str(e)}")
            app.logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({
                'success': False,
                'error': 'Internal server error occurred',
                'timestamp': str(datetime.now())
            }), 500
    return decorated_function

def rate_limit(max_requests=60, per_seconds=60):
    """Simple in-memory rate limiting"""
    request_counts = {}

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
            now = time.time()

            # Clean old entries
            cutoff = now - per_seconds
            request_counts[client_ip] = [t for t in request_counts.get(client_ip, []) if t > cutoff]

            # Check rate limit
            if len(request_counts.get(client_ip, [])) >= max_requests:
                return jsonify({
                    'success': False,
                    'error': 'Rate limit exceeded. Please wait before making more requests.',
                    'retry_after': per_seconds
                }), 429

            # Add current request
            request_counts.setdefault(client_ip, []).append(now)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def create_sigil(phrase, vibe="mystical", size=2048):
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
    if '+' in vibe:
        # Handle combined vibes by layering effects
        vibe_parts = vibe.split('+')
        for i, individual_vibe in enumerate(vibe_parts):
            # Adjust opacity for layering multiple vibes
            if i > 0:
                # Create a semi-transparent overlay for additional vibes
                overlay = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)

                if individual_vibe == 'mystical':
                    create_mystical_sigil(overlay_draw, overlay, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'cosmic':
                    create_cosmic_sigil(overlay_draw, overlay, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'elemental':
                    create_elemental_sigil(overlay_draw, overlay, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'crystal':
                    create_crystal_sigil(overlay_draw, overlay, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'shadow':
                    create_shadow_sigil(overlay_draw, overlay, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'light':
                    create_light_sigil(overlay_draw, overlay, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)

                # Blend the overlay with reduced opacity
                img = Image.alpha_composite(img, overlay)
            else:
                # First vibe at full opacity
                if individual_vibe == 'mystical':
                    create_mystical_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'cosmic':
                    create_cosmic_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'elemental':
                    create_elemental_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'crystal':
                    create_crystal_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'shadow':
                    create_shadow_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
                elif individual_vibe == 'light':
                    create_light_sigil(draw, img, center, size, original_phrase, text_seed, combined_seed, pattern_seed, color_seed)
    else:
        # Single vibe
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

    # Apply additional artistic enhancement
    img = apply_artistic_enhancement(img, vibe, original_phrase)
    
    # Apply new advanced artistic features
    img = apply_advanced_artistic_features(img, vibe, original_phrase)

    print("💾 Converting to high-quality base64...")
    try:
        # Apply final quality enhancements
        print("🎨 Applying final quality pass...")
        img = apply_final_quality_pass(img, vibe, phrase)

        img_buffer = io.BytesIO()
        # Use optimized PNG compression for better file size while maintaining quality
        img.save(img_buffer, format='PNG', optimize=True, compress_level=6)
        img_buffer.seek(0)
        img_data = img_buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode()

        print(f"✅ High-quality image created successfully: {len(img_base64)} characters")
        return img_base64, None

    except MemoryError as e:
        print(f"❌ Memory error: {str(e)}")
        return None, "Image too complex. Try a shorter phrase or simpler vibe combination."
    except Exception as e:
        print(f"❌ Error converting image: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
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
    """Create flowing, ethereal mystical sigil with enhanced artistic detail"""
    random.seed(combined_seed)
    char_data = get_phrase_characteristics(phrase)

    # Enhanced mystical colors - more vibrant and magical
    base_colors = [(180, 100, 255), (255, 140, 255), (140, 220, 255), (220, 180, 255), (200, 140, 255)]
    colors = []
    for i, color in enumerate(base_colors):
        variation = (char_data['ascii_sum'] + i * 60) % 120
        new_color = (
            min(255, max(100, color[0] + variation - 60)),
            min(255, max(100, color[1] + variation - 60)),
            min(255, max(100, color[2] + variation - 60))
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

    # Create enhanced star field with multiple star types
    star_count = 200 + char_data['length'] * 12 + char_data['word_count'] * 25
    for star in range(star_count):
        random.seed(pattern_seed + star + char_data['first_char_value'])
        x = random.randint(0, size)
        y = random.randint(0, size)
        brightness = 120 + (char_data['vowel_count'] * 25) % 135 + random.randint(0, 60)
        star_size = 1 + (char_data['consonant_count'] % 6) + random.randint(0, 3)
        
        # Create different star types
        star_type = star % 4
        
        try:
            if star_type == 0:  # Regular star
                draw.ellipse([x-star_size, y-star_size, x+star_size, y+star_size],
                            fill=(brightness, brightness, brightness, 220))
            elif star_type == 1:  # Cross star
                draw.line([(x-star_size*2, y), (x+star_size*2, y)], 
                         fill=(brightness, brightness, brightness, 200), width=2)
                draw.line([(x, y-star_size*2), (x, y+star_size*2)], 
                         fill=(brightness, brightness, brightness, 200), width=2)
            elif star_type == 2:  # Diamond star
                points = [(x, y-star_size*2), (x+star_size*2, y), (x, y+star_size*2), (x-star_size*2, y)]
                draw.polygon(points, fill=(brightness, brightness, brightness, 180))
            else:  # Pulsing star with color
                color = colors[star % len(colors)]
                for pulse in range(3):
                    pulse_size = star_size + pulse
                    alpha = 200 - pulse * 50
                    draw.ellipse([x-pulse_size, y-pulse_size, x+pulse_size, y+pulse_size],
                               fill=(*color, alpha))
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
    """Create mysterious but beautiful shadow sigil with enhanced brightness - optimized"""
    random.seed(combined_seed)
    char_data = get_phrase_characteristics(phrase)

    # Enhanced shadow colors - much brighter and more vibrant
    base_colors = [(180, 120, 180), (220, 160, 220), (160, 120, 160), (200, 140, 200), (140, 140, 180)]
    colors = []
    for i, color in enumerate(base_colors):
        variation = (char_data['ascii_sum'] + i * 40) % 80
        new_color = (
            min(255, max(120, color[0] + variation - 40)),
            min(255, max(120, color[1] + variation - 40)),
            min(255, max(120, color[2] + variation - 40))
        )
        colors.append(new_color)

    # Reduced tendril count for faster generation
    tendril_count = min(12, 6 + char_data['length'] + char_data['consonant_count'])
    for tendril in range(tendril_count):
        random.seed(pattern_seed + tendril + char_data['ascii_sum'])
        start_angle = (char_data['first_char_value'] + tendril * 25) % 360

        points = []
        current_x, current_y = center

        # Reduced steps for faster generation
        steps = min(25, 15 + char_data['word_count'] * 2)
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

    # Simplified shadow runes for faster generation
    create_shadow_runes_optimized(draw, center, size, phrase, colors, text_seed, char_data)

    # Simplified void spaces
    create_void_effect_optimized(draw, center, size, phrase, combined_seed, char_data)


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


def create_shadow_runes_optimized(draw, center, size, phrase, colors, seed, char_data):
    """Create dark runic symbols with phrase characteristics - optimized"""
    random.seed(seed + char_data['ascii_sum'])

    # Limit rune count for faster generation
    rune_chars = [char for char in phrase if char.isalnum()][:8]  # Max 8 runes
    
    for i, char in enumerate(rune_chars):
        angle = (360 / len(rune_chars)) * i + ord(char) * 3
        distance = size // 6 + char_data['word_count'] * 8
        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))

        # Simplified rune complexity
        rune_complexity = min(4, 2 + (ord(char) % 3))
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

def create_void_effect_optimized(draw, center, size, phrase, seed, char_data):
    """Create void spaces in shadow sigil with phrase characteristics - optimized"""
    random.seed(seed + char_data['ascii_sum'])

    # Reduced void count for faster generation
    void_count = min(6, 2 + char_data['word_count'] + (char_data['length'] % 4))
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

def create_void_effect(draw, center, size, phrase, seed, char_data):
    """Create void spaces in shadow sigil with phrase characteristics"""
    return create_void_effect_optimized(draw, center, size, phrase, seed, char_data)


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
        # Apply advanced visual enhancements
        img = apply_advanced_effects(img, vibe, char_data)

        if vibe == 'shadow':
            # Very dark and mysterious with phrase influence
            brightness_factor = 0.5 + (char_data['consonant_count'] * 0.02)
            contrast_factor = 1.8 + (char_data['unique_chars'] * 0.05)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
            # Add shadow glow effect
            img = add_glow_effect(img, (80, 20, 80), intensity=0.8)
        elif vibe == 'light':
            # Very bright and radiant with phrase influence
            brightness_factor = 1.4 + (char_data['vowel_count'] * 0.02)
            color_factor = 1.3 + (char_data['word_count'] * 0.03)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(color_factor)
            # Add light bloom effect
            img = add_bloom_effect(img, intensity=1.2)
        elif vibe == 'cosmic':
            # Deep space contrast with phrase influence
            contrast_factor = 1.6 + (char_data['length'] * 0.01)
            color_factor = 1.6 + (char_data['numeric_count'] * 0.1)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(color_factor)
            # Add cosmic shimmer
            img = add_shimmer_effect(img)
        elif vibe == 'crystal':
            # Sharp and brilliant with phrase influence
            sharpness_factor = 2.2 + (char_data['consonant_count'] * 0.05)
            brightness_factor = 1.2 + (char_data['special_count'] * 0.05)
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness_factor)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
            # Add crystal refraction effect
            img = add_refraction_effect(img)
        elif vibe == 'elemental':
            # Natural and vivid with phrase influence
            color_factor = 1.5 + (char_data['vowel_count'] * 0.03)
            contrast_factor = 1.3 + (char_data['word_count'] * 0.02)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(color_factor)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
            # Add elemental energy effect
            img = add_energy_effect(img)
        else:  # mystical
            # Ethereal and flowing with phrase influence
            color_factor = 1.4 + (char_data['unique_chars'] * 0.02)
            brightness_factor = 1.1 + (char_data['length'] * 0.005)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(color_factor)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
            # Add mystical aura effect
            img = add_aura_effect(img)

        # Final quality enhancement
        img = enhance_overall_quality(img, char_data)

    except Exception as e:
        print(f"Post-processing warning: {e}")

    return img


def apply_advanced_effects(img, vibe, char_data):
    """Apply advanced visual effects for higher quality"""
    try:
        # Anti-aliasing and smoothing
        img = img.filter(ImageFilter.SMOOTH)

        # Enhance overall quality
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)

        # Add subtle depth
        img = add_depth_effect(img, char_data)

    except Exception as e:
        print(f"Advanced effects warning: {e}")

    return img


def add_glow_effect(img, glow_color, intensity=1.0):
    """Add a glow effect around bright areas"""
    try:
        # Create a blurred version for glow
        glow = img.filter(ImageFilter.GaussianBlur(radius=8))

        # Enhance the glow with the specified color
        glow_array = np.array(glow)
        if len(glow_array.shape) == 3 and glow_array.shape[2] >= 3:
            # Apply color tint to glow
            for i in range(3):
                glow_array[:, :, i] = np.clip(
                    glow_array[:, :, i] * (glow_color[i] / 255.0) * intensity,
                    0, 255
                )

            glow = Image.fromarray(glow_array.astype(np.uint8))

        # Blend with original
        return Image.blend(img, glow, 0.3)
    except:
        return img


def add_bloom_effect(img, intensity=1.0):
    """Add a bloom effect for light vibes"""
    try:
        # Create multiple blur levels
        bloom1 = img.filter(ImageFilter.GaussianBlur(radius=4))
        bloom2 = img.filter(ImageFilter.GaussianBlur(radius=8))
        bloom3 = img.filter(ImageFilter.GaussianBlur(radius=12))

        # Blend them together
        result = Image.blend(img, bloom1, 0.2 * intensity)
        result = Image.blend(result, bloom2, 0.15 * intensity)
        result = Image.blend(result, bloom3, 0.1 * intensity)

        return result
    except:
        return img


def add_shimmer_effect(img):
    """Add shimmer effect for cosmic vibes"""
    try:
        # Add subtle noise for shimmer
        img_array = np.array(img)
        if len(img_array.shape) == 3:
            noise = np.random.normal(0, 8, img_array.shape[:2])
            for i in range(3):
                img_array[:, :, i] = np.clip(img_array[:, :, i] + noise, 0, 255)

        return Image.fromarray(img_array.astype(np.uint8))
    except:
        return img


def add_refraction_effect(img):
    """Add refraction effect for crystal vibes"""
    try:
        # Create a subtle prismatic effect
        img_array = np.array(img)
        if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
            # Slight color separation effect
            shifted_r = np.roll(img_array[:, :, 0], 1, axis=1)
            shifted_b = np.roll(img_array[:, :, 2], -1, axis=1)

            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 0.9 + shifted_r * 0.1, 0, 255)
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.9 + shifted_b * 0.1, 0, 255)

        return Image.fromarray(img_array.astype(np.uint8))
    except:
        return img


def add_energy_effect(img):
    """Add energy effect for elemental vibes"""
    try:
        # Create energy waves
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)

        # Add slight motion blur effect
        img = img.filter(ImageFilter.BLUR)

        return img
    except:
        return img


def add_aura_effect(img):
    """Add aura effect for mystical vibes"""
    try:
        # Create soft aura
        aura = img.filter(ImageFilter.GaussianBlur(radius=12))

        # Blend with original
        return Image.blend(img, aura, 0.25)
    except:
        return img


def add_depth_effect(img, char_data):
    """Add depth and dimension to the image"""
    try:
        # Create a subtle shadow/depth effect
        depth = img.filter(ImageFilter.GaussianBlur(radius=6))

        # Darken the depth layer
        enhancer = ImageEnhance.Brightness(depth)
        depth = enhancer.enhance(0.7)

        # Offset slightly for depth
        depth_array = np.array(depth)
        img_array = np.array(img)

        # Blend with offset
        result = Image.blend(Image.fromarray(depth_array), img, 0.85)

        return result
    except:
        return img


def enhance_overall_quality(img, char_data):
    """Final quality enhancement pass"""
    try:
        # Enhance sharpness based on phrase characteristics
        sharpness_boost = 1.1 + (char_data['unique_chars'] * 0.02)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness_boost)

        # Subtle contrast enhancement
        contrast_boost = 1.05 + (char_data['consonant_count'] * 0.01)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast_boost)

        # Color saturation boost
        color_boost = 1.1 + (char_data['vowel_count'] * 0.015)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(color_boost)

        return img
    except:
        return img

def apply_final_quality_pass(img, vibe, phrase):
    """Apply final quality improvements for maximum visual impact - heavily optimized for speed"""
    try:
        char_data = get_phrase_characteristics(phrase)
        
        # Skip expensive operations that cause timeouts
        # No double-resolution for any vibe to prevent memory/time issues
        
        # Moderate sharpening to prevent processing bottlenecks
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)  # Reduced from 2.5

        # Enhanced contrast for deeper blacks and brighter colors
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.3)  # Reduced from 1.6

        # Boost color vibrancy
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.4)  # Reduced from 2.0

        # Apply simplified vibe-specific final touches
        if vibe == 'light':
            # Simplified light effects
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.2)
        elif vibe == 'shadow':
            # Simplified shadow effects
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.9)
        elif vibe == 'cosmic':
            # Simplified cosmic effects
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.4)
        elif vibe == 'crystal':
            # Simplified crystal effects
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.8)
        elif vibe == 'elemental':
            # Simplified elemental effects
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.6)
        else:  # mystical
            # Simplified mystical effects
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.5)

        # Single anti-aliasing pass for all vibes to save time
        img = img.filter(ImageFilter.SMOOTH)

        # Simplified final sharpening
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)

        # Use simplified detail enhancement for all vibes
        img = enhance_fine_details_optimized(img, char_data)

        return img
    except Exception as e:
        print(f"Final quality pass warning: {e}")
        return img

def add_simple_shadow_glow(img):
    """Simple shadow glow effect to prevent timeouts"""
    try:
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(1.1)
    except:
        return img

def enhance_fine_details_optimized(img, char_data):
    """Optimized fine detail enhancement"""
    try:
        # Simplified enhancement for faster processing
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.15)
        
        return img
    except:
        return img

def apply_artistic_enhancement(img, vibe, phrase):
    """Apply artistic enhancements to improve image quality and aesthetics."""
    char_data = get_phrase_characteristics(phrase)
    try:
        # Enhance artistic elements based on vibe
        if vibe == 'mystical':
            # Add enhanced mystical effects
            img = add_aura_effect(img)
            img = add_mystical_shimmer(img, intensity=1.8)
        elif vibe == 'cosmic':
            # Add enhanced cosmic effects
            img = add_shimmer_effect(img)
            img = add_depth_effect(img, char_data)
            img = add_stellar_glow(img, intensity=1.6)
        elif vibe == 'elemental':
            # Enhanced elemental vibrancy
            img = add_energy_effect(img)
            img = ImageEnhance.Color(img).enhance(1.25)
            img = add_elemental_energy(img, intensity=1.6)
        elif vibe == 'crystal':
            # Enhanced crystal effects
            img = ImageEnhance.Sharpness(img).enhance(1.8)
            img = add_refraction_effect(img)
            img = add_crystal_brilliance(img, intensity=1.8)
        elif vibe == 'shadow':
            # Enhanced shadow effects (much brighter now)
            img = ImageEnhance.Brightness(img).enhance(1.2)  # Brightened
            img = add_shadow_glow_effect(img)
            img = add_mystical_shimmer(img, intensity=1.4)  # Add shimmer to shadows
        elif vibe == 'light':
            # Enhanced light effects
            img = add_bloom_effect(img, intensity=1.5)
            img = ImageEnhance.Brightness(img).enhance(1.15)
            img = add_radiance_boost(img, intensity=1.8)

        # Apply enhanced sharpening for all vibes
        img = ImageEnhance.Sharpness(img).enhance(1.5)

    except Exception as e:
        print(f"Artistic enhancement warning: {e}")

    return img

def apply_advanced_artistic_features(img, vibe, phrase):
    """Apply new advanced artistic features for premium quality"""
    char_data = get_phrase_characteristics(phrase)
    try:
        print("🎨 Applying advanced artistic features...")
        
        # Add fractal enhancement for complexity
        img = add_fractal_enhancement(img, char_data)
        
        # Add holographic effect for premium feel
        img = add_holographic_effect(img, intensity=0.8)
        
        # Vibe-specific advanced features
        if '+' in vibe:
            # Combined vibes get extra enhancement
            img = add_combo_enhancement(img, vibe, char_data)
        
        # Final artistic polish
        img = add_artistic_polish(img, char_data)
        
        print("✨ Advanced artistic features applied")
        return img
        
    except Exception as e:
        print(f"Advanced artistic features warning: {e}")
        return img

def add_combo_enhancement(img, vibe, char_data):
    """Special enhancement for combined vibes"""
    try:
        # Create rainbow gradient overlay for combo vibes
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        width, height = img.size
        
        for y in range(height):
            for x in range(width):
                # Create rainbow effect
                hue = (x + y + char_data['ascii_sum']) % 360
                r = int(127 * (1 + math.sin(math.radians(hue))))
                g = int(127 * (1 + math.sin(math.radians(hue + 120))))
                b = int(127 * (1 + math.sin(math.radians(hue + 240))))
                
                # Apply only to bright areas
                original_pixel = img.getpixel((x, y))
                if isinstance(original_pixel, tuple) and len(original_pixel) >= 3:
                    brightness = sum(original_pixel[:3]) / 3
                    if brightness > 80:
                        alpha = int(30 * (brightness / 255))
                        overlay.putpixel((x, y), (r, g, b, alpha))
        
        return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    except:
        return img

def add_artistic_polish(img, char_data):
    """Final artistic polish for premium quality"""
    try:
        # Enhanced color saturation
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.4)
        
        # Enhanced contrast for depth
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.3)
        
        # Final sharpness for crisp details
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.6)
        
        return img
    except:
        return img

# Placeholder for a potential new function, if not already defined
def add_shadow_glow_effect(img):
    """Helper for shadow glow, can be further customized."""
    try:
        # Simple dark glow around edges
        glow = img.filter(ImageFilter.GaussianBlur(radius=6))
        enhancer = ImageEnhance.Brightness(glow)
        glow = enhancer.enhance(0.7)
        return Image.blend(img, glow, 0.3)
    except:
        return img

def add_radiance_boost(img, intensity=1.0):
    """Add radiant light boost effect"""
    try:
        # Create radiance overlay
        radiance = img.filter(ImageFilter.GaussianBlur(radius=15))
        enhancer = ImageEnhance.Brightness(radiance)
        radiance = enhancer.enhance(1.5 * intensity)
        return Image.blend(img, radiance, 0.4 * intensity)
    except:
        return img

def add_shadow_depth(img, intensity=1.0):
    """Add depth to shadow effects"""
    try:
        # Create depth shadow
        shadow = img.filter(ImageFilter.GaussianBlur(radius=10))
        enhancer = ImageEnhance.Brightness(shadow)
        shadow = enhancer.enhance(0.5 * intensity)
        return Image.blend(img, shadow, 0.35 * intensity)
    except:
        return img

def add_stellar_glow(img, intensity=1.0):
    """Add stellar glow for cosmic vibes"""
    try:
        # Multi-layer stellar effect
        glow1 = img.filter(ImageFilter.GaussianBlur(radius=8))
        glow2 = img.filter(ImageFilter.GaussianBlur(radius=16))

        enhancer = ImageEnhance.Color(glow1)
        glow1 = enhancer.enhance(1.8 * intensity)

        result = Image.blend(img, glow1, 0.25 * intensity)
        result = Image.blend(result, glow2, 0.15 * intensity)
        return result
    except:
        return img

def add_crystal_brilliance(img, intensity=1.0):
    """Add crystal brilliance effect"""
    try:
        # Create brilliant highlights
        brilliant = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        enhancer = ImageEnhance.Brightness(brilliant)
        brilliant = enhancer.enhance(1.4 * intensity)

        enhancer = ImageEnhance.Contrast(brilliant)
        brilliant = enhancer.enhance(1.6 * intensity)

        return Image.blend(img, brilliant, 0.3 * intensity)
    except:
        return img

def add_elemental_energy(img, intensity=1.0):
    """Add elemental energy effects"""
    try:
        # Create energy aura
        energy = img.filter(ImageFilter.EDGE_ENHANCE)
        enhancer = ImageEnhance.Color(energy)
        energy = enhancer.enhance(2.0 * intensity)

        return Image.blend(img, energy, 0.4 * intensity)
    except:
        return img

def add_mystical_shimmer(img, intensity=1.0):
    """Add mystical shimmer effect"""
    try:
        # Create ethereal shimmer
        shimmer = img.filter(ImageFilter.GaussianBlur(radius=12))
        enhancer = ImageEnhance.Color(shimmer)
        shimmer = enhancer.enhance(1.6 * intensity)

        enhancer = ImageEnhance.Brightness(shimmer)
        shimmer = enhancer.enhance(1.2 * intensity)

        return Image.blend(img, shimmer, 0.35 * intensity)
    except:
        return img

def enhance_fine_details(img, char_data):
    """Enhance fine details based on phrase characteristics"""
    try:
        # Detail enhancement based on phrase complexity
        detail_factor = 1.3 + (char_data['unique_chars'] * 0.03)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(detail_factor)

        # Micro-contrast enhancement
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.25)

        # Add artistic texture enhancement
        img = add_artistic_texture(img, char_data)

        return img
    except:
        return img

def add_artistic_texture(img, char_data):
    """Add sophisticated artistic texture to the image"""
    try:
        # Create subtle artistic noise for texture
        img_array = np.array(img)
        if len(img_array.shape) == 3:
            # Add sophisticated texture based on phrase characteristics
            texture_intensity = 5 + (char_data['unique_chars'] % 10)
            texture = np.random.normal(0, texture_intensity, img_array.shape[:2])
            
            # Apply texture differently to each color channel for artistic effect
            for i in range(3):
                channel_variation = (char_data['ascii_sum'] + i * 100) % 50
                img_array[:, :, i] = np.clip(
                    img_array[:, :, i] + texture + channel_variation - 25, 
                    0, 255
                )

        return Image.fromarray(img_array.astype(np.uint8))
    except:
        return img

def add_holographic_effect(img, intensity=1.0):
    """Add holographic shimmer effect for premium quality"""
    try:
        # Create rainbow shimmer effect
        img_array = np.array(img)
        if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
            height, width = img_array.shape[:2]
            
            # Create holographic pattern
            for y in range(height):
                for x in range(width):
                    # Create rainbow interference pattern
                    wave = np.sin((x + y) * 0.02) * intensity * 20
                    
                    # Apply holographic effect to bright areas only
                    brightness = np.mean(img_array[y, x, :3])
                    if brightness > 100:
                        img_array[y, x, 0] = np.clip(img_array[y, x, 0] + wave, 0, 255)
                        img_array[y, x, 1] = np.clip(img_array[y, x, 1] + wave * 0.8, 0, 255)
                        img_array[y, x, 2] = np.clip(img_array[y, x, 2] + wave * 1.2, 0, 255)

        return Image.fromarray(img_array.astype(np.uint8))
    except:
        return img

def add_fractal_enhancement(img, char_data):
    """Add fractal patterns for enhanced complexity"""
    try:
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Create fractal-like patterns based on phrase
        center_x, center_y = img.size[0] // 2, img.size[1] // 2
        
        # Generate multiple fractal branches
        branch_count = 8 + char_data['word_count'] * 3
        for branch in range(branch_count):
            angle = (360 / branch_count) * branch + char_data['first_char_value']
            
            # Create recursive branching pattern
            for depth in range(4):
                length = (img.size[0] // 8) * (0.7 ** depth)
                x = center_x + length * math.cos(math.radians(angle))
                y = center_y + length * math.sin(math.radians(angle))
                
                # Draw fractal branch with fading alpha
                alpha = 150 - depth * 30
                color = (
                    150 + char_data['vowel_count'] * 10,
                    100 + char_data['consonant_count'] * 8,
                    200 + char_data['unique_chars'] * 5,
                    alpha
                )
                
                width = max(1, 4 - depth)
                try:
                    draw.line([(center_x, center_y), (x, y)], fill=color, width=width)
                except:
                    pass
                
                # Update for next iteration
                center_x, center_y = x, y
                angle += 45 + char_data['numeric_count'] * 5
        
        # Blend fractal overlay
        return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    except:
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
@rate_limit(max_requests=30, per_seconds=60)
@handle_errors
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

        # Enhanced validation
        if not phrase:
            return jsonify({'success': False, 'error': 'Please enter your intent or desire'})

        if len(phrase) < 2:
            return jsonify({'success': False, 'error': 'Intent too short (minimum 2 characters)'})

        if len(phrase) > 200:
            return jsonify({'success': False, 'error': 'Intent too long (maximum 200 characters)'})
            
        # Check for potentially problematic characters
        if any(ord(c) > 1114111 for c in phrase):
            return jsonify({'success': False, 'error': 'Invalid characters detected'})
            
        # Limit complex vibe combinations to prevent timeouts
        vibe_count = len(vibe.split('+')) if '+' in vibe else 1
        if vibe_count > 4:
            return jsonify({'success': False, 'error': 'Maximum 4 vibes can be combined'})

        # Sanitize phrase
        phrase = ''.join(char for char in phrase if char.isprintable() or char.isspace())
        if not phrase.strip():
            return jsonify({'success': False, 'error': 'Invalid characters in intent'})

        valid_vibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light']

        # Handle combined vibes (e.g., "mystical+cosmic")
        if '+' in vibe:
            vibe_parts = vibe.split('+')
            # Validate each part and filter to valid vibes only
            valid_parts = [v.strip() for v in vibe_parts if v.strip() in valid_vibes]
            if valid_parts:
                vibe = '+'.join(valid_parts)
            else:
                vibe = 'mystical'
        elif vibe not in valid_vibes:
            vibe = 'mystical'

        print(f"✅ GENERATING SIGIL: '{phrase}' with vibe: '{vibe}'")

        try:
            img_base64, error = create_sigil(phrase, vibe, size=2048)

            if error:
                app.logger.error(f"Sigil creation error: {error}")
                return jsonify({'success': False, 'error': str(error)})

            if not img_base64:
                app.logger.error("No image data generated")
                return jsonify({'success': False, 'error': 'Failed to generate sigil image'})

            print(f"✅ SIGIL GENERATED SUCCESSFULLY - {len(img_base64)} chars")

        except MemoryError as me:
            app.logger.error(f"Memory error during generation: {str(me)}")
            return jsonify({'success': False, 'error': 'Image too complex. Try a shorter phrase.'})
        except Exception as generation_error:
            app.logger.error(f"Generation error: {str(generation_error)}")
            app.logger.error(f"Generation traceback: {traceback.format_exc()}")
            return jsonify({'success': False, 'error': 'Generation temporarily unavailable. Please try again.'})

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
    import os
    import socket
    
    # Find available port starting from 5001
    def find_available_port(start_port=5001):
        for port in range(start_port, start_port + 10):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('0.0.0.0', port))
                    return port
            except OSError:
                continue
        return None
    
    port = find_available_port()
    if not port:
        print("❌ No available ports found in range 5001-5010")
        exit(1)
    
    print(f"Starting Flask sigil generation server on port {port}...")
    
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
        print("⚠️  Waitress not available, installing...")
        import subprocess
        try:
            subprocess.check_call(['pip', 'install', 'waitress'])
            from waitress import serve
            print("✅ Waitress installed and ready...")
            serve(app, host="0.0.0.0", port=port, 
                  threads=8, 
                  connection_limit=200, 
                  cleanup_interval=30,
                  channel_timeout=300)
        except Exception as e:
            print(f"❌ Could not install Waitress: {e}")
            print("Using development server as fallback...")
            app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} still in use, trying Flask dev server...")
            try:
                app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
            except OSError:
                # Try one more port
                port = find_available_port(port + 1)
                if port:
                    print(f"🔄 Retrying on port {port}...")
                    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
                else:
                    print("❌ Could not find available port")
                    exit(1)
        else:
            raise
#!/usr/bin/env python3
"""
Flask backend for Sigilcraft sigil generation
Handles AI-powered sigil creation with multiple energy types
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import time
import hashlib
import base64
from io import BytesIO
import logging
from datetime import datetime
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
ENERGY_TYPES = {
    'elemental': 'Harness the raw power of earth, air, fire, and water',
    'celestial': 'Channel cosmic energies from stars and planets', 
    'quantum': 'Tap into quantum field fluctuations and probability waves',
    'nature': 'Connect with the living essence of plants and animals',
    'ancestral': 'Draw upon the wisdom and power of ancient lineages',
    'digital': 'Interface with cyberspace and digital consciousness streams'
}

def generate_sigil_data(phrase, vibe, seed=None):
    """Generate sigil data based on phrase and energy type"""
    try:
        # Create a unique hash for the sigil
        content = f"{phrase}_{vibe}_{seed or int(time.time())}"
        sigil_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # Simulate sigil generation with different patterns based on energy type
        if vibe == 'elemental':
            pattern = create_elemental_pattern(phrase, sigil_hash)
        elif vibe == 'celestial':
            pattern = create_celestial_pattern(phrase, sigil_hash)
        elif vibe == 'quantum':
            pattern = create_quantum_pattern(phrase, sigil_hash)
        elif vibe == 'nature':
            pattern = create_nature_pattern(phrase, sigil_hash)
        elif vibe == 'ancestral':
            pattern = create_ancestral_pattern(phrase, sigil_hash)
        elif vibe == 'digital':
            pattern = create_digital_pattern(phrase, sigil_hash)
        else:
            pattern = create_default_pattern(phrase, sigil_hash)
        
        # Generate SVG content
        svg_content = create_svg_sigil(pattern, vibe)
        
        return {
            'success': True,
            'svg': svg_content,
            'hash': sigil_hash,
            'energy': vibe,
            'phrase': phrase
        }
        
    except Exception as e:
        logger.error(f"Error generating sigil: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def create_elemental_pattern(phrase, hash_val):
    """Create elemental-themed pattern"""
    return {
        'type': 'elemental',
        'elements': len(phrase) % 4 + 1,
        'intensity': len(hash_val) % 10 + 1,
        'flow': 'circular' if len(phrase) % 2 == 0 else 'linear'
    }

def create_celestial_pattern(phrase, hash_val):
    """Create celestial-themed pattern"""
    return {
        'type': 'celestial',
        'stars': len(phrase) % 8 + 3,
        'orbits': len(hash_val) % 5 + 1,
        'constellation': 'spiral'
    }

def create_quantum_pattern(phrase, hash_val):
    """Create quantum-themed pattern"""
    return {
        'type': 'quantum',
        'particles': len(phrase) % 12 + 5,
        'entanglement': len(hash_val) % 3 + 1,
        'wave_function': 'probability'
    }

def create_nature_pattern(phrase, hash_val):
    """Create nature-themed pattern"""
    return {
        'type': 'nature',
        'growth': len(phrase) % 6 + 2,
        'branches': len(hash_val) % 7 + 3,
        'organic_flow': 'fibonacci'
    }

def create_ancestral_pattern(phrase, hash_val):
    """Create ancestral-themed pattern"""
    return {
        'type': 'ancestral',
        'symbols': len(phrase) % 9 + 4,
        'lineage': len(hash_val) % 4 + 1,
        'tradition': 'runic'
    }

def create_digital_pattern(phrase, hash_val):
    """Create digital-themed pattern"""
    return {
        'type': 'digital',
        'bits': len(phrase) % 16 + 8,
        'encryption': len(hash_val) % 5 + 1,
        'matrix': 'hexadecimal'
    }

def create_default_pattern(phrase, hash_val):
    """Create default pattern"""
    return {
        'type': 'neutral',
        'complexity': len(phrase) % 8 + 2,
        'symmetry': len(hash_val) % 4 + 1
    }

def create_svg_sigil(pattern, energy_type):
    """Create SVG representation of the sigil"""
    width, height = 512, 512
    center_x, center_y = width // 2, height // 2
    
    svg_parts = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        '<style>',
        f'.sigil-{energy_type} {{ fill: none; stroke: #333; stroke-width: 2; }}',
        f'.sigil-{energy_type}-fill {{ fill: #666; opacity: 0.3; }}',
        '</style>',
        '</defs>'
    ]
    
    # Generate pattern based on energy type
    if pattern['type'] == 'elemental':
        svg_parts.extend(create_elemental_svg(center_x, center_y, pattern, energy_type))
    elif pattern['type'] == 'celestial':
        svg_parts.extend(create_celestial_svg(center_x, center_y, pattern, energy_type))
    elif pattern['type'] == 'quantum':
        svg_parts.extend(create_quantum_svg(center_x, center_y, pattern, energy_type))
    elif pattern['type'] == 'nature':
        svg_parts.extend(create_nature_svg(center_x, center_y, pattern, energy_type))
    elif pattern['type'] == 'ancestral':
        svg_parts.extend(create_ancestral_svg(center_x, center_y, pattern, energy_type))
    elif pattern['type'] == 'digital':
        svg_parts.extend(create_digital_svg(center_x, center_y, pattern, energy_type))
    else:
        svg_parts.extend(create_default_svg(center_x, center_y, pattern, energy_type))
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)

def create_elemental_svg(cx, cy, pattern, energy_type):
    """Create elemental SVG elements"""
    elements = []
    radius = 100
    
    # Create circular pattern with elemental symbols
    for i in range(pattern['elements']):
        angle = (i * 360 / pattern['elements']) * 3.14159 / 180
        x = cx + radius * cos_approx(angle)
        y = cy + radius * sin_approx(angle)
        
        elements.append(f'<circle cx="{x}" cy="{y}" r="20" class="sigil-{energy_type}"/>')
        elements.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" class="sigil-{energy_type}"/>')
    
    return elements

def create_celestial_svg(cx, cy, pattern, energy_type):
    """Create celestial SVG elements"""
    elements = []
    
    # Create star pattern
    for i in range(pattern['stars']):
        radius = 50 + (i * 30)
        angle = (i * 137.5) * 3.14159 / 180  # Golden angle
        x = cx + radius * cos_approx(angle)
        y = cy + radius * sin_approx(angle)
        
        elements.append(f'<polygon points="{x},{y-10} {x+8},{y+6} {x-8},{y+6}" class="sigil-{energy_type}"/>')
    
    return elements

def create_quantum_svg(cx, cy, pattern, energy_type):
    """Create quantum SVG elements"""
    elements = []
    
    # Create quantum particle patterns
    for i in range(pattern['particles']):
        radius = 30 + (i * 15)
        angle = (i * 60) * 3.14159 / 180
        x = cx + radius * cos_approx(angle)
        y = cy + radius * sin_approx(angle)
        
        elements.append(f'<ellipse cx="{x}" cy="{y}" rx="8" ry="3" class="sigil-{energy_type}"/>')
    
    return elements

def create_nature_svg(cx, cy, pattern, energy_type):
    """Create nature SVG elements"""
    elements = []
    
    # Create organic branching pattern
    for i in range(pattern['branches']):
        angle = (i * 45) * 3.14159 / 180
        x1 = cx
        y1 = cy
        x2 = cx + 80 * cos_approx(angle)
        y2 = cy + 80 * sin_approx(angle)
        
        elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="sigil-{energy_type}"/>')
        
        # Add leaves
        leaf_x = x2 + 20 * cos_approx(angle + 0.5)
        leaf_y = y2 + 20 * sin_approx(angle + 0.5)
        elements.append(f'<ellipse cx="{leaf_x}" cy="{leaf_y}" rx="8" ry="4" class="sigil-{energy_type}-fill"/>')
    
    return elements

def create_ancestral_svg(cx, cy, pattern, energy_type):
    """Create ancestral SVG elements"""
    elements = []
    
    # Create runic-style symbols
    for i in range(pattern['symbols']):
        angle = (i * 360 / pattern['symbols']) * 3.14159 / 180
        radius = 60
        x = cx + radius * cos_approx(angle)
        y = cy + radius * sin_approx(angle)
        
        # Simple runic-style lines
        elements.append(f'<line x1="{x-10}" y1="{y-15}" x2="{x+10}" y2="{y+15}" class="sigil-{energy_type}"/>')
        elements.append(f'<line x1="{x+10}" y1="{y-15}" x2="{x-10}" y2="{y+15}" class="sigil-{energy_type}"/>')
    
    return elements

def create_digital_svg(cx, cy, pattern, energy_type):
    """Create digital SVG elements"""
    elements = []
    
    # Create digital matrix pattern
    grid_size = 20
    for i in range(-4, 5):
        for j in range(-4, 5):
            if (i + j) % 2 == 0:
                x = cx + i * grid_size
                y = cy + j * grid_size
                elements.append(f'<rect x="{x-5}" y="{y-5}" width="10" height="10" class="sigil-{energy_type}-fill"/>')
    
    return elements

def create_default_svg(cx, cy, pattern, energy_type):
    """Create default SVG elements"""
    elements = []
    
    # Simple geometric pattern
    elements.append(f'<circle cx="{cx}" cy="{cy}" r="50" class="sigil-{energy_type}"/>')
    elements.append(f'<circle cx="{cx}" cy="{cy}" r="80" class="sigil-{energy_type}"/>')
    
    return elements

def cos_approx(angle):
    """Approximate cosine function"""
    # Simple approximation for demo purposes
    import math
    return math.cos(angle)

def sin_approx(angle):
    """Approximate sine function"""
    # Simple approximation for demo purposes
    import math
    return math.sin(angle)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'flask-sigilcraft',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/generate', methods=['POST'])
def generate():
    """Generate sigil endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        phrase = data.get('phrase', '').strip()
        vibe = data.get('vibe', 'elemental').strip()
        seed = data.get('seed')
        
        if not phrase:
            return jsonify({'success': False, 'error': 'Phrase is required'}), 400
        
        if vibe not in ENERGY_TYPES:
            vibe = 'elemental'
        
        logger.info(f"Generating sigil for phrase: '{phrase}' with energy: '{vibe}'")
        
        # Generate the sigil
        result = generate_sigil_data(phrase, vibe, seed)
        
        if result['success']:
            logger.info(f"Successfully generated sigil with hash: {result['hash']}")
            return jsonify(result)
        else:
            logger.error(f"Failed to generate sigil: {result.get('error', 'Unknown error')}")
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in generate endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/energies', methods=['GET'])
def get_energies():
    """Get available energy types"""
    return jsonify({
        'energies': ENERGY_TYPES
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    
    # Check if we're in production (Replit) or development
    if os.environ.get('REPLIT_DEV_DOMAIN'):
        # Production mode with Waitress
        try:
            from waitress import serve
            logger.info(f"✅ Using Waitress production server...")
            serve(app, host='0.0.0.0', port=port, threads=4)
        except ImportError:
            logger.warning("Waitress not available, falling back to Flask dev server")
            app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Development mode
        logger.info(f"🔧 Using Flask development server...")
        app.run(host='0.0.0.0', port=port, debug=True)
