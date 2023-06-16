# coding=utf-8
import telebot

from telebot import types
from check import Bucket


TOKEN = '5638575257:AAGYpIylImQliUOa1qoIXBYTmvNvwa07Dpc'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def first(message):
    key = types.ReplyKeyboardMarkup(True, False)
    key.row('ℹ О нас', '📖 Меню')
    key.row('🚗 Доставка')
    bot.send_message(message.chat.id, 'Выберите действие ⤵', reply_markup=key)


@bot.message_handler(content_types =['text', 'contact'])
def start(message):
    if message.text == 'ℹ О нас':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        bot.send_message(message.chat.id, '🍕Белла Вита Пицца - это новая пиццерия в Сочи!\n\nДобро пожаловать в нашу уютную пиццерию в самом сердце Сочи! Мы предлагаем вам попробовать самые вкусные, ароматные и сочные пиццы, приготовленные по классическим рецептам и вкусовым экспериментам наших поваров.\n\nМы заботимся о качестве наших ингредиентов, используя только свежие и первоклассные продукты от лучших поставщиков. Наша пицца имеет тонкое и хрустящее тесто, а наши соусы являются настоящими шедеврами.\n\nВ нашей пиццерии вы можете наслаждаться обедом или ужином в уютной атмосфере, в компании друзей и семьи. Мы также предлагаем услугу доставки пиццы на дом, чтобы вы могли насладиться нашими блюдами в удобное для вас время и месте.\n\nОбязательно загляните к нам в пиццерию, и мы уверены, что вы останетесь довольны нашими пиццами и нашим гостеприимством!\n\nВ День Рождения скидка 20%\n\n🏡  ул. Северная, 6, Sun City Сочи, 3 этаж\n☎️  8 (495) xxx-xx-xx\n🕘  12:00 - 00:00')
        send = bot.send_message(message.chat.id, 'Выберите действие ⤵', reply_markup=keyboard)
        bot.register_next_step_handler(send, start)
    elif message.text == '📖 Меню':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        bot.send_message(message.chat.id, '1. Маргарита: соус томатный, моцарелла, базилик\n2. Морская: томатный соус, моцарелла, мидии, кальмары, креветки, лук, перец чили\n3. Пепперони: соус томатный, моцарелла, пепперони')
        keyboard.row('🚗 Доставка')
        keyboard.row('Ⓜ Главное меню')
        bot.send_message(message.chat.id, 'Выберите действие ⤵', reply_markup=keyboard)
    elif message.text == '🚗 Доставка':
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        send = bot.send_message(message.chat.id, 'Как вас зовут ?', reply_markup=keyboard)
        bucket = Bucket(message.from_user.id)
        bot.register_next_step_handler(send, a1, bucket)
    elif message.text == 'Ⓜ Главное меню':
        first(message)

def a1(message, bucket):
    bucket.set_name(message.text)

    if message.text == 'Ⓜ Главное меню':
        first(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        send = bot.send_message(message.chat.id, 'Какую вы хотите пиццу ? Большую среднюю или маленькую ?'.format(name=message.text), reply_markup=keyboard)
        bot.register_next_step_handler(send, a2, bucket)

def a2(message, bucket):
    bucket.set_zakaz(message.text)
    if message.text == 'Ⓜ Главное меню':
        first(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        send = bot.send_message(message.chat.id, 'Как будете платить ?', reply_markup=keyboard)
        bot.register_next_step_handler(send, a3, bucket)

def a3(message, bucket):
    bucket.set_payment_method(message.text)
    if message.text == 'Ⓜ Главное меню':
        first(message)
    elif message.text:
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        send = bot.send_message(message.chat.id, 'Какой у вас адрес доставки ?', reply_markup=keyboard)
        bot.register_next_step_handler(send, a4, bucket)

#Повтор заказа
def a4(message, bucket):
    if message.text == 'Ⓜ Главное меню':
        first(message)
    elif message.text:
        bucket.set_address(message.text)
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        zakaz_str = ""
        number = 1
        for i in bucket.zakaz:
            zakaz_str = zakaz_str + str(str(number) + ": " + i + ' ' + bucket.zakaz.get(i)[1] + " - " + str(bucket.zakaz.get(i)[0]) + "шт.\n")
            number +=1

        send = bot.send_message(message.chat.id, f'Вы хотите: \n{zakaz_str}оплата - {bucket.payment_method},\nдоставить по адресу {bucket.address} ?\n', reply_markup=keyboard)
        bot.register_next_step_handler(send, a5, bucket)

def a5(message, bucket):
    if message.text == 'Ⓜ Главное меню':
        first(message)
    elif message.text:
#        keyboard = types.ReplyKeyboardMarkup(True, False)
#        keyboard.row('Ⓜ Главное меню')
        send = bot.send_message(message.chat.id, "Спасибо за заказ")       
        bot.register_next_step_handler(send, first)


def main():
    bot.polling()


if __name__ == "__main__":
    main()