Mbase — небольшая вспомогательная библиотека утилит.

Ниже краткая справка по основным функциям/методам и примеры возвращаемых значений.

1) Конфигурация (mbase.config)
 - Описание: чтение/запись настроек в INI-файл, создание файла по умолчанию.
 - Основные функции:
		- config.create_default() -> dict | list
			- Успех: возвращает словарь/секцию конфигурации, например: {'General': {'version': '1.0', 'author': 'you'}}
			- Ошибка: возвращает список с сообщением, например: ['Ошибка при создании файла конфигурации']
		- config.write(section: str, key: str, value: str) -> bool
			- True при успешной записи, False при исключении.
		- config.read(section: str, key: str) -> str | list
			- Успех: строка с значением, например: 'my_value'
			- Если нет ключа/секции: ['Категория/пункт не найдена']

2) Система (mbase.system)
 - Описание: небольшие привязки к возможностям ОС — список задач, всплывающие сообщения, IP/имя хоста.
 - Основные функции:
		- system.tasklist() -> list[str]
			- Возвращает список строк вида: ['explorer.exe                1234 Console  1  12,345 K', ...]
		- system.msg(title: str, text: str) -> None
			- Показывает окно (tkinter.messagebox). Возвращает None (GUI-эффект).
		- system.ip() -> tuple[str, str]
			- Возвращает (ip, hostname), например: ('192.168.1.10', 'MY-PC')

3) Web/HTTP (mbase.web)
 - Описание: лёгкие обёртки поверх requests для унификации обработки ошибок и сообщений.
 - Основные функции:
		- web.http_error(code: int) -> str
			- Примеры: 404 -> 'Страница не найдена', неизвестный код -> 'Неизвестная ошибка HTTP, код: <code>'

		- web.request(method: str, url: str, **kwargs) -> requests.Response | dict
			- Успех: объект requests.Response (например <Response [200]>)
			- HTTP-ошибка (status != 200): словарь с описанием, например:
				{'status': 'http_error', 'code': 404, 'Mbase': 'Страница не найдена', 'response': '<html>...</html>'}
			- Исключение (timeout, connection error): {'error': 'timeout'} или другое сообщение.

Примеры возвращаемых значений (Python):

```python
# config
config_write_ok = True
config_read_value = 'my_value'                # успешное чтение
config_read_not_found = ['Категория/пункт не найдена']

# system
system_tasklist = ['explorer.exe 1234 ...']  # список строк
system_ip = ('192.168.1.10', 'MY-PC')

# web
web_success = '<Response [200]>'              # объект requests.Response
web_http_error = {'status': 'http_error', 'code': 503, 'Mbase': 'Сервис временно недоступен', 'response': '...'}
web_exception = {'error': 'Connection aborted.'}
```

Мини-примеры использования:

```python
from mbase import config, system, web

# чтение значения
val = config.read('General', 'username')
if isinstance(val, list):
	print('Ошибка или не найден:', val)
else:
	print('Username =', val)

# запрос
resp = web.request('GET', 'https://example.com')
if isinstance(resp, dict):
	print('Ошибка web:', resp)
else:
    print('OK, code', resp.status_code)
    print('Возможная причина по мнению Mbase:', web.http_error(resp.status_code))
```

