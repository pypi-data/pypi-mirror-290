from PIL import Image
import base64
def char_to_gray(char):
    value = ord(char) % 254 + 1
    return (value, value, value)
def string_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)
def encode_to_png(text, filename):
    binary_text = string_to_binary(text)
    encoded = base64.b64encode(binary_text.encode('ascii')).decode('ascii')
    length = len(encoded)
    size = int(length ** 0.5) + (1 if (length ** 0.5) % 1 != 0 else 0)
    img = Image.new('RGB', (size, size), (0, 0, 0))
    pixels = img.load()
    for i, char in enumerate(encoded):
        x = i % size
        y = i // size
        pixels[x, y] = char_to_gray(char)
    img.save(filename)
