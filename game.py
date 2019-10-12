import sys
import engine

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QLCDNumber, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QObject, QSize
from PyQt5.QtGui import QIcon


class Game(QWidget):
    def __init__(self, name_game, width_field, height_field, main_window):
        super().__init__()
        self.name_game = name_game
        self.width_field = width_field
        self.height_field = height_field
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        # Сделал так, т.к. некогда было разибраться с QtDesinger и импортом форм
        # Математика рулит подумал я, ну и немного прогадал, т.к. порядком надоело
        # формы настраивать запуская каждый раз приложение. А с настройкой шрифтов
        # цветов и т.п. вообще все плохо

        # Начало игрового поля
        self.start_field_x = 10
        self.start_field_y = 40

        # Ширина игрового поля в клетках
        # width_field = 10
        # height_field = 10

        # Ширина клетки
        self.cell_size = 20

        # self.setGeometry(300, 300, cell_size * self.width_field + 20,
        #                  cell_size * self.height_field + 50)
        self.setWindowTitle(self.name_game)
        self.setFixedSize(self.cell_size * self.width_field + 20,
                          self.cell_size * self.height_field + 50)
        self.LCD_count = QLCDNumber(self)
        self.LCD_count.move(10, 10)
        label = QLabel(self)
        label.setText("Бомб")
        label.move(80, 15)
        self.btns = []

        for x in range(self.width_field):
            for y in range(self.height_field):
                btn = QPushButton('', self)
                btn.move(self.start_field_x + x * self.cell_size,
                         self.start_field_y + y * self.cell_size)
                btn.resize(self.cell_size, self.cell_size)
                btn.installEventFilter(self)
                btn.setObjectName(f'{x} {y}')
                self.btns.append(btn)
        self.is_show_dialog = True

        self.sapper = engine.Sapper(self.height_field, self.width_field)

        self.LCD_count.display(self.sapper.get_mines())

        self.btn_restart = QPushButton('Начать заново', self)
        self.btn_restart.resize(100, 25)
        self.btn_restart.move(110, 10)

        self.btn_restart.clicked.connect(self.restart_game)

        self.mb_win = QMessageBox()
        self.mb_win.setIcon(QMessageBox.Information)
        self.mb_win.setWindowTitle('Ты выиграл!')
        self.mb_win.setText('Ты выиграл, какой же ты молодец =)')
        self.mb_win.setStandardButtons(QMessageBox.Cancel)

        self.mb_lose = QMessageBox()
        self.mb_lose.setIcon(QMessageBox.Warning)
        self.mb_lose.setWindowTitle('Ты проиграл!')
        self.mb_lose.setText('Ты проиграл, в следующий раз будь внимательнее ;)')
        self.mb_lose.setStandardButtons(QMessageBox.Ok)

    def restart_game(self):
        for btn in self.btns:
            btn.setIcon(QIcon(None))
            btn.setEnabled(True)
            btn.setText('')
        self.is_show_dialog = True

        self.sapper = engine.Sapper(self.height_field, self.width_field)

        self.LCD_count.display(self.sapper.get_mines())

    def closeEvent(self, QCloseEvent):
        # self.main_window.setEnabled(True)
        self.main_window.show()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and obj.isEnabled():
            if event.button() == Qt.LeftButton and not obj.text():
                x, y = map(int, obj.objectName().split())
                self.sapper.next_step(y, x, 'O')
            elif event.button() == Qt.RightButton:
                x, y = map(int, obj.objectName().split())
                self.sapper.next_step(y, x, 'F')

            # Далее происходить по сути перерисовка всего игрового поля
            # это тормозит игру, нужно менять только измененные клетки, а не все подряд
            # нужно подумать над этим!!!
            # пришла такая идея:
            # хранить бутоны не в списке а в двумерном списке или в словаре, чтобы
            # синхронизировать изменения в игре, тогда и в движке нужно доработать этот
            # функционал, сделаю если будет время.

            shadow_field = self.sapper.get_shadow_field()
            for btn in self.btns:
                i, j = map(int, btn.objectName().split())
                if shadow_field[j][i] == '   ':
                    btn.setEnabled(False)
                elif shadow_field[j][i] == '[*]':
                    btn.setIcon(QIcon('m.png'))
                    btn.setIconSize(QSize(14, 14))
                elif shadow_field[j][i] == '[B]':
                    btn.setIcon(QIcon('b.png'))
                    btn.setIconSize(QSize(14, 14))
                elif shadow_field[j][i] == '[F]':
                    btn.setIcon(QIcon('f.png'))
                    btn.setIconSize(QSize(14, 14))
                elif shadow_field[j][i] == '[ ]':
                    btn.setText('')
                    btn.setIcon(QIcon(None))
                elif shadow_field[j][i] != '[ ]':
                    btn.setText(shadow_field[j][i])

            minefield = self.sapper.get_minefield()
            if self.sapper.get_game() == -1 and self.is_show_dialog:
                for btn in self.btns:
                    i, j = map(int, btn.objectName().split())
                    if shadow_field[j][i] == '[F]' and minefield[j][i] == 0:
                        btn.setIcon(QIcon('e.png'))
                        btn.setIconSize(QSize(14, 14))

                self.mb_lose.show()
                self.is_show_dialog = False
            elif self.sapper.get_game() == 1 and self.is_show_dialog:
                self.mb_win.show()
                self.is_show_dialog = False

            self.LCD_count.display(self.sapper.get_mines())

        return QObject.event(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game('Изи-бризи', 10, 15)
    ex.show()
    sys.exit(app.exec())