from time_app import TimeApp
import random

# Получение текущей даты и времени
now = TimeApp.now()

# Генерация случайного числа от 1 до 30 (количество дней)
random_days = random.randint(1, 30)

# Создание новой даты, добавив случайное количество дней
random_date = now + TimeApp.timedelta(days=random_days)

# Вывод сгенерированной даты
print(f"Случайная дата через {random_days} дней: {random_date}")
