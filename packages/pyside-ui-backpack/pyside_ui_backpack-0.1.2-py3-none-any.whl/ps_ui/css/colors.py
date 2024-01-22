from enum import Enum
from collections import namedtuple

Color = namedtuple('Color', ['foreground_color', 'background_color'])

WHITE_BACKGROUND = 'rgb(240, 240, 240)'
DARK_BACKGROUND = 'rgb(50, 50, 50)'


class Colors(Enum):
    '''  buttons color themes '''
    DISABLED = Color('rgb(80, 80, 80)', 'rgb(180, 180, 180)')

    BLUE = Color('rgb(46, 134, 193)', WHITE_BACKGROUND)
    RED = Color('rgb(160, 20, 20)', WHITE_BACKGROUND)
    ORANGE = Color('rgb(236, 183, 41)', WHITE_BACKGROUND)
    GREEN = Color('rgb(40, 205, 50)', WHITE_BACKGROUND)
    YELLOW = Color('rgb(200, 200, 0)', WHITE_BACKGROUND)
    GREY = Color('rgb(80, 80, 80)', WHITE_BACKGROUND)
    WHITE = Color('rgb(30, 30, 30)', WHITE_BACKGROUND)

    # dark theme
    DARK_BLUE = Color('rgb(46, 134, 193)', DARK_BACKGROUND)
    DARK_RED = Color('rgb(160, 20, 20)', DARK_BACKGROUND)
    DARK_ORANGE = Color('rgb(236, 183, 41)', DARK_BACKGROUND)
    DARK_GREEN = Color('rgb(40, 205, 50)', DARK_BACKGROUND)
    DARK_YELLOW = Color('rgb(240, 240, 0)', DARK_BACKGROUND)
    DARK_GREY = Color('rgb(80, 80, 80)', DARK_BACKGROUND)
    DARK_WHITE = Color('rgb(240, 240, 240)', DARK_BACKGROUND)


if __name__ == '__main__':
    print(f'Value for {Colors.BLUE} is '
          f'foreground_color {Colors.BLUE.value.foreground_color} and '
          f'background_color {Colors.BLUE.value.background_color}'
          )
