

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: tuple) -> str:
    """Convert an RGB tuple to a hex color string."""
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

def luminance(rgb: tuple) -> float:
    """Calculate the luminance of an RGB color."""
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def rgb_to_lab(input_color):
    """
    Convert RGB to CIELAB color space.

    :param input_color: A tuple or list representing an RGB color (R, G, B).
    :return: A list representing the corresponding LAB color [L, a, b].

    Based on @manojpandey/rgb2lab.py gist. Link:
    https://gist.github.com/manojpandey/f5ece715132c572c80421febebaf66ae
    """
    # Normalize the RGB values to the [0, 1] range
    rgb = [0, 0, 0]
    for i, value in enumerate(input_color):
        value = value / 255.0

        # Apply the gamma correction
        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        rgb[i] = value * 100  # Scale up for the XYZ conversion

    # Convert RGB to XYZ using the D65 illuminant
    x = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
    y = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
    z = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505

    # Normalize for the reference white point
    x /= 95.047  # ref_x =  95.047
    y /= 100.000 # ref_y = 100.000
    z /= 108.883 # ref_z = 108.883

    # Convert XYZ to LAB
    xyz = [x, y, z]
    for i, value in enumerate(xyz):
        if value > 0.008856:
            xyz[i] = value ** (1/3)
        else:
            xyz[i] = (7.787 * value) + (16 / 116)

    l = (116 * xyz[1]) - 16
    a = 500 * (xyz[0] - xyz[1])
    b = 200 * (xyz[1] - xyz[2])

    return [round(l, 4), round(a, 4), round(b, 4)]

def lab_to_rgb(lab):
    """
    Convert LAB color space to RGB color space.

    :param lab: A tuple representing the LAB color (L, a, b).
    :return: A tuple representing the corresponding RGB color (R, G, B) on a 0-255 scale.
    """
    l, a, b = lab

    # Convert LAB to XYZ
    y = (l + 16) / 116.0
    x = a / 500.0 + y
    z = y - b / 200.0

    # Apply the inverse transformation
    def lab_to_xyz(t):
        return t ** 3 if t > 0.2068966 else (t - 16 / 116.0) / 7.787

    x = lab_to_xyz(x) * 0.95047
    y = lab_to_xyz(y)
    z = lab_to_xyz(z) * 1.08883

    # Convert XYZ to linear RGB
    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    # Apply gamma correction and clamp to 0-1
    def gamma_correct(c):
        c = max(0, min(c, 1))
        return 1.055 * (c ** (1 / 2.4)) - 0.055 if c > 0.0031308 else 12.92 * c

    r = gamma_correct(r)
    g = gamma_correct(g)
    b = gamma_correct(b)

    # Convert to 0-255 range
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))




def adjust_color_brightness(rgb: tuple, factor: float) -> tuple:
    """
    Adjust the brightness of an RGB color by converting to CIELAB, modifying the luminance, and converting back to RGB.
    
    :param rgb: The original RGB color as a tuple.
    :param factor: Factor to adjust brightness by (greater than 1 to lighten, between 0 and 1 to darken).
    :return: A new RGB tuple with adjusted brightness.
    """    
    # Convert RGB to LAB
    lab = rgb_to_lab(rgb)
    
    # Adjust the L (luminance) channel
    lab[0] = lab[0] * factor
    lab[0] = max(0, min(lab[0], 100))  # Ensure luminance is within [0, 100]

    return lab_to_rgb(lab)

def get_lighter_text_color(hex_color: str, lighten_factor: float = 1.2) -> str:
    """
    Lighten the background color to use as the text color.
    
    :param hex_color: The hex color string of the background.
    :param lighten_factor: Factor to lighten the text color.
    :return: A hex color string for the adjusted text color.
    """
    rgb = hex_to_rgb(hex_color)
    adjusted_rgb = adjust_color_brightness(rgb, lighten_factor)
    return rgb_to_hex(adjusted_rgb)
