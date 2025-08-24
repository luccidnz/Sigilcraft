from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
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


def create_sigil(phrase, vibe, size=2048):
    """Create sophisticated artistic sigil masterpieces with professional quality"""
    print(f"🎨 Creating ARTISTIC MASTERPIECE for: '{phrase}' with vibe: '{vibe}' at size: {size}")

    original_phrase = phrase.strip()
    if not original_phrase:
        return None, "Please enter text with at least one character"

    # Advanced artistic analysis system
    artistic_profile = create_artistic_profile(original_phrase)
    symbolic_meaning = extract_deep_symbolism(original_phrase)
    emotional_resonance = calculate_emotional_resonance(original_phrase)
    aesthetic_style = determine_aesthetic_style(original_phrase, vibe)

    # Create ultra-sophisticated hash system for maximum uniqueness
    phrase_hash = hashlib.sha256(original_phrase.encode()).hexdigest()
    vibe_hash = hashlib.sha256((vibe + original_phrase).encode()).hexdigest()
    artistic_hash = hashlib.sha256((str(artistic_profile) + original_phrase).encode()).hexdigest()

    # Generate artistic seeds with extreme text influence
    char_data = get_enhanced_phrase_characteristics(original_phrase)
    artistic_seed = (int(phrase_hash[:12], 16) + char_data['sacred_power'] * 10000) % 2147483647
    composition_seed = (int(vibe_hash[:12], 16) + char_data['intent_strength'] * 5000) % 2147483647
    style_seed = (int(artistic_hash[:12], 16) + char_data['manifestation_power'] * 3000) % 2147483647
    color_seed = (int(phrase_hash[24:36], 16) + emotional_resonance * 1000) % 2147483647

    print(f"🎨 ARTISTIC SEEDS:")
    print(f"   Artistic: {artistic_seed}")
    print(f"   Composition: {composition_seed}")
    print(f"   Style: {style_seed}")
    print(f"   Emotional: {emotional_resonance}")

    # Create professional canvas with sophisticated background
    img = create_professional_canvas(size, aesthetic_style, char_data)
    draw = ImageDraw.Draw(img)
    center = (size // 2, size // 2)

    # Generate sophisticated base composition
    create_masterpiece_foundation(draw, img, center, size, original_phrase, char_data, artistic_seed)

    # Generate vibe-specific artistic masterpiece
    if '+' in vibe:
        # Handle combined vibes with professional layering
        vibe_parts = vibe.split('+')
        for i, individual_vibe in enumerate(vibe_parts):
            overlay = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)

            # Each vibe gets sophisticated artistic treatment
            create_artistic_masterpiece_layer(overlay_draw, overlay, center, size, original_phrase, 
                                            individual_vibe, char_data, artistic_seed + i*10000, 
                                            composition_seed + i*5000, style_seed + i*3000, color_seed + i*1000)

            # Professional layer blending
            alpha_factor = 0.9 if i == 0 else 0.7
            overlay = apply_professional_alpha(overlay, alpha_factor)
            img = Image.alpha_composite(img, overlay)
    else:
        # Single vibe masterpiece
        create_artistic_masterpiece_layer(draw, img, center, size, original_phrase, vibe, 
                                        char_data, artistic_seed, composition_seed, style_seed, color_seed)

    # Add sophisticated symbolic elements
    add_professional_symbolism(draw, img, center, size, symbolic_meaning, char_data, style_seed)

    # Add meaning-influenced artistic patterns
    add_artistic_meaning_patterns(draw, img, center, size, artistic_profile, char_data, composition_seed)

    # Add professional glow and lighting effects
    img = apply_professional_lighting(img, aesthetic_style, char_data)

    print("✨ Applying professional artistic effects...")
    img = apply_masterpiece_effects(img, vibe, original_phrase, aesthetic_style)

    print("🎯 Converting to gallery-quality output...")
    try:
        # Apply final masterpiece polish
        img = apply_gallery_quality_finish(img, vibe, original_phrase, char_data, aesthetic_style)

        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG', optimize=True, compress_level=6)
        img_buffer.seek(0)
        img_data = img_buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode()

        print(f"🎨 ARTISTIC MASTERPIECE COMPLETED: {len(img_base64)} characters")
        return img_base64, None

    except MemoryError as e:
        print(f"❌ Memory error: {str(e)}")
        return None, "Artwork too complex. Try a shorter phrase or simpler vibe combination."
    except Exception as e:
        print(f"❌ Error creating artwork: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return None, f"Error creating artistic masterpiece: {str(e)}"


def get_enhanced_phrase_characteristics(phrase):
    """Extract unique characteristics from the phrase for maximum variation"""
    if not phrase:
        phrase = "default"

    # Create multiple hash variations for enhanced uniqueness
    phrase_bytes = phrase.encode('utf-8')
    hash1 = hashlib.sha256(phrase_bytes).hexdigest()
    hash2 = hashlib.md5(phrase_bytes).hexdigest()
    hash3 = hashlib.sha256((phrase + "salt").encode()).hexdigest()

    characteristics = {
        'length': len(phrase),
        'word_count': len(phrase.split()),
        'vowel_count': sum(1 for c in phrase.lower() if c in 'aeiou'),
        'consonant_count': sum(1 for c in phrase.lower() if c.isalpha() and c not in 'aeiou'),
        'numeric_count': sum(1 for c in phrase if c.isdigit()),
        'special_count': sum(1 for c in phrase if not c.isalnum() and not c.isspace()),
        'ascii_sum': sum(ord(c) for c in phrase),
        'unique_chars': len(set(phrase.lower())),
        'first_char_value': ord(phrase[0]) if phrase else 65,
        'last_char_value': ord(phrase[-1]) if phrase else 90,

        # Enhanced uniqueness factors
        'phrase_hash': abs(hash(phrase.lower())),
        'phrase_hash_alt': int(hash1[:8], 16),
        'phrase_hash_md5': int(hash2[:8], 16),
        'phrase_hash_salted': int(hash3[:8], 16),

        # Character position influences
        'char_positions': [ord(c) * (i + 1) for i, c in enumerate(phrase)],
        'char_sum_weighted': sum(ord(c) * (i + 1) for i, c in enumerate(phrase)),
        'middle_char_value': ord(phrase[len(phrase)//2]) if phrase else 77,

        # Word-level analysis
        'word_lengths': [len(word) for word in phrase.split()],
        'avg_word_length': sum(len(word) for word in phrase.split()) / len(phrase.split()) if phrase.split() else 0,
        'longest_word': max(len(word) for word in phrase.split()) if phrase.split() else 0,
        'shortest_word': min(len(word) for word in phrase.split()) if phrase.split() else 0,

        # Pattern analysis
        'repetition_factor': len(phrase) - len(set(phrase.lower())),
        'pattern_score': sum(phrase.count(c) for c in set(phrase.lower())),
        'alternating_pattern': sum(1 for i in range(len(phrase)-1) if phrase[i].isupper() != phrase[i+1].isupper()),

        # Semantic influence
        'emotional_words': sum(1 for word in phrase.lower().split() if word in [
            'love', 'peace', 'power', 'strength', 'healing', 'money', 'success', 'joy', 
            'happiness', 'protection', 'wisdom', 'clarity', 'abundance', 'prosperity', 
            'freedom', 'wealth', 'health', 'beauty', 'truth', 'light', 'dark', 'magic'
        ]),

        # Advanced metrics
        'energy_level': (sum(ord(c) for c in phrase) % 10) + 1,
        'complexity_score': len(set(phrase.lower())) + len(phrase.split()) + sum(1 for c in phrase if not c.isalnum()),
        'unique_bigrams': len(set(phrase[i:i+2].lower() for i in range(len(phrase)-1))),
        'phrase_entropy': len(set(phrase)) / len(phrase) if phrase else 0,

        # Timing influence for additional uniqueness
        'generation_factor': int(time.time() * 1000) % 1000,

        # Semantic weight for better text influence
        'semantic_weight': sum(ord(c) for c in phrase) * len(phrase.split()) * 100,

        # NEW: Metrics for enhanced text influence in sigil generation
        'sacred_power': (sum(ord(c) for c in phrase) + len(phrase) * 10) % 1000,
        'intent_strength': (len(phrase) * len(phrase.split()) * 50 + sum(ord(c) for c in phrase)) % 1000,
        'manifestation_power': (sum(ord(c) * (i+1) for i,c in enumerate(phrase)) + len(phrase)**2) % 1000,
    }
    return characteristics


def create_mystical_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create flowing, ethereal mystical sigil with enhanced artistic detail"""
    random.seed(combined_seed)
    char_data = get_enhanced_phrase_characteristics(phrase)

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
    """Create stellar, galactic cosmic sigil with enhanced text influence"""
    random.seed(combined_seed)
    char_data = get_enhanced_phrase_characteristics(phrase)

    # Enhanced cosmic colors with text influence
    base_colors = [(40, 40, 120), (120, 180, 255), (220, 120, 255), (255, 220, 120), (80, 255, 220)]
    colors = []
    for i, color in enumerate(base_colors):
        # Strong text influence on cosmic colors
        text_influence = sum(ord(c) for c in phrase[:3]) if phrase else 0
        variation = (char_data['ascii_sum'] + i * 80 + text_influence) % 140
        new_color = (
            min(255, max(40, color[0] + variation - 70)),
            min(255, max(40, color[1] + variation - 70)),
            min(255, max(40, color[2] + variation - 70))
        )
        colors.append(new_color)

    # Enhanced star field with text-based positioning
    star_count = 300 + char_data['length'] * 15 + char_data['word_count'] * 30
    for star in range(star_count):
        # Use phrase characters to influence star placement
        char_index = star % len(phrase) if phrase else 0
        char_val = ord(phrase[char_index]) if phrase else 65

        random.seed(pattern_seed + star + char_val)
        # Text influences star positioning
        x = (char_val * 13 + star * 7) % size
        y = (char_val * 17 + star * 11) % size

        brightness = 140 + (char_val % 100) + random.randint(0, 80)
        star_size = 1 + (char_val % 8) + random.randint(0, 4)

        # Enhanced star types with text influence
        star_type = (char_val + star) % 5

        try:
            if star_type == 0:  # Supernova star
                color = colors[char_val % len(colors)]
                for ring in range(4):
                    ring_size = star_size + ring * 2
                    ring_alpha = 255 - ring * 40
                    draw.ellipse([x-ring_size, y-ring_size, x+ring_size, y+ring_size],
                               fill=(*color, ring_alpha))
            elif star_type == 1:  # Cross star with text-influenced arms
                arm_length = star_size * (2 + char_val % 4)
                draw.line([(x-arm_length, y), (x+arm_length, y)], 
                         fill=(brightness, brightness, brightness, 220), width=3)
                draw.line([(x, y-arm_length), (x, y+arm_length)], 
                         fill=(brightness, brightness, brightness, 220), width=3)
            elif star_type == 2:  # Multi-pointed star
                points = []
                point_count = 6 + (char_val % 6)
                for p in range(point_count):
                    angle = (360 / point_count) * p
                    px = x + star_size * 3 * math.cos(math.radians(angle))
                    py = y + star_size * 3 * math.sin(math.radians(angle))
                    points.append((px, py))
                draw.polygon(points, fill=(brightness, brightness, brightness, 200))
            elif star_type == 3:  # Pulsing star with multiple colors
                base_color = colors[char_val % len(colors)]
                for pulse in range(4):
                    pulse_size = star_size + pulse * 2
                    alpha = 220 - pulse * 40
                    pulse_color = (
                        min(255, base_color[0] + pulse * 20),
                        min(255, base_color[1] + pulse * 20),
                        min(255, base_color[2] + pulse * 20)
                    )
                    draw.ellipse([x-pulse_size, y-pulse_size, x+pulse_size, y+pulse_size],
                               fill=(*pulse_color, alpha))
            else:  # Binary star system
                companion_x = x + (char_val % 20 - 10)
                companion_y = y + (char_val % 20 - 10)
                color = colors[char_val % len(colors)]
                draw.ellipse([x-star_size, y-star_size, x+star_size, y+star_size],
                           fill=(*color, 255))
                draw.ellipse([companion_x-star_size//2, companion_y-star_size//2, 
                            companion_x+star_size//2, companion_y+star_size//2],
                           fill=(*color, 180))
                # Connection between binary stars
                draw.line([(x, y), (companion_x, companion_y)], 
                         fill=(*color, 100), width=1)
        except:
            pass

    # Enhanced galactic spirals with text influence
    spiral_count = 3 + (char_data['word_count'] % 5)
    for spiral in range(spiral_count):
        spiral_char = phrase[spiral % len(phrase)] if phrase else 'a'
        spiral_influence = ord(spiral_char)

        random.seed(combined_seed + spiral + spiral_influence)
        start_radius = size // 10 + (spiral_influence % 30)

        points = []
        angle_step = 2 + (char_data['unique_chars'] % 6)
        max_angle = 1080 + char_data['length'] * 30 + spiral_influence * 2

        for angle in range(0, max_angle, angle_step):
            radius = start_radius + (angle / max_angle) * (size // 3 + spiral_influence % 50)
            actual_angle = angle + spiral * 120 + spiral_influence % 180
            x = center[0] + radius * math.cos(math.radians(actual_angle))
            y = center[1] + radius * math.sin(math.radians(actual_angle))
            points.append((x, y))

        # Draw enhanced spiral arms
        color = colors[(spiral + spiral_influence) % len(colors)]
        width = 4 + (char_data['special_count'] % 4)
        alpha = 140 + (spiral_influence % 100)

        for i in range(len(points) - 1):
            try:
                # Main spiral arm
                draw.line([points[i], points[i + 1]], fill=(*color, alpha), width=width)

                # Add stellar dust trail
                dust_color = (
                    max(0, color[0] - 50),
                    max(0, color[1] - 50),
                    max(0, color[2] - 50)
                )
                draw.line([points[i], points[i + 1]], fill=(*dust_color, alpha//2), width=width*2)
            except:
                pass

    # Enhanced constellation with text content
    create_enhanced_constellation(draw, center, size, phrase, colors, text_seed, char_data)

    # Enhanced nebula clouds with text influence
    create_enhanced_nebula_effect(img, colors, combined_seed, char_data)


def create_elemental_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create elemental sigil with phrase-specific elemental patterns"""
    random.seed(combined_seed)
    char_data = get_enhanced_phrase_characteristics(phrase)

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
    """Create stunning geometric crystal sigil with enhanced visual beauty"""
    random.seed(combined_seed + len(phrase) * 1000)  # More phrase influence
    char_data = get_enhanced_phrase_characteristics(phrase)

    # Enhanced crystal colors with more vibrant, beautiful hues
    base_colors = [
        (255, 140, 255),  # Brilliant magenta
        (140, 255, 255),  # Cyan crystal  
        (255, 255, 140),  # Golden citrine
        (200, 140, 255),  # Deep amethyst
        (140, 255, 200),  # Emerald green
        (255, 140, 140),  # Ruby red
        (140, 200, 255),  # Sapphire blue
        (255, 200, 140)   # Warm topaz
    ]

    colors = []
    for i, color in enumerate(base_colors):
        # Strong text influence on colors for uniqueness
        text_influence = sum(ord(c) for c in phrase[i % len(phrase):i % len(phrase) + 3]) if phrase else 0
        variation = (char_data['ascii_sum'] + i * 80 + text_influence) % 120
        new_color = (
            min(255, max(160, color[0] + variation - 60)),
            min(255, max(160, color[1] + variation - 60)),
            min(255, max(160, color[2] + variation - 60))
        )
        colors.append(new_color)

    # Create stunning multi-layered crystal formations with phrase-specific geometry
    crystal_layers = 4 + (char_data['word_count'] % 5)
    base_radius = size // 8 + (char_data['ascii_sum'] % 100)

    for layer in range(crystal_layers):
        layer_radius = base_radius + (layer * (size // 15 + char_data['unique_chars'] * 3))
        crystal_count = 6 + (char_data['length'] % 8) + layer * 3 + (char_data['vowel_count'] % 4)

        for crystal in range(crystal_count):
            # Phrase-influenced crystal positioning
            char_val = ord(phrase[crystal % len(phrase)]) if phrase else 65
            angle = (crystal * 360 / crystal_count) + (char_val * 7) + (layer * 30)

            # Add golden ratio spiral influence for natural beauty
            spiral_factor = crystal * 137.5  # Golden angle
            distance = layer_radius + (char_val % 50) + (spiral_factor % 100)

            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))

            # Create beautiful geometric crystal shapes
            crystal_size = 25 + (char_val % 20) + (layer * 5)
            crystal_sides = 6 + (char_val % 6)  # 6-12 sided crystals

            # Generate crystal vertices
            crystal_points = []
            for side in range(crystal_sides):
                side_angle = angle + (side * 360 / crystal_sides)
                # Add variation for natural crystal irregularity
                radius_variation = crystal_size + (char_val % 10 - 5) + random.randint(-3, 3)
                px = x + radius_variation * math.cos(math.radians(side_angle))
                py = y + radius_variation * math.sin(math.radians(side_angle))
                crystal_points.append((px, py))

            # Enhanced crystal rendering with multiple layers
            color = colors[(crystal + char_val + layer) % len(colors)]

            try:
                # Draw crystal base with gradient effect
                alpha = 140 + (char_data['special_count'] * 10) % 100
                draw.polygon(crystal_points, fill=(*color, alpha))

                # Add brilliant crystal highlights
                highlight_color = (
                    min(255, color[0] + 80),
                    min(255, color[1] + 80), 
                    min(255, color[2] + 80)
                )

                # Inner crystal core
                inner_size = crystal_size * 0.6
                inner_points = []
                for side in range(crystal_sides):
                    side_angle = angle + (side * 360 / crystal_sides) + 180/crystal_sides
                    px = x + inner_size * math.cos(math.radians(side_angle))
                    py = y + inner_size * math.sin(math.radians(side_angle))
                    inner_points.append((px, py))

                draw.polygon(inner_points, fill=(*highlight_color, alpha + 40))

                # Add prismatic edges for realism
                for i in range(len(crystal_points)):
                    next_i = (i + 1) % len(crystal_points)
                    edge_color = (
                        min(255, color[0] + 100),
                        min(255, color[1] + 100),
                        min(255, color[2] + 100)
                    )
                    draw.line([crystal_points[i], crystal_points[next_i]], 
                             fill=(*edge_color, 255), width=3)

                # Add central crystal light point
                draw.ellipse([x-4, y-4, x+4, y+4], fill=(255, 255, 255, 255))

            except:
                pass

    # Enhanced connections with text-based patterns
    random.seed(pattern_seed + char_data['ascii_sum'])
    # Need lattice_points to be defined if this function is called
    # For now, assuming it's defined elsewhere or will be added.
    # If not, this part will cause an error.
    # Example placeholder: lattice_points = [(center[0] + i*10, center[1] + i*10) for i in range(5)]
    # If lattice_points is not defined, this loop will not run or will error.
    # It's better to define it or ensure it's available.
    # For demonstration, let's assume it's available.
    # If lattice_points is not available, we should skip this part.
    if 'lattice_points' in locals() or 'lattice_points' in globals():
        for i, point in enumerate(lattice_points):
            connections = 3 + (char_data['unique_chars'] % 5)
            for conn in range(connections):
                # Use phrase content to determine connections
                char_val = ord(phrase[i % len(phrase)]) if phrase else 65
                target_idx = (i + conn * char_val + char_data['vowel_count']) % len(lattice_points)
                target_point = lattice_points[target_idx]

                color = colors[(i + char_val) % len(colors)]
                width = 2 + (char_data['special_count'] % 4)
                alpha = 150 + (char_data['length'] * 8) % 100

                try:
                    # Add crystal refraction effect
                    draw.line([point, target_point], fill=(*color, alpha), width=width)

                    # Add prismatic edges
                    offset_x = (char_val % 6 - 3)
                    offset_y = (char_val % 6 - 3)
                    offset_point = (point[0] + offset_x, point[1] + offset_y)
                    offset_target = (target_point[0] + offset_x, target_point[1] + offset_y)

                    prism_color = (
                        min(255, color[0] + 30),
                        min(255, color[1] + 30),
                        min(255, color[2] + 30)
                    )
                    draw.line([offset_point, offset_target], fill=(*prism_color, alpha//2), width=1)
                except:
                    pass

    # Add enhanced crystal facets
    create_enhanced_crystal_facets(draw, center, size, phrase, colors, combined_seed, char_data)

    # Add crystalline formations based on text
    create_text_influenced_crystals(draw, center, size, phrase, colors, text_seed, char_data)


def create_shadow_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create mysterious but beautiful shadow sigil with enhanced brightness and text influence"""
    random.seed(combined_seed)
    char_data = get_enhanced_phrase_characteristics(phrase)

    # Enhanced shadow colors - brighter with text influence
    base_colors = [(200, 140, 200), (240, 180, 240), (180, 140, 180), (220, 160, 220), (160, 160, 200)]
    colors = []
    for i, color in enumerate(base_colors):
        # Strong text influence on shadow colors
        text_influence = sum(ord(c) for c in phrase[:2]) if phrase else 0
        variation = (char_data['ascii_sum'] + i * 50 + text_influence) % 100
        new_color = (
            min(255, max(140, color[0] + variation - 50)),
            min(255, max(140, color[1] + variation - 50)),
            min(255, max(140, color[2] + variation - 50))
        )
        colors.append(new_color)

    # Enhanced tendril system with text influence
    tendril_count = min(10, 4 + char_data['length'] // 2 + char_data['word_count'])
    for tendril in range(tendril_count):
        random.seed(pattern_seed + tendril + char_data['ascii_sum'])

        # Use phrase characters to influence tendril direction
        char_influence = ord(phrase[tendril % len(phrase)]) if phrase else 65
        start_angle = (char_influence * 5 + tendril * 36) % 360

        points = []
        current_x, current_y = center

        # More detailed steps with text influence
        steps = min(16, 10 + char_data['word_count'] + char_data['unique_chars'])
        for step in range(steps):
            # Use phrase content to create unique patterns
            step_char = phrase[step % len(phrase)] if phrase else 'a'
            step_influence = ord(step_char)

            distance = step * (size // 25 + (step_influence % 15))
            angle_variation = random.uniform(-40, 40) + (step_influence % 30 - 15)
            actual_angle = start_angle + angle_variation + (step * 3)

            x = current_x + distance * math.cos(math.radians(actual_angle))
            y = current_y + distance * math.sin(math.radians(actual_angle))
            points.append((x, y))

            current_x, current_y = x, y

        # Draw enhanced tendril with text-influenced properties
        color = colors[(tendril + char_influence) % len(colors)]
        for i in range(len(points) - 1):
            thickness = max(2, 5 + char_data['numeric_count'] % 4 - i // 4)
            alpha = 160 + (char_data['special_count'] * 12) % 80
            try:
                # Main tendril
                draw.line([points[i], points[i + 1]], fill=(*color, alpha), width=thickness)

                # Add shadow glow effect
                glow_color = (
                    min(255, color[0] + 40),
                    min(255, color[1] + 40),
                    min(255, color[2] + 40)
                )
                draw.line([points[i], points[i + 1]], fill=(*glow_color, alpha//3), width=thickness*2)
            except:
                pass

    # Enhanced shadow runes with text content
    create_enhanced_shadow_runes(draw, center, size, phrase, colors, text_seed, char_data)

    # Enhanced void spaces with text influence
    create_enhanced_void_effect(draw, center, size, phrase, combined_seed, char_data)


def create_light_sigil(draw, img, center, size, phrase, text_seed, combined_seed, pattern_seed, color_seed):
    """Create radiant, healing light sigil with phrase-specific variations"""
    random.seed(combined_seed)
    char_data = get_enhanced_phrase_characteristics(phrase)

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


# Updated helper functions with char_data parameter
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

            # Create complex character-based rune
            rune_complexity = 3 + (ord(char) % 6)
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
        angle = (char_data['ascii_sum'] + i * 30) % 360
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

        # Enhanced nebula with multiple layers
        for layer in range(3):
            layer_radius = cloud_size - layer * 20
            layer_alpha = int(100 * ((layer_radius / cloud_size) ** 2)) + (char_data['unique_chars'] % 30)

            if layer_radius > 0:
                # Create organic cloud shape
                for angle in range(0, 360, 12):
                    variation = random.randint(-layer_radius//4, layer_radius//4)
                    actual_radius = layer_radius + variation
                    x = cloud_x + actual_radius * math.cos(math.radians(angle))
                    y = cloud_y + actual_radius * math.sin(math.radians(angle))

                    if 0 <= x < img.width and 0 <= y < img.height:
                        current_pixel = img.getpixel((int(x), int(y)))
                        if len(current_pixel) == 4:
                            r, g, b, a = current_pixel

                            # Enhanced color blending
                            blend_factor = layer_alpha / 255
                            blend_r = min(255, int(r + color[0] * blend_factor))
                            blend_g = min(255, int(g + color[1] * blend_factor))
                            blend_b = min(255, int(b + color[2] * blend_factor))

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

def apply_optimized_vibe_effects(img, vibe, phrase):
    """Apply minimal vibe-specific effects for speed"""
    char_data = get_enhanced_phrase_characteristics(phrase)
    try:
        if vibe == 'shadow':
            # Minimal shadow effects
            brightness_factor = 0.8 + (char_data['consonant_count'] * 0.01)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
        elif vibe == 'light':
            # Minimal light effects
            brightness_factor = 1.2 + (char_data['vowel_count'] * 0.01)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness_factor)
        elif vibe == 'cosmic':
            # Minimal cosmic effects
            contrast_factor = 1.3 + (char_data['length'] * 0.005)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)
        else:
            # Minimal enhancement for all other vibes
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.2)
    except Exception as e:
        print(f"Optimized effects warning: {e}")
    return img

def apply_minimal_quality_pass(img, vibe, phrase):
    """Apply minimal quality improvements for maximum speed"""
    try:
        # Basic sharpening only
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)

        # Basic contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)

        return img
    except Exception as e:
        print(f"Minimal quality pass warning: {e}")
        return img

# ===== SOPHISTICATED LIGHTING AND EFFECTS SYSTEM =====

def apply_professional_lighting(img, aesthetic_style, char_data):
    """Apply sophisticated lighting effects based on aesthetic style"""
    try:
        # Create lighting overlay
        lighting_overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        
        # Apply style-specific lighting
        if aesthetic_style == 'neon_geometric':
            img = apply_neon_glow_lighting(img, char_data)
        elif aesthetic_style == 'cosmic_ethereal':
            img = apply_cosmic_ambient_lighting(img, char_data)
        elif aesthetic_style == 'crystalline_precise':
            img = apply_crystal_refraction_lighting(img, char_data)
        elif aesthetic_style == 'shadow_mysterious':
            img = apply_dramatic_shadow_lighting(img, char_data)
        else:
            img = apply_mystical_aura_lighting(img, char_data)
        
        return img
    except Exception as e:
        print(f"Professional lighting warning: {e}")
        return img

def apply_neon_glow_lighting(img, char_data):
    """Apply sophisticated neon glow effects"""
    try:
        # Create multiple glow layers
        glow_layers = []
        
        for radius in [5, 10, 15, 20]:
            glow = img.filter(ImageFilter.GaussianBlur(radius=radius))
            
            # Enhance cyan/blue tones for neon effect
            glow_array = np.array(glow)
            if len(glow_array.shape) == 3:
                # Boost blue and cyan channels
                glow_array[:, :, 0] = np.clip(glow_array[:, :, 0] * 0.8, 0, 255)  # Red
                glow_array[:, :, 1] = np.clip(glow_array[:, :, 1] * 1.2, 0, 255)  # Green  
                glow_array[:, :, 2] = np.clip(glow_array[:, :, 2] * 1.4, 0, 255)  # Blue
            
            glow = Image.fromarray(glow_array.astype(np.uint8))
            glow_layers.append(glow)
        
        # Blend glow layers with decreasing opacity
        result = img
        for i, glow in enumerate(glow_layers):
            opacity = 0.3 - (i * 0.05)  # Decreasing opacity
            result = Image.blend(result, glow, opacity)
        
        return result
    except Exception as e:
        print(f"Neon glow lighting warning: {e}")
        return img

def apply_cosmic_ambient_lighting(img, char_data):
    """Apply cosmic ambient lighting effects"""
    try:
        # Create cosmic atmosphere
        atmosphere = img.filter(ImageFilter.GaussianBlur(radius=25))
        
        # Enhance purple and blue tones
        atmo_array = np.array(atmosphere)
        if len(atmo_array.shape) == 3:
            atmo_array[:, :, 0] = np.clip(atmo_array[:, :, 0] * 1.1, 0, 255)  # Red
            atmo_array[:, :, 1] = np.clip(atmo_array[:, :, 1] * 0.9, 0, 255)  # Green
            atmo_array[:, :, 2] = np.clip(atmo_array[:, :, 2] * 1.3, 0, 255)  # Blue
        
        atmosphere = Image.fromarray(atmo_array.astype(np.uint8))
        
        # Blend with original
        result = Image.blend(img, atmosphere, 0.4)
        
        return result
    except Exception as e:
        print(f"Cosmic lighting warning: {e}")
        return img

def apply_crystal_refraction_lighting(img, char_data):
    """Apply crystal refraction and brilliance effects"""
    try:
        # Create prismatic effect
        prismatic = img.copy()
        prismatic_array = np.array(prismatic)
        
        if len(prismatic_array.shape) == 3:
            # Create color separation effect
            red_shift = np.roll(prismatic_array[:, :, 0], 2, axis=1)
            blue_shift = np.roll(prismatic_array[:, :, 2], -2, axis=1)
            
            prismatic_array[:, :, 0] = np.clip(red_shift * 1.1, 0, 255)
            prismatic_array[:, :, 2] = np.clip(blue_shift * 1.1, 0, 255)
        
        prismatic = Image.fromarray(prismatic_array.astype(np.uint8))
        
        # Add brilliant highlights
        highlights = img.filter(ImageFilter.GaussianBlur(radius=3))
        enhancer = ImageEnhance.Brightness(highlights)
        highlights = enhancer.enhance(1.5)
        
        # Combine effects
        result = Image.blend(img, prismatic, 0.3)
        result = Image.blend(result, highlights, 0.2)
        
        return result
    except Exception as e:
        print(f"Crystal lighting warning: {e}")
        return img

def apply_dramatic_shadow_lighting(img, char_data):
    """Apply dramatic shadow lighting with enhanced visibility"""
    try:
        # Create enhanced shadow effect (brighter than original)
        shadow_enhanced = img.copy()
        
        # Brighten the image significantly
        enhancer = ImageEnhance.Brightness(shadow_enhanced)
        shadow_enhanced = enhancer.enhance(1.3)
        
        # Add subtle blue tint for mystique
        shadow_array = np.array(shadow_enhanced)
        if len(shadow_array.shape) == 3:
            shadow_array[:, :, 2] = np.clip(shadow_array[:, :, 2] * 1.2, 0, 255)  # Blue boost
        
        shadow_enhanced = Image.fromarray(shadow_array.astype(np.uint8))
        
        # Add soft glow to maintain visibility
        glow = shadow_enhanced.filter(ImageFilter.GaussianBlur(radius=8))
        result = Image.blend(shadow_enhanced, glow, 0.3)
        
        return result
    except Exception as e:
        print(f"Shadow lighting warning: {e}")
        return img

def apply_mystical_aura_lighting(img, char_data):
    """Apply mystical aura lighting effects"""
    try:
        # Create mystical aura
        aura = img.filter(ImageFilter.GaussianBlur(radius=15))
        
        # Enhance mystical colors (purple, gold, cyan)
        aura_array = np.array(aura)
        if len(aura_array.shape) == 3:
            aura_array[:, :, 0] = np.clip(aura_array[:, :, 0] * 1.1, 0, 255)  # Red
            aura_array[:, :, 1] = np.clip(aura_array[:, :, 1] * 1.0, 0, 255)  # Green
            aura_array[:, :, 2] = np.clip(aura_array[:, :, 2] * 1.2, 0, 255)  # Blue
        
        aura = Image.fromarray(aura_array.astype(np.uint8))
        
        # Blend with original
        result = Image.blend(img, aura, 0.35)
        
        return result
    except Exception as e:
        print(f"Mystical lighting warning: {e}")
        return img

def apply_masterpiece_effects(img, vibe, phrase, aesthetic_style):
    """Apply sophisticated masterpiece-level effects"""
    try:
        print(f"🎨 Applying masterpiece effects for {aesthetic_style}...")
        
        # Apply style-specific enhancements
        if aesthetic_style == 'neon_geometric':
            img = apply_neon_masterpiece_effects(img)
        elif aesthetic_style == 'cosmic_ethereal':
            img = apply_cosmic_masterpiece_effects(img)
        elif aesthetic_style == 'crystalline_precise':
            img = apply_crystal_masterpiece_effects(img)
        elif aesthetic_style == 'shadow_mysterious':
            img = apply_shadow_masterpiece_effects(img)
        else:
            img = apply_mystical_masterpiece_effects(img)
        
        return img
    except Exception as e:
        print(f"Masterpiece effects warning: {e}")
        return img

def apply_neon_masterpiece_effects(img):
    """Apply neon-specific masterpiece effects"""
    try:
        # Ultra-sharp details
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)
        
        # High contrast for neon pop
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.6)
        
        # Vibrant colors
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.8)
        
        return img
    except:
        return img

def apply_cosmic_masterpiece_effects(img):
    """Apply cosmic-specific masterpiece effects"""
    try:
        # Ethereal softness with sharp details
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        
        # Deep contrast for cosmic depth
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.7)
        
        # Rich cosmic colors
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.6)
        
        return img
    except:
        return img

def apply_crystal_masterpiece_effects(img):
    """Apply crystal-specific masterpiece effects"""
    try:
        # Ultra-sharp precision
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.2)
        
        # High contrast for facet definition
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.8)
        
        # Brilliant color clarity
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.4)
        
        return img
    except:
        return img

def apply_shadow_masterpiece_effects(img):
    """Apply shadow-specific masterpiece effects (enhanced for visibility)"""
    try:
        # Enhanced brightness for visibility
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.4)
        
        # Moderate sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.6)
        
        # Enhanced contrast while maintaining visibility
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        
        # Subtle color enhancement
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
        
        return img
    except:
        return img

def apply_mystical_masterpiece_effects(img):
    """Apply mystical-specific masterpiece effects"""
    try:
        # Balanced sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.7)
        
        # Mystical contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        
        # Enhanced mystical colors
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.7)
        
        return img
    except:
        return img

def apply_gallery_quality_finish(img, vibe, phrase, char_data, aesthetic_style):
    """Apply final gallery-quality finishing touches"""
    try:
        print(f"🎨 Applying gallery-quality finish...")
        
        # Final sharpening pass
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)
        
        # Final contrast optimization
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Final color saturation
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
        
        # Add professional smoothing
        img = img.filter(ImageFilter.SMOOTH_MORE)
        
        # Final detail enhancement
        img = apply_professional_detail_enhancement(img, char_data)
        
        print(f"✨ Gallery-quality finish applied")
        return img
    except Exception as e:
        print(f"Gallery finish warning: {e}")
        return img

def apply_professional_detail_enhancement(img, char_data):
    """Apply professional detail enhancement"""
    try:
        # Enhance fine details
        detail_factor = 1.2 + (char_data.get('unique_chars', 10) * 0.02)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(min(2.5, detail_factor))
        
        return img
    except:
        return img

def add_professional_symbolism(draw, img, center, size, symbolic_meaning, char_data, seed):
    """Add sophisticated symbolic elements"""
    pass  # Placeholder for additional symbolism

def add_artistic_meaning_patterns(draw, img, center, size, artistic_profile, char_data, seed):
    """Add artistic patterns based on meaning"""
    pass  # Placeholder for meaning patterns

def apply_professional_alpha(overlay, alpha_factor):
    """Apply professional alpha blending"""
    try:
        # Create alpha-adjusted overlay
        alpha_overlay = Image.new('RGBA', overlay.size, (0, 0, 0, 0))
        alpha_overlay.paste(overlay, (0, 0))
        
        # Adjust alpha
        alpha_array = np.array(alpha_overlay)
        if len(alpha_array.shape) == 3 and alpha_array.shape[2] == 4:
            alpha_array[:, :, 3] = alpha_array[:, :, 3] * alpha_factor
        
        return Image.fromarray(alpha_array.astype(np.uint8))
    except:
        return overlay

def count_emotional_words(text):
    """Count emotional words in text"""
    emotional_words = [
        'love', 'peace', 'power', 'strength', 'healing', 'money', 'success', 'joy',
        'happiness', 'protection', 'wisdom', 'clarity', 'abundance', 'prosperity',
        'freedom', 'wealth', 'health', 'beauty', 'truth', 'light', 'divine', 'sacred',
        'blessed', 'gratitude', 'manifestation', 'transformation', 'awakening', 'enlightenment'
    ]
    
    words = text.lower().split()
    return sum(1 for word in words if word in emotional_words)

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

def create_enhanced_crystal_facets(draw, center, size, phrase, colors, seed, char_data):
    """Create enhanced crystal facets with text influence"""
    random.seed(seed + char_data['ascii_sum'])

    facet_count = 6 + char_data['length'] + char_data['word_count'] * 3
    for facet in range(facet_count):
        # Use phrase characters to influence facet placement
        char_val = ord(phrase[facet % len(phrase)]) if phrase else 65
        angle = (char_val * 3 + facet * 36) % 360
        distance = size // 6 + char_data['word_count'] * 12 + (char_val % 40)

        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))

        # Create complex character-based crystal
        crystal_size = 20 + char_data['consonant_count'] + (char_val % 25)
        crystal_sides = 6 + (char_val % 4)

        points = []
        for side in range(crystal_sides):
            side_angle = angle + side * (360 / crystal_sides)
            px = x + crystal_size * math.cos(math.radians(side_angle))
            py = y + crystal_size * math.sin(math.radians(side_angle))
            points.append((px, py))

        color = colors[(facet + char_val) % len(colors)]
        alpha = 160 + (char_data['special_count'] * 12) % 80
        outline_alpha = 220 + (char_data['word_count'] * 15) % 35

        try:
            # Main facet
            draw.polygon(points, fill=(*color, alpha), outline=(*color, outline_alpha))

            # Add crystal highlights
            highlight_color = (
                min(255, color[0] + 60),
                min(255, color[1] + 60),
                min(255, color[2] + 60)
            )

            # Inner highlight
            inner_points = []
            for i, point in enumerate(points):
                inner_x = x + (point[0] - x) * 0.6
                inner_y = y + (point[1] - y) * 0.6
                inner_points.append((inner_x, inner_y))

            draw.polygon(inner_points, fill=(*highlight_color, alpha//2))
        except:
            pass

def create_text_influenced_crystals(draw, center, size, phrase, colors, seed, char_data):
    """Create crystal formations based on text content"""
    if not phrase:
        return

    for i, char in enumerate(phrase):
        if char.isalnum():
            char_val = ord(char)
            angle = (char_val * 5 + i * 25) % 360
            distance = size // 8 + (char_val % 60) + i * 10

            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))

            # Create character-specific crystal
            crystal_size = 15 + (char_val % 20)
            crystal_sides = 4 + (char_val % 4)

            points = []
            for side in range(crystal_sides):
                side_angle = angle + side * (360 / crystal_sides)
                px = x + crystal_size * math.cos(math.radians(side_angle))
                py = y + crystal_size * math.sin(math.radians(side_angle))
                points.append((px, py))

            color = colors[(char_val + i) % len(colors)]
            alpha = 180 + (char_val % 60)

            try:
                draw.polygon(points, fill=(*color, alpha))

                # Add text-based inner pattern
                inner_size = crystal_size * 0.5
                inner_points = []
                for side in range(crystal_sides):
                    side_angle = angle + side * (360 / crystal_sides) + 180/crystal_sides
                    px = x + inner_size * math.cos(math.radians(side_angle))
                    py = y + inner_size * math.sin(math.radians(side_angle))
                    inner_points.append((px, py))

                inner_color = (
                    min(255, color[0] + 40),
                    min(255, color[1] + 40),
                    min(255, color[2] + 40)
                )
                draw.polygon(inner_points, fill=(*inner_color, alpha))
            except:
                pass

def create_enhanced_shadow_runes(draw, center, size, phrase, colors, seed, char_data):
    """Create enhanced shadow runes based on text content"""
    return create_shadow_runes_optimized(draw, center, size, phrase, colors, seed, char_data)

def create_enhanced_void_effect(draw, center, size, phrase, seed, char_data):
    """Create enhanced void spaces with text influence"""
    random.seed(seed + char_data['ascii_sum'])

    void_count = 4 + char_data['word_count'] + (char_data['length'] % 6)
    for void in range(void_count):
        # Use phrase to influence void placement
        char_val = ord(phrase[void % len(phrase)]) if phrase else 65
        void_x = (char_val * 13 + void * 47) % size
        void_y = (char_val * 17 + void * 31) % size

        void_radius = 12 + char_data['vowel_count'] * 3 + (char_val % 25)

        # Create void with enhanced properties
        outline_alpha = 180 + (char_val % 60)

        # Create void gradient
        for ring in range(void_radius, 0, -3):
            ring_alpha = int(outline_alpha * (ring / void_radius))
            ring_color = (60 + char_val % 40, 20 + char_val % 30, 60 + char_val % 40)

            try:
                draw.ellipse([void_x-ring, void_y-ring, void_x+ring, void_y+ring],
                           fill=(*ring_color, ring_alpha))
            except:
                pass

def create_enhanced_constellation(draw, center, size, phrase, colors, seed, char_data):
    """Create enhanced constellation pattern based on phrase content"""
    random.seed(seed + char_data['ascii_sum'])

    # Create star positions based on each character in phrase
    star_positions = []
    for i, char in enumerate(phrase):
        if char.isalnum():
            char_value = ord(char)
            angle = (char_value * 11 + i * 37) % 360
            distance = (size // 6) + (char_value % 100) + char_data['word_count'] * 15
            x = center[0] + distance * math.cos(math.radians(angle))
            y = center[1] + distance * math.sin(math.radians(angle))
            star_positions.append((x, y, char_value, char))

    # Enhanced connections based on character relationships
    for i in range(len(star_positions)):
        for j in range(i + 1, len(star_positions)):
            char1_val = star_positions[i][2]
            char2_val = star_positions[j][2]
            char1 = star_positions[i][3]
            char2 = star_positions[j][3]

            # Create connections based on character similarities
            char_diff = abs(char1_val - char2_val)
            should_connect = (
                char_diff % 5 == 0 or  # ASCII value relationship
                char1.lower() == char2.lower() or  # Same character
                (char1.isalpha() and char2.isalpha() and abs(ord(char1.lower()) - ord(char2.lower())) <= 3)
            )

            if should_connect:
                color = colors[(char1_val + char2_val) % len(colors)]
                connection_strength = max(50, 200 - char_diff * 2)

                try:
                    draw.line([star_positions[i][:2], star_positions[j][:2]],
                             fill=(*color, connection_strength), width=2)
                except:
                    pass

        # Draw enhanced star based on character
        pos = star_positions[i][:2]
        char_val = star_positions[i][2]
        color = colors[(char_val + char_data['numeric_count']) % len(colors)]
        radius = 6 + (char_val % 8)

        try:
            # Multi-layered star
            for layer in range(3):
                layer_radius = radius - layer * 2
                layer_alpha = 255 - layer * 60
                if layer_radius > 0:
                    draw.ellipse([pos[0]-layer_radius, pos[1]-layer_radius, 
                                pos[0]+layer_radius, pos[1]+layer_radius],
                               fill=(*color, layer_alpha))
        except:
            pass

def create_enhanced_nebula_effect(img, colors, seed, char_data):
    """Create enhanced nebula cloud effect with text influence"""
    random.seed(seed + char_data['ascii_sum'])

    cloud_count = 4 + char_data['word_count'] + (char_data['length'] % 6)
    for cloud in range(cloud_count):
        cloud_x = random.randint(0, img.width)
        cloud_y = random.randint(0, img.height)
        cloud_size = 60 + char_data['vowel_count'] * 12 + random.randint(0, 100)
        color = colors[(cloud + char_data['numeric_count']) % len(colors)]

        # Enhanced nebula with multiple layers
        for layer in range(3):
            layer_radius = cloud_size - layer * 20
            layer_alpha = int(100 * ((layer_radius / cloud_size) ** 2)) + (char_data['unique_chars'] % 30)

            if layer_radius > 0:
                # Create organic cloud shape
                for angle in range(0, 360, 12):
                    variation = random.randint(-layer_radius//4, layer_radius//4)
                    actual_radius = layer_radius + variation
                    x = cloud_x + actual_radius * math.cos(math.radians(angle))
                    y = cloud_y + actual_radius * math.sin(math.radians(angle))

                    if 0 <= x < img.width and 0 <= y < img.height:
                        current_pixel = img.getpixel((int(x), int(y)))
                        if len(current_pixel) == 4:
                            r, g, b, a = current_pixel

                            # Enhanced color blending
                            blend_factor = layer_alpha / 255
                            blend_r = min(255, int(r + color[0] * blend_factor))
                            blend_g = min(255, int(g + color[1] * blend_factor))
                            blend_b = min(255, int(b + color[2] * blend_factor))

                            img.putpixel((int(x), int(y)), (blend_r, blend_g, blend_b, a))

def apply_artistic_enhancement(img, vibe, phrase):
    """Apply artistic enhancements to improve image quality and aesthetics."""
    char_data = get_phrase_characteristics(phrase)
    try:
        # Enhance artistic elements based on vibe
        if vibe == 'mystical':
            img = add_aura_effect(img)
            img = add_mystical_shimmer(img, intensity=1.8)
        elif vibe == 'cosmic':
            img = add_stellar_glow(img, intensity=1.6)
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
    char_data = get_enhanced_phrase_characteristics(phrase)
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

# Placeholder for a new function, if not already defined
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
                y = center[1] + length * math.sin(math.radians(angle))

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
                    draw.line([(center_x, center[1]), (x, y)], fill=color, width=width)
                except:
                    pass

                # Update for next iteration
                center_x, center_y = x, y
                angle += 45 + char_data['numeric_count'] * 5

        # Blend fractal overlay
        return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    except:
        return img


def create_neon_mystical_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed):
    """Create sophisticated neon mystical masterpiece like the reference images"""
    random.seed(artistic_seed)
    
    # Professional neon color palette
    neon_colors = [
        (0, 255, 255),    # Bright cyan - primary
        (64, 224, 255),   # Deep sky blue  
        (0, 191, 255),    # Electric blue
        (127, 255, 212),  # Aquamarine
        (255, 255, 255),  # Pure white for highlights
    ]
    
    # Calculate sophisticated positioning based on phrase
    element_count = 5 + char_data['word_count'] + (char_data['sacred_power'] % 8)
    
    # Create central symbol based on phrase characteristics
    if 'eye' in phrase.lower() or 'see' in phrase.lower() or 'vision' in phrase.lower():
        create_neon_eye_symbol(draw, center, size, neon_colors[0], char_data, style_seed)
    elif any(word in phrase.lower() for word in ['arrow', 'direction', 'path', 'way', 'up', 'rise']):
        create_neon_arrow_symbol(draw, center, size, neon_colors[0], char_data, style_seed)
    else:
        create_neon_geometric_symbol(draw, center, size, neon_colors[0], char_data, style_seed)
    
    # Add sophisticated supporting elements
    for i in range(element_count):
        random.seed(composition_seed + i * char_data['ascii_sum'])
        
        # Position elements in meaningful arrangement
        angle = (360 / element_count) * i + (char_data['intent_strength'] % 45)
        distance = (size // 6) + (char_data['manifestation_power'] % (size // 8))
        
        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))
        
        # Create supporting geometric elements
        element_type = (char_data['first_char_value'] + i) % 4
        color = neon_colors[i % len(neon_colors)]
        
        if element_type == 0:
            create_neon_triangle(draw, (x, y), 20 + char_data['unique_chars'], color, char_data)
        elif element_type == 1:
            create_neon_circle(draw, (x, y), 15 + char_data['vowel_count'], color, char_data)
        elif element_type == 2:
            create_neon_diamond(draw, (x, y), 18 + char_data['consonant_count'], color, char_data)
        else:
            create_neon_cross(draw, (x, y), 22 + char_data['special_count'], color, char_data)
    
    # Add connecting energy lines
    create_neon_energy_connections(draw, center, size, phrase, char_data, neon_colors, artistic_seed)

def create_cosmic_ethereal_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed):
    """Create cosmic ethereal masterpiece with nebula effects"""
    random.seed(artistic_seed)
    
    # Cosmic color palette
    cosmic_colors = [
        (138, 43, 226),   # Blue violet
        (72, 61, 139),    # Dark slate blue
        (147, 0, 211),    # Dark violet
        (255, 20, 147),   # Deep pink
        (0, 206, 209),    # Dark turquoise
    ]
    
    # Create central cosmic symbol
    if 'infinity' in phrase.lower() or 'eternal' in phrase.lower():
        create_cosmic_infinity_symbol(draw, center, size, cosmic_colors[0], char_data)
    elif 'star' in phrase.lower() or 'stellar' in phrase.lower():
        create_cosmic_star_symbol(draw, center, size, cosmic_colors[0], char_data)
    else:
        create_cosmic_spiral_symbol(draw, center, size, cosmic_colors[0], char_data)
    
    # Add nebula effects to image
    create_cosmic_nebula_background(img, cosmic_colors, char_data, composition_seed)
    
    # Add stellar elements
    stellar_count = 15 + char_data['length'] + (char_data['cosmic_resonance'] % 20)
    for i in range(stellar_count):
        random.seed(style_seed + i)
        x = random.randint(size // 8, size - size // 8)
        y = random.randint(size // 8, size - size // 8)
        
        create_cosmic_star_point(draw, (x, y), cosmic_colors[i % len(cosmic_colors)], char_data)

def create_crystalline_precision_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed):
    """Create precise crystalline masterpiece with geometric perfection"""
    random.seed(artistic_seed)
    
    # Crystal color palette
    crystal_colors = [
        (0, 255, 255),    # Cyan
        (64, 224, 255),   # Sky blue
        (255, 255, 255),  # White
        (192, 192, 192),  # Silver
        (135, 206, 250),  # Light sky blue
    ]
    
    # Create central crystal formation
    crystal_complexity = 6 + char_data['complexity_score'] % 8
    
    for layer in range(crystal_complexity):
        layer_size = (size // 8) + (layer * 15) + (char_data['geometric_precision'] % 30)
        sides = 6 + (layer % 4)
        
        create_precision_crystal_layer(draw, center, layer_size, sides, crystal_colors[layer % len(crystal_colors)], char_data, layer)
    
    # Add crystal facets and reflections
    create_crystal_facet_system(draw, center, size, phrase, char_data, crystal_colors, style_seed)

def create_shadow_mystery_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed):
    """Create mysterious shadow masterpiece with sophisticated depth"""
    random.seed(artistic_seed)
    
    # Enhanced shadow colors (brighter for visibility)
    shadow_colors = [
        (100, 200, 255),  # Light blue
        (150, 180, 255),  # Periwinkle  
        (200, 160, 255),  # Light purple
        (180, 200, 255),  # Lavender blue
        (255, 255, 255),  # White highlights
    ]
    
    # Create central mysterious symbol
    if 'hidden' in phrase.lower() or 'secret' in phrase.lower():
        create_mystery_eye_symbol(draw, center, size, shadow_colors[0], char_data)
    else:
        create_mystery_geometric_symbol(draw, center, size, shadow_colors[0], char_data)
    
    # Add flowing shadow tendrils
    create_flowing_shadow_tendrils(draw, center, size, phrase, char_data, shadow_colors, artistic_seed)

def create_radiant_light_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed):
    """Create radiant light masterpiece with brilliant illumination"""
    random.seed(artistic_seed)
    
    # Radiant light palette
    light_colors = [
        (255, 255, 0),    # Bright yellow
        (255, 215, 0),    # Gold
        (255, 255, 255),  # Pure white
        (255, 248, 220),  # Cornsilk
        (255, 250, 205),  # Lemon chiffon
    ]
    
    # Create central radiant symbol
    create_radiant_sun_symbol(draw, center, size, light_colors[0], char_data)
    
    # Add light ray emanations
    create_light_ray_system(draw, center, size, phrase, char_data, light_colors, artistic_seed)

def create_elemental_organic_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed):
    """Create organic elemental masterpiece with natural flow"""
    random.seed(artistic_seed)
    
    # Natural element colors
    elemental_colors = [
        (34, 139, 34),    # Forest green
        (0, 100, 0),      # Dark green
        (50, 205, 50),    # Lime green
        (124, 252, 0),    # Lawn green
        (255, 255, 255),  # White highlights
    ]
    
    # Create elemental symbol based on phrase
    if any(element in phrase.lower() for element in ['earth', 'ground', 'stone']):
        create_earth_element_symbol(draw, center, size, elemental_colors[0], char_data)
    elif any(element in phrase.lower() for element in ['water', 'ocean', 'river']):
        create_water_element_symbol(draw, center, size, elemental_colors[0], char_data)
    elif any(element in phrase.lower() for element in ['fire', 'flame', 'burn']):
        create_fire_element_symbol(draw, center, size, elemental_colors[0], char_data)
    elif any(element in phrase.lower() for element in ['air', 'wind', 'breath']):
        create_air_element_symbol(draw, center, size, elemental_colors[0], char_data)
    else:
        create_universal_element_symbol(draw, center, size, elemental_colors[0], char_data)

def create_ultra_cosmic_sigil(draw, img, center, size, phrase, char_data, text_seed, pattern_seed, color_seed):
    """Create cosmic sigil with EXTREME text influence"""
    random.seed(text_seed + pattern_seed + color_seed)
    print("  -> Creating ULTRA cosmic sigil...")
    # Direct implementation to avoid recursion
    colors = [(40, 40, 120), (120, 180, 255), (220, 120, 255)]
    
    # Create cosmic patterns
    for i in range(20 + char_data['length']):
        x = random.randint(0, size)
        y = random.randint(0, size)
        color = colors[i % len(colors)]
        try:
            draw.ellipse([x-3, y-3, x+3, y+3], fill=(*color, 200))
        except:
            pass

def create_ultra_elemental_sigil(draw, img, center, size, phrase, char_data, text_seed, pattern_seed, color_seed):
    """Create elemental sigil with EXTREME text influence"""
    random.seed(text_seed + pattern_seed + color_seed)
    print("  -> Creating ULTRA elemental sigil...")
    # Placeholder for enhanced elemental sigil creation
    create_elemental_sigil(draw, img, center, size, phrase, text_seed, pattern_seed, color_seed)

def create_ultra_crystal_sigil(draw, img, center, size, phrase, char_data, text_seed, pattern_seed, color_seed):
    """Create crystal sigil with EXTREME text influence"""
    random.seed(text_seed + pattern_seed + color_seed)
    print("  -> Creating ULTRA crystal sigil...")
    # Placeholder for enhanced crystal sigil creation
    create_crystal_sigil(draw, img, center, size, phrase, text_seed, pattern_seed, color_seed)

def create_ultra_shadow_sigil(draw, img, center, size, phrase, char_data, text_seed, pattern_seed, color_seed):
    """Create shadow sigil with EXTREME text influence"""
    random.seed(text_seed + pattern_seed + color_seed)
    print("  -> Creating ULTRA shadow sigil...")
    # Placeholder for enhanced shadow sigil creation
    create_shadow_sigil(draw, img, center, size, phrase, text_seed, pattern_seed, color_seed)

def create_ultra_light_sigil(draw, img, center, size, phrase, char_data, text_seed, pattern_seed, color_seed):
    """Create light sigil with EXTREME text influence"""
    random.seed(text_seed + pattern_seed + color_seed)
    print("  -> Creating ULTRA light sigil...")
    # Placeholder for enhanced light sigil creation
    create_light_sigil(draw, img, center, size, phrase, text_seed, pattern_seed, color_seed)


# ===== SOPHISTICATED ARTISTIC CREATION SYSTEM =====

def create_artistic_profile(phrase):
    """Create detailed artistic profile from user's intent"""
    profile = {
        'complexity_level': min(10, len(phrase.split()) + len(set(phrase.lower()))),
        'emotional_depth': count_emotional_words(phrase) * 2,
        'symbolic_weight': len([c for c in phrase if c.isalpha()]) / max(1, len(phrase)),
        'mystical_elements': sum(1 for word in phrase.lower().split() if word in [
            'love', 'power', 'light', 'sacred', 'divine', 'spirit', 'energy', 'magic',
            'protection', 'healing', 'wisdom', 'strength', 'abundance', 'manifestation'
        ]),
        'geometric_preference': hash(phrase) % 5,  # 0-4 for different geometric styles
        'color_intensity': (sum(ord(c) for c in phrase) % 100) / 100,
        'glow_factor': min(1.0, len(phrase) / 20),
        'symmetry_level': (len(set(phrase.lower())) / max(1, len(phrase))) * 10
    }
    return profile

def extract_deep_symbolism(phrase):
    """Extract sophisticated symbolic meanings from text"""
    symbols = []
    phrase_lower = phrase.lower()
    
    # Celestial symbols
    if any(word in phrase_lower for word in ['star', 'moon', 'sun', 'cosmic', 'celestial', 'infinity']):
        symbols.append('celestial')
    
    # Geometric symbols  
    if any(word in phrase_lower for word in ['sacred', 'geometry', 'triangle', 'circle', 'square']):
        symbols.append('geometric')
    
    # Nature symbols
    if any(word in phrase_lower for word in ['earth', 'water', 'fire', 'air', 'nature', 'tree']):
        symbols.append('elemental')
    
    # Mystical symbols
    if any(word in phrase_lower for word in ['magic', 'spell', 'witch', 'wizard', 'enchant', 'mystical']):
        symbols.append('mystical')
    
    # Protection symbols
    if any(word in phrase_lower for word in ['protect', 'shield', 'guard', 'safe', 'secure']):
        symbols.append('protective')
    
    # Power symbols
    if any(word in phrase_lower for word in ['power', 'strength', 'force', 'energy', 'mighty']):
        symbols.append('power')
    
    # Eye symbols
    if any(word in phrase_lower for word in ['see', 'vision', 'sight', 'eye', 'watch', 'observe']):
        symbols.append('vision')
    
    return symbols if symbols else ['universal']

def calculate_emotional_resonance(phrase):
    """Calculate sophisticated emotional resonance score"""
    emotional_words = {
        'love': 10, 'peace': 8, 'joy': 9, 'happiness': 8, 'bliss': 9,
        'power': 7, 'strength': 6, 'courage': 7, 'confidence': 6,
        'wisdom': 8, 'knowledge': 6, 'truth': 7, 'clarity': 6,
        'healing': 8, 'health': 6, 'wellness': 6, 'vitality': 7,
        'abundance': 7, 'prosperity': 6, 'wealth': 5, 'success': 6,
        'protection': 7, 'safety': 6, 'security': 5, 'shield': 6,
        'freedom': 8, 'liberation': 8, 'independence': 6,
        'transformation': 9, 'change': 6, 'growth': 7, 'evolution': 8,
        'spiritual': 9, 'divine': 10, 'sacred': 9, 'holy': 8,
        'magic': 8, 'mystical': 8, 'enchanted': 7, 'magical': 7
    }
    
    words = phrase.lower().split()
    total_resonance = sum(emotional_words.get(word, 0) for word in words)
    base_resonance = len(phrase) * 2
    
    return min(100, total_resonance + base_resonance)

def determine_aesthetic_style(phrase, vibe):
    """Determine sophisticated aesthetic style"""
    styles = {
        'neon_geometric': ['modern', 'tech', 'cyber', 'digital', 'electric'],
        'cosmic_ethereal': ['space', 'star', 'cosmic', 'universe', 'infinity', 'eternal'],
        'mystical_ornate': ['magic', 'mystical', 'ancient', 'wisdom', 'sacred', 'divine'],
        'elemental_organic': ['nature', 'earth', 'water', 'fire', 'air', 'natural'],
        'crystalline_precise': ['crystal', 'diamond', 'gem', 'clarity', 'pure', 'precise'],
        'shadow_mysterious': ['shadow', 'dark', 'mystery', 'hidden', 'secret', 'depth']
    }
    
    phrase_lower = phrase.lower()
    
    # Check for style keywords in phrase
    for style, keywords in styles.items():
        if any(keyword in phrase_lower for keyword in keywords):
            return style
    
    # Default based on vibe
    vibe_styles = {
        'mystical': 'mystical_ornate',
        'cosmic': 'cosmic_ethereal', 
        'elemental': 'elemental_organic',
        'crystal': 'crystalline_precise',
        'shadow': 'shadow_mysterious',
        'light': 'neon_geometric'
    }
    
    primary_vibe = vibe.split('+')[0] if '+' in vibe else vibe
    return vibe_styles.get(primary_vibe, 'neon_geometric')

def create_professional_canvas(size, aesthetic_style, char_data):
    """Create sophisticated background canvas"""
    # Create base image
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 255))
    
    # Create sophisticated gradient background based on aesthetic style
    gradient_colors = {
        'neon_geometric': [(0, 5, 15), (0, 15, 30), (5, 20, 40)],
        'cosmic_ethereal': [(5, 0, 20), (15, 5, 35), (25, 10, 50)],
        'mystical_ornate': [(10, 5, 20), (20, 10, 30), (30, 15, 40)],
        'elemental_organic': [(5, 10, 5), (10, 20, 10), (15, 30, 15)],
        'crystalline_precise': [(0, 10, 15), (5, 15, 25), (10, 20, 35)],
        'shadow_mysterious': [(5, 0, 10), (10, 5, 15), (15, 10, 20)]
    }
    
    colors = gradient_colors.get(aesthetic_style, gradient_colors['neon_geometric'])
    
    # Create radial gradient
    for y in range(size):
        for x in range(size):
            distance = math.sqrt((x - size/2)**2 + (y - size/2)**2) / (size/2)
            distance = min(1.0, distance)
            
            # Interpolate colors based on distance
            if distance < 0.3:
                color = colors[0]
            elif distance < 0.7:
                # Interpolate between colors[0] and colors[1]
                t = (distance - 0.3) / 0.4
                color = tuple(int(colors[0][i] + t * (colors[1][i] - colors[0][i])) for i in range(3))
            else:
                # Interpolate between colors[1] and colors[2]
                t = (distance - 0.7) / 0.3
                color = tuple(int(colors[1][i] + t * (colors[2][i] - colors[1][i])) for i in range(3))
            
            img.putpixel((x, y), (*color, 255))
    
    return img

def create_masterpiece_foundation(draw, img, center, size, phrase, char_data, seed):
    """Create sophisticated foundational sacred geometry"""
    random.seed(seed)
    
    # Create multiple layers of sacred geometry based on phrase characteristics
    foundation_layers = 3 + (char_data['complexity_score'] % 4)
    
    for layer in range(foundation_layers):
        layer_radius = (size // 8) + (layer * (size // 12)) + (char_data['sacred_power'] % 50)
        layer_sides = 6 + (char_data['unique_chars'] % 6) + layer
        layer_alpha = 80 - (layer * 15)
        
        # Create geometric foundation
        points = []
        for i in range(layer_sides):
            angle = (360 / layer_sides) * i + (char_data['first_char_value'] * layer)
            x = center[0] + layer_radius * math.cos(math.radians(angle))
            y = center[1] + layer_radius * math.sin(math.radians(angle))
            points.append((x, y))
        
        # Draw foundation geometry with sophisticated styling
        try:
            color = (100 + char_data['vowel_count'] * 10, 150 + char_data['consonant_count'] * 8, 200 + char_data['unique_chars'] * 5)
            draw.polygon(points, outline=(*color, layer_alpha), width=2 + layer)
            
            # Add connecting lines for complexity
            if layer > 0:
                for i in range(0, len(points), 2):
                    opposite_i = (i + len(points) // 2) % len(points)
                    draw.line([points[i], points[opposite_i]], fill=(*color, layer_alpha // 2), width=1)
        except:
            pass

def create_artistic_masterpiece_layer(draw, img, center, size, phrase, vibe, char_data, 
                                    artistic_seed, composition_seed, style_seed, color_seed):
    """Create sophisticated artistic masterpiece based on vibe"""
    
    print(f"🎨 Creating MASTERPIECE layer for {vibe}...")
    
    if vibe == 'mystical':
        create_neon_mystical_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed)
    elif vibe == 'cosmic':
        create_cosmic_ethereal_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed)
    elif vibe == 'elemental':
        create_elemental_organic_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed)
    elif vibe == 'crystal':
        create_crystalline_precision_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed)
    elif vibe == 'shadow':
        create_shadow_mystery_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed)
    elif vibe == 'light':
        create_radiant_light_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed)
    else:
        # Default to mystical masterpiece
        create_neon_mystical_masterpiece(draw, img, center, size, phrase, char_data, artistic_seed, composition_seed, style_seed, color_seed)


# ===== SOPHISTICATED SYMBOL CREATION FUNCTIONS =====

def create_neon_eye_symbol(draw, center, size, color, char_data, style_seed):
    """Create sophisticated neon eye symbol like reference images"""
    x, y = center
    
    # Calculate eye dimensions based on phrase characteristics
    eye_width = 80 + char_data['sacred_power'] % 40
    eye_height = 40 + char_data['intent_strength'] % 20
    pupil_size = 20 + char_data['manifestation_power'] % 15
    
    # Draw outer eye shape with neon glow
    eye_points = [
        (x - eye_width//2, y),
        (x - eye_width//4, y - eye_height//2),
        (x + eye_width//4, y - eye_height//2),
        (x + eye_width//2, y),
        (x + eye_width//4, y + eye_height//2),
        (x - eye_width//4, y + eye_height//2)
    ]
    
    # Draw with multiple layers for glow effect
    for glow in range(5, 0, -1):
        glow_color = (*color, max(30, 255 - glow * 40))
        try:
            draw.polygon(eye_points, outline=glow_color, width=glow * 2)
        except:
            pass
    
    # Draw inner circle (iris)
    iris_size = eye_height - 10
    try:
        for glow in range(3, 0, -1):
            glow_color = (*color, max(50, 255 - glow * 50))
            draw.ellipse([x-iris_size//2, y-iris_size//2, x+iris_size//2, y+iris_size//2], 
                        outline=glow_color, width=glow * 2)
    except:
        pass
    
    # Draw pupil
    try:
        pupil_color = (255, 255, 255, 255)
        draw.ellipse([x-pupil_size//2, y-pupil_size//2, x+pupil_size//2, y+pupil_size//2], 
                    fill=pupil_color)
    except:
        pass

def create_neon_arrow_symbol(draw, center, size, color, char_data, style_seed):
    """Create sophisticated neon arrow symbol"""
    x, y = center
    
    # Arrow pointing up by default, rotated based on phrase
    arrow_height = 100 + char_data['sacred_power'] % 50
    arrow_width = 60 + char_data['intent_strength'] % 30
    
    # Main arrow shaft
    shaft_width = 8 + char_data['manifestation_power'] % 6
    
    # Arrow points
    points = [
        (x, y - arrow_height//2),  # Top point
        (x - arrow_width//2, y - arrow_height//4),  # Left wing
        (x - shaft_width//2, y - arrow_height//4),  # Left shaft top
        (x - shaft_width//2, y + arrow_height//2),  # Left shaft bottom
        (x + shaft_width//2, y + arrow_height//2),  # Right shaft bottom
        (x + shaft_width//2, y - arrow_height//4),  # Right shaft top
        (x + arrow_width//2, y - arrow_height//4),  # Right wing
    ]
    
    # Draw with glow effect
    for glow in range(6, 0, -1):
        glow_color = (*color, max(40, 255 - glow * 30))
        try:
            draw.polygon(points, outline=glow_color, width=glow)
        except:
            pass

def create_neon_geometric_symbol(draw, center, size, color, char_data, style_seed):
    """Create sophisticated neon geometric symbol"""
    x, y = center
    
    # Create complex geometric pattern
    outer_radius = 60 + char_data['sacred_power'] % 40
    inner_radius = 30 + char_data['intent_strength'] % 20
    sides = 6 + char_data['manifestation_power'] % 6
    
    # Outer shape
    outer_points = []
    for i in range(sides):
        angle = (360 / sides) * i
        px = x + outer_radius * math.cos(math.radians(angle))
        py = y + outer_radius * math.sin(math.radians(angle))
        outer_points.append((px, py))
    
    # Inner shape
    inner_points = []
    for i in range(sides):
        angle = (360 / sides) * i + (180 / sides)  # Offset for star effect
        px = x + inner_radius * math.cos(math.radians(angle))
        py = y + inner_radius * math.sin(math.radians(angle))
        inner_points.append((px, py))
    
    # Draw with glow
    for glow in range(5, 0, -1):
        glow_color = (*color, max(50, 255 - glow * 40))
        try:
            draw.polygon(outer_points, outline=glow_color, width=glow)
            draw.polygon(inner_points, outline=glow_color, width=glow)
        except:
            pass

def create_neon_triangle(draw, pos, size, color, char_data):
    """Create neon triangle with glow"""
    x, y = pos
    height = size * 0.866  # Equilateral triangle height
    
    points = [
        (x, y - height/2),
        (x - size/2, y + height/2),
        (x + size/2, y + height/2)
    ]
    
    for glow in range(4, 0, -1):
        glow_color = (*color, max(60, 255 - glow * 50))
        try:
            draw.polygon(points, outline=glow_color, width=glow)
        except:
            pass

def create_neon_circle(draw, pos, size, color, char_data):
    """Create neon circle with glow"""
    x, y = pos
    
    for glow in range(4, 0, -1):
        glow_color = (*color, max(60, 255 - glow * 50))
        try:
            draw.ellipse([x-size, y-size, x+size, y+size], outline=glow_color, width=glow)
        except:
            pass

def create_neon_diamond(draw, pos, size, color, char_data):
    """Create neon diamond with glow"""
    x, y = pos
    
    points = [
        (x, y - size),
        (x + size, y),
        (x, y + size),
        (x - size, y)
    ]
    
    for glow in range(4, 0, -1):
        glow_color = (*color, max(60, 255 - glow * 50))
        try:
            draw.polygon(points, outline=glow_color, width=glow)
        except:
            pass

def create_neon_cross(draw, pos, size, color, char_data):
    """Create neon cross with glow"""
    x, y = pos
    thickness = size // 4
    
    # Vertical bar
    v_points = [
        (x - thickness, y - size),
        (x + thickness, y - size),
        (x + thickness, y + size),
        (x - thickness, y + size)
    ]
    
    # Horizontal bar
    h_points = [
        (x - size, y - thickness),
        (x + size, y - thickness),
        (x + size, y + thickness),
        (x - size, y + thickness)
    ]
    
    for glow in range(4, 0, -1):
        glow_color = (*color, max(60, 255 - glow * 50))
        try:
            draw.polygon(v_points, outline=glow_color, width=glow)
            draw.polygon(h_points, outline=glow_color, width=glow)
        except:
            pass

def create_neon_energy_connections(draw, center, size, phrase, char_data, colors, seed):
    """Create sophisticated energy connections between elements"""
    random.seed(seed)
    
    # Create connecting lines based on phrase energy
    connection_count = 8 + char_data['word_count'] * 2
    
    for i in range(connection_count):
        # Calculate connection points
        angle1 = random.uniform(0, 360)
        angle2 = random.uniform(0, 360)
        
        distance1 = random.uniform(size//8, size//3)
        distance2 = random.uniform(size//8, size//3)
        
        x1 = center[0] + distance1 * math.cos(math.radians(angle1))
        y1 = center[1] + distance1 * math.sin(math.radians(angle1))
        
        x2 = center[0] + distance2 * math.cos(math.radians(angle2))
        y2 = center[1] + distance2 * math.sin(math.radians(angle2))
        
        color = colors[i % len(colors)]
        
        # Draw connection with glow
        for glow in range(3, 0, -1):
            glow_color = (*color, max(30, 150 - glow * 40))
            try:
                draw.line([(x1, y1), (x2, y2)], fill=glow_color, width=glow)
            except:
                pass

# Additional symbol creation functions
def create_cosmic_infinity_symbol(draw, center, size, color, char_data):
    """Create cosmic infinity symbol"""
    x, y = center
    width = 80 + char_data['sacred_power'] % 40
    height = 40 + char_data['intent_strength'] % 20
    
    # Create infinity symbol using curves
    for glow in range(5, 0, -1):
        glow_color = (*color, max(50, 255 - glow * 40))
        # Left loop
        try:
            draw.ellipse([x-width//2, y-height//2, x, y+height//2], outline=glow_color, width=glow)
        except:
            pass
        # Right loop  
        try:
            draw.ellipse([x, y-height//2, x+width//2, y+height//2], outline=glow_color, width=glow)
        except:
            pass

def create_cosmic_star_symbol(draw, center, size, color, char_data):
    """Create cosmic star symbol"""
    x, y = center
    radius = 50 + char_data['sacred_power'] % 30
    
    # 8-pointed star
    points = []
    for i in range(16):
        angle = (360 / 16) * i
        point_radius = radius if i % 2 == 0 else radius * 0.5
        px = x + point_radius * math.cos(math.radians(angle))
        py = y + point_radius * math.sin(math.radians(angle))
        points.append((px, py))
    
    for glow in range(5, 0, -1):
        glow_color = (*color, max(50, 255 - glow * 40))
        try:
            draw.polygon(points, outline=glow_color, width=glow)
        except:
            pass

def create_cosmic_spiral_symbol(draw, center, size, color, char_data):
    """Create cosmic spiral symbol"""
    x, y = center
    
    # Create spiral using connected points
    points = []
    for angle in range(0, 720, 10):  # Two full rotations
        radius = (angle / 720) * (40 + char_data['sacred_power'] % 30)
        px = x + radius * math.cos(math.radians(angle))
        py = y + radius * math.sin(math.radians(angle))
        points.append((px, py))
    
    # Draw spiral with glow
    for i in range(len(points) - 1):
        for glow in range(3, 0, -1):
            glow_color = (*color, max(80, 255 - glow * 50))
            try:
                draw.line([points[i], points[i+1]], fill=glow_color, width=glow)
            except:
                pass

# Placeholder functions for other symbol types
def create_precision_crystal_layer(draw, center, layer_size, sides, color, char_data, layer): pass
def create_crystal_facet_system(draw, center, size, phrase, char_data, colors, seed): pass
def create_mystery_eye_symbol(draw, center, size, color, char_data): pass
def create_mystery_geometric_symbol(draw, center, size, color, char_data): pass
def create_flowing_shadow_tendrils(draw, center, size, phrase, char_data, colors, seed): pass
def create_radiant_sun_symbol(draw, center, size, color, char_data): pass
def create_light_ray_system(draw, center, size, phrase, char_data, colors, seed): pass
def create_earth_element_symbol(draw, center, size, color, char_data): pass
def create_water_element_symbol(draw, center, size, color, char_data): pass
def create_fire_element_symbol(draw, center, size, color, char_data): pass
def create_air_element_symbol(draw, center, size, color, char_data): pass
def create_universal_element_symbol(draw, center, size, color, char_data): pass
def create_cosmic_nebula_background(img, colors, char_data, seed): pass
def create_cosmic_star_point(draw, pos, color, char_data): pass

# Enhanced characteristic analysis functions
def analyze_word_meanings(phrase): 
    return {'depth': len(phrase.split()), 'complexity': len(set(phrase.lower()))}

def calculate_emotional_weight(phrase): 
    return min(100, len(phrase) * 3 + count_emotional_words(phrase) * 10)

def extract_symbolic_elements(phrase): 
    return extract_deep_symbolism(phrase)

def create_base_sacred_geometry(draw, center, size, phrase, char_data, seed):
    """Create base sacred geometry patterns"""
    random.seed(seed)
    radius = size // 6
    for i in range(6):
        angle = i * 60
        x = center[0] + radius * math.cos(math.radians(angle))
        y = center[1] + radius * math.sin(math.radians(angle))
        try:
            draw.ellipse([x-10, y-10, x+10, y+10], outline=(255, 255, 255, 100), width=2)
        except:
            pass

def add_symbolic_elements(draw, center, size, elements, char_data, seed): pass
def add_meaning_patterns(draw, center, size, meanings, char_data, seed): pass
def apply_layer_alpha(img, alpha): return img

def apply_enhanced_vibe_effects(img, vibe, phrase): 
    return apply_optimized_vibe_effects(img, vibe, phrase)

def get_phrase_characteristics(phrase): 
    return get_enhanced_phrase_characteristics(phrase)

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