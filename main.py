import sys
import game

from PyQt5.QtWidgets import QApplication,  QPushButton
from PyQt5.QtWidgets import QMainWindow


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Сапёр')
        self.setFixedSize(300, 300)

        self.btn = QPushButton('Изи-бризи', self)
        self.btn.resize(100, 50)
        self.btn.move(100, 20)

        self.btn.clicked.connect(self.open_easy_game)

        self.btn = QPushButton('Намана', self)
        self.btn.resize(100, 50)
        self.btn.move(100, 90)

        self.btn.clicked.connect(self.open_medium_game)

        self.btn = QPushButton('Сложна', self)
        self.btn.resize(100, 50)
        self.btn.move(100, 160)

        self.btn.clicked.connect(self.open_hard_game)

        self.btn = QPushButton('О программе', self)
        self.btn.resize(100, 50)
        self.btn.move(100, 230)

        self.btn.clicked.connect(self.open_about_game)

    def open_easy_game(self):
        self.game = game.Game('Изи-бризи', 10, 10, self)
        self.game.show()
        # self.setEnabled(False)
        self.hide()

    def open_medium_game(self):
        self.game = game.Game('Намана', 15, 10, self)
        self.game.show()
        self.hide()

    def open_hard_game(self):
        self.game = game.Game('Сложна', 20, 10, self)
        self.game.show()
        self.hide()

    def open_about_game(self):
        self.game = game.Game('О программе', 90, 40, self)
        self.game.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainForm()
    ex.show()
    sys.exit(app.exec())