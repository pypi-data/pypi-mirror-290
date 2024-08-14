# DCEN - Data Concealment and Extraction via Numerical encoding

## Description

**DCEN** is a _utility_ that enables encoding and decoding of data arrays by creating image files containing graphical information without data loss due to compression. DCEN uses [ASCII](https://theasciicode.com.ar/) padding, so make sure you use only ASCII symbols. (No cyrylica) 

## Features

- Encoding text messages into PNG images using grayscale color gradations.
- Decoding text messages from PNG images, restoring the original text.
- Does not require external data or keys; encoding and decoding are based on grayscale values in the image.

## Installation

To install the `dcen` package, use `pip`:

```
pip install dcen
```

## Usage

### Encoding a Message

To encode a message into a PNG image, use the `encode` function:

```
import dcen

# Encoding a message into an image
message = "Hello, World!"
dcen.encode(message, "encoded_image.png")
```

### Decoding a Message

To decode a message from a PNG image, use the `decode` function:

```
import dcen

# Decoding a message from an image
decoded_message = dcen.decode("encoded_image.png")
print(decoded_message)
```

## Functions

### `dcen.encode(text: str, filename: str)`

⬆ Encodes the given `text` into a PNG image and saves it as `filename`.

- **Parameters:**
  - `text` (str): Message to be encoded.
  - `filename` (str): Name of the file where the PNG image will be saved.

- **Returns:**
  - Encoded data as a PNG image.

### `dcen.decode(filename: str) -> str`

⬆ Decodes the message from a PNG image file.

- **Parameters:**
  - `filename` (str): Name of the file from which the message will be decoded.

- **Returns:**
  - Decoded message as a string.

## Requirements

- Python 3.6 or higher
- Pillow (Python Imaging Library)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.