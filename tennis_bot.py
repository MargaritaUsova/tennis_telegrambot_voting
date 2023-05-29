import telebot
from telebot import types
import os
from telegram.ext import Updater, CommandHandler

class Ren_bot:
    def __init__(self, url):
        self.bot = telebot.TeleBot(url)
        with open('names.txt', 'r') as f:
            self.nums = f.read().splitlines()
        directory = 'bot_images'
        self.images = []
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                self.images.append(f)
        self.i = 0
        self.flg = False
        self.flg_vote_end = False
        with open('users.txt', 'r') as f:
            self.us = f.read().split()
        f.close()


    def start(self):
# создание кнопок для бота
        @self.bot.message_handler(commands = ['start'])
        def start_screen(message):
            self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            self.username = message.from_user.username
            btn1 = types.KeyboardButton('Голосование')
            self.markup.add(btn1)
            if self.username in self.us:
                self.bot.send_message(message.chat.id,
                                      text="Привет, {0.first_name}! Вы уже голосовали! ".format(
                                          message.from_user), reply_markup=self.markup)
                self.flg_vote_end = True
            else:
                self.bot.send_message(message.chat.id,
                                  text="Привет, {0.first_name}! Примите участие в нашем голосовании! Для общения необходимо импользовать кнопки".format(
                                      message.from_user), reply_markup=self.markup)

        # варианты предложений для каждой кнопки (для каждого направления)
        @self.bot.message_handler(content_types=['text'])
        def func(message):
            if self.username in self.us:
                self.bot.send_message(message.chat.id,
                                      text="Вы уже голосовали! Спасибо за участие ".format(
                                          message.from_user))
            elif message.text == 'Голосование':
                if self.username in self.us:
                    self.bot.send_message(message.chat.id,
                                          text="Вы уже голосовали!".format(
                                              message.from_user))
                else:
                    self.flg = True
            if self.flg and not self.flg_vote_end:

                if not self.flg_vote_end and self.username not in self.us:
                    #print(self.flg, 'flg from 1')
                    self.markup = types.InlineKeyboardMarkup()
                    self.flg = False
                    #print(self.flg, 'flg from 2')
                    img = open(self.images[self.i], 'rb')
                    self.bot.send_photo(message.chat.id, img)
                    if self.username not in self.us:
                        vote = telebot.types.InlineKeyboardButton(text='Проголосовать', callback_data='vote')
                        self.markup.add(vote)
                        if self.i < len(self.nums) - 1:
                            next_ = types.InlineKeyboardButton(text='Дальше ⏩️', callback_data='next')
                            self.markup.add(next_)
                            self.i += 1
                        self.bot.send_message(message.chat.id, text=str(self.nums[self.i]), reply_markup=self.markup,
                                              parse_mode="html")

                elif self.flg_vote_end and self.username not in self.us:
                    self.bot.send_message(message.chat.id,
                                          text="Вы".format(
                                              message.from_user))


        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            if call.data == "vote":
                #print(str(call.message.from_user.id), 'qw', self.us, str(call.message.from_user.id) in self.us)
                if self.username not in self.us:
                    self.flg_vote_end = True
                    self.bot.send_message(call.message.chat.id, 'Спасибо за участие в голосовании')
                    file = open("rating.txt", "a")
                    file.write(' ' + str(self.i))
                    file.close()
                    file = open("users.txt", "a")
                    file.write(' ' + self.username)
                    file.close()
                    with open('users.txt', 'r') as f:
                        self.us = f.read().split()
                        print(self.username)
                    f.close()
                else:
                    self.bot.send_message(call.message.chat.id, 'Вы уже голосовали. Спасибо за участие в голосовании')
            elif call.data == 'next':
                self.flg = True
                func(call.message)

        self.bot.polling(none_stop=True)
