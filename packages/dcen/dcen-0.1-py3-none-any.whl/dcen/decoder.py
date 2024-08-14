from PIL import Image
import base64
def gray_to_char(gray_value):
    return chr(gray_value - 1)
def decode_from_png(filename):
    img = Image.open(filename)
    pixels = img.load()
    width, height = img.size
    encoded_chars = []

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if (r, g, b) == (0, 0, 0):
                continue
            char = gray_to_char(r)
            encoded_chars.append(char)
    encoded_text = ''.join(encoded_chars)
    binary_text = base64.b64decode(encoded_text).decode('ascii')
    decoded_text = binary_to_string(binary_text)
    return decoded_text
def binary_to_string(binary_str):
    binary_values = [binary_str[i:i + 8] for i in range(0, len(binary_str), 8)]
    decoded_str = ''.join(chr(int(bv, 2)) for bv in binary_values)
    return decoded_str