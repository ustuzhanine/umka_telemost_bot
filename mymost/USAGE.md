# 🚀 Инструкция по использованию API Яндекс Телемост

> **Пошаговое руководство для работы с полнофункциональным клиентом API Телемост**

## 📋 Содержание

1. [Быстрый старт](#-быстрый-старт)
2. [Установка и настройка](#-установка-и-настройка)
3. [Проверка токена](#-проверка-токена)
4. [Запуск примеров](#-запуск-примеров)
5. [Использование в коде](#-использование-в-коде)
6. [Диагностика проблем](#-диагностика-проблем)
7. [Справочник методов](#-справочник-методов)

---

## 🚀 Быстрый старт

### Шаг 1: Установка зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 2: Настройка токена
```bash
# Создайте .env файл с вашим токеном
echo "YANDEX_OAUTH_TOKEN=ваш_токен_здесь" > .env
```

### Шаг 3: Проверка готовности
```bash
python check_token_type.py
```

### Шаг 4: Запуск примеров
```bash
python examples.py
```

---

## ⚙️ Установка и настройка

### 1. Клонирование и установка

```bash
# Перейдите в папку проекта
cd /path/to/telemost

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка токена

**Вариант А: Создание .env файла**
```bash
# Создайте файл .env
nano .env

# Добавьте ваш токен:
YANDEX_OAUTH_TOKEN=y0_AgAAAABl...ваш_токен...
CLIENT_ID=ваш_client_id
LOG_LEVEL=INFO
```

**Вариант Б: Использование готового шаблона**
```bash
# Скопируйте шаблон
cp env_example.txt .env

# Отредактируйте токен
nano .env
```

### 3. Проверка корректности настройки

```bash
# Проверьте, что файлы на месте
ls -la *.py

# Должны быть:
# telemost_api.py
# examples.py
# examples_advanced.py
# check_token_type.py
```

---

## 🔍 Проверка токена

### Полная диагностика токена
```bash
python check_token_type.py
```

**Что показывает:**
- ✅ Формат токена
- 👤 Информация о пользователе
- 🏢 Тип аккаунта (личный/корпоративный)
- 🎥 Доступ к API Телемост
- 💡 Рекомендации по исправлению

### Быстрая проверка
```bash
# Базовая диагностика
python test_token.py

# Проверка разрешений
python check_permissions.py
```

### Тестирование нового токена
```bash
python test_new_token.py
# Введите новый токен для тестирования
```

---

## 📚 Запуск примеров

### 1. Основной клиент API
```bash
python telemost_api.py
```

**Что делает:**
- 🚀 Демонстрирует основные возможности
- 📝 Создает простую встречу
- 📺 Показывает встречу с трансляцией
- 📊 Выводит отформатированную информацию
- 💾 Сохраняет данные в JSON файл

**Пример вывода:**
```
🚀 Демонстрация возможностей Яндекс Телемост API
============================================================

1️⃣ Создание простой встречи...
✅ Встреча создана: conf_12345
🔗 Ссылка: https://telemost.yandex.ru/j/12345

2️⃣ Создание встречи с трансляцией...
📺 Ссылка на просмотр: https://telemost.yandex.ru/live/67890
```

### 2. Простые примеры
```bash
python examples.py
```

**Что демонстрирует:**
- 1️⃣ Создание простой встречи
- 2️⃣ Встреча с трансляцией
- 3️⃣ Встреча с соорганизаторами
- 4️⃣ Кастомная встреча со всеми параметрами

### 3. Полная демонстрация
```bash
python examples_advanced.py
```

**Что включает:**
- 🔥 **Базовые CRUD операции** - создание, чтение, обновление, удаление
- 🚀 **Продвинутые встречи** - с трансляциями и настройками
- 👥 **Управление соорганизаторами** - добавление, удаление, обновление
- 📋 **Работа со списком встреч** - получение и пагинация
- ⚙️ **Настройки по умолчанию** - глобальные настройки
- 🚨 **Обработка ошибок** - демонстрация всех типов ошибок
- 🔍 **Валидация данных** - проверка корректности

---

## 💻 Использование в коде

### Базовое использование

```python
from telemost_api import TelemostAPI

# Инициализация (токен из .env)
api = TelemostAPI()

# Создание простой встречи
meeting = api.create_simple_meeting()
print(f"Ссылка: {meeting['join_url']}")
```

### Встреча с трансляцией

```python
meeting = api.create_meeting_with_stream(
    stream_title="Важная презентация",
    stream_description="Квартальные результаты компании",
    stream_access_level="ORGANIZATION"  # Только для сотрудников
)

print(f"Встреча: {meeting['join_url']}")
print(f"Трансляция: {meeting['live_stream']['watch_url']}")
```

### Продвинутая встреча

```python
meeting = api.create_advanced_meeting(
    waiting_room_level="ADMINS",  # Только организаторы пропускают
    stream_title="Корпоративный вебинар",
    stream_description="Обучение новых сотрудников",
    stream_access_level="ORGANIZATION",
    cohost_emails=["manager@company.ru", "hr@company.ru"]
)
```

### Управление встречами

```python
# Получение информации
meeting_info = api.get_meeting("meeting_id")

# Обновление настроек
api.update_meeting("meeting_id", waiting_room_level="PUBLIC")

# Удаление встречи
api.delete_meeting("meeting_id")

# Список всех встреч
meetings = api.list_meetings(limit=10)
```

### Обработка ошибок

```python
from telemost_api import TelemostAPI, TelemostAuthError, TelemostValidationError

try:
    api = TelemostAPI()
    meeting = api.create_simple_meeting()
    
except TelemostAuthError:
    print("❌ Проблема с токеном - проверьте .env файл")
    
except TelemostValidationError as e:
    print(f"❌ Ошибка в параметрах: {e}")
    
except Exception as e:
    print(f"❌ Неожиданная ошибка: {e}")
```

---

## 🔧 Диагностика проблем

### Проблема: "Ошибка 403 - API доступен пользователям Яндекс 360"

**Причина:** У вас личный аккаунт, а нужен корпоративный

**Решение:**
1. Зарегистрируйтесь в [Яндекс 360 для бизнеса](https://360.yandex.ru/)
2. Создайте организацию с корпоративным доменом
3. Получите токен от корпоративного аккаунта

**Проверка типа аккаунта:**
```bash
python check_token_type.py
```

### Проблема: "Токен не найден"

**Решение:**
```bash
# Проверьте наличие .env файла
ls -la .env

# Создайте, если отсутствует
echo "YANDEX_OAUTH_TOKEN=ваш_токен" > .env
```

### Проблема: "Ошибка импорта модуля"

**Решение:**
```bash
# Установите зависимости
pip install -r requirements.txt

# Проверьте установку
python -c "import requests, dotenv; print('OK')"
```

### Проблема: "Ошибка валидации email"

**Решение:** Используйте корректные email адреса:
```python
# ❌ Неправильно
cohost_emails = ["invalid-email"]

# ✅ Правильно  
cohost_emails = ["user@company.ru"]
```

---

## 📖 Справочник методов

### 🚀 Создание встреч

| Метод | Описание | Пример |
|-------|----------|---------|
| `create_simple_meeting()` | Простая публичная встреча | `api.create_simple_meeting()` |
| `create_meeting_with_stream()` | Встреча с трансляцией | `api.create_meeting_with_stream("Название")` |
| `create_meeting_with_cohosts()` | Встреча с соорганизаторами | `api.create_meeting_with_cohosts(["user@company.ru"])` |
| `create_advanced_meeting()` | Встреча со всеми параметрами | `api.create_advanced_meeting(...)` |

### 📋 Управление встречами

| Метод | Описание | Пример |
|-------|----------|---------|
| `get_meeting(id)` | Получить информацию о встрече | `api.get_meeting("conf_123")` |
| `update_meeting(id, ...)` | Обновить настройки встречи | `api.update_meeting("conf_123", waiting_room_level="PUBLIC")` |
| `delete_meeting(id)` | Удалить встречу | `api.delete_meeting("conf_123")` |
| `list_meetings(limit)` | Список встреч | `api.list_meetings(10)` |

### 👥 Соорганизаторы

| Метод | Описание | Пример |
|-------|----------|---------|
| `get_meeting_cohosts(id)` | Список соорганизаторов | `api.get_meeting_cohosts("conf_123")` |
| `add_meeting_cohost(id, email)` | Добавить соорганизатора | `api.add_meeting_cohost("conf_123", "user@company.ru")` |
| `update_meeting_cohosts(id, list)` | Обновить список | `api.update_meeting_cohosts("conf_123", [...])` |
| `remove_meeting_cohost(id, cohost_id)` | Удалить соорганизатора | `api.remove_meeting_cohost("conf_123", "user_456")` |

### 🛠 Утилиты

| Метод | Описание | Пример |
|-------|----------|---------|
| `save_meeting_data(data)` | Сохранить данные в JSON | `api.save_meeting_data(meeting)` |
| `get_meeting_info_formatted(id)` | Красивое форматирование | `api.get_meeting_info_formatted("conf_123")` |
| `validate_meeting_data(data)` | Валидация данных | `api.validate_meeting_data(meeting)` |

---

## 🎯 Практические сценарии

### Сценарий 1: Еженедельное совещание
```python
api = TelemostAPI()

meeting = api.create_meeting_with_cohosts(
    cohost_emails=["manager@company.ru"],
    waiting_room_level="ORGANIZATION"
)

# Сохраняем ссылку для переиспользования
with open("weekly_meeting.txt", "w") as f:
    f.write(meeting['join_url'])
```

### Сценарий 2: Публичный вебинар
```python
webinar = api.create_meeting_with_stream(
    stream_title="Открытый вебинар по продукту",
    stream_description="Демонстрация новых возможностей",
    stream_access_level="PUBLIC",
    waiting_room_level="PUBLIC"
)

print(f"Регистрация: {webinar['join_url']}")
print(f"Трансляция: {webinar['live_stream']['watch_url']}")
```

### Сценарий 3: Корпоративная презентация
```python
presentation = api.create_advanced_meeting(
    waiting_room_level="ADMINS",
    stream_title="Квартальные результаты",
    stream_access_level="ORGANIZATION",
    cohost_emails=["ceo@company.ru", "cfo@company.ru"]
)

# Красивое форматирование для отправки коллегам
info = api.get_meeting_info_formatted(presentation['id'])
print(info)
```

---

## 📞 Поддержка

### Если что-то не работает:

1. **Проверьте токен:**
   ```bash
   python check_token_type.py
   ```

2. **Проверьте зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Посмотрите логи:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

4. **Изучите примеры:**
   ```bash
   python examples_advanced.py
   ```

### Полезные ссылки:
- 🏢 [Яндекс 360 для бизнеса](https://360.yandex.ru/)
- 🔑 [OAuth приложения](https://oauth.yandex.ru/)
- 📚 [Документация API](https://cloud.yandex.ru/docs/api-design-guide/)

---

**🎉 Готово! Теперь вы знаете все для работы с API Яндекс Телемост!**
