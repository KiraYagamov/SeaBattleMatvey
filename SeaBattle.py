from random import randint

class BattleField:
    field = []

    def __init__(self, size: int = 10):
        for _ in range(size):
            self.field.append([0] * size)
        self.positions_lost = 0

    def clear_field(self):
        self.positions_lost = 0
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                self.field[y][x] = 0
    
    def print_field(self):
        for i in range(len(self.field)):
            print(self.field[i])

    def generate_random_field(self, recursion_count: int = 0):
        if recursion_count > len(self.field)**2:
            print("Не удалось создать поле")
            return
        sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for size in sizes:
            if self.add_ship(size) != 0:
                self.clear_field()
                self.generate_random_field(recursion_count+1)
                return
    
    def add_ship(self, ship_size: int, recursion_count: int = 0, posX: int = -1, posY: int = -1, angle: int = -1) -> None:
        # Проверка лимита рекурсии
        if recursion_count > len(self.field)**2 or recursion_count > 0 and (posX != -1 or posY != -1 or angle != -1):
            print("Не удалось создать корабль")
            return 1
        
        # Установка координат для спавна корабля
        if posX == -1 and posY == -1 or \
                not (0 <= posX <= len(self.field) - ship_size) or not (0 <= posY <= len(self.field) - ship_size):
            ship_posX = randint(0, len(self.field) - ship_size)
            ship_posY = randint(0, len(self.field) - ship_size)
        else:
            ship_posX = posX
            ship_posY = posY

        # Установка поворота корабля
        if angle == -1 or not (0 <= angle <= 1):
            vertical = randint(0, 1)
        else:
            vertical = angle

        # Получение координат, в которые должен попасть корабль
        if vertical == 0:
            ship_place = []
            ship_place_upper = self.field[max(ship_posY-1, 0)][ship_posX-1:ship_posX + ship_size+1]
            ship_place_lower = self.field[min(ship_posY+1, len(self.field)-1)][ship_posX-1:ship_posX + ship_size+1]
            ship_place.extend(ship_place_upper)
            ship_place.extend(self.field[ship_posY][ship_posX-1:ship_posX + ship_size+1])
            ship_place.extend(ship_place_lower)
        else:
            ship_place = [self.field[max(min(ship_posY + i, len(self.field)-1), 0)][max(min(ship_posX + j, len(self.field)-1), 0)] for i in range(-1, ship_size+1) for j in range(-1, 2)]

        # Проверка занятости этих координат
        if 1 in ship_place:
            # Если это место занято, пробуем сгенерировать еще раз, но в другом месте
            return self.add_ship(ship_size, recursion_count + 1, posX, posY, angle)
        
        # Добавляем к оставшимся позициям размер корабля
        self.positions_lost += ship_size
        
        # Если у корабля поворот горизонтальный (не вертикальный), то заполняем единицами горизонтально (по оси Х)
        if vertical == 0:
            for i in range(ship_size):
                self.field[ship_posY][ship_posX + i] = 1
        # Если же у корабля поворот вертикальный, то заполняем единицами вертикально (по оси Y)
        else:
            for i in range(ship_size):
                self.field[ship_posY + i][ship_posX] = 1
        return 0
    
    def shot(self, posX: int, posY: int) -> None:
        if self.field[posY][posX] == 0:
            print("Вы не попали!")
            self.field[posY][posX] = 2
            return 0
        elif self.field[posY][posX] == 1:
            print("Вы попали!")
            self.field[posY][posX] = 2
            self.positions_lost -= 1
            return 1
        else:
            print("Вы уже стреляли сюда!")
            self.field[posY][posX] = 2
            return 2
        
    
    def check_border(self, shot_pos: int) -> bool:
        return 0 <= shot_pos < len(self.field)
    
    def play(self) -> None:
        while self.positions_lost > 0:
            shot_posX, shot_posY = map(int, input("Введите координаты: ").split())
            shot_posX -= 1
            shot_posY -= 1
            if not self.check_border(shot_posX) or not self.check_border(shot_posY):
                print("Вы вышли за границы поля")
                continue
            self.shot(shot_posX, shot_posY)
        print("Игра завершена!")
