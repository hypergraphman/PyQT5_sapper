import random


class Sapper:
    def __init__(self, size_x, size_y):
        self.height_size = size_x
        self.width_size = size_y
        self.shadow_field = []
        self.minefield = []
        self.mines = 0
        self.count_units_close = self.height_size * self.width_size
        self.fill_field()
        self.game = 0

    def get_minefield(self):
        return self.minefield

    def get_game(self):
        return self.game

    def get_mines(self):
        return self.mines

    def get_shadow_field(self):
        return self.shadow_field

    def fill_field(self):
        for i in range(self.height_size):
            new_line_shadow_field = []
            new_line_minefield = []
            for j in range(self.width_size):
                unit = random.choice([1, 0, 0, 0, 0, 0])
                self.mines += unit
                new_line_minefield.append(unit)
                new_line_shadow_field.append('[ ]')
            self.shadow_field.append(new_line_shadow_field)
            self.minefield.append(new_line_minefield)

    def print_field(self):
        print(f'mines = {self.mines}')
        print(end='  ')
        for j in range(self.width_size):
            print(f' {j} ', end='')

        for i in range(self.height_size):
            print(end=f'\n{i} ')
            for j in range(self.width_size):
                print(self.shadow_field[i][j], end='')

        print()

    def open_unit(self, x, y):
        if 0 <= x < self.height_size and 0 <= y < self.width_size and\
                self.shadow_field[x][y] != '[ ]':
            return
        if self.height_size <= x or x < 0 or self.width_size <= y or y < 0:
            return
        if self.minefield[x][y] == 1:
            self.shadow_field[x][y] = '[*]'
            return

        count_units_around = 0
        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:
                if 0 <= i < self.height_size and 0 <= j < self.width_size and\
                        self.minefield[i][j]:
                    count_units_around += 1

        self.shadow_field[x][y] = f' {(" ", count_units_around)[bool(count_units_around)]} '
        self.count_units_close -= 1

        if self.shadow_field[x][y] == '   ':
            for i in [x - 1, x, x + 1]:
                for j in [y - 1, y, y + 1]:
                    self.open_unit(i, j)

    def next_step(self, x, y, cmd):
        if self.game == 0:
            if cmd == 'F' and self.shadow_field[x][y] == '[ ]':
                self.shadow_field[x][y] = '[F]'
                self.mines -= 1
                self.count_units_close -= 1
            elif cmd == 'F' and self.shadow_field[x][y] == '[F]':
                self.shadow_field[x][y] = '[ ]'
                self.mines += 1
                self.count_units_close += 1
            elif cmd == 'O' and self.shadow_field[x][y] != '[F]':
                if self.minefield[x][y]:
                    self.shadow_field[x][y] = '[B]'
                    for i in range(self.height_size):
                        for j in range(self.width_size):
                            if self.shadow_field[i][j] == '[ ]':
                                self.open_unit(i, j)
                    self.game = -1  # Проигрыш
                    return
                else:
                    self.open_unit(x, y)
            if self.count_units_close == 0:
                self.game = 1  # Победа
            else:
                self.game = 0  # Продолжение игры

    def console_game(self):
        while True:
            self.print_field()
            print('Введите координаты, потом одну из комманд "O", "F"')
            x = int(input('x = '))
            y = int(input('y = '))
            cmd = input('cmd = ')
            self.next_step(y, x, cmd)
            if self.game == -1:
                self.print_field()
                print('Ты проиграл')
                break
            elif self.game == 0:
                continue
            else:
                self.print_field()
                print("Ты выиграл")
                break


if __name__ == '__main__':
    sapper = Sapper(5, 7)
    sapper.console_game()
