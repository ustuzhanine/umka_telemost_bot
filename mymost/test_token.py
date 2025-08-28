#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования токена Яндекс Телемост API
"""

import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def test_token():
    """Тестируем токен"""
    token = os.getenv('YANDEX_OAUTH_TOKEN')
    
    print(f"Токен из .env: {token[:20]}..." if token else "Токен не найден")
    
    if not token:
        print("❌ YANDEX_OAUTH_TOKEN не найден в .env файле")
        return
    
    # Пробуем сделать запрос к API
    url = "https://cloud-api.yandex.net/v1/telemost-api/conferences"
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json'
    }
    
    # Минимальные данные для создания встречи
    data = {
        "waiting_room_level": "PUBLIC"
    }
    
    try:
        print("🔄 Тестируем токен...")
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Токен работает! Встреча создана успешно")
            result = response.json()
            print(f"ID встречи: {result['id']}")
            print(f"Ссылка: {result['join_url']}")
        elif response.status_code == 401:
            print("❌ Ошибка авторизации (401)")
            print("Возможные причины:")
            print("1. Токен устарел")
            print("2. Неправильный формат токена") 
            print("3. У приложения нет нужных разрешений")
            print("4. Токен не для Яндекс 360 для бизнеса")
        elif response.status_code == 403:
            print("❌ Доступ запрещен (403)")
            print("У приложения нет разрешения telemost-api:conferences.create")
        else:
            print(f"❌ Неожиданная ошибка: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Детали: {error_data}")
            except:
                print(f"Ответ: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")

def show_token_info():
    """Показываем информацию о токене"""
    token = os.getenv('YANDEX_OAUTH_TOKEN')
    
    if not token:
        print("❌ Токен не найден")
        return
        
    print("📋 Информация о токене:")
    print(f"Длина: {len(token)} символов")
    print(f"Начинается с: {token[:10]}...")
    print(f"Заканчивается на: ...{token[-10:]}")
    
    # Проверяем формат
    if token.startswith('y0_'):
        print("✅ Формат токена правильный (начинается с y0_)")
    else:
        print("⚠️  Токен не начинается с y0_ - возможно неправильный формат")

if __name__ == "__main__":
    print("🔍 Диагностика токена Яндекс Телемост API")
    print("=" * 50)
    
    show_token_info()
    print()
    test_token()
