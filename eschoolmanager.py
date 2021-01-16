from selenium import webdriver
import time

class textprocess: # отвечает за переработку текста таблицы оценок
    def process(text) -> str: # метод переработки
        output: str = ''
        temparray: list = []
        def isCapCyrLetter(character) -> bool: # проверка на то, является ли символ заглавной кириллической буквой; необходима для переработки текста
            capcyrletters: list = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р',
                             'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', ]
            for i in capcyrletters:
                if character == i:
                    return True
            return False

        def isCyrLetter(character) -> bool:# проверка на то, является ли символ строчной кириллической буквой; необходима для переработки текста
            cyrletters: list = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
                          'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', '.']
            for i in cyrletters:
                if character == i:
                    return True
            return False
        #тут от текста отделяется верхняя строка таблицы, в которой содержатся даты
        flag: bool = False
        for i in range(len(text) - 1):
            if isCapCyrLetter(text[i]):
                if flag:
                    text = text[i] + text.split(text[i], 1)[1]
                    break
                text = text.split(text[i], 1)[1]
                flag = True

        #очистка текста от лишних отступов и пробелов
        for i in range(len(text)):
            if text[i] != ' ' or (isCyrLetter(text[i - 1]) and isCyrLetter((text[i + 1]))):
               temparray.append(text[i])
        for i in range(1, len(temparray)):
            if isCapCyrLetter(temparray[i]):
                temparray[i - 2] = ''
                if temparray[i - 3] != '\n':
                    temparray[i - 3] = ''
                elif isCyrLetter(temparray[i - 1]):
                    temparray[i] = ' '
        for i in temparray:
            output += i
        return(output)

#класс для взаимодействия с электронным журналом
class eschoolmng:
    #метод, получающий оценки
    def getmarx(login:str, password:str) -> str:
        #открываем браузер и переходим по ссылке на таблицу оценок
        driver = webdriver.Chrome("C:\\Users\\gvosk\\chromedriver.exe")
        driver.get("https://app.eschool.center/#/Private/studentMarks")
        #нас отсылает на страницу входа; заполняем поле для имени пользователя
        username_textbox = driver.find_element_by_id("inputLogin")
        username_textbox.send_keys(login)
        #и для пароля
        password_textbox = driver.find_element_by_id("inputPassword")
        password_textbox.send_keys(password)
        #кликаем (на) кнопку входа
        login_button = driver.find_element_by_id("btn-login")
        login_button.click()

        while True:
            #если таблица загрузилась, копируем себе текст таблицы
            try:
                marxText: str = driver.find_element_by_id("tableMarksScroll").text
                break
            #если нет, то ждем
            except:
                time.sleep(2)
        driver.close()
        #возвращаем переработанный текст таблицы
        return(textprocess.process(marxText))