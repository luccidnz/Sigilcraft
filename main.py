
import os; os.system("pip install pillow")

from PIL import Image, ImageDraw, ImageFont
import string
import math

def create_sigil(phrase, filename='sigil.png'):
    phrase = phrase.upper()
    phrase = ''.join([c for c in phrase if c in string.ascii_uppercase])
    phrase = ''.join(sorted(set(phrase), key=phrase.index))

    img = Image.new('RGB', (500, 500), color='black')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    radius = 180
    center = (250, 250)
    angle_step = 360 / len(phrase)
    points = []

    for i, letter in enumerate(phrase):
        angle = math.radians(i * angle_step - 90)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        draw.text((x - 10, y - 10), letter, font=font, fill='white')
        points.append((x, y))

    draw.line(points, fill='red', width=3)
    img.save(filename)
    print(f"✅ Sigil saved as {filename}")

if __name__ == "__main__":
    phrase = input("🔮 Enter your intent or desire: ")
    create_sigil(phrase)
