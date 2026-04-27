# 1. Импорт модуля asyncio для работы с асинхронным кодом (нужен для бота)
import asyncio
#2 Импорт библиотеки requests для выполнения запросов к сайту ЦБ РФ
import requests
# 3. Импорт модуля logging для записи сообщений о работе программы (логи)
import logging
# 4. Импорт модуля xml.etree.ElementTree под псевдонимом ET для парсинга XML-ответа
import xml.etree.ElementTree as ET
# 5. Импорт классов Bot (бот) и Dispatcher (диспетчер сообщений) из библиотеки aiogram
from aiogram import Bot, Dispatcher
# 6. Импорт типа Message (сообщение) из aiogram для обработки входящих сообщений
from aiogram.types import Message
# 7. Импорт фильтров Command и CommandStart для /rates и /start
from aiogram.filters import Command, CommandStart
# 9. Для вывода отклика, что происходит с ботом
logging.basicConfig(level=logging.INFO)
# 10. URL-адрес, по которому ЦБ РФ публикует ежедневные курсы валют
url = 'https://www.cbr.ru/scripts/XML_daily.asp'
# 11. Функция для с получением url
def parser(url):
    # 12. Начало блока try – попытка выполнить код, который может вызвать ошибку
    try:
        # 13. Выполнить GET-запрос по указанному URL
        r = requests.get(url)
        # 14. Преобразовать содержимое ответа в ElementTree-объект root
        root = ET.fromstring(r.content)
        # 15. Найти все элементы с тегом 'Valute' внутри root и перебрать их
        for valute in root.findall('Valute'):
            #16. Код доллара США
            if valute.get('ID') == 'R01235':
                return [valute.find('Value').text]
    # 16. Если в блоке try возникла любая ошибка
    except:
        # 17. Выдать пустой список
        return []
    # 18. Если цикл завершился, но доллар не найден – вернуть пустой список
    return []

API_TOKEN = '8717913702:AAF4_PRMS63JJBg59DG3QAd66nGCktYvn5A'

# 19. Создание экземпляра бота с переданным токеном
bot = Bot(token=API_TOKEN)
# 20. Обработчик для команд
disp = Dispatcher()

# 21. Две границы по заданию
Low = 89.0
Up = 99.0

# 22. Связка с команды start = /strat
@disp.message(CommandStart())
async def start(message: Message):
    await message.reply("SEND ME! /rates")

# 23. Связка с командой rates = /rates
@disp.message(Command("rates"))
async def rates(message: Message):
    # 24. Вызов функции parser(url), для списка
    lst = parser(url)
    try:
        # 25. Замена с запятой на точку
        current_rate = float(lst[0].replace(',', '.'))

        # 26. Работа с границами и курсом
        if current_rate > Up:
            await message.answer(f"Current exchange rates {current_rate} above the border {Up}.")
        elif current_rate < Low:
            await message.answer(f"Current exchange rates {current_rate} below the border {Low}.")
        else:
            await message.answer(f"Current exchange rates: {current_rate} rubles.")
    except (IndexError, ValueError):
        await message.answer("Error retrieving data from the site.")


async def main():
    # 27. Запуск поллинга (постоянного опроса серверов Telegram) для получения обновлений
    await disp.start_polling(bot)

# 28. Запуск
if __name__ == '__main__':
    asyncio.run(main())