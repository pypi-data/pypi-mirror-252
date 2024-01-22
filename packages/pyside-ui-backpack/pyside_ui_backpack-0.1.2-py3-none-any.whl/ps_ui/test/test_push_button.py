import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow

from ps_ui.css.colors import Colors
from ps_ui.widgets.push_button import PushButton


if __name__ == '__main__':
    # create a qt application
    app = QApplication(sys.argv)

    # create a main window
    main_window = QMainWindow()

    # set the size of the main window
    main_window.setMinimumSize(400, 400)

    main_window.show()

    # create a push button for every color in Colors
    for index, color in enumerate(Colors):
        push_button = PushButton(
            main_window, f'push_button {index}', color.name, (100, 30), color, True)
        column = index % 2
        row = index // 2
        push_button.move(20 + (column * 120), 20 + (row * 40))
        push_button.show()

    # start the event loop
    sys.exit(app.exec_())
