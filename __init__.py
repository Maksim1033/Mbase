try:
    import time
    from subprocess import Popen, PIPE
    from tkinter import messagebox
    import requests
    import socket
    import configparser
    import base64
except ImportError:
    print("Библиотека MBASE: Ошибка импорта модулей, пытаюсь установить недостающие модули")
    print("5 секунд...")
    time.sleep(5)
    import pip
    print("pip:")
    pip.main(['install', 'requests', 'configparser'])
    print("Модули установлены, продолжаю перезапустите программу.")
    
      
"""   
Удобная библиотека с базовыми инструментами: mbase
Автор: Maxim1033
"""  
       
class config:
    """Mbase: Создание и управление конфигурацией.
    """
    def __init__(self, filename='config.ini', category="General", conf=configparser.ConfigParser()):
        """:param filename: Название файла
        :param category: Категория по умолчанию в конфиге"""
        self.conf = conf
        self.filename = filename
        try:
            conf[category] = {}
            with open(filename, 'w') as configfile:
                conf.write(configfile)
            return conf[category]
        except Exception as e:
            print(f"MBASE: Ошибка при создании файла конфигурации: {e}")
            return ["Ошибка при создании файла конфигурации"]
    def write(self, item, value, category="General", filename=None, conf=configparser.ConfigParser()):
        """ Запись конфигурации в файл. 
        :param item: Название
        :param value: То что в хотите записать
        :param category: Категория в которую записать
        :param filename: Опционально, название файла конфигурации."""
        if filename is None:
            filename = self.filename
    
        try:
            conf.read(filename)
            if category not in conf:
                conf[category] = {}
            conf[category][item] = value
            with open(filename, 'w') as configfile:
                conf.write(configfile)
            return True
        except Exception as e:
            print(f"MBASE: Ошибка при записи в файл конфигурации: {e}")
            return False
    def read(self, item, category="General", filename=None, conf=configparser.ConfigParser()):
        """ Чтение конфигурации из файла. 
        :param item: Название пункта
        :param category: Категория в которую записать
        :param filename: Опционально, название файла конфигурации."""

        if filename is None:
            filename = self.filename

        try:
            conf.read(filename)
            if category in conf:
                return conf[category][item]
            else:
                print(f"MBASE: Ошибка при поиске категории: {e}")
                return ["Категория/пункт не найдена"]
        except Exception as e:
            print(f"MBASE: Ошибка при чтении файла конфигурации: {e}")
            return ["Ошибка при чтении файла конфигурации"]
            
        
class system:
    def tasklist():
        """ Получает список запущенных задач в системе. Нужно указать присваемую переменную для получения результата."""
        tasks = [line.decode('cp866', 'ignore') for line in Popen('tasklist', stdout=PIPE).stdout.readlines()]
        return tasks

    def msg(text, title="Сообщение"):
        """ Отправляет сообщение в виде всплывающего окна. """
        messagebox.showinfo(text, title)

    def ip():
            """ Получает IP-адрес, имя хоста текущей машины. Нужно указать присваемую переменную для получения результата."""
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip, hostname


class web:
    def http_error(code):
        """ Возвращает текстовое описание HTTP ошибки по коду. Эта функция сделалана Maksim1033, Xanthurs """
        http_errors = {
            200: "Успешный запрос",
            400: "Возможно, ошибка куки, попробуйте очистить куки",
            401: "Ошибка авторизации",
            403: "У вас нет доступа к этому ресурсу",
            404: "Страница не найдена",
            500: "Внутренняя ошибка сервера, попробуйте позже или обновите браузер/приложение",
            502: "Возможно, высокая нагрузка на сервер, или ошибка VPN",
            503: "Сервис в данный момент недоступен, попробуйте позже",
            504: "Попробуйте перезагрузить сайт или перезагрузить ваш роутер",
            505: "Версия HTTP не поддерживается сервером, попробуйте обновить браузер/приложение"
        }
        return http_errors.get(code, "Неизвестная ошибка HTTP, код (http_errors): {}".format(code))

    def request(url, data, method='GET', headers=None, params=None, json=None, timeout=10):
        """ Выполняет HTTP-запрос к указанному URL. Возвращает ответ в переменную. """
        try:
            response = requests.request(method, url, headers=headers, params=params, data=data, json=json, timeout=timeout)
            if response.status_code != 200:
                return {
                    "status": "http_error",
                    "code": response.status_code,
                    "Mbase": web.http_error(response.status_code),
                    "response": response.text
                }
            return response
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

