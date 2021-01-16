import telebot
import config
import eschoolmanager

bot = telebot.TeleBot(config.token)


# класс для взаимодействия с файлом с данными логинов и паролей
class dataprocess:
    # проверка файла на содержание в нем текста
    def text_finder(file, text: str) -> int:
        count: int = 1
        with open(file) as file:
            for line in file:
                if text in line:
                    return (count)
                count += 1
            return (0)

    # поиск логина по id chata
    def login_finder(file, text) -> str:
        with open(file) as file:
            for line in file:
                if text in line:
                    return (line.split()[1])
            return (0)

    # то же самое, но пароля
    def pass_finder(file, text) -> str:
        with open(file) as file:
            for line in file:
                if text in line:
                    return (line.split()[2])
            return (0)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_responder(message):
    msgtext: str = message.text.split()
    # это команда /login?
    if msgtext[0] == '/login' and len(msgtext) == 3:
        # если этот пользователь тг не зарегистрирован в боте? регистрируем
        if not dataprocess.text_finder('login_data.txt', str(message.chat.id)):
            with open('login_data.txt', 'a') as file:
                file.write(str(message.chat.id) + ' ' + msgtext[1] + ' ' + msgtext[2] + '\n')
            bot.send_message(message.chat.id, 'Logged in successfully!')
        # иначе удаляем старые данные регистрации и регистрируем
        else:
            with open('login_data.txt', "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if not str(message.chat.id) in i:
                        f.write(i)
                f.truncate()
                with open('login_data.txt', 'a') as file:
                    file.write(str(message.chat.id) + ' ' + msgtext[1] + ' ' + msgtext[2] + '\n')
            bot.send_message(message.chat.id, 'Re-logged in successfully!')
    # пользователь хочет получить свои оценки?
    elif msgtext[0] == '/getmarx':
        bot.send_message(message.chat.id, 'Please wait...')
        # шлем оценки пользователя
        if dataprocess.text_finder('login_data.txt', str(message.chat.id)):
            bot.send_message(message.chat.id, eschoolmanager.eschoolmng.getmarx(
                dataprocess.login_finder('login_data.txt', str(message.chat.id)),
                dataprocess.pass_finder('login_data.txt', str(message.chat.id))))
    else:
        bot.send_message(message.chat.id, 'Invalid command')


if __name__ == '__main__':
    bot.polling()
