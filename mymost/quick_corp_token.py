#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрое получение корпоративного токена
"""

import webbrowser

def get_corporate_token():
    """Быстрое получение корпоративного токена"""
    
    print("🏢 БЫСТРОЕ ПОЛУЧЕНИЕ КОРПОРАТИВНОГО ТОКЕНА")
    print("=" * 50)
    
    print("\n⚠️  КРИТИЧЕСКИ ВАЖНО:")
    print("🔴 Вы ДОЛЖНЫ создать корпоративного пользователя в Яндекс 360!")
    print("🔴 Токен ДОЛЖЕН быть получен от admin@yourcompany.ru")
    print("🔴 НЕ используйте ustuzhanine@yandex.ru!")
    
    print("\n📋 ЧТО СДЕЛАТЬ СНАЧАЛА:")
    print("1. Перейдите в https://admin.yandex.ru/")
    print("2. Войдите под аккаунтом, которым регистрировали организацию")
    print("3. 'Сотрудники' → 'Добавить сотрудника'")
    print("4. Создайте: admin@yourcompany.ru")
    print("5. Роль: Администратор")
    
    domain = input("\n🌐 Какой домен у вашей организации? (например: mycompany.ru): ").strip()
    
    if not domain:
        print("❌ Домен обязателен!")
        return
    
    corp_email = f"admin@{domain}"
    print(f"\n✅ Корпоративный email: {corp_email}")
    
    print(f"\n📝 ИНСТРУКЦИЯ:")
    print(f"1. Создайте пользователя {corp_email} в админ-панели")
    print(f"2. Выйдите из аккаунта ustuzhanine")
    print(f"3. Войдите под {corp_email}")
    print(f"4. Получите токен")
    
    ready = input("\n✅ Создали корпоративного пользователя и вошли под ним? (y/n): ").lower()
    
    if ready != 'y':
        print("\n🔄 Сначала создайте корпоративного пользователя!")
        print("https://admin.yandex.ru/ → Сотрудники → Добавить")
        return
    
    # Проверяем текущий аккаунт
    print("\n🔍 ПРОВЕРКА АККАУНТА")
    check_url = "https://passport.yandex.ru/profile"
    
    try:
        webbrowser.open(check_url)
        print("✅ Страница профиля открыта")
    except:
        print(f"Перейдите вручную: {check_url}")
    
    print(f"\n📝 В профиле должно быть:")
    print(f"✅ Логин: admin (или другой корпоративный)")
    print(f"✅ Email: {corp_email}")
    print(f"❌ НЕ должно быть: ustuzhanine, urionfidel")
    
    account_correct = input("\n✅ Вы под корпоративным аккаунтом? (y/n): ").lower()
    
    if account_correct != 'y':
        print("\n🔄 ВЫЙДИТЕ И ВОЙДИТЕ ПОД КОРПОРАТИВНЫМ АККАУНТОМ!")
        return
    
    client_id = input("\n🆔 Client ID OAuth приложения: ").strip()
    
    if not client_id:
        print("❌ Client ID обязателен!")
        return
    
    # Генерируем URL для токена
    scopes = [
        "telemost-api:conferences.create",
        "telemost-api:conferences.read",
        "telemost-api:conferences.update", 
        "telemost-api:conferences.delete"
    ]
    
    scope_string = "%20".join(scopes)
    token_url = f"https://oauth.yandex.ru/authorize?response_type=token&client_id={client_id}&scope={scope_string}"
    
    print(f"\n🔑 ПОЛУЧЕНИЕ КОРПОРАТИВНОГО ТОКЕНА")
    print(f"Откроется страница авторизации...")
    print(f"\n⚠️  УБЕДИТЕСЬ: авторизуетесь под {corp_email}!")
    
    try:
        webbrowser.open(token_url)
        print("✅ Страница авторизации открыта")
    except:
        print("❌ Перейдите вручную:")
        print(token_url)
    
    token = input("\n🔑 Корпоративный токен: ").strip()
    
    if token:
        # Быстрый тест
        import requests
        
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
                
                print(f"\n👤 Пользователь: {login}")
                print(f"📧 Email: {email}")
                
                if email.endswith(f'@{domain}'):
                    print("✅ ЭТО КОРПОРАТИВНЫЙ ТОКЕН!")
                    
                    # Тест API
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
                        print("🎉 API ТЕЛЕМОСТ РАБОТАЕТ!")
                        meeting = response.json()
                        print(f"📋 Тестовая встреча: {meeting['id']}")
                        
                        # Сохраняем рабочий токен
                        env_content = f"""# РАБОЧИЙ КОРПОРАТИВНЫЙ ТОКЕН
YANDEX_OAUTH_TOKEN={token}
CLIENT_ID={client_id}

# Информация
# Пользователь: {login}
# Email: {email}
# Домен: {domain}
# Статус: РАБОТАЕТ
"""
                        with open("final_working_token.env", "w") as f:
                            f.write(env_content)
                        
                        print("💾 Сохранено: final_working_token.env")
                        print("\n🚀 ГОТОВО!")
                        print("cp final_working_token.env .env")
                        
                    else:
                        print("❌ API все еще не работает")
                        print("Проверьте настройки Яндекс 360")
                else:
                    print("❌ Это все еще не корпоративный токен!")
                    print(f"Нужен email @{domain}")
        
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    get_corporate_token()
