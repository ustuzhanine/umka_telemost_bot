#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки разрешений токена
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_token_info():
    """Проверяем информацию о токене через Яндекс API"""
    token = os.getenv('YANDEX_OAUTH_TOKEN')
    
    if not token:
        print("❌ Токен не найден")
        return
    
    # Проверяем токен через Яндекс API
    url = "https://login.yandex.ru/info"
    headers = {
        'Authorization': f'OAuth {token}'
    }
    
    try:
        print("🔍 Проверяем информацию о токене...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            info = response.json()
            print("✅ Токен действительный!")
            print(f"ID пользователя: {info.get('id', 'N/A')}")
            print(f"Email: {info.get('default_email', 'N/A')}")
            print(f"Логин: {info.get('login', 'N/A')}")
            
            # Проверяем разрешения (scopes)
            client_id = info.get('client_id')
            if client_id:
                print(f"Client ID приложения: {client_id}")
            
        else:
            print(f"❌ Ошибка при проверке токена: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")

def test_minimal_api_call():
    """Делаем минимальный вызов к API для проверки доступа"""
    token = os.getenv('YANDEX_OAUTH_TOKEN')
    
    # Попробуем GET запрос (если есть read разрешения)
    url = "https://cloud-api.yandex.net/v1/telemost-api/conferences"
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        print("🔍 Проверяем доступ к API Телемост (GET)...")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Есть доступ на чтение!")
            data = response.json()
            print(f"Количество встреч: {len(data.get('conferences', []))}")
        elif response.status_code == 403:
            print("❌ Нет разрешения telemost-api:conferences.read")
        elif response.status_code == 401:
            print("❌ Проблема с авторизацией")
        else:
            print(f"❌ Неожиданный ответ: {response.status_code}")
            try:
                print(response.json())
            except:
                print(response.text)
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")

if __name__ == "__main__":
    print("🔍 Проверка разрешений токена")
    print("=" * 40)
    
    check_token_info()
    print()
    test_minimal_api_call()
    
    print("\n" + "=" * 40)
    print("📋 Инструкция по исправлению:")
    print("1. Перейдите на https://oauth.yandex.ru/")
    print("2. Найдите ваше приложение")
    print("3. В разделе 'Доступ к данным' добавьте:")
    print("   - telemost-api:conferences.create")
    print("   - telemost-api:conferences.read") 
    print("   - telemost-api:conferences.update")
    print("4. Сохраните изменения")
    print("5. Получите новый токен")
