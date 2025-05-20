import telebot
from SeaBattle import BattleField
from player import Player
from game import Game

token = "7228333271:AAGAr5I4sJu_5xTZciFkpyMwupWvbZhoSLM"
bot = telebot.TeleBot(token)

currentGameID = 0
players = {}
private_games = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id not in players.keys():
        bot.send_message(message.chat.id, "Привет! Я бот морского боя")
        player = Player(message.chat.id)
        players[message.chat.id] = player
    else:
        bot.send_message(message.chat.id, "Мы уже знакомы!")

@bot.message_handler(commands=['create_game'])
def create_game(message):
    global currentGameID
    if message.chat.id not in players.keys():
        bot.send_message(message.chat.id, "Сначала введите /start")
        return
    player = players[message.chat.id]
    if player.game != None:
        bot.send_message(message.chat.id, "Вы уже состоите в игре!")
        return
    
    game = Game(currentGameID, player)
    player.game = game
    private_games[currentGameID] = game
    bot.send_message(message.chat.id, f"Идентификатор вашей игры: {currentGameID}")

    currentGameID += 1


@bot.message_handler(commands=['connect_game'])
def connect_game(message):
    if message.chat.id not in players.keys():
        bot.send_message(message.chat.id, "Сначала введите /start")
        return
    player = players[message.chat.id]
    if player.game != None:
        bot.send_message(message.chat.id, "Вы уже состоите в игре!")
        return
    msg = bot.send_message(message.chat.id, "Введите идентификатор игры!")
    bot.register_next_step_handler(msg, connect)
    
def connect(message):
    try:
        gameID = int(message.text)
        if gameID not in private_games.keys():
            bot.send_message(message.chat.id, "Игры с таким идентификатором не существует")
            return
        player = players[message.chat.id]
        game = private_games[gameID]
        player.game = game
        game.members.append(player)
        private_games[gameID] = None
        for member in game.members:
            bot.send_message(member.chatID, "Игра началась!")
        game.start_game(bot)
    except :
        bot.send_message(message.chat.id, "Некорректный идентификатор!")

@bot.message_handler(commands=['quit'])
def quit(message):
    if message.chat.id not in players.keys():
        bot.send_message(message.chat.id, "Сначала введите /start")
        return
    player = players[message.chat.id]
    if player.game == None:
        bot.send_message(message.chat.id, "Вы не состоите ни в одной игре!")
        return
    game = player.game
    for member in game.members:
        member.game = None
        bot.send_message(member.chatID, "Игра прервана!")
    game.members.clear()
    if game.gameID in private_games.keys():
        private_games[game.gameID] = None

@bot.message_handler(content_types='text')
def text(message):
    if message.chat.id not in players.keys():
        bot.send_message(message.chat.id, "Сначала введите /start")
        return
    player = players[message.chat.id]
    if player.game == None:
        bot.send_message(message.chat.id, "Сначала войдите в игру: /connect_game")
        return
    game = player.game
    try:
        posX, posY = map(int, message.text.split())
        game.shot(bot, player, posX, posY)
    except:
        bot.send_message(message.chat.id, "Некорректные координаты!")

bot.infinity_polling()
