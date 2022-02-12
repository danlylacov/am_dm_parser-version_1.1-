# -*- coding: utf8 -*-

# заход на сервер: ssh -i "C:\Users\Даниил\Desktop\amazonserver.pem" ubuntu@18.184.178.208
#  scp -i C:\Users\Даниил\Desktop\amazonserver.pem -r C:\Users\Даниил\PycharmProjects\am_dm_parser @184.178.208: /home/ubuntu

import telebot
from telebot import types
import sqlite3
from main import get_song, get_singer, get_accords
from qwer import accords_
import os


token = '5159594918:AAGpVlavozfBPkTfqzNqvWwpoYTZNd_CFYE'
bot = telebot.TeleBot(token)

db = sqlite3.connect('am_dm.sqlite', check_same_thread=False)
cur = db.cursor()


def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
        print('11')




@bot.message_handler(commands=['start'])
def start_message(message):
    text = cur.execute('SELECT id FROM users')
    users_ids = []
    for el in text:
        users_ids.append(str(el[0]))

    if str(message.chat.id) not in users_ids:
        cur.execute('insert into USERS (id, user_name) values (?,?)', (message.chat.id, message.chat.username, ))
        db.commit()
    else:
        print('ercer')
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Поиск по песне', 'Поиск по исполнителю')
    keyboard.add('О боте, поддержка')
    bot.send_message(message.chat.id, 'ПРИВЕТ, '+message.chat.first_name+'!\nЯ бот по поиску аккордов, табулатур для песен!\nИнстукция по использованию:\n\n1) выберете, как вы хотите начать поиск:\n         по исполнителю\n         по песне\n\n2) Нажмите на соответствующую кнопку\n\n3) Напишите исполнителя/название песни\n\n 4) Подождите пока запрос обрабатывается(примерное время ожидания 15 сек)\n\n\n\n\nПо воросам сотрудничества:\nEmail: danlylacov@yandex.ru\ntel:+7-952-098-71-30(telegram, whats app)', reply_markup=keyboard)

@bot.message_handler(commands=['dan74244678'])
def admin(message):
    users = cur.execute('SELECT id from users')
    q = 0
    for el in users:
        q +=1
    bot.send_message(message.chat.id, 'В боте '+str(q)+' пользователей!')



@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'поиск по песне':
        bot.send_message(message.chat.id, 'Напишите название песни:')
        bot.register_next_step_handler(message, song)
    if message.text.lower() == 'поиск по исполнителю':
        bot.send_message(message.chat.id, 'Напишите исполнителя:')
        bot.register_next_step_handler(message, singer)
    if message.text.lower() == 'о боте, поддержка':
        bot.send_message(message.chat.id, 'Я бот по поиску аккордов, табулатур для песен!\nИнстукция по использованию:\n\n1) выберете, как вы хотите начать поиск:\n         по исполнителю\n         по песне\n\n2) Нажмите на соответствующую кнопку\n\n3) Напишите исполнителя/название песни\n\n 4) Подождите пока запрос обрабатывается(примерное время ожидания 15 сек)\n\n\n\n\nПо воросам сотрудничества:\nEmail: danlylacov@yandex.ru\ntel:+7-952-098-71-30(telegram, whats app)')


def song(message):
    try:
        bot.send_message(message.chat.id, 'Запрос принят в обработку!\nПодбираю аккорды... ')
        print(message.text.lower())
        otv, acr = get_song(message.text.lower())
        acr = list(acr)
        keyboard = types.InlineKeyboardMarkup()
        for i in range(len(acr)):
            key_yes = types.InlineKeyboardButton(text=str(acr[i]), callback_data=str(acr[i])[:15])
            keyboard.row(key_yes)
        bot.send_message(message.chat.id, otv+'\n\n\n\nПри нажатии на аккорд я вышлю вам его аппликатуру:', reply_markup=keyboard)
    except:
        bot.send_message(message.chat.id,
                         "Извините по вашему запросу ничего не найдено\nПроверьте правильность написания названия песни!")

def singer(message):
    try:
        bot.send_message(message.chat.id, 'Запрос принят в обработку!\nИщу исполнителя...\n(примерное время ожидания 15 сек)')
        songs = get_singer(message.text.lower())
        keyboard = types.InlineKeyboardMarkup()
        print(songs)
        for i in range(20):
            key_yes = types.InlineKeyboardButton(text=str(songs[i]), callback_data=str(songs[i])[:20]+' ' +str(message.text.lower()))
            keyboard.add(key_yes)
        bot.send_message(
            message.chat.id, 'Вот песни: ', reply_markup=keyboard)
    except:
        bot.send_message(message.chat.id, "Извините по вашему запросу ничего не найдено\nПроверьте правильность написания исполнителя!")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
        acr = []
        for i in range(len(accords_)):
            q = accords_[i].split()[0]
            acr.append(q)
        if call.data in acr:
            for i in range(len(accords_)):
                if accords_[i].split()[0] == call.data:
                    print(accords_[i].split()[-1].split(',')[0])
                    print('call.data:'+ call.data)
                    a = cur.execute('select photo from acords where name = ?', (call.data,))
                    for el in a:
                        os.path.join('3.jpg')
                        write_to_file(el[0], '3.jpg')
                        print(el[0])

            bot.send_photo(call.message.chat.id, open('3.jpg','rb'))

        else:
            bot.send_message(call.message.chat.id, 'Запрос принят в обработку!\nПодбираю аккорды...\n(примерное время ожидания 15 сек)')
            otv, acr = get_song(call.data)
            acr = list(acr)
            keyboard = types.InlineKeyboardMarkup()
            for i in range(len(acr)):
                key_yes = types.InlineKeyboardButton(text=str(acr[i]), callback_data=str(acr[i])[:15])
                keyboard.row(key_yes)
            bot.send_message(call.message.chat.id, otv+'\n\n\n\nПри нажатии на аккорд я вышлю вам его аппликатуру:', reply_markup=keyboard)







bot.polling()