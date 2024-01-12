"""
Module that stores values of predefiened colors.
"""

from typing import TypeAlias

Color: TypeAlias = tuple[int, int, int]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)


def invert_color(color: Color) -> Color:
    """
    Invert a color using the formula
    ``new_color = (255, 255, 255) - old_color``.

    :param color: color to invert
    :type color: Color
    :return: inverted color
    :rtype: tuple
    """
    return (255 - color[0], 255 - color[1], 255 - color[2])

def darken_color(color: Color, intensity: float) -> Color:
    """
    Darken a RGB color rescaling each component proportionally.

    :param color: original color
    :type color: Color
    :param intensity: intensity to apply, 1 maintain the same color, 0 returns black
    :type intensity: float
    :return: darkened color
    :rtype: Color
    """

    return (int(color[0] * intensity),
            int(color[1] * intensity),
            int(color[2] * intensity))
