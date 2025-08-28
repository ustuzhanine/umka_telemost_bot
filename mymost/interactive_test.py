#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интерактивное тестирование Телемост API
"""

from telemost_api import TelemostAPI
import json
from datetime import datetime

def interactive_test():
    """Интерактивное тестирование API"""
    
    print("🚀 ИНТЕРАКТИВНОЕ ТЕСТИРОВАНИЕ ТЕЛЕМОСТ API")
    print("=" * 60)
    
    try:
        api = TelemostAPI()
        print("✅ API инициализирован успешно")
        
        # Меню действий
        while True:
            print("\n📋 ВЫБЕРИТЕ ДЕЙСТВИЕ:")
            print("1. 🎬 Создать простую встречу")
            print("2. 📺 Создать встречу с трансляцией")
            print("3. 🔒 Создать приватную встречу")
            print("4. ℹ️  Получить информацию о встрече")
            print("5. ✏️  Обновить встречу")
            print("6. 🗑️  Удалить встречу")
            print("7. 📊 Показать статистику")
            print("8. 💾 Сохранить все данные")
            print("0. ❌ Выход")
            
            choice = input("\n👉 Ваш выбор: ").strip()
            
            if choice == "0":
                print("👋 До свидания!")
                break
            elif choice == "1":
                create_simple_meeting(api)
            elif choice == "2":
                create_stream_meeting(api)
            elif choice == "3":
                create_private_meeting(api)
            elif choice == "4":
                get_meeting_info(api)
            elif choice == "5":
                update_meeting(api)
            elif choice == "6":
                delete_meeting(api)
            elif choice == "7":
                show_statistics(api)
            elif choice == "8":
                save_all_data(api)
            else:
                print("❌ Неверный выбор!")
    
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")

def create_simple_meeting(api):
    """Создание простой встречи"""
    print("\n🎬 СОЗДАНИЕ ПРОСТОЙ ВСТРЕЧИ")
    print("-" * 40)
    
    try:
        meeting = api.create_simple_meeting()
        
        print(f"✅ Встреча создана!")
        print(f"🆔 ID: {meeting['id']}")
        print(f"🔗 Ссылка: {meeting['join_url']}")
        print(f"🚪 Комната ожидания: {meeting.get('waiting_room_level', 'N/A')}")
        
        # Сохраняем в глобальную переменную для дальнейшего использования
        global last_meeting_id
        last_meeting_id = meeting['id']
        
    except Exception as e:
        print(f"❌ Ошибка создания: {e}")

def create_stream_meeting(api):
    """Создание встречи с трансляцией"""
    print("\n📺 СОЗДАНИЕ ВСТРЕЧИ С ТРАНСЛЯЦИЕЙ")
    print("-" * 40)
    
    title = input("📝 Название трансляции (или Enter для авто): ").strip()
    if not title:
        title = f"Трансляция {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    description = input("📄 Описание (необязательно): ").strip()
    
    try:
        meeting = api.create_meeting_with_stream(
            stream_title=title,
            stream_description=description or None
        )
        
        print(f"✅ Встреча с трансляцией создана!")
        print(f"🆔 ID: {meeting['id']}")
        print(f"🔗 Ссылка для участников: {meeting['join_url']}")
        
        if 'live_stream' in meeting:
            print(f"👀 Ссылка для просмотра: {meeting['live_stream']['view_url']}")
            print(f"📺 Название трансляции: {meeting['live_stream']['title']}")
        
        global last_meeting_id
        last_meeting_id = meeting['id']
        
    except Exception as e:
        print(f"❌ Ошибка создания: {e}")

def create_private_meeting(api):
    """Создание приватной встречи"""
    print("\n🔒 СОЗДАНИЕ ПРИВАТНОЙ ВСТРЕЧИ")
    print("-" * 40)
    
    print("Выберите уровень доступа:")
    print("1. ADMINS - только администраторы")
    print("2. ORGANIZATION - участники организации")
    
    choice = input("👉 Ваш выбор: ").strip()
    
    level_map = {
        "1": "ADMINS",
        "2": "ORGANIZATION"
    }
    
    level = level_map.get(choice, "ADMINS")
    
    try:
        meeting = api.create_meeting(waiting_room_level=level)
        
        print(f"✅ Приватная встреча создана!")
        print(f"🆔 ID: {meeting['id']}")
        print(f"🔗 Ссылка: {meeting['join_url']}")
        print(f"🔒 Уровень доступа: {level}")
        
        global last_meeting_id
        last_meeting_id = meeting['id']
        
    except Exception as e:
        print(f"❌ Ошибка создания: {e}")

def get_meeting_info(api):
    """Получение информации о встрече"""
    print("\n ℹ️ ИНФОРМАЦИЯ О ВСТРЕЧЕ")
    print("-" * 40)
    
    meeting_id = input("🆔 ID встречи (или Enter для последней): ").strip()
    
    if not meeting_id:
        try:
            meeting_id = last_meeting_id
            print(f"📋 Используем последнюю встречу: {meeting_id}")
        except NameError:
            print("❌ Нет последней встречи. Укажите ID.")
            return
    
    try:
        info = api.get_meeting_info(meeting_id)
        
        print(f"✅ Информация получена:")
        print(f"🆔 ID: {info['id']}")
        print(f"🔗 Ссылка: {info['join_url']}")
        print(f"🚪 Комната ожидания: {info.get('waiting_room_level', 'N/A')}")
        
        if 'live_stream' in info:
            print(f"📺 Трансляция: {info['live_stream']['title']}")
            print(f"👀 Ссылка просмотра: {info['live_stream']['view_url']}")
        
        if 'cohosts' in info:
            print(f"👥 Соорганизаторов: {len(info['cohosts'])}")
        
    except Exception as e:
        print(f"❌ Ошибка получения: {e}")

def update_meeting(api):
    """Обновление встречи"""
    print("\n✏️ ОБНОВЛЕНИЕ ВСТРЕЧИ")
    print("-" * 40)
    
    meeting_id = input("🆔 ID встречи (или Enter для последней): ").strip()
    
    if not meeting_id:
        try:
            meeting_id = last_meeting_id
            print(f"📋 Используем последнюю встречу: {meeting_id}")
        except NameError:
            print("❌ Нет последней встречи. Укажите ID.")
            return
    
    print("\nЧто обновить?")
    print("1. Уровень доступа")
    print("2. Название трансляции")
    
    choice = input("👉 Ваш выбор: ").strip()
    
    try:
        if choice == "1":
            print("Новый уровень доступа:")
            print("1. PUBLIC - открытая")
            print("2. ADMINS - только администраторы")
            print("3. ORGANIZATION - участники организации")
            
            level_choice = input("👉 Выбор: ").strip()
            level_map = {"1": "PUBLIC", "2": "ADMINS", "3": "ORGANIZATION"}
            new_level = level_map.get(level_choice, "PUBLIC")
            
            result = api.update_meeting(meeting_id, waiting_room_level=new_level)
            print(f"✅ Уровень доступа обновлен на: {new_level}")
            
        elif choice == "2":
            new_title = input("📝 Новое название трансляции: ").strip()
            if new_title:
                result = api.update_meeting(meeting_id, live_stream={'title': new_title})
                print(f"✅ Название трансляции обновлено: {new_title}")
        
    except Exception as e:
        print(f"❌ Ошибка обновления: {e}")

def delete_meeting(api):
    """Удаление встречи"""
    print("\n🗑️ УДАЛЕНИЕ ВСТРЕЧИ")
    print("-" * 40)
    
    meeting_id = input("🆔 ID встречи (или Enter для последней): ").strip()
    
    if not meeting_id:
        try:
            meeting_id = last_meeting_id
            print(f"📋 Используем последнюю встречу: {meeting_id}")
        except NameError:
            print("❌ Нет последней встречи. Укажите ID.")
            return
    
    confirm = input(f"⚠️ Удалить встречу {meeting_id}? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y', 'да']:
        try:
            api.delete_meeting(meeting_id)
            print("✅ Встреча удалена!")
            
        except Exception as e:
            print(f"❌ Ошибка удаления: {e}")
    else:
        print("❌ Удаление отменено")

def show_statistics(api):
    """Показать статистику созданных встреч"""
    print("\n📊 СТАТИСТИКА")
    print("-" * 40)
    
    # Подсчитываем файлы встреч
    import glob
    meeting_files = glob.glob("meeting_*.json")
    
    print(f"📁 Сохраненных встреч: {len(meeting_files)}")
    
    if meeting_files:
        print("\n📋 Последние встречи:")
        for file in sorted(meeting_files)[-5:]:  # Показываем последние 5
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"  🆔 {data['id']} - {file}")
            except:
                print(f"  ❌ {file} (ошибка чтения)")

def save_all_data(api):
    """Сохранить все данные"""
    print("\n💾 СОХРАНЕНИЕ ДАННЫХ")
    print("-" * 40)
    
    try:
        # Создаем сводный файл
        import glob
        meeting_files = glob.glob("meeting_*.json")
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_meetings": len(meeting_files),
            "meetings": []
        }
        
        for file in meeting_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                summary["meetings"].append({
                    "id": data['id'],
                    "join_url": data['join_url'],
                    "file": file
                })
            except:
                pass
        
        summary_file = f"telemost_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Сводка сохранена: {summary_file}")
        print(f"📊 Всего встреч: {len(meeting_files)}")
        
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")

# Глобальная переменная для хранения ID последней встречи
last_meeting_id = None

if __name__ == "__main__":
    interactive_test()
