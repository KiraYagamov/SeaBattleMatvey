import telebot
from SeaBattle import BattleField

token = "7228333271:AAGAr5I4sJu_5xTZciFkpyMwupWvbZhoSLM"
bot = telebot.TeleBot(token)

field = BattleField(8)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я бот морского боя")

@bot.message_handler(commands=['generate_field'])
def generate_field(message):
    field.generate_random_field()
    field.print_field()
    bot.send_message(message.chat.id, "Поле создано!")

@bot.message_handler(content_types='text')
def text_handler(message):
    if field is None:
        bot.send_message(message.chat.id, "Поле не создано!")
        return
    try:
        shot_posX, shot_posY = map(int, message.text.split())
        shot_posX -= 1
        shot_posY -= 1
        if not field.check_border(shot_posX) or not field.check_border(shot_posY):
            bot.send_message(message.chat.id, "Вы вышли за границы поля")
            return
        shot_value = field.shot(shot_posX, shot_posY)
        if shot_value == 0:
            bot.send_message(message.chat.id, "Вы не попали!")
        elif shot_value == 1:
            bot.send_message(message.chat.id, "Вы попали!")
        else:
            bot.send_message(message.chat.id, "Вы уже стреляли сюда!")
    except:
        bot.send_message(message.chat.id, "Введите координаты!")

bot.infinity_polling()
