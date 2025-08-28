#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание OAuth приложения с корпоративного аккаунта Яндекс 360
"""

import webbrowser
import requests

def create_business_oauth_app():
    """Создание OAuth приложения для корпоративного аккаунта"""
    
    print("🏢 СОЗДАНИЕ КОРПОРАТИВНОГО OAUTH ПРИЛОЖЕНИЯ")
    print("=" * 60)
    
    print("\n📋 ТРЕБОВАНИЯ:")
    print("✅ Корпоративный аккаунт Яндекс 360 (admin@yourcompany.ru)")
    print("✅ Подтвержденный домен организации") 
    print("✅ Активный платный тариф")
    print("✅ Права администратора в организации")
    
    print("\n⚠️  ВАЖНО:")
    print("🔴 НЕ используйте личный аккаунт (ustuzhanine@yandex.ru)")
    print("🟢 Используйте ТОЛЬКО корпоративный аккаунт (admin@yourcompany.ru)")
    
    input("\n📍 Убедились, что все готово? Нажмите Enter...")
    
    # Проверяем текущий аккаунт
    print("\n🔍 ПРОВЕРКА ТЕКУЩЕГО АККАУНТА")
    print("Сейчас проверим, под каким аккаунтом вы авторизованы в браузере...")
    
    # Открываем страницу проверки аккаунта
    check_url = "https://passport.yandex.ru/profile"
    print(f"\n🌐 Открываю проверку аккаунта: {check_url}")
    
    try:
        webbrowser.open(check_url)
        print("✅ Страница открыта")
    except:
        print(f"❌ Перейдите вручную: {check_url}")
    
    print("\n📝 Проверьте в открывшейся странице:")
    print("👤 Логин должен быть: admin@yourcompany.ru (или другой корпоративный)")
    print("❌ НЕ должно быть: ustuzhanine, urionfidel или другие личные аккаунты")
    
    account_ok = input("\n✅ Вы авторизованы под КОРПОРАТИВНЫМ аккаунтом? (y/n): ").lower().strip()
    
    if account_ok != 'y':
        print("\n🔄 СМЕНА АККАУНТА:")
        print("1. Выйдите из текущего аккаунта")
        print("2. Войдите под корпоративным аккаунтом")
        print("3. Запустите скрипт заново")
        return
    
    print("\n🔧 СОЗДАНИЕ OAUTH ПРИЛОЖЕНИЯ")
    
    # Открываем OAuth страницу
    oauth_url = "https://oauth.yandex.ru/"
    print(f"\n🌐 Открываю OAuth консоль: {oauth_url}")
    
    try:
        webbrowser.open(oauth_url)
        print("✅ OAuth консоль открыта")
    except:
        print(f"❌ Перейдите вручную: {oauth_url}")
    
    print("\n📝 В OAuth консоли:")
    print("1. Нажмите 'Создать новое приложение'")
    print("2. Заполните данные:")
    print("   • Название: 'Telemost API Integration'")
    print("   • Описание: 'API для создания встреч в Телемост'")
    print("   • Платформы: 'Серверное приложение'")
    print("3. В разделе 'Доступ к данным' добавьте разрешения:")
    print("   ✅ telemost-api:conferences.create")
    print("   ✅ telemost-api:conferences.read")
    print("   ✅ telemost-api:conferences.update") 
    print("   ✅ telemost-api:conferences.delete")
    print("4. Сохраните приложение")
    
    input("\n📍 Создали приложение? Нажмите Enter...")
    
    client_id = input("\n🆔 Введите Client ID нового приложения: ").strip()
    
    if not client_id:
        print("❌ Client ID обязателен!")
        return
    
    print(f"\n✅ Client ID: {client_id}")
    
    # Формируем URL для получения токена
    print("\n🔑 ПОЛУЧЕНИЕ ТОКЕНА")
    
    scopes = [
        "telemost-api:conferences.create",
        "telemost-api:conferences.read",
        "telemost-api:conferences.update", 
        "telemost-api:conferences.delete"
    ]
    
    scope_string = "%20".join(scopes)
    token_url = f"https://oauth.yandex.ru/authorize?response_type=token&client_id={client_id}&scope={scope_string}"
    
    print("🌐 Открываю страницу авторизации...")
    print("\n⚠️  КРИТИЧЕСКИ ВАЖНО:")
    print("🔴 Убедитесь, что авторизуетесь под КОРПОРАТИВНЫМ аккаунтом!")
    print("🔴 Если откроется личный аккаунт - выйдите и войдите под корпоративным!")
    
    try:
        webbrowser.open(token_url)
        print("✅ Страница авторизации открыта")
    except:
        print(f"❌ Перейдите вручную: {token_url}")
    
    print(f"\n🔗 URL авторизации:")
    print(f"{token_url}")
    
    print("\n📝 После авторизации:")
    print("1. Разрешите доступ к данным")
    print("2. Скопируйте токен из URL после #access_token=")
    print("3. Токен должен начинаться с y0_AgA или y0__x")
    
    token = input("\n🔑 Вставьте полученный токен: ").strip()
    
    if not token:
        print("❌ Токен не введен!")
        return
    
    print(f"\n✅ Токен получен: {token[:20]}...{token[-10:]}")
    
    # Тестируем токен
    print("\n🧪 ТЕСТИРОВАНИЕ КОРПОРАТИВНОГО ТОКЕНА")
    
    try:
        # Проверяем тип аккаунта
        print("🔍 Проверка типа аккаунта...")
        response = requests.get(
            'https://login.yandex.ru/info',
            headers={'Authorization': f'OAuth {token}'},
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            login = user_info.get('login', 'N/A')
            email = user_info.get('default_email', 'N/A')
            
            print(f"👤 Пользователь: {login}")
            print(f"📧 Email: {email}")
            
            # Проверяем тип аккаунта
            if email == 'N/A' or email.endswith(('@yandex.ru', '@yandex.com')):
                print("❌ ЭТО ЛИЧНЫЙ АККАУНТ!")
                print("🔄 Нужно получить токен от корпоративного аккаунта")
                print("💡 Выйдите из личного аккаунта и войдите под корпоративным")
                return
            else:
                print("✅ ЭТО КОРПОРАТИВНЫЙ АККАУНТ!")
                domain = email.split('@')[1] if '@' in email else 'unknown'
                print(f"🏢 Домен организации: {domain}")
        
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
            print("🎉 УСПЕХ! API ТЕЛЕМОСТ РАБОТАЕТ!")
            print(f"📋 ID тестовой встречи: {meeting['id']}")
            print(f"🔗 Ссылка: {meeting['join_url']}")
            
            # Сохраняем рабочий токен
            env_content = f"""# РАБОЧИЙ КОРПОРАТИВНЫЙ ТОКЕН ЯНДЕКС 360
YANDEX_OAUTH_TOKEN={token}

# Данные приложения
CLIENT_ID={client_id}
TOKEN_TYPE=bearer
EXPIRES_IN=31536000

# Настройки
LOG_LEVEL=INFO

# Информация о тесте
# Пользователь: {login}
# Email: {email}
# Тест пройден: {response.status_code == 201}
"""
            
            with open("working_business_token.env", "w", encoding="utf-8") as f:
                f.write(env_content)
            
            print(f"\n💾 Рабочий токен сохранен: working_business_token.env")
            
            print("\n🚀 ГОТОВО К РАБОТЕ!")
            print("Скопируйте токен в основной .env:")
            print("cp working_business_token.env .env")
            
        else:
            error_data = response.json() if response.content else {}
            print(f"❌ API Телемост не работает: {response.status_code}")
            print(f"Ошибка: {error_data.get('message', 'Неизвестная ошибка')}")
            
            if 'ApiRestrictedToOrganizations' in error_data.get('error', ''):
                print("\n💡 ВОЗМОЖНЫЕ ПРИЧИНЫ:")
                print("1. Токен все еще от личного аккаунта")
                print("2. Домен не подтвержден в Яндекс 360")
                print("3. Тариф не активен или не оплачен")
                print("4. У пользователя нет прав в организации")
    
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
    
    print("\n" + "=" * 60)
    print("📋 ЕСЛИ ТОКЕН НЕ РАБОТАЕТ:")
    print("1. Убедитесь, что используете корпоративный аккаунт")
    print("2. Проверьте, что домен подтвержден в admin.yandex.ru")
    print("3. Убедитесь, что тариф активен и оплачен")
    print("4. Попробуйте создать нового корпоративного пользователя")

if __name__ == "__main__":
    create_business_oauth_app()
