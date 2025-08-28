#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для определения типа токена Яндекс (личный vs корпоративный)
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_token():
    """Анализируем тип токена"""
    token = os.getenv('YANDEX_OAUTH_TOKEN')
    
    if not token:
        print("❌ Токен не найден в .env файле")
        return
    
    print("🔍 АНАЛИЗ ТОКЕНА ЯНДЕКС")
    print("=" * 50)
    print(f"📋 Токен: {token[:20]}...{token[-10:]}")
    print(f"📏 Длина: {len(token)} символов")
    
    # Проверяем формат
    if token.startswith(('y0_AgA', 'y0__x')):
        print("✅ Формат токена корректный")
    else:
        print("⚠️ Неожиданный формат токена")
    
    # Получаем информацию о пользователе
    print("\n🔍 Информация о пользователе:")
    try:
        response = requests.get(
            'https://login.yandex.ru/info',
            headers={'Authorization': f'OAuth {token}'},
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            
            login = user_info.get('login', 'N/A')
            email = user_info.get('default_email', 'N/A')
            client_id = user_info.get('client_id', 'N/A')
            
            print(f"👤 Логин: {login}")
            print(f"📧 Email: {email}")
            print(f"🆔 Client ID: {client_id}")
            
            # Анализируем тип аккаунта
            print("\n🏢 АНАЛИЗ ТИПА АККАУНТА:")
            
            if email.endswith(('@yandex.ru', '@yandex.com', '@gmail.com')):
                print("❌ ТИП: ЛИЧНЫЙ АККАУНТ")
                print("   • Домен: Публичный (@yandex.ru, @gmail.com)")
                print("   • Доступ к Телемост: НЕТ")
                print("   • Нужно: Корпоративный аккаунт Яндекс 360")
            else:
                print("✅ ТИП: КОРПОРАТИВНЫЙ АККАУНТ")
                print(f"   • Домен: Корпоративный ({email.split('@')[1]})")
                print("   • Доступ к Телемост: ВОЗМОЖЕН")
                
        else:
            print(f"❌ Ошибка получения данных: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тестируем доступ к Телемост API
    print("\n🎥 ТЕСТ ДОСТУПА К ТЕЛЕМОСТ:")
    try:
        response = requests.post(
            'https://cloud-api.yandex.net/v1/telemost-api/conferences',
            headers={
                'Authorization': f'OAuth {token}',
                'Content-Type': 'application/json'
            },
            json={'waiting_room_level': 'PUBLIC'},
            timeout=10
        )
        
        if response.status_code == 201:
            print("🎉 УСПЕХ! Доступ к Телемост API есть!")
            meeting = response.json()
            print(f"📋 Создана тестовая встреча: {meeting['id']}")
        elif response.status_code == 403:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('message', 'Доступ запрещен')
            
            if 'ApiRestrictedToOrganizations' in error_data.get('error', ''):
                print("❌ ДОСТУП ЗАПРЕЩЕН: Нужен корпоративный аккаунт")
                print("   • Ошибка: ApiRestrictedToOrganizations")
                print("   • Решение: Зарегистрируйтесь в Яндекс 360 для бизнеса")
            else:
                print(f"❌ ДОСТУП ЗАПРЕЩЕН: {error_msg}")
        else:
            print(f"❌ Неожиданная ошибка: {response.status_code}")
            print(f"   Ответ: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Ошибка тестирования API: {e}")
    
    print("\n" + "=" * 50)
    print("💡 РЕКОМЕНДАЦИИ:")
    print("1. Для Телемост API нужен корпоративный домен")
    print("2. Зарегистрируйтесь в https://360.yandex.ru/")
    print("3. Создайте организацию с собственным доменом")
    print("4. Получите токен от корпоративного аккаунта")

if __name__ == "__main__":
    analyze_token()
