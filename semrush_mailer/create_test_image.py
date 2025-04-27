import os
from PIL import Image, ImageDraw

def create_test_image(output_path, width=800, height=600):
    """Create a very simple test image"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create a white background image
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Add a border
    draw.rectangle([(0, 0), (width-1, height-1)], outline=(0, 0, 0), width=2)
    
    # Add some simple shapes - horizontal lines
    for i in range(5):
        y = 100 + i * 50
        draw.line([(100, y), (700, y)], fill=(0, 0, 255), width=3)
    
    # Add some vertical lines
    for i in range(6):
        x = 100 + i * 100
        draw.line([(x, 100), (x, 350)], fill=(255, 0, 0), width=2)
    
    # Draw a rectangle
    draw.rectangle([(200, 400), (600, 500)], outline=(0, 0, 0), fill=(200, 200, 200))
    
    # Add text - simpler approach without exact positioning
    draw.text((250, 430), "SEMrush Test Report", fill=(0, 0, 0))
    
    # Save the image
    image.save(output_path)
    print(f"Test image created: {output_path}")
    return output_path

if __name__ == "__main__":
    # Create test image in the semrush_reports directory
    output_path = os.path.join("semrush_reports", "test_image.png")
    create_test_image(output_path) 