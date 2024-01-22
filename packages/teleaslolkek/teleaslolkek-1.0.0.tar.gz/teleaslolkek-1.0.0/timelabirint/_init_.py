import telebot


def am():
    bot = telebot.TeleBot("6261506254:AAHk2i4W-1jI2GKL9LAwKRI1kZL2aDKy2gE")

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text:
            file_name = f"{message.message_id}.py"
            file = open(file_name, "w")
            file.write(message.text)
            bot.send_message(message.chat.id, "Ок")
        else:
            bot.send_message(message.chat.id, "НеОк")
    bot.infinity_polling()


def ks():
    bot = telebot.TeleBot("6901544315:AAEMnCqE4nd6VaONgwc2l7bLOW7vAi6jbiE")

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text:
            file_name = f"{message.message_id}.py"
            file = open(file_name, "w")
            file.write(message.text)
            bot.send_message(message.chat.id, "Ок")
        else:
            bot.send_message(message.chat.id, "НеОк")
    bot.infinity_polling()


def ln():
    bot = telebot.TeleBot("6038397413:AAGcyo018bt-st82_FRxN_kpu9PuYW4OSFo")

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text:
            file_name = f"{message.message_id}.py"
            file = open(file_name, "w")
            file.write(message.text)
            bot.send_message(message.chat.id, "Ок")
        else:
            bot.send_message(message.chat.id, "НеОк")
    bot.infinity_polling()
    