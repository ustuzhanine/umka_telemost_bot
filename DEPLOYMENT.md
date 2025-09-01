# Инструкция по развертыванию Telemost Telegram Web App

## 🚀 Быстрое развертывание

### 1. Подготовка

```bash
# Клонируйте репозиторий
git clone https://github.com/AVRSLLC/umka_telemost.git
cd umka_telemost

# Создайте файл .env на основе примера
cp env.example .env

# Отредактируйте .env файл с вашими данными
nano .env

# Установите правильные права
chmod 600 .env
```

### 2. Запуск с Docker (рекомендуется)

```bash
# Запуск в фоне
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### 3. Проверка работоспособности

```bash
# Проверка API
curl http://localhost:5000/api/health

# Проверка Web App
curl http://localhost:5000/

# Создание тестовой встречи
curl -X POST http://localhost:5000/api/meetings \
  -H "Content-Type: application/json" \
  -d '{"title":"Тестовая встреча","description":"Проверка развертывания"}'
```

## 🔧 Ручное развертывание

### На сервере

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
python src/main.py
```

### С Gunicorn (для продакшена)

```bash
# Установка Gunicorn
pip install gunicorn

# Запуск с Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

## 🌐 Настройка домена и SSL

### 1. DNS настройка

Настройте DNS запись для домена `tg.umka-contur.ru`:

```
Type: A
Name: tg
Value: YOUR_SERVER_IP
```

### 2. SSL сертификат (Let's Encrypt)

```bash
# Установка Certbot
sudo apt update
sudo apt install certbot

# Получение сертификата
sudo certbot certonly --standalone -d tg.umka-contur.ru

# Автоматическое обновление сертификатов
sudo crontab -e
# Добавить строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Nginx (рекомендуется)

Создайте конфигурацию Nginx:

```nginx
server {
    listen 80;
    server_name tg.umka-contur.ru;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tg.umka-contur.ru;

    ssl_certificate /etc/letsencrypt/live/tg.umka-contur.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tg.umka-contur.ru/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Статические файлы
    location /static/ {
        alias /path/to/your/app/src/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🤖 Настройка Telegram бота

### 1. Создание бота

1. Перейдите к [@BotFather](https://t.me/botfather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Сохраните токен бота

### 2. Настройка Web App

1. Отправьте `/setmenubutton` @BotFather
2. Выберите вашего бота
3. Выберите "Web App"
4. Укажите URL: `https://tg.umka-contur.ru`
5. Добавьте описание

### 3. Настройка Menu Button

1. Отправьте `/setmenubutton` @BotFather
2. Выберите бота
3. Укажите текст: "Создать встречу"
4. Укажите URL: `https://tg.umka-contur.ru`

## 📋 Необходимые переменные окружения

Создайте файл `.env` со следующими переменными:

```env
# Обязательные
YANDEX_OAUTH_TOKEN=your_yandex_oauth_token

# Опциональные
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
CLIENT_ID=your_client_id
CORPORATE_EMAIL=admin@umka.pro
DOMAIN=umka.pro

# Настройки сервера
PORT=5000
HOST=0.0.0.0
DEBUG=false
SECRET_KEY=your_secret_key
```

## 🔍 Проверка развертывания

### 1. Проверка API

```bash
curl https://tg.umka-contur.ru/api/health
```

Ожидаемый ответ:
```json
{
  "status": "healthy",
  "telemost_api": "available"
}
```

### 2. Проверка Web App

Откройте в браузере: `https://tg.umka-contur.ru`

### 3. Проверка Telegram бота

1. Найдите вашего бота в Telegram
2. Нажмите кнопку "Создать встречу"
3. Web App должен открыться

## 🐛 Устранение неисправностей

### Приложение не запускается

```bash
# Проверьте логи Docker
docker-compose logs

# Проверьте переменные окружения
cat .env

# Проверьте порт
netstat -tlnp | grep 5000
```

### Web App не открывается в Telegram

1. Убедитесь, что домен доступен по HTTPS
2. Проверьте настройки бота в @BotFather
3. Проверьте CORS настройки в коде

### API возвращает ошибки

1. Проверьте Yandex OAuth токен
2. Проверьте права доступа к Yandex Telemost API
3. Проверьте логи приложения

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи приложения
2. Убедитесь, что все переменные окружения установлены
3. Проверьте сетевые настройки и firewall
4. Свяжитесь с разработчиками
