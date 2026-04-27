# 1. Импортируем библиотеку requests для отправки HTTP-запросов к веб-сайтам.
import requests
# 2. Из библиотеки BeautifulSoup импортируем основной класс для парсинга HTML/XML.
from bs4 import BeautifulSoup
# 3. Импортируем pandas для работы с табличными данными и сохранения в Excel/ODS.
import pandas as pd
# 4. Импортируем sys для управления завершением программы, требуется именно (sys.exit()).
import sys
# 5. Импортируем модуль re для работы с регулярными выражениями, а именно очистка цены.
import re

# 6. Функция для обработки книг
def parse_books():
    # 7. Адрес указанный в варианте 10. Книги про питон.
    url = "https://www.chitai-gorod.ru/search?phrase=python"
    # 8. Имитировать запрос от реального браузера.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
    }
    # 9. Начинаем блок try для перехвата исключений при сетевом запросе или парсинге.
    try:
        # 10. Выполняем запрос к сайту с указанными заголовками и таймаутом 15 секунд.
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Статус ответа: {response.status_code}")
        # 11. Если происходит превышение и сайт не грузится.
        if response.status_code != 200:
            print("Ошибка загрузки страницы")
            return []

        # 12. Создаём объект красивого супчика для разбора HTML-кода с помощью метода html.parser.
        soup = BeautifulSoup(response.text, "html.parser")
        # 13 Ищем все HTML-элементы <article> с классом "product-card".
        cards = soup.find_all('article', class_='product-card')
        if not cards:
            # 14. Иначе ищем универсальный тег div
            cards = soup.find_all('div', class_='product-card')

        print(f"Найдено карточек: {len(cards)}")
        books = []

        for card in cards:
            # 15. Название и ищем его в <a> так как чаще всего именно он отвечает за названия и с двумя __
            title_tag = card.find('a', class_='product-card__title')
            if not title_tag:
                # 16. Название и ищем его в <a> так как чаще всего именно он отвечает за названия и с двумя _
                title_tag = card.find('a', class_='product-card_title')
            if not title_tag:
                # 17. Поиск по атрибуту href, содержащему '/book/'
                title_tag = card.find('a', href=lambda h: h and '/book/' in h)
                # 18. Извлекаем текст названия: если тег найден, то берём его текст (очищенный от пробелов),
                # иначе присваиваем строку-заглушку "Название не найдено".
            title = title_tag.get_text(strip=True) if title_tag else "Название не найдено"

            # Автор (ищем несколькими способами).
            author = "Автор не указан"
            # 19. Ищем автора через тег <a>.
            author_tag = card.find('a', class_='product-card__author')
            if not author_tag:
                # 20. Ищем автора через тег <span>.
                author_tag = card.find('span', class_='product-card__author')
            if not author_tag:
                # 21. Ищем автора через тег <div>.
                author_tag = card.find('div', class_='product-card__authors')
            if not author_tag:
                # 22. Возможно автор лежит внутри span без класса.
                author_tag = card.find('span', attrs={'data-testid': 'product-card-author'})
            if not author_tag:
                # 23. Последняя попытка: ищем любой span, который может содержать имя, хотя бы какое-то.
                spans = card.find_all('span')
                for sp in spans:
                    # 24. Извлекаем текст из span, удаляя лишние пробелы.
                    text = sp.get_text(strip=True)
                    # 25. Каким бывает автор? Обычно короткий, без цифр, не содержит '₽'.
                    if text and len(text) < 50 and not re.search(r'[₽\d]', text) and ' ' in text:
                        author_tag = sp
                        break
            # 26. Если после всех попыток author_tag найден.
            if author_tag:
                # 27. Достаём текст и записываем его в переменную.
                author = author_tag.get_text(strip=True)

            # Цена (очищаем от лишнего)
            # 27. Значение по умолчанию.
            price = "Цена не указана"
            # 28. Ищем цену с классом product-card__price.
            price_tag = card.find('div', class_='product-card__price')
            if not price_tag:
                # 29. Ищем цену с новым классом product-mini-card-price.
                price_tag = card.find('div', class_='product-mini-card-price')
            if not price_tag:
                # 30. Ищем цену с альтернативным классом product-mini-card-price.
                price_tag = card.find('div', class_='product-card__price-current')
            if price_tag:
                # 31. Получаем текст из тега, удаляем лишние пробелы и заменяем неразрывные пробелы \xa0 на обычные.
                raw_price = price_tag.get_text(strip=True).replace('\xa0', ' ')
                # 32. Ищем последовательность любых циифр и знак рубля в самом конце.
                match = re.search(r'(\d[\d\s]*₽)', raw_price)
                if match:
                    # 33. Если совпало, то извлекаем найденную цену.
                    price = match.group(1)
                else:
                    # 34. Иначе ничего не меняем. Цены нет.
                    price = raw_price
            # 35. Словарь для всех трёх пунктов.
            books.append({
                'Название': title,
                'Автор': author,
                'Цена': price
            })
        # 36. Возвращаем заполненный список books из функции parse_books().
        return books
    # 37. except: перехватывает любое исключение (общее, но с сохранением в переменную e).
    except Exception as e:
        # 38. Выводим ошибку.
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return []
# 38. Определяем функцию save_to_files, принимающую DataFrame и два имени файлов.
def save_to_files(df, xlsx_filename, ods_filename):
    try:
        # 39. Метод для xlsx.
        df.to_excel(xlsx_filename, index=False, engine='openpyxl')
        print(f"Файл {xlsx_filename} сохранён.")
    except Exception as e:
        print(f"Ошибка при сохранении .xlsx: {e}")

    try:
        # 40. Метод для ods.
        df.to_excel(ods_filename, index=False, engine='odf')
        print(f"Файл {ods_filename} сохранён.")
    except ImportError:
        # 41. Если проблемы с библиотекой, то рекомендуем установку.
        print("Для .ods установите odfpy: pip install odfpy")
    except Exception as e:
        print(f"Ошибка при сохранении .ods: {e}")

def main():

    # 42. Начало парсинга.
    print("Парсинг книг с chitai-gorod.ru...")
    books_data = parse_books()
    # 43. При неудаче.
    if not books_data:
        print("Не удалось получить данные. Завершение.")
        sys.exit(1)

    print(f"\nНайдено книг: {len(books_data)}")
    print("\nПервые 5 записей:")
    # 44. Выводим три пункта.
    for i, b in enumerate(books_data[:5], 1):
        print(f"{i}. {b['Название']} | {b['Автор']} | {b['Цена']}")
    # 45. Создаём pandas DataFrame из списка словарей books_data.
    df = pd.DataFrame(books_data)
    save_to_files(df, "Lab1_Variant10_Result.xlsx", "Lab1_Variant10_Result.ods")
    print("\nГотово! Файлы созданы.")

if __name__ == "__main__":
    main()