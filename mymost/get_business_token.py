#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Помощник для получения корпоративного токена Яндекс 360
"""

import webbrowser
import sys

def get_business_token():
    """Пошаговое получение корпоративного токена"""
    
    print("🏢 ПОЛУЧЕНИЕ КОРПОРАТИВНОГО ТОКЕНА ЯНДЕКС 360")
    print("=" * 60)
    
    print("\n📋 ШАГ 1: Подготовка")
    print("Убедитесь, что у вас есть:")
    print("✅ Корпоративный аккаунт Яндекс 360 (admin@yourcompany.ru)")
    print("✅ Подтвержденный домен организации")
    print("✅ Активный платный тариф")
    
    input("\n📍 Нажмите Enter, когда будете готовы...")
    
    print("\n🔧 ШАГ 2: Создание OAuth приложения")
    print("1. Откроется страница OAuth Яндекс")
    print("2. Войдите под КОРПОРАТИВНЫМ аккаунтом (admin@yourcompany.ru)")
    print("3. Создайте новое приложение")
    
    # Открываем OAuth страницу
    oauth_url = "https://oauth.yandex.ru/"
    print(f"\n🌐 Открываю: {oauth_url}")
    
    try:
        webbrowser.open(oauth_url)
        print("✅ Страница открыта в браузере")
    except:
        print(f"❌ Не удалось открыть автоматически. Перейдите вручную: {oauth_url}")
    
    input("\n📍 Создали приложение? Нажмите Enter...")
    
    print("\n⚙️ ШАГ 3: Настройка разрешений")
    print("В созданном приложении добавьте разрешения:")
    print("✅ telemost-api:conferences.create")
    print("✅ telemost-api:conferences.read") 
    print("✅ telemost-api:conferences.update")
    print("✅ telemost-api:conferences.delete")
    
    client_id = input("\n🆔 Введите Client ID вашего приложения: ").strip()
    
    if not client_id:
        print("❌ Client ID обязателен!")
        return
    
    print(f"\n✅ Client ID: {client_id}")
    
    print("\n🔑 ШАГ 4: Получение токена")
    
    # Формируем URL для получения токена
    scopes = [
        "telemost-api:conferences.create",
        "telemost-api:conferences.read", 
        "telemost-api:conferences.update",
        "telemost-api:conferences.delete"
    ]
    
    scope_string = "%20".join(scopes)
    token_url = f"https://oauth.yandex.ru/authorize?response_type=token&client_id={client_id}&scope={scope_string}"
    
    print("1. Откроется страница авторизации")
    print("2. Войдите под КОРПОРАТИВНЫМ аккаунтом")
    print("3. Разрешите доступ к данным")
    print("4. Скопируйте токен из URL после #access_token=")
    
    print(f"\n🌐 Открываю страницу авторизации...")
    print(f"URL: {token_url}")
    
    try:
        webbrowser.open(token_url)
        print("✅ Страница авторизации открыта")
    except:
        print(f"❌ Перейдите вручную: {token_url}")
    
    print("\n📝 После авторизации URL будет выглядеть так:")
    print("https://oauth.yandex.ru/verification_code#access_token=y0_AgA...&token_type=bearer&expires_in=31536000")
    print("                                                    ^^^^^^^^")
    print("                                                    Ваш токен")
    
    token = input("\n🔑 Вставьте полученный токен: ").strip()
    
    if not token:
        print("❌ Токен не введен!")
        return
    
    if not token.startswith(('y0_AgA', 'y0__x')):
        print("⚠️ Предупреждение: токен не начинается с y0_AgA или y0__x")
    
    print(f"\n✅ Токен получен: {token[:20]}...{token[-10:]}")
    
    # Сохраняем токен в файл
    env_content = f"""# Корпоративный токен Яндекс 360 для API Телемост
YANDEX_OAUTH_TOKEN={token}

# Дополнительные параметры
CLIENT_ID={client_id}
TOKEN_TYPE=bearer
EXPIRES_IN=31536000

# Настройки логирования
LOG_LEVEL=INFO
"""
    
    with open("business_token.env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("\n💾 Токен сохранен в файл: business_token.env")
    
    print("\n🧪 ШАГ 5: Тестирование токена")
    print("Сейчас протестируем ваш корпоративный токен...")
    
    # Тестируем токен
    import requests
    
    try:
        # Проверяем авторизацию
        print("\n🔍 Проверка авторизации...")
        response = requests.get(
            'https://login.yandex.ru/info',
            headers={'Authorization': f'OAuth {token}'},
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            login = user_info.get('login', 'N/A')
            email = user_info.get('default_email', 'N/A')
            
            print(f"✅ Авторизация успешна!")
            print(f"👤 Пользователь: {login}")
            print(f"📧 Email: {email}")
            
            # Проверяем тип аккаунта
            if email.endswith(('.ru', '.com')) and '@' in email and not email.endswith('@yandex.ru'):
                print("🏢 ТИП: КОРПОРАТИВНЫЙ АККАУНТ ✅")
            else:
                print("⚠️ ВНИМАНИЕ: Возможно, это не корпоративный аккаунт")
        
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
            print("🎉 УСПЕХ! API Телемост работает!")
            print(f"📋 Тестовая встреча создана: {meeting['id']}")
            print(f"🔗 Ссылка: {meeting['join_url']}")
            
            print("\n✅ ВСЕ ГОТОВО ДЛЯ РАБОТЫ!")
            print("Скопируйте business_token.env в .env:")
            print("cp business_token.env .env")
            
        else:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('message', 'Неизвестная ошибка')
            
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"Сообщение: {error_msg}")
            
            if response.status_code == 403:
                if 'ApiRestrictedToOrganizations' in error_data.get('error', ''):
                    print("\n💡 РЕШЕНИЕ:")
                    print("1. Убедитесь, что токен получен от корпоративного аккаунта")
                    print("2. Проверьте, что домен подтвержден в Яндекс 360")
                    print("3. Убедитесь, что тариф активен и оплачен")
    
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
    
    print("\n" + "=" * 60)
    print("📋 СЛЕДУЮЩИЕ ШАГИ:")
    print("1. Скопируйте токен в .env: cp business_token.env .env")
    print("2. Протестируйте: python check_token_type.py")
    print("3. Запустите примеры: python examples.py")

if __name__ == "__main__":
    get_business_token()
