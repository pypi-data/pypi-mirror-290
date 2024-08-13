from pathlib import Path
from typing import Union, TYPE_CHECKING
from xml.sax.saxutils import escape

from .color_utils import get_lighter_text_color

if TYPE_CHECKING:
    import numpy as np

def save_matrix_to_svg(
    text_matrix: "np.ndarray",
    color_matrix: "np.ndarray",
    output_file: Union[str, Path],
    font_size: int = 10,
    line_height_ratio: float = 1.0,
    lighten_factor: float = 1.2
) -> Path:
    """
    Generates an SVG file displaying the text matrix with colors from the color matrix,
    adjusting the text color to be a little bit lighter than the background color.

    :param text_matrix: A 2D NumPy array of characters representing the text.
    :param color_matrix: A 2D NumPy array of hex color strings.
    :param output_file: The file path where the SVG file will be saved.
    :param font_size: The font size to use in the SVG output.
    :param line_height_ratio: The ratio of line-height to font-size to adjust the aspect ratio (default is 1).
    :param lighten_factor: Factor to lighten the text color relative to the background color.
    :return: The path to the generated SVG file.
    """
    output_file = Path(output_file)

    # Calculate character width and height
    char_width = font_size * line_height_ratio
    char_height = font_size * line_height_ratio

    # Calculate the total width and height of the SVG canvas
    svg_width = char_width * text_matrix.shape[1]
    svg_height = char_height * text_matrix.shape[0]

    # Start building the SVG content
    svg_content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" font-family="monospace" font-size="{font_size}px">',
        f'<style>',
        f'text {{ dominant-baseline: middle; text-anchor: middle; }}',
        f'</style>'
    ]

    # Adjust dy for characters with descenders
    descender_adjustment = {
        '(': "0.25em", ')': "0.25em", '[': "0.25em", ']': "0.25em",
        '{': "0.25em", '}': "0.25em", '$': "0.25em", ';': "0.25em",
        '|': "0.1em"
    }

    for row_idx in range(text_matrix.shape[0]):
        for col_idx in range(text_matrix.shape[1]):
            char = escape(text_matrix[row_idx, col_idx])
            color = color_matrix[row_idx, col_idx]
            text_color = get_lighter_text_color(color, lighten_factor)

            x = col_idx * char_width + char_width / 2
            y = row_idx * char_height + char_height / 2

            # Adjust dy if the character has a descender
            dy = descender_adjustment.get(char, "0.35em")

            svg_content.append(
                f'<rect x="{col_idx * char_width}" y="{row_idx * char_height}" width="{char_width}" height="{char_height}" fill="{color}"/>'
            )
            svg_content.append(
                f'<text x="{x}" y="{y}" dy="{dy}" fill="{text_color}">{char}</text>'
            )

    # Close the SVG tag
    svg_content.append('</svg>')

    # Write the SVG content to the output file
    with output_file.open('w') as f:
        f.write('\n'.join(svg_content))

    return output_file
