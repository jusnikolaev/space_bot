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
    info_text = "\t Commands: \n /constellation NAME - planet constellation , \n /position NAME - planet position in current moment"
    bot.sendMessage(update.message.chat_id, text = info_text)

#Функция вычисления созвездия
def planet_constellation(planet):
    date = datetime.datetime.now()
    curr_date = date.strftime('%Y/%m/%d')
    planet_constll = PLANETS.get(planet, "Sry...I dont know")
    if isinstance(planet_constll, str):
        return planet_constll
    else:
        return constellation(planet_constll(str(curr_date)))
    
   
#Функция вычисления положения планеты
def planet_position(planet):
    date = datetime.datetime.now()
    curr_date = date.strftime('%Y/%m/%d')
    planet_ctor = PLANETS.get(planet, "Sry...I dont know")
    planet_pos = planet_ctor()
    if isinstance(planet_ctor, str):
        return planet_pos
    else:
        planet_pos.compute(curr_date)
        return planet_pos

def constellation_bot(bot, update, args):
    planet = str(args[0]).lower()
    planet_coord = planet_constellation(planet)
    bot.sendMessage(update.message.chat_id, text = str(planet_coord))

def planet_position_bot(bot, update, args):
    planet = str(args[0]).lower()
    right_ascension = str(planet_position(planet).a_ra)
    declination = str(planet_position(planet).a_dec)
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