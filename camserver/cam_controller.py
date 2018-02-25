import io
import time
import picamera
from PIL import Image
import zbar


def readQR(stream):
    pil = Image.open(stream)
    scanner = zbar.ImageScanner()
    pil = pil.convert('L')
    width, height = pil.size
    raw = pil.tobytes()
    # configure the reader
    scanner.parse_config('enable')
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for barcodes
    scanner.scan(image)

    # extract results
    for symbol in image:
        # do something useful with results
        return symbol.data

