import sys
import subprocess
import importlib

# --- стандартная библиотека ---
import time
import socket
import logging
import configparser
from subprocess import Popen, PIPE
from tkinter import messagebox

# --- внешние зависимости ---
REQUIRED_PACKAGES = [
    'requests',
]

def ensure_packages(packages):
    missing = []

    for pkg in packages:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print("MBASE: отсутствуют модули:", ", ".join(missing))
        print("Устанавливаю...")

        subprocess.check_call([
            sys.executable, "-m", "pip", "install", *missing
        ])

        print("Установка завершена. Перезапусти программу.")
        sys.exit(1)


ensure_packages(REQUIRED_PACKAGES)

# гарантированный импорт после установки
import requests

"""     
Удобная библиотека с базовыми инструментами: mbase
Автор: Maxim1033
Version: VERSION
"""     
       
class mconfig:
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
        except Exception as e:
            print(f"MBASE: Ошибка при создании файла конфигурации: {str(e)}")
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
            
class mlogger:
    @staticmethod
    def setup_logger(name: str = "logger", log_file: str = "log.txt", level=logging.DEBUG) -> logging.Logger:
        """Создает и настраивает логгер.
        
        :param name: Имя логгера.
        :param log_file: Путь к файлу для записи логов.
        :param level: Уровень логирования.
        :return: Настроенный логгер.
        """
        
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

class msystem:
    @staticmethod
    def tasklist():
        """ Получает список запущенных задач в системе. Нужно указать присваемую переменную для получения результата."""
        tasks = [line.decode('cp866', 'ignore') for line in Popen('tasklist', stdout=PIPE).stdout.readlines()]
        return tasks

    @staticmethod
    def msg(text, title="Сообщение"):
        """ Отправляет сообщение в виде всплывающего окна. """
        messagebox.showinfo(text, title)

    @staticmethod
    def ip():
            """ Получает IP-адрес, имя хоста текущей машины. Нужно указать присваемую переменную для получения результата."""
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip, hostname


class mweb:
    @staticmethod
    def http_error(code):
        """ Возвращает текстовое описание HTTP ошибки по коду. Эта функция сделалана Maksim1033, Xanthurs """
        http_errors = {
            200: "Успешный запрос",
            201: "Запрос принят и обработан",
            202: "Запрос принят, но не обработан",
            203: "Информация в ответе может быть неактуальна",
            204: "Нет содержимого для отображения",
            205: "Содержимое сброшено",
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


class mtime:
    @staticmethod
    def sleep(minutes=None, hours=None):
        """ Задержка выполнения программы на указанное количество минут или часов. """
        ts = time.sleep
        if minutes is not None:
            ts(minutes * 60)
        elif hours is not None:
            ts(hours * 3600)
    
    @staticmethod
    def current_time(format="%H:%M:%S", timezone=time.localtime()):
        """ Получает текущее время в формате ЧЧ:ММ:СС. Нужно указать присваемую переменную для получения результата."""
        return time.strftime(format, timezone)
    
    @staticmethod
    def days_decode(days, text=True):
        """ Преобразует количество дней в годы, месяцы и дни. Нужно указать присваемую переменную для получения результата."""
        years, remainder = divmod(days, 365)
        months, remaining_days = divmod(remainder, 30)

        if not text:
            return years, months, remaining_days

        def choose_form(value: int, forms: tuple[str, str, str]) -> str:
            """Подбирает правильную форму слова для русского языка."""
            if value % 100 in (11, 12, 13, 14):
                return forms[2]
            last = value % 10
            if last == 1:
                return forms[0]
            if last in (2, 3, 4):
                return forms[1]
            return forms[2]

        def format_part(value: int, forms: tuple[str, str, str]):
            return f"{value} {choose_form(value, forms)}" if value > 0 else None

        parts = [
            format_part(years, ("год", "года", "лет")),
            format_part(months, ("месяц", "месяца", "месяцев")),
            format_part(remaining_days, ("день", "дня", "дней")),
        ]

        return ", ".join(part for part in parts if part) or "0 дней"
    
