import sys

from hrchacha.exceptions.exception import HRChachaException
from hrchacha.ui.main_window import MainWindowUI

if __name__ == "__main__":
    try:
        app = MainWindowUI()
        app.run()
    except Exception as e:
        raise HRChachaException(e, sys)