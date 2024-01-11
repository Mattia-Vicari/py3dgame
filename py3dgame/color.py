"""
Module that implements the Color class.
"""

from dataclasses import dataclass

@dataclass
class Color:
    """
    Class containing RGB triplets as `tuple` with value between 0 and 255.
    """

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    purple = (255, 0, 255)
    cyan = (0, 255, 255)


def invert_color(color: Color) -> tuple:
    return (255 - color[0], 255 - color[1], 255 - color[2])
