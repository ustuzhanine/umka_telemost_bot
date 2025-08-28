#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простые примеры использования API Яндекс Телемост
Для полных примеров см. examples_advanced.py
"""

from telemost_api import TelemostAPI, TelemostAPIError, TelemostAuthError, TelemostValidationError


def example_simple_meeting():
    """Пример создания простой встречи"""
    print("1️⃣ Создание простой встречи")
    print("-" * 30)
    
    api = TelemostAPI()
    meeting = api.create_simple_meeting()
    
    print(f"✅ ID встречи: {meeting['id']}")
    print(f"🔗 Ссылка: {meeting['join_url']}")
    
    # Сохраняем данные
    filename = api.save_meeting_data(meeting)
    print(f"💾 Сохранено: {filename}")
    print()


def example_meeting_with_stream():
    """Пример создания встречи с трансляцией"""
    print("2️⃣ Создание встречи с трансляцией")
    print("-" * 40)
    
    api = TelemostAPI()
    meeting = api.create_meeting_with_stream(
        stream_title="Важная презентация",
        stream_description="Презентация новых возможностей продукта",
        stream_access_level="PUBLIC"
    )
    
    print(f"✅ ID встречи: {meeting['id']}")
    print(f"🔗 Ссылка для участников: {meeting['join_url']}")
    if 'live_stream' in meeting:
        print(f"👀 Ссылка для просмотра: {meeting['live_stream'].get('watch_url', 'N/A')}")
    print()


def example_meeting_with_cohosts():
    """Пример создания встречи с соорганизаторами"""
    print("3️⃣ Создание встречи с соорганизаторами")
    print("-" * 45)
    
    api = TelemostAPI()
    
    try:
        meeting = api.create_meeting_with_cohosts(
            cohost_emails=["cohost1@example.com", "cohost2@example.com"],
            waiting_room_level="ORGANIZATION"
        )
        
        print(f"✅ ID встречи: {meeting['id']}")
        print(f"🔗 Ссылка: {meeting['join_url']}")
        print(f"👥 Соорганизаторы: cohost1@example.com, cohost2@example.com")
        
    except TelemostValidationError as e:
        print(f"⚠️ Ошибка валидации: {e}")
        print("ℹ️ Используйте реальные email адреса")
    
    print()


def example_custom_meeting():
    """Пример создания кастомной встречи"""
    print("4️⃣ Создание кастомной встречи")
    print("-" * 35)
    
    api = TelemostAPI()
    
    try:
        # Используем новый метод create_advanced_meeting
        meeting = api.create_advanced_meeting(
            waiting_room_level="ADMINS",
            stream_title="Вебинар по Python",
            stream_description="Изучаем работу с API",
            stream_access_level="PUBLIC",
            cohost_emails=["assistant@example.com"]
        )
        
        print(f"✅ ID встречи: {meeting['id']}")
        print(f"🔗 Ссылка для участников: {meeting['join_url']}")
        
        if 'live_stream' in meeting:
            print(f"👀 Ссылка для просмотра: {meeting['live_stream'].get('watch_url', 'N/A')}")
        
        print(f"🚪 Комната ожидания: ADMINS (только организаторы могут пропускать)")
        
        # Показываем красиво отформатированную информацию
        formatted_info = api.get_meeting_info_formatted(meeting['id'])
        print("\n" + formatted_info)
        
    except TelemostValidationError as e:
        print(f"⚠️ Ошибка валидации: {e}")
    except TelemostAPIError as e:
        print(f"🚫 Ошибка API: {e}")
    
    print()


if __name__ == "__main__":
    print("🚀 Простые примеры API Яндекс Телемост")
    print("=" * 50)
    print("ℹ️ Для полного функционала см. examples_advanced.py")
    print()
    
    try:
        # Запускаем примеры
        example_simple_meeting()
        example_meeting_with_stream()
        example_meeting_with_cohosts() 
        example_custom_meeting()
        
        print("\n✨ Все примеры завершены!")
        print("📚 Для более сложных примеров запустите: python examples_advanced.py")
        
    except TelemostAuthError as e:
        print(f"🔐 Ошибка авторизации: {e}")
        print("ℹ️ Проверьте токен в .env файле")
    except TelemostValidationError as e:
        print(f"⚠️ Ошибка валидации: {e}")
    except TelemostAPIError as e:
        print(f"🚫 Ошибка API: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
