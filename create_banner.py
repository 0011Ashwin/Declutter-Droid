from PIL import Image, ImageDraw, ImageFont
import random

def create_banner(output_path="banner_cover.png"):
    width, height = 1200, 400
    # Banana Yellow background
    background_color = (255, 225, 53)
    text_color = (50, 50, 50) 
    
    img = Image.new('RGB', (width, height), color=background_color)
    d = ImageDraw.Draw(img)
    
    # Add some "Nano" dots (styling)
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(5, 20)
        d.ellipse([x, y, x+r, y+r], fill=(255, 240, 100))

    # Add Text
    try:
        # Try to load a default font, size 40 (might be small but readable)
        # On Windows, arial.ttf usually exists
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()

    text = "Nano Banana Model"
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    
    d.text(((width - text_w) / 2, (height - text_h) / 2), text, font=font, fill=text_color)
    
    # Draw a simple banana shape (curve)
    shape_color = (200, 180, 0)
    # Just a symbolic curve
    d.arc([width - 300, 50, width - 100, 350], start=30, end=150, fill=shape_color, width=20)

    img.save(output_path)
    print(f"Banner saved to {output_path}")

if __name__ == "__main__":
    create_banner()
