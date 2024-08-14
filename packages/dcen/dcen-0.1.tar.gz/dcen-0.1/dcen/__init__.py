from .encoder import encode_to_png
from .decoder import decode_from_png

def encode(text, filename):
    encode_to_png(text, filename)

def decode(filename):
    return decode_from_png(filename)
