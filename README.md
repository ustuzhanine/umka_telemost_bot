# Telemost Telegram Web App

Telegram Web App для создания встреч в Яндекс Телемост с возможностью отправки ссылок выбранным контактам.

## Возможности

- 🎥 Создание встреч в Яндекс Телемост
- ⚙️ Настройка уровня доступа и трансляции
- 📱 Интерфейс, адаптированный для Telegram Web App
- 📤 Отправка ссылок на встречу через Telegram Bot API
- 🎨 Поддержка темы Telegram

## Требования

- Python 3.11+
- Яндекс OAuth токен для Telemost API
- Telegram Bot Token (опционально, для отправки сообщений)

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd telemost_tg_app
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения в файле `.env`:
```env
# Обязательно
YANDEX_OAUTH_TOKEN=your_yandex_oauth_token

# Опционально (для отправки сообщений)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Корпоративные данные
CLIENT_ID=your_client_id
CORPORATE_EMAIL=admin@your-domain.com
CORPORATE_LOGIN=admin@your-domain.com
DOMAIN=your-domain.com
```

## Запуск

### Локальная разработка

```bash
source venv/bin/activate
python src/main.py
```

Приложение будет доступно по адресу: http://localhost:5000

### Развертывание

Для развертывания в продакшене используйте WSGI сервер, например Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

## API Endpoints

### Встречи

- `POST /api/meetings` - Создание встречи
- `GET /api/meetings` - Список встреч
- `GET /api/meetings/<id>` - Информация о встрече
- `PATCH /api/meetings/<id>` - Обновление встречи
- `DELETE /api/meetings/<id>` - Удаление встречи

### Отправка сообщений

- `POST /api/send-meeting` - Отправка ссылки на встречу контактам
- `GET /api/bot-status` - Статус Telegram бота

### Служебные

- `GET /api/health` - Проверка состояния API

## Структура проекта

```
telemost_tg_app/
├── src/
│   ├── static/
│   │   └── index.html          # Telegram Web App интерфейс
│   ├── routes/
│   │   ├── meetings.py         # API для встреч
│   │   └── user.py            # Пользователи (шаблон)
│   ├── models/
│   │   └── user.py            # Модели БД (шаблон)
│   ├── database/
│   │   └── app.db             # SQLite база данных
│   ├── telemost_api.py        # Клиент Telemost API
│   ├── telegram_bot.py        # Клиент Telegram Bot API
│   └── main.py               # Главный файл Flask приложения
├── venv/                     # Виртуальное окружение
├── requirements.txt          # Зависимости Python
├── .env                     # Переменные окружения
└── README.md               # Документация
```

## Настройка Telegram Web App

1. Создайте бота через @BotFather
2. Получите токен бота и добавьте в `.env`
3. Настройте Web App в боте:
   - Отправьте команду `/newapp` в @BotFather
   - Выберите вашего бота
   - Укажите URL вашего приложения
   - Добавьте описание и иконку

## Использование

1. Откройте Telegram Web App через вашего бота
2. Заполните форму создания встречи:
   - Название (опционально)
   - Описание (опционально)
   - Уровень доступа
   - Настройки трансляции (опционально)
3. Выберите контакты для отправки
4. Нажмите "Создать встречу"
5. Отправьте ссылку выбранным контактам

## Особенности

- **Адаптивный дизайн**: Интерфейс адаптирован для мобильных устройств
- **Тема Telegram**: Автоматическое применение цветовой схемы Telegram
- **Симуляция отправки**: Если токен бота не настроен, отправка симулируется
- **Обработка ошибок**: Подробная обработка ошибок API и сети
- **Логирование**: Детальное логирование всех операций

## Безопасность

- Все токены хранятся в переменных окружения
- CORS настроен для безопасного взаимодействия
- Валидация всех входящих данных
- Обработка ошибок без раскрытия внутренней информации

## Лицензия

MIT License

