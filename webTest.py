# -*- coding: utf-8 -*-
#Модуль unittest предоставляет богатый набор инструментов для написания и
#запуска тестов. Однако достаточно лишь некоторых из них, чтобы
#удовлетворить потребности большинства пользователей.
import unittest
# 1. Импортируем файл с сайтом
from web_app_for_test import app

# Класс с тестами для проверки работы веб-приложения с памятными датами.
class TestDateEvents(unittest.TestCase):

    def setUp(self):
        # 2. Создаёт тестового клиента перед каждым тестом
        # Клиент для отправки фейковых HTTP-запросов
        self.app = app.test_client()
        # Включает тестовый режим (отключает перехват ошибок)
        self.app.testing = True

    def test_1(self):
        # 3. Имитируем POST-запрос к сайту с данными формы: поле num_1 = '01.01'
        response = self.app.post('/', data={'num_1': '01.01'})
        # 4. Из ответа получаем тело (HTML) в виде байтов и декодируем в UTF-8-строку
        text = response.data.decode('utf-8')
        # 5. Содержит подстроку 'Новый год'?
        self.assertIn('Новый год', text)
    # 6. Дальнейшие проверки будут практически одинаковы, изменяется только дата.
    # Эти тесты проверяют корректность дат
    # и их названий
    def test_2(self):
        response = self.app.post('/', data={'num_1': '23.02'})
        text = response.data.decode('utf-8')
        self.assertIn('День защитника Отечества', text)

    def test_3(self):
        response = self.app.post('/', data={'num_1': '08.03'})
        text = response.data.decode('utf-8')
        self.assertIn('Международный женский день', text)

    def test_4(self):
        response = self.app.post('/', data={'num_1': '09.05'})
        text = response.data.decode('utf-8')
        self.assertIn('День Победы', text)

    def test_5(self):
        response = self.app.post('/', data={'num_1': '12.06'})
        text = response.data.decode('utf-8')
        self.assertIn('День России', text)
    # 7. Проверка на отсутствие праздника или события, выходом из границ месяца и дня
    def test_6(self):
        response = self.app.post('/', data={'num_1': '99.99'})
        text = response.data.decode('utf-8')
        self.assertIn('Нет никакого праздника или события в этот день', text)
    # 8. Проверка на отсутствие праздника или события
    def test_7(self):
        response = self.app.post('/', data={'num_1': '30.02'})
        text = response.data.decode('utf-8')
        self.assertIn('Нет никакого праздника или события в этот день', text)
    # 9. Проверки на не существующие/неверные форматы
    def test_8(self):
        response = self.app.post('/', data={'num_1': '01-01'})
        text = response.data.decode('utf-8')
        self.assertIn('Неверный формат. Используй ДД.ММ для корректности', text)

    def test_9(self):
        response = self.app.post('/', data={'num_1': '01/01'})
        text = response.data.decode('utf-8')
        self.assertIn('Неверный формат. Используй ДД.ММ для корректности', text)

    def test_10(self):
        response = self.app.post('/', data={'num_1': 'первое января'})
        text = response.data.decode('utf-8')
        self.assertIn('Неверный формат. Используй ДД.ММ для корректности', text)

    def test_11(self):
        response = self.app.post('/', data={'num_1': ''})
        text = response.data.decode('utf-8')
        self.assertIn('Неверный формат. Используй ДД.ММ для корректности', text)

    def test_12(self):
        response = self.app.post('/', data={'num_1': '9.5'})
        text = response.data.decode('utf-8')
        self.assertIn('День Победы', text)

    # 10. Проверка игнорирования пробелов
    def test_13(self):
        response = self.app.post('/', data={'num_1': ' 01.01 '})
        text = response.data.decode('utf-8')
        self.assertIn('Новый год', text)

    # 11. Проверка на лишнюю точку в конце – неверный формат
    def test_14(self):
        response = self.app.post('/', data={'num_1': '01.01.'})
        text = response.data.decode('utf-8')
        self.assertIn('Неверный формат. Используй ДД.ММ для корректности', text)

    # 12. Проверка на только день, без точки и месяца – неверный формат
    def test_15(self):
        response = self.app.post('/', data={'num_1': '01'})
        text = response.data.decode('utf-8')
        self.assertIn('Неверный формат. Используй ДД.ММ для корректности', text)

    # 13. Проверка на буквы вместо месяца – ожидаем 'Неверный формат' (проверка isdigit)
    def test_16(self):
        response = self.app.post('/', data={'num_1': '01.abc'})
        text = response.data.decode('utf-8')
        self.assertIn('Неверный формат. Используй ДД.ММ для корректности', text)

    # 14. Проверка февраля на – нет события (дата не в словаре)
    def test_17(self):
        response = self.app.post('/', data={'num_1': '29.02'})
        text = response.data.decode('utf-8')
        self.assertIn('Нет никакого праздника или события в этот день', text)

    # 15. Проверка даты 4.11 без ведущих нулей
    def test_18(self):
        response = self.app.post('/', data={'num_1': '4.11'})
        text = response.data.decode('utf-8')
        self.assertIn('День народного единства', text)


if __name__ == '__main__':
    unittest.main()