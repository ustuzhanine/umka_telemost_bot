#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальная настройка корпоративного токена
"""

import webbrowser
import requests

def final_token_setup():
    """Финальная настройка корпоративного токена"""
    
    print("🎯 ФИНАЛЬНАЯ НАСТРОЙКА КОРПОРАТИВНОГО ТОКЕНА")
    print("=" * 60)
    
    print("\n✅ Отлично! У вас есть корпоративный администратор")
    
    print("\n🔄 ШАГ 1: СМЕНА АККАУНТА")
    print("Сейчас нужно переключиться на корпоративный аккаунт...")
    
    # Открываем страницу выхода
    logout_url = "https://passport.yandex.ru/passport?mode=logout"
    print(f"\n🚪 Открываю страницу выхода: {logout_url}")
    
    try:
        webbrowser.open(logout_url)
        print("✅ Страница выхода открыта")
    except:
        print("❌ Перейдите вручную для выхода")
    
    print("\n📝 На открывшейся странице:")
    print("1. Выйдите из текущего аккаунта (ustuzhanine)")
    print("2. Войдите под корпоративным администратором")
    
    corp_email = input("\n📧 Какой email у созданного администратора? (admin@yourcompany.ru): ").strip()
    
    if not corp_email or '@' not in corp_email:
        print("❌ Введите корректный корпоративный email!")
        return
    
    print(f"\n✅ Корпоративный email: {corp_email}")
    
    input(f"\n📍 Вошли под {corp_email}? Нажмите Enter...")
    
    print("\n🔧 ШАГ 2: СОЗДАНИЕ/НАСТРОЙКА OAUTH ПРИЛОЖЕНИЯ")
    
    # Проверяем, есть ли уже приложение
    has_app = input("\nУ вас уже есть OAuth приложение? (y/n): ").lower().strip()
    
    if has_app == 'n':
        print("\n🆕 Создаем новое OAuth приложение...")
        oauth_url = "https://oauth.yandex.ru/"
        
        try:
            webbrowser.open(oauth_url)
            print("✅ OAuth консоль открыта")
        except:
            print(f"Перейдите вручную: {oauth_url}")
        
        print("\n📝 В OAuth консоли:")
        print("1. Нажмите 'Создать приложение'")
        print("2. Название: 'Telemost API Corporate'")
        print("3. Описание: 'Corporate API for Telemost'")
        print("4. Платформы: 'Серверное приложение'")
        
        input("\n📍 Создали приложение? Нажмите Enter...")
    
    print("\n⚙️ ШАГ 3: НАСТРОЙКА РАЗРЕШЕНИЙ")
    print("В OAuth приложении найдите 'Доступ к данным' и добавьте:")
    print("✅ telemost-api:conferences.create")
    print("✅ telemost-api:conferences.read")
    print("✅ telemost-api:conferences.update")
    print("✅ telemost-api:conferences.delete")
    
    input("\n📍 Настроили разрешения? Нажмите Enter...")
    
    client_id = input("\n🆔 Введите Client ID приложения: ").strip()
    
    if not client_id:
        print("❌ Client ID обязателен!")
        return
    
    print(f"\n✅ Client ID: {client_id}")
    
    print("\n🔑 ШАГ 4: ПОЛУЧЕНИЕ КОРПОРАТИВНОГО ТОКЕНА")
    
    # Формируем URL для получения токена
    scopes = [
        "telemost-api:conferences.create",
        "telemost-api:conferences.read",
        "telemost-api:conferences.update",
        "telemost-api:conferences.delete"
    ]
    
    scope_string = "%20".join(scopes)
    token_url = f"https://oauth.yandex.ru/authorize?response_type=token&client_id={client_id}&scope={scope_string}"
    
    print("🌐 Открываю страницу авторизации...")
    print(f"\n⚠️  КРИТИЧЕСКИ ВАЖНО:")
    print(f"🟢 Должен быть авторизован: {corp_email}")
    print(f"🔴 НЕ должно быть: ustuzhanine или другие личные аккаунты")
    
    try:
        webbrowser.open(token_url)
        print("✅ Страница авторизации открыта")
    except:
        print("❌ Перейдите вручную:")
        print(token_url)
    
    print(f"\n📝 На странице авторизации:")
    print(f"1. Убедитесь, что вверху показан {corp_email}")
    print(f"2. Если показан другой аккаунт - выйдите и войдите под {corp_email}")
    print(f"3. Разрешите доступ к данным")
    print(f"4. Скопируйте токен из URL после #access_token=")
    
    token = input(f"\n🔑 Вставьте корпоративный токен: ").strip()
    
    if not token:
        print("❌ Токен не введен!")
        return
    
    print(f"\n✅ Токен получен: {token[:20]}...{token[-10:]}")
    
    print("\n🧪 ШАГ 5: ТЕСТИРОВАНИЕ КОРПОРАТИВНОГО ТОКЕНА")
    
    # Тестируем токен
    success = test_corporate_token(token, corp_email)
    
    if success:
        # Сохраняем рабочий токен
        env_content = f"""# ФИНАЛЬНЫЙ РАБОЧИЙ КОРПОРАТИВНЫЙ ТОКЕН
YANDEX_OAUTH_TOKEN={token}
CLIENT_ID={client_id}

# Корпоративные данные
CORPORATE_EMAIL={corp_email}
DOMAIN={corp_email.split('@')[1]}

# Настройки
LOG_LEVEL=INFO
TOKEN_TYPE=bearer
EXPIRES_IN=31536000

# Статус: ПРОТЕСТИРОВАН И РАБОТАЕТ
"""
        
        with open("FINAL_WORKING_TOKEN.env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print("\n💾 Рабочий токен сохранен: FINAL_WORKING_TOKEN.env")
        
        print("\n🚀 ФИНАЛЬНЫЕ ДЕЙСТВИЯ:")
        print("1. Скопируйте рабочий токен:")
        print("   cp FINAL_WORKING_TOKEN.env .env")
        print("2. Протестируйте все функции:")
        print("   python examples.py")
        print("3. Запустите полную демонстрацию:")
        print("   python examples_advanced.py")
        
        print("\n🎉 ПОЗДРАВЛЯЕМ! ВСЕ ГОТОВО К РАБОТЕ!")
        
    else:
        print("\n❌ Токен все еще не работает")
        print("💡 Возможные проблемы:")
        print("1. Токен получен не от корпоративного аккаунта")
        print("2. Домен не подтвержден в Яндекс 360")
        print("3. Тариф не активен")
        print("4. У пользователя нет прав администратора")

def test_corporate_token(token, expected_email):
    """Тестирует корпоративный токен"""
    
    try:
        print("🔍 Проверка авторизации...")
        
        # Проверяем авторизацию
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
            expected_domain = expected_email.split('@')[1]
            
            if email == expected_email or (email == 'N/A' and expected_domain in expected_email):
                print("✅ Корпоративный аккаунт подтвержден!")
            else:
                print(f"⚠️  Email не совпадает. Ожидался: {expected_email}")
                if email.endswith(('@yandex.ru', '@yandex.com')):
                    print("❌ Это личный аккаунт!")
                    return False
        else:
            print(f"❌ Ошибка авторизации: {response.status_code}")
            return False
        
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
            print(f"📋 Тестовая встреча создана: {meeting['id']}")
            print(f"🔗 Ссылка на встречу: {meeting['join_url']}")
            
            if 'live_stream' in meeting:
                print(f"📺 Ссылка на трансляцию: {meeting['live_stream']['watch_url']}")
            
            return True
            
        else:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('message', 'Неизвестная ошибка')
            
            print(f"❌ Ошибка API Телемост: {response.status_code}")
            print(f"Сообщение: {error_msg}")
            
            if 'ApiRestrictedToOrganizations' in str(error_data):
                print("\n💡 Проблема: API все еще недоступен")
                print("Возможные причины:")
                print("1. Токен от личного аккаунта (не корпоративного)")
                print("2. Домен не подтвержден в admin.yandex.ru")
                print("3. Тариф Яндекс 360 не активен")
            
            return False
    
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    final_token_setup()
