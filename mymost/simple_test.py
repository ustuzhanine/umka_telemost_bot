#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простое тестирование Телемост API
"""

from telemost_api import TelemostAPI
import json

def simple_test():
    """Простое пошаговое тестирование"""
    
    print("🚀 ПРОСТОЕ ТЕСТИРОВАНИЕ ТЕЛЕМОСТ API")
    print("=" * 50)
    
    try:
        # Инициализация API
        print("1️⃣ Инициализация API...")
        api = TelemostAPI()
        print("✅ API готов к работе!")
        
        # Создание простой встречи
        print("\n2️⃣ Создание простой встречи...")
        meeting = api.create_simple_meeting()
        meeting_id = meeting['id']
        join_url = meeting['join_url']
        
        print(f"✅ Встреча создана!")
        print(f"   🆔 ID: {meeting_id}")
        print(f"   🔗 Ссылка: {join_url}")
        
        # Получение информации о встрече
        print(f"\n3️⃣ Получение информации о встрече {meeting_id}...")
        meeting_info = api.get_meeting(meeting_id)
        
        print(f"✅ Информация получена:")
        print(f"   🚪 Комната ожидания: {meeting_info.get('waiting_room_level', 'N/A')}")
        
        # Создание встречи с трансляцией
        print(f"\n4️⃣ Создание встречи с трансляцией...")
        stream_meeting = api.create_meeting_with_stream(
            stream_title="Тестовая трансляция",
            stream_description="Проверка работы трансляций"
        )
        
        stream_id = stream_meeting['id']
        stream_join_url = stream_meeting['join_url']
        
        print(f"✅ Встреча с трансляцией создана!")
        print(f"   🆔 ID: {stream_id}")
        print(f"   🔗 Ссылка для участников: {stream_join_url}")
        
        if 'live_stream' in stream_meeting:
            view_url = stream_meeting['live_stream']['view_url']
            print(f"   👀 Ссылка для просмотра: {view_url}")
        
        # Обновление встречи
        print(f"\n5️⃣ Обновление первой встречи...")
        api.update_meeting(meeting_id, waiting_room_level="ADMINS")
        print("✅ Встреча обновлена (доступ только администраторам)")
        
        # Проверка обновления
        updated_info = api.get_meeting(meeting_id)
        new_level = updated_info.get('waiting_room_level', 'N/A')
        print(f"   🔒 Новый уровень доступа: {new_level}")
        
        # Итоговая информация
        print(f"\n🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        print("=" * 50)
        print("📋 СОЗДАННЫЕ ВСТРЕЧИ:")
        print(f"   1. Простая встреча: {join_url}")
        print(f"   2. Встреча с трансляцией: {stream_join_url}")
        
        if 'live_stream' in stream_meeting:
            print(f"   3. Ссылка для просмотра: {view_url}")
        
        print(f"\n💡 ПОЛЕЗНЫЕ КОМАНДЫ:")
        print(f"   • Информация о встрече: python -c \"from telemost_api import TelemostAPI; api=TelemostAPI(); print(api.get_meeting('{meeting_id}'))\"")
        print(f"   • Удалить встречу: python -c \"from telemost_api import TelemostAPI; api=TelemostAPI(); api.delete_meeting('{meeting_id}')\"")
        
        # Сохраняем результаты
        results = {
            "test_timestamp": api._get_timestamp(),
            "simple_meeting": {
                "id": meeting_id,
                "url": join_url,
                "access_level": new_level
            },
            "stream_meeting": {
                "id": stream_id,
                "join_url": stream_join_url,
                "view_url": stream_meeting.get('live_stream', {}).get('view_url', 'N/A')
            }
        }
        
        results_file = f"test_results_{api._get_timestamp()}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Результаты сохранены: {results_file}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ТЕСТИРОВАНИЯ: {e}")
        print("💡 Проверьте:")
        print("   • Корректность токена в .env")
        print("   • Подключение к интернету")
        print("   • Права доступа к API")
        return False

def quick_meeting():
    """Быстрое создание встречи"""
    
    print("⚡ БЫСТРОЕ СОЗДАНИЕ ВСТРЕЧИ")
    print("-" * 30)
    
    try:
        api = TelemostAPI()
        meeting = api.create_simple_meeting()
        
        print(f"✅ Встреча готова!")
        print(f"🔗 {meeting['join_url']}")
        
        return meeting['join_url']
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_meeting()
    else:
        simple_test()
