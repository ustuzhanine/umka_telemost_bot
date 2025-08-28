#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрая проверка типа аккаунта по токену
"""

import requests

def check_account_type(token):
    """Проверяем тип аккаунта по токену"""
    
    if not token:
        print("❌ Токен не указан")
        return
    
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
            
            print(f"👤 Логин: {login}")
            print(f"📧 Email: {email}")
            
            # Анализируем тип аккаунта
            if email == 'N/A' or email.endswith('@yandex.ru'):
                print("❌ ТИП: ЛИЧНЫЙ АККАУНТ")
                print("   Нужен корпоративный аккаунт с доменом @yourcompany.ru")
                return False
            elif '@' in email and not email.endswith(('@yandex.ru', '@yandex.com')):
                print("✅ ТИП: КОРПОРАТИВНЫЙ АККАУНТ")
                print(f"   Домен: {email.split('@')[1]}")
                return True
            else:
                print("⚠️ ТИП: НЕОПРЕДЕЛЕН")
                return False
        else:
            print(f"❌ Ошибка получения данных: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🔍 ПРОВЕРКА ТИПА АККАУНТА")
    print("=" * 40)
    
    token = input("Введите токен для проверки: ").strip()
    
    if token:
        is_business = check_account_type(token)
        
        if is_business:
            print("\n🎉 Отлично! Этот токен подойдет для API Телемост")
        else:
            print("\n💡 НУЖНО:")
            print("1. Создать корпоративного пользователя в Яндекс 360")
            print("2. Получить токен от корпоративного аккаунта")
            print("3. Убедиться, что домен подтвержден")
    else:
        print("❌ Токен не введен")
