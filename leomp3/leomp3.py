from PyQt5.QtWidgets import QApplication
from leomp3.gui import Music_Player_GUI
import sys


def main():
    App = QApplication(sys.argv)
    window = Music_Player_GUI()

    sys.exit(App.exec())


if __name__ == '__main__':
    main()
