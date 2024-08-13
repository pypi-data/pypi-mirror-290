import argparse
import logging
from pathlib import Path
from typing import Tuple, Optional

from .image_processing import image_to_matrix

def resolve_output_and_filetype(
    image: str,
    output: Optional[str],
    filetype: Optional[str]
) -> Tuple[Path, str]:
    """
    Resolve the output file path and file type based on the input image, output, and filetype arguments.

    :param image: The input image file path.
    :param output: The desired output file path (can be None).
    :param filetype: The desired output file type (can be None).
    :return: A tuple containing the resolved output file path and file type.
    """
    input_path = Path(image)

    if output:
        output_path = Path(output)
        if filetype is None:
            if output_path.suffix.lower() in [".html", ".svg", ".pdf"]:
                filetype = output_path.suffix.lower()[1:]
            else:
                raise ValueError("Cannot infer filetype from the output file extension. Please specify --filetype.")
    else:
        if filetype is None:
            filetype = "pdf"  # Default to PDF if neither filetype nor output is specified
        output_path = input_path.with_suffix(f".{filetype}")

    return output_path, filetype


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art with embedded Brainfuck code and export as HTML, SVG, or PDF.")
    
    # Required positional argument for the input image
    parser.add_argument("image", type=str, help="The input image file.")
    
    # Optional arguments
    parser.add_argument("-o", "--output", type=str, help="The output file name with extension.")
    parser.add_argument("-f", "--filetype", type=str, choices=["html", "svg", "pdf"], help="The output file type. Defaults to infer from the output filename.")
    parser.add_argument("-t", "--text", type=str, default="", help="The text to encode as Brainfuck code. Default is empty.")
    parser.add_argument("-W", "--width", type=int, default=64, help="The width of the output in characters. Default is 64.")
    parser.add_argument("-H", "--height", type=int, default=64, help="The height of the output in characters. Default is 64.")
    parser.add_argument("-a", "--alphabet", type=str, help="The alphabet of non-BF characters to fill the text. Default is None, using the function's default.")
    
    # Additional optional parameters
    parser.add_argument("-s", "--font_size", type=int, default=10, help="The font size to use in the output. Default is 10.")
    parser.add_argument("-r", "--line_height_ratio", type=float, default=1.0, help="The ratio of line height to font size. Default is 1.0.")
    parser.add_argument("-l", "--lighten_factor", type=float, default=1.2, help="Factor to lighten the text color relative to the background color. Default is 1.2.")
    
    args = parser.parse_args()

    # Resolve the output path and file type
    output_path, filetype = resolve_output_and_filetype(args.image, args.output, args.filetype)
    
    # Validate input image path
    image_path = Path(args.image)
    if not image_path.exists():
        logging.error(f"Input image file '{args.image}' does not exist.")
        return
    
    # Process the image and generate text and color matrices
    text_matrix, color_matrix = image_to_matrix(
        image=image_path,
        text=args.text,
        width=args.width,
        height=args.height,
        alphabet=args.alphabet
    )
    
    # Save the output in the specified format
    if filetype == "html":
        from .output_html import save_matrix_to_html
        save_matrix_to_html(
            text_matrix=text_matrix,
            color_matrix=color_matrix,
            output_file=output_path,
            font_size=args.font_size,
            line_height_ratio=args.line_height_ratio,
            lighten_factor=args.lighten_factor
        )
    elif filetype == "svg":
        from .output_svg import save_matrix_to_svg
        save_matrix_to_svg(
            text_matrix=text_matrix,
            color_matrix=color_matrix,
            output_file=output_path,
            font_size=args.font_size,
            line_height_ratio=args.line_height_ratio,
            lighten_factor=args.lighten_factor
        )
    elif filetype == "pdf":
        from .output_pdf import save_matrix_to_pdf
        save_matrix_to_pdf(
            text_matrix=text_matrix,
            color_matrix=color_matrix,
            output_file=output_path,
            font_size=args.font_size,
            line_height_ratio=args.line_height_ratio,
            lighten_factor=args.lighten_factor
        )

    logging.info(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()
