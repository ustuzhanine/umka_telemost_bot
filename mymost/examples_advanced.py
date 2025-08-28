#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Расширенные примеры использования API Яндекс Телемост
Демонстрирует все возможности полнофункционального клиента
"""

from telemost_api import TelemostAPI, TelemostAPIError, TelemostAuthError, TelemostValidationError
import time
import json


def demo_basic_operations():
    """Демонстрация базовых операций CRUD"""
    print("🔥 БАЗОВЫЕ ОПЕРАЦИИ CRUD")
    print("=" * 50)
    
    api = TelemostAPI()
    
    # Создание встречи
    print("\n1. Создание встречи...")
    meeting = api.create_simple_meeting()
    meeting_id = meeting['id']
    print(f"✅ Встреча создана: {meeting_id}")
    
    # Получение информации о встрече
    print("\n2. Получение информации о встрече...")
    meeting_info = api.get_meeting(meeting_id)
    print(f"📋 Получена информация: {meeting_info.get('id', 'N/A')}")
    
    # Обновление встречи
    print("\n3. Обновление настроек встречи...")
    try:
        updated_meeting = api.update_meeting(
            meeting_id, 
            waiting_room_level="ORGANIZATION"
        )
        print("✅ Встреча обновлена")
    except TelemostAPIError as e:
        print(f"⚠️ Не удалось обновить: {e}")
    
    # Удаление встречи
    print("\n4. Удаление встречи...")
    try:
        api.delete_meeting(meeting_id)
        print("✅ Встреча удалена")
    except TelemostAPIError as e:
        print(f"⚠️ Не удалось удалить: {e}")


def demo_advanced_meetings():
    """Демонстрация создания продвинутых встреч"""
    print("\n🚀 ПРОДВИНУТЫЕ ВСТРЕЧИ")
    print("=" * 50)
    
    api = TelemostAPI()
    
    # Встреча с трансляцией
    print("\n1. Встреча с трансляцией...")
    stream_meeting = api.create_meeting_with_stream(
        stream_title="Вебинар по Python разработке",
        stream_description="Изучаем лучшие практики разработки на Python",
        stream_access_level="PUBLIC",
        waiting_room_level="ADMINS"
    )
    print(f"📺 Встреча с трансляцией: {stream_meeting['id']}")
    if 'live_stream' in stream_meeting:
        print(f"🔗 Ссылка на просмотр: {stream_meeting['live_stream'].get('watch_url', 'N/A')}")
    
    # Встреча с соорганизаторами
    print("\n2. Встреча с соорганизаторами...")
    try:
        cohost_meeting = api.create_meeting_with_cohosts(
            cohost_emails=["cohost1@example.com", "cohost2@example.com"],
            waiting_room_level="ORGANIZATION"
        )
        print(f"👥 Встреча с соорганизаторами: {cohost_meeting['id']}")
    except TelemostValidationError as e:
        print(f"⚠️ Ошибка валидации: {e}")
    
    # Максимально продвинутая встреча
    print("\n3. Максимально продвинутая встреча...")
    try:
        advanced_meeting = api.create_advanced_meeting(
            waiting_room_level="ADMINS",
            stream_title="Корпоративная презентация Q4 2024",
            stream_description="Результаты квартала и планы на следующий период",
            stream_access_level="ORGANIZATION",
            cohost_emails=["ceo@company.com", "cto@company.com"]
        )
        print(f"🎯 Продвинутая встреча: {advanced_meeting['id']}")
        
        # Показываем красиво отформатированную информацию
        formatted_info = api.get_meeting_info_formatted(advanced_meeting['id'])
        print(formatted_info)
        
        # Сохраняем данные
        filename = api.save_meeting_data(advanced_meeting, "advanced_meeting.json")
        print(f"💾 Данные сохранены: {filename}")
        
    except TelemostAPIError as e:
        print(f"❌ Ошибка создания: {e}")


def demo_cohosts_management():
    """Демонстрация управления соорганизаторами"""
    print("\n👥 УПРАВЛЕНИЕ СООРГАНИЗАТОРАМИ")
    print("=" * 50)
    
    api = TelemostAPI()
    
    # Создаем встречу
    meeting = api.create_simple_meeting()
    meeting_id = meeting['id']
    print(f"📋 Создана встреча: {meeting_id}")
    
    # Получаем текущих соорганизаторов
    print("\n1. Получение списка соорганизаторов...")
    try:
        cohosts = api.get_meeting_cohosts(meeting_id)
        print(f"👥 Текущих соорганизаторов: {len(cohosts.get('cohosts', []))}")
    except TelemostAPIError as e:
        print(f"⚠️ Не удалось получить: {e}")
    
    # Добавляем соорганизатора
    print("\n2. Добавление соорганизатора...")
    try:
        api.add_meeting_cohost(meeting_id, "newcohost@example.com")
        print("✅ Соорганизатор добавлен")
    except TelemostAPIError as e:
        print(f"⚠️ Не удалось добавить: {e}")
    
    # Обновляем весь список соорганизаторов
    print("\n3. Обновление списка соорганизаторов...")
    try:
        new_cohosts = [
            {"email": "lead@company.com"},
            {"email": "manager@company.com"}
        ]
        api.update_meeting_cohosts(meeting_id, new_cohosts)
        print("✅ Список соорганизаторов обновлен")
    except TelemostAPIError as e:
        print(f"⚠️ Не удалось обновить: {e}")


def demo_meetings_list():
    """Демонстрация работы со списком встреч"""
    print("\n📋 РАБОТА СО СПИСКОМ ВСТРЕЧ")
    print("=" * 50)
    
    api = TelemostAPI()
    
    # Создаем несколько встреч для демонстрации
    print("\n1. Создание нескольких встреч...")
    created_meetings = []
    
    for i in range(3):
        try:
            meeting = api.create_simple_meeting()
            created_meetings.append(meeting['id'])
            print(f"✅ Встреча {i+1}: {meeting['id']}")
            time.sleep(1)  # Небольшая пауза между созданием
        except TelemostAPIError as e:
            print(f"❌ Ошибка создания встречи {i+1}: {e}")
    
    # Получаем список встреч
    print("\n2. Получение списка встреч...")
    try:
        meetings_list = api.list_meetings(limit=10)
        conferences = meetings_list.get('conferences', [])
        print(f"📊 Всего встреч найдено: {len(conferences)}")
        
        # Показываем краткую информацию о каждой встрече
        for meeting in conferences[:5]:  # Показываем только первые 5
            print(f"  • {meeting.get('id', 'N/A')} - {meeting.get('join_url', 'N/A')[:50]}...")
            
    except TelemostAPIError as e:
        print(f"❌ Не удалось получить список: {e}")


def demo_settings_management():
    """Демонстрация управления настройками по умолчанию"""
    print("\n⚙️ УПРАВЛЕНИЕ НАСТРОЙКАМИ ПО УМОЛЧАНИЮ")
    print("=" * 50)
    
    api = TelemostAPI()
    
    # Получаем текущие настройки
    print("\n1. Получение текущих настроек...")
    try:
        current_settings = api.get_default_settings()
        print("✅ Настройки получены:")
        print(json.dumps(current_settings, indent=2, ensure_ascii=False))
    except TelemostAPIError as e:
        print(f"⚠️ Не удалось получить настройки: {e}")
    
    # Обновляем настройки
    print("\n2. Обновление настроек...")
    try:
        new_settings = {
            "waiting_room_level": "ORGANIZATION"
        }
        updated_settings = api.update_default_settings(new_settings)
        print("✅ Настройки обновлены")
    except TelemostAPIError as e:
        print(f"⚠️ Не удалось обновить настройки: {e}")


def demo_error_handling():
    """Демонстрация обработки ошибок"""
    print("\n🚨 ДЕМОНСТРАЦИЯ ОБРАБОТКИ ОШИБОК")
    print("=" * 50)
    
    api = TelemostAPI()
    
    # Ошибка валидации - неправильный email
    print("\n1. Ошибка валидации (неправильный email)...")
    try:
        api.create_meeting_with_cohosts(["invalid-email"])
        print("❌ Это не должно было сработать")
    except TelemostValidationError as e:
        print(f"✅ Корректно поймана ошибка валидации: {e}")
    
    # Ошибка валидации - слишком длинное название трансляции
    print("\n2. Ошибка валидации (слишком длинное название)...")
    try:
        long_title = "x" * 1025  # Больше 1024 символов
        api.create_meeting_with_stream(long_title)
        print("❌ Это не должно было сработать")
    except TelemostValidationError as e:
        print(f"✅ Корректно поймана ошибка валидации: {e}")
    
    # Ошибка - несуществующая встреча
    print("\n3. Попытка получить несуществующую встреча...")
    try:
        api.get_meeting("nonexistent-meeting-id")
        print("❌ Это не должно было сработать")
    except TelemostAPIError as e:
        print(f"✅ Корректно поймана ошибка API: {e}")


def demo_data_validation():
    """Демонстрация валидации данных"""
    print("\n🔍 ВАЛИДАЦИЯ ДАННЫХ")
    print("=" * 50)
    
    api = TelemostAPI()
    
    # Создаем встречу и валидируем данные
    meeting = api.create_simple_meeting()
    
    print("\n1. Валидация корректных данных встречи...")
    try:
        is_valid = api.validate_meeting_data(meeting)
        print(f"✅ Данные корректны: {is_valid}")
    except TelemostValidationError as e:
        print(f"❌ Ошибка валидации: {e}")
    
    # Тестируем валидацию некорректных данных
    print("\n2. Валидация некорректных данных...")
    invalid_data = {"id": "test", "join_url": "invalid-url"}
    
    try:
        api.validate_meeting_data(invalid_data)
        print("❌ Валидация должна была провалиться")
    except TelemostValidationError as e:
        print(f"✅ Корректно поймана ошибка: {e}")


def main():
    """Главная функция - запуск всех демонстраций"""
    print("🎯 ПОЛНАЯ ДЕМОНСТРАЦИЯ API ЯНДЕКС ТЕЛЕМОСТ")
    print("=" * 60)
    print("Демонстрируем все возможности полнофункционального клиента")
    
    demos = [
        ("Базовые операции CRUD", demo_basic_operations),
        ("Продвинутые встречи", demo_advanced_meetings),
        ("Управление соорганизаторами", demo_cohosts_management),
        ("Список встреч", demo_meetings_list),
        ("Настройки по умолчанию", demo_settings_management),
        ("Обработка ошибок", demo_error_handling),
        ("Валидация данных", demo_data_validation),
    ]
    
    for name, demo_func in demos:
        try:
            print(f"\n{'🔸' * 20}")
            print(f"🎬 ДЕМО: {name}")
            demo_func()
            print(f"✅ Демо '{name}' завершено")
            
        except TelemostAuthError as e:
            print(f"🔐 Ошибка авторизации в '{name}': {e}")
            print("💡 Проверьте токен в .env файле")
            break
            
        except TelemostAPIError as e:
            print(f"🚫 Ошибка API в '{name}': {e}")
            
        except Exception as e:
            print(f"💥 Неожиданная ошибка в '{name}': {e}")
    
    print(f"\n{'🌟' * 20}")
    print("🎉 ВСЕ ДЕМОНСТРАЦИИ ЗАВЕРШЕНЫ!")
    print("📚 Изучите код примеров для понимания всех возможностей API")


if __name__ == "__main__":
    main()
