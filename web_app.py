# 1. Импортируем необходимые классы и функции из Flask:
# Flask - главный класс приложения,
# request - для получения данных HTTP-запроса,
# render_template - для отображения HTML-шаблона,
# redirect - для перенаправления на другой URL,
# url_for - для генерации URL по имени функции-обработчика,
# flash - для временного хранения сообщения между запросами.
from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
# 2. Импортируем datetime из одноимённого модуля для проверки дат
from datetime import datetime
# 3. Создаём экземпляр веб-приложения
app = Flask(__name__)
# 4. Дополнительный ключ для работы с flash-сообщениями
app.secret_key = 'supersecretkey'

events = {
    "01.01": "Новый год",
    "25.01": "Татьянин день",
    "23.02": "День защитника Отечества",
    "08.03": "Международный женский день",
    "12.04": "День космонавтики",
    "01.05": "Праздник Весны и Труда",
    "09.05": "День Победы",
    "12.06": "День России",
    "22.08": "День Государственного флага РФ",
    "01.09": "День знаний",
    "05.10": "День учителя",
    "04.11": "День народного единства"
}
# 5. Декоратор связывает функцию index с URL + методы GET и POST.
@app.route('/', methods=['GET', 'POST'])
def index():
    # 6. POST пользователь отправил форму
    if request.method == 'POST':
        # 7. Получение даты от пользователя
        date_input = request.form.get('num_1')
        # 8. Проверка на наличие точки
        if '.' not in date_input:
            flash("Неверный формат. Используй ДД.ММ для корректности")
            return redirect(url_for('index'))
        # 9. Деление строки
        parts = date_input.split('.')
        if len(parts) != 2:
            flash("Неверный формат. Используй ДД.ММ для корректности")
            return redirect(url_for('index'))
        # 10. Извлекаем строки дня и месяца
        day_str, month_str = parts
        # 11. Проверка, что обе части состоят только из цифр
        if not (day_str.isdigit() and month_str.isdigit()):
            flash("Неверный формат. Используй ДД.ММ для корректности")
            return redirect(url_for('index'))
        # 12. Преобразуем строки в целые числа для дальнейшей проверки
        day = int(day_str)
        month = int(month_str)

        # 13. Проверка существования даты (год берём любой)
        try:
            # 14. Если дата невалидна, вызовет ValueError
            datetime(2000, month, day)
        except ValueError:
            flash("Неверный формат. Несуществующий день или месяц")
            return redirect(url_for('index'))

        # 14. Приводим день и месяц к двузначному формату (например, '5' -> '05') для поиска в словаре
        key = f"{day:02d}.{month:02d}"
        # 15. Проверка
        if key in events:
            flash(events[key])
        else:
            flash("Нет никакого праздника или события в этот день")
        return redirect(url_for('index'))

    # 16. Получаем все flash-сообщения (они будут удалены из сессии после чтения)
    messages = get_flashed_messages()
    # 17. Если список messages не пуст, берём первое сообщение, иначе задаём начальный текст
    event = messages[0] if messages else "Напиши дату, о которой хочешь узнать"
    # 18. Передаём в ans
    return render_template('index.html', ans=event)

if __name__ == '__main__':
    app.run()