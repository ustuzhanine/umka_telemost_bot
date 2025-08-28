#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Подробная инструкция по настройке разрешений OAuth приложения
"""

import webbrowser

def show_oauth_permissions_guide():
    """Показывает подробную инструкцию по настройке разрешений"""
    
    print("🔧 НАСТРОЙКА РАЗРЕШЕНИЙ OAUTH ПРИЛОЖЕНИЯ")
    print("=" * 50)
    
    print("\n📍 ШАГ 1: Откройте OAuth консоль")
    oauth_url = "https://oauth.yandex.ru/"
    print(f"URL: {oauth_url}")
    
    try:
        webbrowser.open(oauth_url)
        print("✅ OAuth консоль открыта в браузере")
    except:
        print("❌ Перейдите вручную по ссылке выше")
    
    print("\n📍 ШАГ 2: Найдите ваше приложение")
    print("• В списке приложений найдите созданное приложение")
    print("• Нажмите на НАЗВАНИЕ приложения (не на иконки)")
    
    print("\n📍 ШАГ 3: Найдите раздел разрешений")
    print("Ищите один из этих разделов:")
    print("🔹 'Доступ к данным'")
    print("🔹 'Data access'") 
    print("🔹 'Permissions'")
    print("🔹 'Права доступа'")
    print("🔹 'Scopes'")
    
    print("\n📍 ШАГ 4: Добавьте разрешения")
    print("В поле поиска или списке найдите и отметьте:")
    
    permissions = [
        "telemost-api:conferences.create",
        "telemost-api:conferences.read", 
        "telemost-api:conferences.update",
        "telemost-api:conferences.delete"
    ]
    
    for i, perm in enumerate(permissions, 1):
        print(f"✅ {i}. {perm}")
    
    print("\n📍 ШАГ 5: Сохраните изменения")
    print("• Нажмите 'Сохранить' или 'Save'")
    print("• Дождитесь подтверждения")
    
    print("\n" + "=" * 50)
    print("🚨 ЕСЛИ НЕ ВИДИТЕ РАЗРЕШЕНИЯ TELEMOST:")
    print("1. Убедитесь, что приложение создано с корпоративного аккаунта")
    print("2. Проверьте, что у вас активен Яндекс 360 для бизнеса")
    print("3. Убедитесь, что домен подтвержден")
    print("4. Попробуйте обновить страницу")
    
    input("\n📍 Настроили разрешения? Нажмите Enter для продолжения...")
    
    # Получаем Client ID
    client_id = input("\n🆔 Введите Client ID приложения: ").strip()
    
    if client_id:
        print(f"\n✅ Client ID: {client_id}")
        
        # Генерируем URL для получения токена
        scopes = "%20".join(permissions)
        token_url = f"https://oauth.yandex.ru/authorize?response_type=token&client_id={client_id}&scope={scopes}"
        
        print("\n🔑 ПОЛУЧЕНИЕ ТОКЕНА")
        print("Сейчас откроется страница для получения токена...")
        print("\n⚠️  ВАЖНО: Авторизуйтесь под КОРПОРАТИВНЫМ аккаунтом!")
        
        try:
            webbrowser.open(token_url)
            print("✅ Страница авторизации открыта")
        except:
            print("❌ Перейдите вручную:")
            print(token_url)
        
        print("\n📝 После авторизации:")
        print("1. Разрешите доступ к данным")
        print("2. Скопируйте токен из URL после #access_token=")
        
        token = input("\n🔑 Вставьте полученный токен: ").strip()
        
        if token:
            print(f"\n✅ Токен получен: {token[:20]}...{token[-10:]}")
            
            # Сохраняем в файл
            env_content = f"""# Корпоративный токен с правильными разрешениями
YANDEX_OAUTH_TOKEN={token}
CLIENT_ID={client_id}
LOG_LEVEL=INFO
"""
            
            with open("new_business_token.env", "w", encoding="utf-8") as f:
                f.write(env_content)
            
            print("💾 Токен сохранен в: new_business_token.env")
            
            # Тестируем токен
            print("\n🧪 ТЕСТИРОВАНИЕ ТОКЕНА...")
            test_token(token)
        else:
            print("❌ Токен не введен")
    else:
        print("❌ Client ID не введен")

def test_token(token):
    """Быстрое тестирование токена"""
    import requests
    
    try:
        # Проверяем авторизацию
        print("🔍 Проверка авторизации...")
        response = requests.get(
            'https://login.yandex.ru/info',
            headers={'Authorization': f'OAuth {token}'},
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            login = user_info.get('login', 'N/A')
            email = user_info.get('default_email', 'N/A')
            
            print(f"✅ Авторизация успешна")
            print(f"👤 Пользователь: {login}")
            print(f"📧 Email: {email}")
            
            # Проверяем тип аккаунта
            if email.endswith(('@yandex.ru', '@yandex.com')) or email == 'N/A':
                print("⚠️  Это может быть личный аккаунт")
            else:
                print("✅ Корпоративный аккаунт")
        
        # Тестируем API Телемост
        print("\n🎥 Тестирование API Телемост...")
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
            meeting = response.json()
            print("🎉 УСПЕХ! API работает!")
            print(f"📋 Тестовая встреча: {meeting['id']}")
            print(f"🔗 Ссылка: {meeting['join_url']}")
            
            print("\n🚀 ВСЕ ГОТОВО!")
            print("Скопируйте токен в основной .env:")
            print("cp new_business_token.env .env")
            
        else:
            error_data = response.json() if response.content else {}
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"Сообщение: {error_data.get('message', 'Неизвестная ошибка')}")
            
            if 'ApiRestrictedToOrganizations' in str(error_data):
                print("\n💡 Проблема: Нужен корпоративный аккаунт")
                print("1. Убедитесь, что токен от корпоративного пользователя")
                print("2. Проверьте настройки Яндекс 360")
    
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")

if __name__ == "__main__":
    show_oauth_permissions_guide()
