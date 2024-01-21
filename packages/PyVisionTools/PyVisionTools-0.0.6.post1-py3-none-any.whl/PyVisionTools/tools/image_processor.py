import io
import urllib.request
import struct
from typing import Tuple

class ImageLoader:
    def open_image_from_url(self, image_url):
        try:
            with urllib.request.urlopen(image_url) as response:
                img_data = response.read()
            return img_data
        except Exception as e:
            print(f"Error opening image from URL: {e}")
            return None

class ImageProcessor:
    def __init__(self):
        pass

    @classmethod
    def resize_image(cls, img_data, new_width, new_height) -> Tuple[int, int, bytes]:
        try:
            width, height = struct.unpack("<LL", img_data[:8])

            resized_pixels = cls._resize_pixels(width, height, img_data[8:], new_width, new_height)

            resized_data = struct.pack("<LL", new_width, new_height) + resized_pixels
            return new_width, new_height, resized_data
        except Exception as e:
            print(f"Error resizing image: {e}")
            return None

    @classmethod
    def _resize_pixels(cls, width, height, pixels, new_width, new_height):
        resized_pixels = bytearray()

        for y in range(new_height):
            for x in range(new_width):
                source_x = int(x / new_width * width)
                source_y = int(y / new_height * height)

                pixel_index = (source_y * width + source_x) * 3
                resized_pixels.extend(pixels[pixel_index:pixel_index + 3])

        return resized_pixels

class ImageSaver:
    def save_image(self, img_data, filename):
        try:
            with open(filename, 'wb') as file:
                file.write(img_data)
            print(f"Image saved as {filename}")
        except Exception as e:
            print(f"Error saving image: {e}")
