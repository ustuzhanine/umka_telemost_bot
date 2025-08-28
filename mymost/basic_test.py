#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Базовое тестирование - создание встреч
"""

from telemost_api import TelemostAPI

def main():
    """Базовое тестирование"""
    
    print("🎯 БАЗОВОЕ ТЕСТИРОВАНИЕ ТЕЛЕМОСТ")
    print("=" * 40)
    
    # Инициализация
    api = TelemostAPI()
    print("✅ API инициализирован")
    
    # Тест 1: Простая встреча
    print("\n1️⃣ Создание простой встречи...")
    try:
        meeting1 = api.create_simple_meeting()
        print(f"✅ Создана: {meeting1['join_url']}")
        meeting1_id = meeting1['id']
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return
    
    # Тест 2: Встреча с трансляцией
    print("\n2️⃣ Создание встречи с трансляцией...")
    try:
        meeting2 = api.create_meeting_with_stream("Тестовая трансляция")
        print(f"✅ Создана: {meeting2['join_url']}")
        
        # Проверяем есть ли данные о трансляции
        if 'live_stream' in meeting2 and 'view_url' in meeting2['live_stream']:
            print(f"📺 Просмотр: {meeting2['live_stream']['view_url']}")
        
        meeting2_id = meeting2['id']
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        meeting2_id = None
    
    # Тест 3: Получение информации
    print(f"\n3️⃣ Получение информации о встрече...")
    try:
        info = api.get_meeting(meeting1_id)
        print(f"✅ Уровень доступа: {info.get('waiting_room_level', 'N/A')}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 4: Обновление встречи
    print(f"\n4️⃣ Обновление встречи...")
    try:
        api.update_meeting(meeting1_id, waiting_room_level="ADMINS")
        updated_info = api.get_meeting(meeting1_id)
        print(f"✅ Новый уровень: {updated_info.get('waiting_room_level', 'N/A')}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Итог
    print(f"\n🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print("📋 СОЗДАННЫЕ ВСТРЕЧИ:")
    print(f"   • Простая: https://telemost.360.yandex.ru/j/{meeting1_id}")
    if meeting2_id:
        print(f"   • С трансляцией: https://telemost.360.yandex.ru/j/{meeting2_id}")
    
    print(f"\n⚡ БЫСТРОЕ СОЗДАНИЕ НОВОЙ ВСТРЕЧИ:")
    print(f"   python basic_test.py quick")

def quick():
    """Быстрое создание встречи"""
    try:
        api = TelemostAPI()
        meeting = api.create_simple_meeting()
        print(f"🔗 {meeting['join_url']}")
    except Exception as e:
        print(f"❌ {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick()
    else:
        main()
