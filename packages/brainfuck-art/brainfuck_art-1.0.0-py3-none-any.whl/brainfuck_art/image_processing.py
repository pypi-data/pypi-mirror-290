from typing import Optional, Union
from PIL import Image
import numpy as np
from pathlib import Path

from .brainfuck_generation import text_to_bf

__all__ = ["image_to_matrix"]

DEFAULT_ALPHABET = r"%$&/()¿?=!\\º#*ª;{}"

ImageType = Union[Image.Image, str, Path]

def image_to_matrix(
    image: ImageType,
    text: Optional[str] = None,
    width: int = 512,
    height: int = 512,
    alphabet: Optional[str] = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generates two matrices: one for text and one for the color values of an image.
    
    :param image: The input image, which can be a PIL Image, a file path, or a string path.
    :param text: Optional text to encode in the text matrix using Brainfuck.
    :param width: The target width for both the image and text matrices.
    :param height: The target height for both the image and text matrices.
    :param alphabet: Optional custom alphabet for generating the text matrix.
    :return: A tuple containing the text matrix and the color matrix.
    """
    text = None if text is None else text_to_bf(text)
    text_matrix = get_text_matrix(width=width, height=height, hidden_text=text, alphabet=alphabet)
    color_matrix = get_color_matrix(image, width=width, height=height)

    return text_matrix, color_matrix

def read_image(image: ImageType) -> Image.Image:
    """
    Opens an image file and returns a PIL Image object.
    
    :param image: The input image, which can be a PIL Image, a file path, or a string path.
    :return: A PIL Image object.
    """
    if isinstance(image, str):
        image = Path(image)
    if isinstance(image, Path):
        image = Image.open(image)

    return image

def get_color_matrix(image: ImageType, width: int = 512, height: int = 512) -> np.ndarray:
    """
    Resizes the image to the specified width and height, converts it to RGB, 
    and returns a NumPy array of the same dimensions with hex color values.
    
    :param image: The input PIL Image, a file path, or a string path.
    :param width: The target width for the image.
    :param height: The target height for the image.
    :return: A 2D NumPy array of strings containing hex color values.
    """
    image = read_image(image=image)
    image = image.resize((width, height), resample=Image.Resampling.LANCZOS).convert('RGB')

    rgb_array = np.array(image)
    hex_array = np.array([f'#{r:02x}{g:02x}{b:02x}' for r, g, b in rgb_array.reshape(-1, 3)])

    return hex_array.reshape(height, width)

def get_text_matrix(
    width: int = 512,
    height: int = 512,
    hidden_text: Optional[str] = None,
    alphabet: Optional[str] = None
) -> np.ndarray:
    """
    Generates a text matrix of specified width and height, optionally embedding hidden text.
    
    :param width: The target width for the text matrix.
    :param height: The target height for the text matrix.
    :param hidden_text: Optional hidden text to embed in the matrix.
    :param alphabet: Optional custom alphabet to use for the matrix.
    :return: A 2D NumPy array of characters representing the text matrix.
    """
    if alphabet is None:
        alphabet = DEFAULT_ALPHABET

    # Sample width*height from the alphabet
    base_text = np.random.choice(list(alphabet), size=width*height)
    
    if hidden_text is not None:
        # Sample len(hidden_text) positions to replace with hidden_text
        positions = np.random.choice(width*height, size=len(hidden_text), replace=False)
        # Sort the positions to insert the hidden text in order
        positions = np.sort(positions)
        for i, pos in enumerate(positions):
            base_text[pos] = hidden_text[i]

    return base_text.reshape(height, width)
