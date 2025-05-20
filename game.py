from SeaBattle import BattleField
class Game:
    def __init__(self, gameID, initiator):
        self.gameID = gameID
        self.members = [initiator]
        self.step = 0

    def start_game(self, bot=None):
        self.step = 0
        self.fields = []
        for member in self.members:
            field = BattleField()
            field.generate_random_field()
            if bot != None:
                bot.send_message(member.chatID, "Ваше игровое поле:")
                bot.send_message(member.chatID, field.get_string_field())
            self.fields.append(field)
    
    def shot(self, bot, member, posX, posY):
        memberIndex = self.members.index(member)
        if memberIndex != self.step:
            bot.send_message(member.chatID, "Сейчас не Ваш ход!")
            return
        enemy = 1 if self.step == 0 else 0
        enemy_field = self.fields[enemy]
        if not enemy_field.check_border(posX) or not enemy_field.check_border(posY):
            bot.send_message(member.chatID, "Вы вышли за границы поля")
            return
        shot_result = enemy_field.shot(posX, posY)
        if shot_result == 0:
            bot.send_message(member.chatID, "Вы не попали!")
            bot.send_message(self.members[enemy].chatID, f"В вас не попали!")
            self.step = 1 if self.step == 0 else 0
        elif shot_result == 1:
            bot.send_message(member.chatID, "Вы попали!")
            bot.send_message(self.members[enemy].chatID, f"Вас подбили в координатах: {posX}, {posY}")
        else:
            bot.send_message(member.chatID, "Вы уже стреляли сюда!")
