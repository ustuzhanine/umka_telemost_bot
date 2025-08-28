#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Получение корпоративного токена с новым Client ID
"""

import webbrowser
import requests

def get_token_with_client_id():
    """Получение токена с известным Client ID"""
    
    client_id = "e43e6efcf21b4850b558558b7256a852"
    corp_email = "admin@umka.pro"
    
    print("🎯 ПОЛУЧЕНИЕ КОРПОРАТИВНОГО ТОКЕНА")
    print("=" * 50)
    print(f"🆔 Client ID: {client_id}")
    print(f"📧 Корпоративный email: {corp_email}")
    
    print("\n⚠️  ВАЖНО:")
    print("🟢 Вы ДОЛЖНЫ быть авторизованы под admin@umka.pro")
    print("🔴 НЕ под ustuzhanine или другими личными аккаунтами")
    
    # Проверяем текущий аккаунт
    check_url = "https://passport.yandex.ru/profile"
    print(f"\n🔍 Сначала проверим текущий аккаунт: {check_url}")
    
    try:
        webbrowser.open(check_url)
        print("✅ Страница профиля открыта")
    except:
        print("❌ Перейдите вручную для проверки")
    
    print(f"\n📝 В профиле должно быть:")
    print(f"✅ Логин: admin (или похожий)")
    print(f"✅ Email: {corp_email}")
    print(f"❌ НЕ должно быть: ustuzhanine, urionfidel")
    
    account_ok = input(f"\n✅ Вы под корпоративным аккаунтом {corp_email}? (y/n): ").lower().strip()
    
    if account_ok != 'y':
        print(f"\n🔄 СНАЧАЛА ВОЙДИТЕ ПОД {corp_email}!")
        print("1. Выйдите из текущего аккаунта")
        print(f"2. Войдите под {corp_email}")
        print("3. Запустите скрипт заново")
        return
    
    print("\n🔧 НАСТРОЙКА РАЗРЕШЕНИЙ")
    print("В OAuth приложении должны быть добавлены разрешения:")
    print("✅ telemost-api:conferences.create")
    print("✅ telemost-api:conferences.read")
    print("✅ telemost-api:conferences.update")
    print("✅ telemost-api:conferences.delete")
    
    permissions_ok = input("\n✅ Разрешения добавлены в OAuth приложении? (y/n): ").lower().strip()
    
    if permissions_ok != 'y':
        oauth_url = f"https://oauth.yandex.ru/client/{client_id}"
        print(f"\n🔧 Откроется настройка приложения: {oauth_url}")
        
        try:
            webbrowser.open(oauth_url)
            print("✅ Настройки приложения открыты")
        except:
            print("❌ Перейдите вручную для настройки разрешений")
        
        input("\n📍 Добавили разрешения? Нажмите Enter...")
    
    print("\n🔑 ПОЛУЧЕНИЕ ТОКЕНА")
    
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
    print(f"🟢 На странице авторизации должен быть: {corp_email}")
    print(f"🔴 Если показан другой аккаунт - выйдите и войдите под {corp_email}")
    
    print(f"\n🔗 URL авторизации:")
    print(f"{token_url}")
    
    try:
        webbrowser.open(token_url)
        print("\n✅ Страница авторизации открыта")
    except:
        print("\n❌ Перейдите по ссылке выше вручную")
    
    print(f"\n📝 На странице авторизации:")
    print(f"1. Убедитесь, что вверху показан {corp_email}")
    print(f"2. Разрешите доступ к данным")
    print(f"3. Скопируйте токен из URL после #access_token=")
    print(f"4. Токен должен начинаться с y0_AgA или y0__x")
    
    token = input(f"\n🔑 Вставьте корпоративный токен: ").strip()
    
    if not token:
        print("❌ Токен не введен!")
        return
    
    if not token.startswith(('y0_AgA', 'y0__x')):
        print("⚠️ Предупреждение: токен не начинается с ожидаемого префикса")
    
    print(f"\n✅ Токен получен: {token[:20]}...{token[-10:]}")
    
    print("\n🧪 ТЕСТИРОВАНИЕ КОРПОРАТИВНОГО ТОКЕНА")
    
    # Тестируем токен
    success = test_token_comprehensive(token, corp_email, client_id)
    
    if success:
        print("\n🎉 ПОЗДРАВЛЯЕМ! КОРПОРАТИВНЫЙ ТОКЕН РАБОТАЕТ!")
        print("\n🚀 ФИНАЛЬНЫЕ ДЕЙСТВИЯ:")
        print("1. Скопируйте рабочий токен в .env:")
        print("   cp WORKING_CORPORATE_TOKEN.env .env")
        print("2. Протестируйте API:")
        print("   python check_token_type.py")
        print("3. Запустите примеры:")
        print("   python examples.py")
        print("4. Полная демонстрация:")
        print("   python examples_advanced.py")
    else:
        print("\n❌ Токен все еще не работает")
        print("💡 Возможные решения:")
        print("1. Убедитесь, что токен получен от admin@umka.pro")
        print("2. Проверьте, что домен umka.pro подтвержден в admin.yandex.ru")
        print("3. Убедитесь, что тариф Яндекс 360 активен")

def test_token_comprehensive(token, expected_email, client_id):
    """Комплексное тестирование токена"""
    
    try:
        print("🔍 1. Проверка авторизации...")
        
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
            
            # Анализируем тип аккаунта
            if email == expected_email:
                print("✅ Email совпадает с ожидаемым!")
            elif email == 'N/A':
                print("⚠️ Email не отображается, но это может быть нормально")
            elif email.endswith('@umka.pro'):
                print("✅ Корпоративный домен umka.pro!")
            elif email.endswith(('@yandex.ru', '@yandex.com')):
                print("❌ Это личный аккаунт Яндекса!")
                return False
            else:
                print(f"✅ Корпоративный аккаунт: {email}")
        else:
            print(f"❌ Ошибка авторизации: {response.status_code}")
            return False
        
        print("\n🎥 2. Тестирование API Телемост...")
        
        # Тестируем API Телемост
        response = requests.post(
            'https://cloud-api.yandex.net/v1/telemost-api/conferences',
            headers={
                'Authorization': f'OAuth {token}',
                'Content-Type': 'application/json'
            },
            json={'waiting_room_level': 'PUBLIC'},
            timeout=10
        )
        
        print(f"Статус ответа API: {response.status_code}")
        
        if response.status_code == 201:
            meeting = response.json()
            print("🎉 УСПЕХ! API ТЕЛЕМОСТ РАБОТАЕТ!")
            print(f"📋 ID тестовой встречи: {meeting['id']}")
            print(f"🔗 Ссылка на встречу: {meeting['join_url']}")
            
            # Сохраняем рабочий токен
            env_content = f"""# РАБОЧИЙ КОРПОРАТИВНЫЙ ТОКЕН ЯНДЕКС 360
YANDEX_OAUTH_TOKEN={token}

# Данные приложения
CLIENT_ID={client_id}

# Корпоративные данные
CORPORATE_EMAIL={expected_email}
CORPORATE_LOGIN={login}
DOMAIN=umka.pro

# Тестовая встреча
TEST_MEETING_ID={meeting['id']}
TEST_MEETING_URL={meeting['join_url']}

# Настройки
LOG_LEVEL=INFO
TOKEN_TYPE=bearer
EXPIRES_IN=31536000

# СТАТУС: ПРОТЕСТИРОВАН И РАБОТАЕТ ✅
# Дата тестирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            with open("WORKING_CORPORATE_TOKEN.env", "w", encoding="utf-8") as f:
                f.write(env_content)
            
            print(f"\n💾 Рабочий токен сохранен: WORKING_CORPORATE_TOKEN.env")
            
            return True
            
        else:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('message', 'Неизвестная ошибка')
            error_code = error_data.get('error', 'Unknown')
            
            print(f"❌ Ошибка API Телемост: {response.status_code}")
            print(f"Код ошибки: {error_code}")
            print(f"Сообщение: {error_msg}")
            
            if 'ApiRestrictedToOrganizations' in str(error_data):
                print("\n💡 Диагностика:")
                print("• Ошибка означает: нужен корпоративный аккаунт")
                print("• Возможные причины:")
                print("  1. Токен все еще от личного аккаунта")
                print("  2. Домен umka.pro не подтвержден")
                print("  3. Тариф Яндекс 360 не активен")
                print("  4. У пользователя нет прав в организации")
            
            return False
    
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    from datetime import datetime
    get_token_with_client_id()
