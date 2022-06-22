from random import randrange

# создаем класс для корабля
class Ship:
    def __init__(self, decks):
        self.decks = int(decks)  # число палуб
        self.placement = []

    def hit(self, row, col):
        item = [row, col]
        self.placement.remove(item)
        if len(self.placement) == 0:
            print("Убил")
        else:
            print("Ранил...")
        # print(self.placement)
#
# # создаем класс доски на которую размещаются корабли
class Board:
    board = []
    def __init__(self):
        self.board = [[" ", "|", 1, "|", 2, "|", 3, "|", 4, "|", 5, "|", 6, "|"],
               [1, "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|"],
               [2, "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|"],
               [3, "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|"],
               [4, "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|"],
               [5, "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|"],
               [6, "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|", "0", "|"]]

    def print_board(self, whose_board):
        print(whose_board.upper() + " BOARD")
        for row in self.board:
            local_row = row.copy()
            for item in row:
                if str(item)[0] == "<":
                    local_row[local_row.index(item)] = "■"
            print(*local_row)
        l = "-"
        print(l*30)

    def place_ship(self, ship, direction, row, col):
        decks = ship.decks
        init_row = row
        init_col = col
        # Сначала нужно проверить, можно ли разместить на доске корабль
        for i in range(decks):
            row = init_row
            col = init_col
            if direction == "H":
                col = init_col + i
            else:
                row = init_row + i
            if col < 7 and row < 7 and self.board[row][col*2] == "0" and \
                    self.board[max(row-1, 1)][max(col-1, 1) * 2] == "0" and \
                    self.board[max(row-1, 1)][col * 2] == "0" and \
                    self.board[max(row-1, 1)][min(col+1, 6) * 2] == "0" and \
                    self.board[row][max(col-1, 1) * 2] == "0" and \
                    self.board[row][min(col+1, 6) * 2] == "0" and \
                    self.board[min(row+1, 6)][max(col-1, 1) * 2] == "0" and \
                    self.board[min(row+1, 6)][col * 2] == "0" and \
                    self.board[min(row+1, 6)][min(col+1, 6) * 2] == "0":

                # print("Можно разместить палубу в точку " + str(row) + ", " + str(col))
                pass
            else:
                # print("Невозможно разместить палубу в точку " + str(row) + ", " + str(col))
                return 0

        # размещаем корабль
        for i in range(decks):
            row = init_row
            col = init_col
            if direction == "H":
                col = init_col + i
            else:
                row = init_row + i
            # self.board[row][col*2] = "■"
            self.board[row][col*2] = ship
            # Сообщим кораблю его координаты палубы
            ship.placement.append([row, col])

        # print(ship.placement)
        return 1

    def auto_place_ship(self, ship):
        res = 0
        while res < 1000:
            i = randrange(2)
            if i == 0:
                direction = "V"
            else:
                direction = "H"
            row = randrange(6) + 1
            col = randrange(6) + 1
            if self.place_ship(ship, direction, row, col) == 1:
                return 1
            else:
                res += 1

        print("Не удалось разместить корабль на доску")
        res = 1/0

    def auto_place_ships(self, ships):
        for ship in ships:
            self.auto_place_ship(ship)
        self.ships = ships

    def manual_place_ship(self, ship):
        decks = ship.decks
        while True:
            if decks == 1:
                direction = "V"
                row = input("Выберите номер ряда 1-палубного корабля (1-6):")
                col = input("Выберите номер столбца 1-палубного корабля (1-6):")
            else:
                direction = input(f"Выберите направление {decks}-палубного корабля (V/H):").upper()
                row = input(f"Выберите номер ряда для левой верхней палубы {decks}-палубного корабля (1-6):")
                col = input(f"Выберите номер столбца для левой верхней палубы {decks}-палубного корабля (1-6):")

            if self.place_ship(ship, direction, int(row), int(col)) == 0:
                print("Не удалось разместить корабль на доску")
            else:
                self.print_board('Gamer')
                return 1

    def manual_place_ships(self, ships):
        for ship in ships:
            self.manual_place_ship(ship)
        self.ships = ships

    def hit(self, row, col):
        if str(self.board[row][col*2]) == "0":
            self.board[row][col * 2] = "T"
            return False
        elif str(self.board[row][col*2]) == "X" or str(self.board[row][col*2]) == "T":
            # Для дублированных ходов
            return False
        else:
            self.board[row][col * 2].hit(row, col)
            if len(self.board[row][col * 2].placement) == 0:
                # Нужно удалить корабль
                self.ships.remove(self.board[row][col * 2])
            self.board[row][col * 2] = "X"
            return True

########################## Расстановка поля боя
# создаем 2 игровых поля
print("Sea fight")
gamer_board = Board()
computer_board = Board()

# Создадим корабли ИИ
computer_ships = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]
# Разместим корабли ИИ
computer_board.auto_place_ships(computer_ships)

computer_board.print_board('Computer')

gamer_board.print_board('Gamer')

# Создадим корабли игрока
gamer_ships = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]
# Разместим корабли игрока
# gamer_board.auto_place_ships(gamer_ships)
gamer_board.manual_place_ships(gamer_ships)

gamer_board.print_board('Gamer')
computer_board.print_board('Computer')

######################### GAME ########################
gamer_step = True
while True:
    if gamer_step:
        print("Ход игрока...")
        hit_row = int(input("Выберите номер ряда для удара (1-6):"))
        hit_col = int(input("Выберите номер столбца для удара (1-6):"))
        is_hit = computer_board.hit(hit_row, hit_col)
    else:
        print("Ход компьютера...")
        hit_row = randrange(6) + 1
        hit_col = randrange(6) + 1
        is_hit = gamer_board.hit(hit_row, hit_col)

    print(f"Ударили по полю {hit_row}, {hit_col}")
    if is_hit:
        print("Попадание!!!")
        if gamer_step and len(computer_ships) == 0:
            print("Победил игрок!!!")
            break
        elif not gamer_step and len(gamer_ships) == 0:
            print("Победил компьютер!!!")
            break
    else:
        print("Мимо, переход хода :(")
        gamer_step = not gamer_step
    print("#"*30)
    gamer_board.print_board('Gamer')
    computer_board.print_board('Computer')
