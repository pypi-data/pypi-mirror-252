from typing import Callable
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt


def wait_cursor(method: Callable) -> Callable:
    ''' qt wait cursor decorator
     Note:
        The wait cursor will be set for the duration of the method call.
        The method must be a function or a method of a class.

    Use QApplication.processEvents() to update the UI while the wait cursor is active.
    '''

    def wrapper(*args, **kwargs):

        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()

        try:
            r = method(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            QApplication.restoreOverrideCursor()
            QApplication.processEvents()

        return r

    return wrapper
