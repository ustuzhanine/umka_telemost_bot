#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования нового токена перед обновлением .env
"""

import requests
import json
from datetime import datetime

def test_token(token):
    """Тестируем новый токен"""
    if not token:
        print("❌ Токен не указан")
        return False
    
    print(f"🔍 Тестируем токен: {token[:20]}...")
    
    # Проверяем авторизацию
    info_url = "https://login.yandex.ru/info"
    headers = {'Authorization': f'OAuth {token}'}
    
    try:
        response = requests.get(info_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Ошибка авторизации: {response.status_code}")
            return False
        
        user_info = response.json()
        print(f"✅ Авторизация OK. Пользователь: {user_info.get('login', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Ошибка при проверке авторизации: {e}")
        return False
    
    # Тестируем создание встречи
    api_url = "https://cloud-api.yandex.net/v1/telemost-api/conferences"
    api_headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json'
    }
    
    data = {"waiting_room_level": "PUBLIC"}
    
    try:
        print("🚀 Создаем тестовую встречу...")
        response = requests.post(api_url, headers=api_headers, json=data, timeout=30)
        
        if response.status_code == 201:
            meeting = response.json()
            print("✅ Встреча успешно создана!")
            print(f"📋 ID: {meeting['id']}")
            print(f"🔗 Ссылка: {meeting['join_url']}")
            
            # Сохраняем результат
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_meeting_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(meeting, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Данные сохранены в: {filename}")
            return True
            
        else:
            print(f"❌ Ошибка создания встречи: {response.status_code}")
            try:
                error = response.json()
                print(f"Детали: {error}")
            except:
                print(f"Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при создании встречи: {e}")
        return False

if __name__ == "__main__":
    print("🔑 Тестирование нового токена")
    print("=" * 50)
    
    # Запрашиваем токен у пользователя
    print("Вставьте новый токен (или нажмите Enter для выхода):")
    new_token = input().strip()
    
    if not new_token:
        print("Выход...")
        exit()
    
    if test_token(new_token):
        print("\n" + "=" * 50)
        print("✅ Токен работает отлично!")
        print("Теперь обновите файл .env:")
        print(f"YANDEX_OAUTH_TOKEN={new_token}")
    else:
        print("\n" + "=" * 50)
        print("❌ Токен не работает. Попробуйте получить новый.")
