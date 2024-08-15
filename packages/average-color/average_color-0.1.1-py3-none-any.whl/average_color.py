from typing import Union
import sys
from pathlib import Path
from PIL import Image


def get_average_color(filepath: Union[str, Path]) -> tuple[int, int, int]:
    with Image.open(filepath) as img:
        num_pixels = img.width * img.height
        red = sum(img.getdata(0))
        green = sum(img.getdata(1))
        blue = sum(img.getdata(2))
    avg_red = red // num_pixels
    avg_green = green // num_pixels
    avg_blue = blue // num_pixels

    return (avg_red, avg_green, avg_blue)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/image")
        return 1

    filepath = sys.argv[1]
    color = get_average_color(filepath)
    print(rgb_to_hex(color))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
