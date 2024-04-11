import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np

def simulate_brushstrokes(image, strength=1.0):
    """
    Simulate the brushstrokes effect by applying a directional blur or distortion.
    """
    # This is a placeholder for an actual implementation, which might involve
    # more complex operations like segmenting the image and applying varying
    # directional blurs or distortions to simulate strokes.
    return image.filter(ImageFilter.GaussianBlur(radius=strength))

def apply_enhanced_texture(image, texture_strength=1):
    """
    Apply an enhanced texture to simulate the canvas or paper, including brushstrokes.
    """
    width, height = image.size
    noise = np.random.normal(loc=128, scale=80, size=(height, width, 3)).clip(0, 255).astype(np.uint8)  # Increased texture
    noise_image = Image.fromarray(noise, 'RGB')
    image = Image.blend(image, noise_image, texture_strength)
    return simulate_brushstrokes(image, strength=np.random.uniform(0.5, 2.0))

def enhanced_color_adjustment(image):
    """
    Apply enhanced color adjustments to mimic painting's vibrant and varied colors.
    """
    color_factor = np.random.uniform(1.1, 1.3)  # Enhanced color vibrancy
    brightness_factor = np.random.uniform(0.9, 1.1)
    contrast_factor = np.random.uniform(1.1, 1.3)  # Enhanced contrast for depth

    image = ImageEnhance.Color(image).enhance(color_factor)
    image = ImageEnhance.Brightness(image).enhance(brightness_factor)
    image = ImageEnhance.Contrast(image).enhance(contrast_factor)
    return image

def fresson_quadrichromy_effect(image, texture_path=None, painting_like=True):
    # Load the image
    image = Image.open(image).convert("RGB")
    
    # Apply random nuanced color adjustments and simulate the pigment layering
    image = enhanced_color_adjustment(image) if painting_like else random_color_adjustment(image)
    
    # Apply enhanced texture and brushstrokes for a painting-like effect
    texture_strength = np.random.uniform(0.1, 0.25) if painting_like else np.random.uniform(0.05, 0.15)
    image = apply_enhanced_texture(image, texture_strength=texture_strength)
    
    if texture_path:
        texture = Image.open(texture_path).convert("RGBA")
        texture = texture.resize(image.size)
        texture = texture.convert("RGB")
        blend_factor = np.random.uniform(0.2, 0.4) if painting_like else np.random.uniform(0.1, 0.3)
        image = Image.blend(image, texture, blend_factor)
    
    # Apply a soft focus effect with more randomness to mimic the variability of painting
    blur_radius = np.random.uniform(0, 1) if painting_like else np.random.uniform(0.0, 2)
    image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    # Manually adjust color balance with enhanced randomness for a painting effect
    red, green, blue = image.split()
    red_factor = np.random.uniform(0.95, 1.05)
    green_factor = np.random.uniform(1.0, 1.1)
    blue_factor = np.random.uniform(0.9, 1.0)
    red = red.point(lambda p: p * red_factor + np.random.uniform(15, 25) if painting_like else p * red_factor + np.random.uniform(10, 20))
    green = green.point(lambda p: p * green_factor)
    blue = blue.point(lambda p: p * blue_factor - np.random.uniform(10, 20) if painting_like else p * blue_factor - np.random.uniform(5, 10))
    image = Image.merge("RGB", (red, green, blue))
    
    return image

# Streamlit app
st.title('Fresson Quadrichromy Effect Simulator')

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
    # Convert the uploaded file to an image object directly
    image = Image.open(uploaded_file).convert("RGB")

    painting_like = st.checkbox('Apply painting-like enhancements', value=True)

    # Display the original image
    st.image(image, caption='Original Image', use_column_width=True)

    # Process the image when the button is clicked
    if st.button('Apply Effect'):
        # Apply the Fresson Quadrichromy effect
        result_image = fresson_quadrichromy_effect(image, painting_like=painting_like)
        
        # Display the processed image
        st.image(result_image, caption='Processed Image', use_column_width=True)

        # Save the result image to a bytes buffer and provide a download link
        buf = io.BytesIO()  # You need to import io at the top
        result_image.save(buf, format='JPEG')
        buf.seek(0)
        st.download_button(label='Download Result', data=buf, file_name='processed_image.jpg', mime='image/jpeg')
