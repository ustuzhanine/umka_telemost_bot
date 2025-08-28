# 🎥 Полнофункциональный клиент для API Яндекс Телемост

> **Полный набор инструментов для автоматизации работы с видеовстречами в Яндекс Телемост**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Возможности

- 🚀 **CRUD операции** - создание, чтение, обновление, удаление встреч
- 👥 **Управление соорганизаторами** - добавление, удаление, обновление списка
- 📺 **Трансляции** - создание встреч с live-стримингом
- ⚙️ **Настройки по умолчанию** - управление глобальными настройками
- 🔒 **Комната ожидания** - гибкая настройка уровней доступа
- 📊 **Список встреч** - получение и пагинация
- 🛡️ **Валидация данных** - проверка корректности параметров
- 🚨 **Обработка ошибок** - детальная диагностика проблем
- 💾 **Сохранение данных** - автоматическое сохранение информации о встречах

## ⚠️ Требования

**API Яндекс Телемост доступен только для пользователей Яндекс 360 для бизнеса!**

### Для работы необходимо:

1. **Аккаунт Яндекс 360 для бизнеса** - [Регистрация](https://360.yandex.ru/)
2. **Корпоративный домен** (например: `user@yourcompany.ru`)
3. **OAuth-приложение** с необходимыми разрешениями
4. **Бизнес-токен** от корпоративного аккаунта

## 📁 Структура проекта

```
telemost/
├── 📄 telemost_api.py       # Полнофункциональный API клиент
├── 📝 examples.py           # Простые примеры использования
├── 🚀 examples_advanced.py  # Расширенные примеры и демо
├── 🔍 test_token.py         # Диагностика токена
├── 🧪 test_new_token.py     # Тестирование нового токена
├── 🔐 check_permissions.py  # Проверка разрешений
├── 📦 requirements.txt      # Зависимости Python
├── 🔒 .env                  # Токены (не в git)
├── 📚 README.md            # Документация
└── 💾 *.json               # Сохраненные данные встреч
```

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка токена
```bash
# Создайте файл .env
echo "YANDEX_OAUTH_TOKEN=your_business_token_here" > .env
```

### 3. Запуск примеров
```bash
# Простые примеры
python examples.py

# Расширенная демонстрация
python examples_advanced.py

# Основной модуль
python telemost_api.py
```

## 🎯 Основные возможности API

### 📅 Управление встречами
- ✅ `create_meeting()` - Создание встреч с полной настройкой
- ✅ `get_meeting()` - Получение информации о встрече
- ✅ `update_meeting()` - Обновление настроек встречи
- ✅ `delete_meeting()` - Удаление встречи
- ✅ `list_meetings()` - Список встреч с пагинацией

### 👥 Управление соорганизаторами
- ✅ `get_meeting_cohosts()` - Получение списка соорганизаторов
- ✅ `add_meeting_cohost()` - Добавление соорганизатора
- ✅ `update_meeting_cohosts()` - Обновление списка соорганизаторов
- ✅ `remove_meeting_cohost()` - Удаление соорганизатора

### ⚙️ Настройки и утилиты
- ✅ `get_default_settings()` - Настройки по умолчанию
- ✅ `update_default_settings()` - Обновление настроек
- ✅ `save_meeting_data()` - Сохранение данных встреч
- ✅ `validate_meeting_data()` - Валидация данных
- ✅ `get_meeting_info_formatted()` - Красивое форматирование

### 🎬 Удобные методы (shortcuts)
- ✅ `create_simple_meeting()` - Простая встреча
- ✅ `create_meeting_with_stream()` - Встреча с трансляцией
- ✅ `create_meeting_with_cohosts()` - Встреча с соорганизаторами
- ✅ `create_advanced_meeting()` - Встреча со всеми параметрами

## 🔧 Примеры использования

### Простая встреча
```python
from telemost_api import TelemostAPI

api = TelemostAPI()
meeting = api.create_simple_meeting()
print(f"Ссылка: {meeting['join_url']}")
```

### Встреча с трансляцией
```python
meeting = api.create_meeting_with_stream(
    stream_title="Важная презентация",
    stream_description="Квартальные результаты",
    stream_access_level="ORGANIZATION"
)
```

### Продвинутая встреча
```python
meeting = api.create_advanced_meeting(
    waiting_room_level="ADMINS",
    stream_title="Корпоративный вебинар",
    cohost_emails=["ceo@company.com", "cto@company.com"]
)
```

## 🛡️ Обработка ошибок

```python
from telemost_api import TelemostAPI, TelemostAuthError, TelemostValidationError

try:
    api = TelemostAPI()
    meeting = api.create_simple_meeting()
except TelemostAuthError:
    print("Проверьте токен в .env файле")
except TelemostValidationError as e:
    print(f"Ошибка валидации: {e}")
```

## 📊 Логирование

Встроенное логирование всех операций:
```python
import logging
logging.basicConfig(level=logging.INFO)
# Теперь все операции будут логироваться
```

## 🔑 Получение бизнес-токена

### 1. Создание OAuth-приложения
- Перейдите в [Яндекс OAuth](https://oauth.yandex.ru/)
- Создайте новое приложение
- Укажите платформы и callback URL

### 2. Настройка разрешений
Добавьте следующие разрешения в разделе "Доступ к данным":
- ✅ `telemost-api:conferences.create` - создание встреч
- ✅ `telemost-api:conferences.read` - чтение данных встреч
- ✅ `telemost-api:conferences.update` - обновление встреч
- ✅ `telemost-api:conferences.delete` - удаление встреч

### 3. Получение токена
```bash
# Замените YOUR_CLIENT_ID на ваш реальный Client ID
https://oauth.yandex.ru/authorize?response_type=token&client_id=YOUR_CLIENT_ID
```

### 4. Тестирование токена
```bash
python test_new_token.py
# Вставьте новый токен для проверки
```

## 🔒 Настройка .env файла

```env
# OAuth токен для Яндекс Телемост API (обязательно)
YANDEX_OAUTH_TOKEN=y0_AgAAAABl...

# Дополнительные настройки (опционально)
CLIENT_ID=d6ae5c6eb0a34355a...

# Настройки логирования
LOG_LEVEL=INFO
```

## 🧪 Тестирование

```bash
# Проверка токена
python test_token.py

# Проверка разрешений
python check_permissions.py

# Тестирование нового токена
python test_new_token.py
```

## 🔄 Альтернативы

Если Яндекс 360 недоступен:
- **Zoom API** - для интеграции с Zoom
- **Google Meet API** - для Google Workspace
- **Microsoft Teams API** - для Microsoft 365
- **Jitsi Meet** - открытое решение

---

## 📞 Поддержка

- 📧 **Issues**: Создавайте issue для вопросов и предложений
- 📚 **Документация**: Изучите примеры в `examples_advanced.py`
- 🚀 **Вклад**: Pull requests приветствуются!