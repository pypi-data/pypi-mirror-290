from pathlib import Path
from typing import Union, TYPE_CHECKING

from .color_utils import get_lighter_text_color

if TYPE_CHECKING:
    import numpy as np

__all__ = ["save_matrix_to_html"]

def save_matrix_to_html(
    text_matrix: "np.ndarray",
    color_matrix: "np.ndarray",
    output_file: Union[str, Path],
    font_size: int = 10,
    line_height_ratio: float = 1.0,
    lighten_factor: float = 1.2,
    title: str = "Hi!"
) -> Path:
    """
    Generates an HTML file displaying the text matrix with colors from the color matrix,
    adjusting the text color to be a little bit lighter than the background color.
    
    :param text_matrix: A 2D NumPy array of characters representing the text.
    :param color_matrix: A 2D NumPy array of hex color strings.
    :param output_file: The file path where the HTML file will be saved.
    :param font_size: The font size to use in the HTML output.
    :param line_height_ratio: The ratio of line-height to font-size to adjust the aspect ratio (default is 1).
    :param lighten_factor: Factor to lighten the text color relative to the background color.
    """
    output_file = Path(output_file)

    # Start building the HTML content
    html_content = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        f"<title{title}></title>",
        "<style>",
        f".matrix {{ font-family: monospace; font-size: {font_size}px; line-height: {line_height_ratio}; white-space: pre; vertical-align: middle; }}",
        "</style>",
        "</head>",
        "<body>",
        "<div class='matrix'>"
    ]

    for row_idx in range(text_matrix.shape[0]):
        row_html = []
        current_color = None
        buffer = []

        for col_idx in range(text_matrix.shape[1]):
            char = text_matrix[row_idx, col_idx]
            color = color_matrix[row_idx, col_idx]
            text_color = get_lighter_text_color(color, lighten_factor)

            if color != current_color:
                if buffer:
                    # Flush the buffer for the previous color and text color
                    row_html.append(f"<span style='color:{text_color}; background-color:{current_color}'>{''.join(buffer)}</span>")
                buffer = [char]
                current_color = color
            else:
                buffer.append(char)

        # Flush the last buffer
        if buffer:
            row_html.append(f"<span style='color:{text_color}; background-color:{current_color}'>{''.join(buffer)}</span>")

        html_content.append(''.join(row_html))
        html_content.append("<br>")  # Add a line break after each row

    # Close the HTML tags
    html_content.extend([
        "</div>",
        "</body>",
        "</html>"
    ])

    # Write the HTML content to the output file
    with output_file.open('w') as f:
        f.write(''.join(html_content))

    return output_file