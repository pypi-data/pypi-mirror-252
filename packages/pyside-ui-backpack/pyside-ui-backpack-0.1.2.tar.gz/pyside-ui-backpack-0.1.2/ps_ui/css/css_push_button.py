from PySide2.QtWidgets import QPushButton, QMainWindow, QGraphicsDropShadowEffect
from PySide2.QtGui import QColor

from ps_ui.css.colors import Colors


def style_push_button(QtWindow: QMainWindow, button: QPushButton,
                      color: Colors = Colors.GREY, shadow: bool = True):
    ''' apply style to a QPushButton widget

        Colors are:
            red for red/white
            orange for orange/black
            disabled for gray/gray
            blue for blue/white
            green for green/black
            lightgrey for lightgrey/white
            black for dark-gray/white
            gray for gray/white (default)

    shadow is a boolean to enable/disable shadow effect

    Args:
        QtWindow (QMainWindow): parent QMainWindow
        button (QPushButton): QPushButton widget
        color (Colors, optional): color theme. Defaults to Colors.GRAY.
        shadow (bool, optional): enable/disable shadow effect. Defaults to True.

    '''

    css_basic_btn = """
        color:{};
        background:{};
        font-size:12px;
        font-family:Segoe UI;
        """.format(color.value.foreground_color, color.value.background_color)

    button.setStyleSheet(css_basic_btn)

    if shadow:
        shadow = QGraphicsDropShadowEffect(QtWindow)
        shadow.setBlurRadius(6)
        shadow.setOffset(3)
        shadow.setColor(QColor(0, 0, 0, 60))
        button.setGraphicsEffect(shadow)
