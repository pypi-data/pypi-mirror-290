from pathlib import Path
from typing import Union, TYPE_CHECKING
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import tempfile
from .output_svg import save_matrix_to_svg

if TYPE_CHECKING:
    import numpy as np

def save_matrix_to_pdf(
    text_matrix: "np.ndarray",
    color_matrix: "np.ndarray",
    output_file: Union[str, Path],
    font_size: int = 10,
    line_height_ratio: float = 1.0,
    lighten_factor: float = 1.2
) -> Path:
    """
    Generates a PDF file displaying the text matrix with colors from the color matrix,
    adjusting the text color to be a little bit lighter than the background color.

    :param text_matrix: A 2D NumPy array of characters representing the text.
    :param color_matrix: A 2D NumPy array of hex color strings.
    :param output_file: The file path where the PDF file will be saved.
    :param font_size: The font size to use in the PDF output.
    :param line_height_ratio: The ratio of line-height to font-size to adjust the aspect ratio (default is 1).
    :param lighten_factor: Factor to lighten the text color relative to the background color.
    :return: The path to the generated PDF file.
    """
    output_file = Path(output_file)

    # Create a temporary SVG file
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp_svg:
        tmp_svg_path = Path(tmp_svg.name)
        
        # Generate the SVG using the save_matrix_to_svg function
        save_matrix_to_svg(
            text_matrix=text_matrix,
            color_matrix=color_matrix,
            output_file=tmp_svg_path,
            font_size=font_size,
            line_height_ratio=line_height_ratio,
            lighten_factor=lighten_factor
        )
    
    try:
        # Convert the SVG to a ReportLab drawing
        drawing = svg2rlg(tmp_svg_path)
        
        # Write the drawing to a PDF
        with output_file.open('wb') as pdf_file:
            renderPDF.drawToFile(drawing, pdf_file)
    finally:
        # Clean up the temporary SVG file
        tmp_svg_path.unlink()

    return output_file
