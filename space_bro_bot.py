from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
from ephem import * 


#Словарь с планетами 
PLANETS = {
    'mercury': Mercury,
    'venus': Venus,
    'mars': Mars,
    'jupiter': Jupiter,
    'saturn': Saturn,
    'uranus': Uranus,
    'neptune': Neptune
    }

#Ответ на текстовое сообщение пользователя
def info(bot, update):
    info_text = """\t Commands: 
 /constellation NAME - planet constellation , 
 /position NAME - planet position in current moment"""
    bot.sendMessage(update.message.chat_id, text=info_text)

#Функция вычисления созвездия
def planet_constellation(planet):
    date = datetime.datetime.now()
    curr_date = date.strftime('%Y/%m/%d')
    #if isinstance(planet_constll, str):
    if planet not in PLANETS:
        return "Sry...I dont know"
    else:
        planet_constll = PLANETS[planet]
        return constellation(planet_constll(str(curr_date)))

#Функция вычисления положения планеты
def planet_position(planet):
    date = datetime.datetime.now()
    curr_date = date.strftime('%Y/%m/%d')
    if planet in PLANETS:
        planet_ctor = PLANETS[planet]
        planet_pos = planet_ctor()
        planet_pos.compute(curr_date)
        return planet_pos
    else:
        return None

def constellation_bot(bot, update, args):
    planet = str(args[0] if args else '').lower()
    planet_coord = planet_constellation(planet)
    bot.sendMessage(update.message.chat_id, text = str(planet_coord))

def planet_position_bot(bot, update, args):
    planet = str(args[0] if args else '').lower()
    planet_pos = planet_position(planet)
    if not planet_pos:
         bot.sendMessage(update.message.chat_id, text = 'Sry... I dont know')
    else:
        right_ascension, declination = str(planet_pos.a_ra), str(planet_pos.a_dec)
        bot.sendMessage(update.message.chat_id, text = declination + ' , ' + right_ascension)
    

#Главная функция 
def main():

    updater = Updater('296338487:AAGV-3gmwtvytQsTSYQd7_WLwTNgqV8D1G8')
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('constellation', constellation_bot, pass_args=True))
    dp.add_handler(CommandHandler('position', planet_position_bot, pass_args=True))
    dp.add_handler(MessageHandler([Filters.text], info))

    updater.start_polling()
    updater.idle()

main()