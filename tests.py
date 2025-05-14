from SeaBattle import BattleField

ship_size = 3
field = BattleField(8)
# field.add_ship(ship_size=6, posX=1, posY=0, angle=0)
field.generate_random_field()
field.print_field()
field.play()
