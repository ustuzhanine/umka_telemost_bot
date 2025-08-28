#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUD встреч, управление соорганизаторами, настройки
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Union
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()


class TelemostAPIError(Exception):
    """Базовый класс для ошибок API Телемост"""
    pass


class TelemostAuthError(TelemostAPIError):
    """Ошибка авторизации"""
    pass


class TelemostValidationError(TelemostAPIError):
    """Ошибка валидации данных"""
    pass


class TelemostAPI:
    """Полнофункциональный класс для работы с API Яндекс Телемост"""
    
    def __init__(self, oauth_token: Optional[str] = None):
        """Инициализация API клиента
        
        Args:
            oauth_token: OAuth токен. Если не указан, берется из переменной окружения
        """
        self.oauth_token = oauth_token or os.getenv('YANDEX_OAUTH_TOKEN')
        self.base_url = "https://cloud-api.yandex.net/v1/telemost-api"
        
        if not self.oauth_token:
            raise TelemostAuthError("Не найден YANDEX_OAUTH_TOKEN в переменных окружения")
        
        logger.info("TelemostAPI инициализирован")
    
    def _get_headers(self) -> Dict[str, str]:
        """Получить заголовки для запросов"""
        return {
            'Authorization': f'OAuth {self.oauth_token}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Базовый метод для выполнения HTTP-запросов
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE)
            endpoint: Конечная точка API
            data: Данные для отправки в теле запроса
            params: Параметры запроса
        
        Returns:
            Ответ API в виде словаря
        
        Raises:
            TelemostAPIError: При ошибках API
            TelemostAuthError: При ошибках авторизации
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            logger.debug(f"{method} {url}")
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params,
                timeout=30
            )
            
            # Проверяем статус ответа
            if response.status_code == 401:
                raise TelemostAuthError("Неавторизованный запрос. Проверьте токен.")
            elif response.status_code == 403:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('message', 'Доступ запрещен')
                raise TelemostAPIError(f"Ошибка 403: {error_msg}")
            elif response.status_code >= 400:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('message', f'Ошибка {response.status_code}')
                raise TelemostAPIError(f"Ошибка API {response.status_code}: {error_msg}")
            
            # Возвращаем JSON для успешных ответов
            if response.content:
                return response.json()
            else:
                return {'status': 'success', 'status_code': response.status_code}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети: {e}")
            raise TelemostAPIError(f"Ошибка сети: {e}")
    
    def _validate_email(self, email: str) -> bool:
        """Простая валидация email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validate_waiting_room_level(self, level: str) -> bool:
        """Проверка уровня комнаты ожидания"""
        valid_levels = ['PUBLIC', 'ORGANIZATION', 'ADMINS']
        return level in valid_levels
    
    def _validate_access_level(self, level: str) -> bool:
        """Проверка уровня доступа"""
        valid_levels = ['PUBLIC', 'ORGANIZATION']
        return level in valid_levels
    
    # ===========================================
    # CRUD операции для встреч
    # ===========================================
    
    def create_meeting(
        self,
        waiting_room_level: str = "PUBLIC",
        live_stream: Optional[Dict[str, Any]] = None,
        cohosts: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Создать встречу в Телемост
        
        Args:
            waiting_room_level: Уровень комнаты ожидания 
                               ("PUBLIC", "ORGANIZATION", "ADMINS")
            live_stream: Параметры трансляции (опционально)
            cohosts: Список соорганизаторов (опционально)
        
        Returns:
            Словарь с данными созданной встречи
        
        Raises:
            TelemostValidationError: При некорректных данных
        """
        # Валидация
        if not self._validate_waiting_room_level(waiting_room_level):
            raise TelemostValidationError(f"Некорректный уровень комнаты ожидания: {waiting_room_level}")
        
        # Валидация cohosts
        if cohosts:
            if len(cohosts) > 30:
                raise TelemostValidationError("Максимум 30 соорганизаторов")
            
            for cohost in cohosts:
                if 'email' in cohost and not self._validate_email(cohost['email']):
                    raise TelemostValidationError(f"Некорректный email: {cohost['email']}")
        
        # Валидация live_stream
        if live_stream:
            if 'title' in live_stream and len(live_stream['title']) > 1024:
                raise TelemostValidationError("Название трансляции не должно превышать 1024 символа")
            
            if 'description' in live_stream and len(live_stream['description']) > 2048:
                raise TelemostValidationError("Описание трансляции не должно превышать 2048 символов")
            
            if 'access_level' in live_stream and not self._validate_access_level(live_stream['access_level']):
                raise TelemostValidationError(f"Некорректный уровень доступа: {live_stream['access_level']}")
        
        # Формируем тело запроса
        data = {"waiting_room_level": waiting_room_level}
        
        if live_stream:
            data["live_stream"] = live_stream
            
        if cohosts:
            data["cohosts"] = cohosts
        
        logger.info(f"Создание встречи с параметрами: {waiting_room_level}")
        result = self._make_request('POST', 'conferences', data)
        
        if result.get('id'):
            logger.info(f"Встреча создана: {result['id']}")
        
        return result
    
    def get_meeting(self, meeting_id: str) -> Dict[str, Any]:
        """
        Получить информацию о встрече
        
        Args:
            meeting_id: ID встречи
        
        Returns:
            Информация о встрече
        """
        if not meeting_id:
            raise TelemostValidationError("ID встречи обязателен")
        
        logger.info(f"Получение данных встречи: {meeting_id}")
        return self._make_request('GET', f'conferences/{meeting_id}')
    
    def update_meeting(
        self, 
        meeting_id: str,
        waiting_room_level: Optional[str] = None,
        live_stream: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Обновить настройки встречи
        
        Args:
            meeting_id: ID встречи
            waiting_room_level: Новый уровень комнаты ожидания
            live_stream: Новые параметры трансляции
        
        Returns:
            Обновленные данные встречи
        """
        if not meeting_id:
            raise TelemostValidationError("ID встречи обязателен")
        
        data = {}
        
        if waiting_room_level is not None:
            if not self._validate_waiting_room_level(waiting_room_level):
                raise TelemostValidationError(f"Некорректный уровень комнаты ожидания: {waiting_room_level}")
            data['waiting_room_level'] = waiting_room_level
        
        if live_stream is not None:
            data['live_stream'] = live_stream
        
        if not data:
            raise TelemostValidationError("Нет данных для обновления")
        
        logger.info(f"Обновление встречи: {meeting_id}")
        return self._make_request('PATCH', f'conferences/{meeting_id}', data)
    
    def delete_meeting(self, meeting_id: str) -> Dict[str, Any]:
        """
        Удалить встречу
        
        Args:
            meeting_id: ID встречи
        
        Returns:
            Подтверждение удаления
        """
        if not meeting_id:
            raise TelemostValidationError("ID встречи обязателен")
        
        logger.info(f"Удаление встречи: {meeting_id}")
        return self._make_request('DELETE', f'conferences/{meeting_id}')
    
    def list_meetings(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Получить список встреч
        
        Args:
            limit: Количество встреч на страницу (макс. 100)
            offset: Смещение для пагинации
        
        Returns:
            Список встреч
        """
        if limit > 100:
            raise TelemostValidationError("Максимальный limit: 100")
        
        params = {'limit': limit, 'offset': offset}
        
        logger.info(f"Получение списка встреч (limit: {limit}, offset: {offset})")
        return self._make_request('GET', 'conferences', params=params)
    
    # ===========================================
    # Управление соорганизаторами
    # ===========================================
    
    def get_meeting_cohosts(self, meeting_id: str) -> Dict[str, Any]:
        """
        Получить список соорганизаторов встречи
        
        Args:
            meeting_id: ID встречи
        
        Returns:
            Список соорганизаторов
        """
        if not meeting_id:
            raise TelemostValidationError("ID встречи обязателен")
        
        logger.info(f"Получение соорганизаторов встречи: {meeting_id}")
        return self._make_request('GET', f'conferences/{meeting_id}/cohosts')
    
    def update_meeting_cohosts(
        self, 
        meeting_id: str, 
        cohosts: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Обновить список соорганизаторов встречи
        
        Args:
            meeting_id: ID встречи
            cohosts: Новый список соорганизаторов
        
        Returns:
            Обновленный список соорганизаторов
        """
        if not meeting_id:
            raise TelemostValidationError("ID встречи обязателен")
        
        if len(cohosts) > 30:
            raise TelemostValidationError("Максимум 30 соорганизаторов")
        
        # Валидация emailов
        for cohost in cohosts:
            if 'email' in cohost and not self._validate_email(cohost['email']):
                raise TelemostValidationError(f"Некорректный email: {cohost['email']}")
        
        data = {'cohosts': cohosts}
        
        logger.info(f"Обновление соорганизаторов встречи: {meeting_id}")
        return self._make_request('PUT', f'conferences/{meeting_id}/cohosts', data)
    
    def add_meeting_cohost(
        self, 
        meeting_id: str, 
        email: str
    ) -> Dict[str, Any]:
        """
        Добавить соорганизатора к встрече
        
        Args:
            meeting_id: ID встречи
            email: Email соорганизатора
        
        Returns:
            Подтверждение добавления
        """
        if not meeting_id:
            raise TelemostValidationError("ID встречи обязателен")
        
        if not self._validate_email(email):
            raise TelemostValidationError(f"Некорректный email: {email}")
        
        data = {'email': email}
        
        logger.info(f"Добавление соорганизатора {email} к встрече: {meeting_id}")
        return self._make_request('POST', f'conferences/{meeting_id}/cohosts', data)
    
    def remove_meeting_cohost(
        self, 
        meeting_id: str, 
        cohost_id: str
    ) -> Dict[str, Any]:
        """
        Удалить соорганизатора из встречи
        
        Args:
            meeting_id: ID встречи
            cohost_id: ID соорганизатора
        
        Returns:
            Подтверждение удаления
        """
        if not meeting_id:
            raise TelemostValidationError("ID встречи обязателен")
        
        if not cohost_id:
            raise TelemostValidationError("ID соорганизатора обязателен")
        
        logger.info(f"Удаление соорганизатора {cohost_id} из встречи: {meeting_id}")
        return self._make_request('DELETE', f'conferences/{meeting_id}/cohosts/{cohost_id}')
    
    # ===========================================
    # Настройки по умолчанию
    # ===========================================
    
    def get_default_settings(self) -> Dict[str, Any]:
        """
        Получить настройки по умолчанию для встреч
        
        Returns:
            Настройки по умолчанию
        """
        logger.info("Получение настроек по умолчанию")
        return self._make_request('GET', 'default-settings')
    
    def update_default_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обновить настройки по умолчанию
        
        Args:
            settings: Новые настройки
        
        Returns:
            Обновленные настройки
        """
        if not settings:
            raise TelemostValidationError("Настройки не могут быть пустыми")
        
        logger.info("Обновление настроек по умолчанию")
        return self._make_request('PATCH', 'default-settings', settings)
    
    # ===========================================
    # Удобные методы (шорткаты)
    # ===========================================
    
    def create_simple_meeting(self) -> Dict[str, Any]:
        """Создать простую публичную встречу без трансляции"""
        return self.create_meeting()
    
    def create_meeting_with_stream(
        self,
        stream_title: str,
        stream_description: str = "",
        stream_access_level: str = "PUBLIC",
        waiting_room_level: str = "PUBLIC"
    ) -> Dict[str, Any]:
        """
        Создать встречу с трансляцией
        
        Args:
            stream_title: Название трансляции
            stream_description: Описание трансляции
            stream_access_level: Уровень доступа ("PUBLIC", "ORGANIZATION")
            waiting_room_level: Уровень комнаты ожидания
        """
        live_stream = {
            "title": stream_title[:1024],  # Максимум 1024 символа
            "description": stream_description[:2048],  # Максимум 2048 символов
            "access_level": stream_access_level
        }
        
        return self.create_meeting(
            waiting_room_level=waiting_room_level,
            live_stream=live_stream
        )
    
    def create_meeting_with_cohosts(
        self,
        cohost_emails: List[str],
        waiting_room_level: str = "PUBLIC"
    ) -> Dict[str, Any]:
        """
        Создать встречу с соорганизаторами
        
        Args:
            cohost_emails: Список email соорганизаторов
            waiting_room_level: Уровень комнаты ожидания
        """
        cohosts = [{"email": email} for email in cohost_emails[:30]]  # Максимум 30
        
        return self.create_meeting(
            waiting_room_level=waiting_room_level,
            cohosts=cohosts
        )
    
    def create_advanced_meeting(
        self,
        waiting_room_level: str = "PUBLIC",
        stream_title: Optional[str] = None,
        stream_description: str = "",
        stream_access_level: str = "PUBLIC",
        cohost_emails: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Создать расширенную встречу со всеми параметрами
        
        Args:
            waiting_room_level: Уровень комнаты ожидания
            stream_title: Название трансляции (если нужна)
            stream_description: Описание трансляции
            stream_access_level: Уровень доступа к трансляции
            cohost_emails: Список email соорганизаторов
        
        Returns:
            Данные созданной встречи
        """
        live_stream = None
        if stream_title:
            live_stream = {
                "title": stream_title[:1024],
                "description": stream_description[:2048],
                "access_level": stream_access_level
            }
        
        cohosts = None
        if cohost_emails:
            cohosts = [{"email": email} for email in cohost_emails[:30]]
        
        return self.create_meeting(
            waiting_room_level=waiting_room_level,
            live_stream=live_stream,
            cohosts=cohosts
        )
    
    # ===========================================
    # Утилиты и помощники
    # ===========================================
    
    def get_meeting_info_formatted(self, meeting_id: str) -> str:
        """
        Получить красиво отформатированную информацию о встрече
        
        Args:
            meeting_id: ID встречи
        
        Returns:
            Отформатированная строка с информацией
        """
        meeting = self.get_meeting(meeting_id)
        
        info = f"""
📋 Информация о встрече
{'='*50}
🆔 ID: {meeting.get('id', 'N/A')}
🔗 Ссылка: {meeting.get('join_url', 'N/A')}
🚪 Комната ожидания: {meeting.get('waiting_room_level', 'N/A')}
        """.strip()
        
        if 'live_stream' in meeting:
            stream = meeting['live_stream']
            info += f"""

📺 Трансляция:
🎥 Название: {stream.get('title', 'N/A')}
📝 Описание: {stream.get('description', 'N/A')}
🔍 Доступ: {stream.get('access_level', 'N/A')}
👀 Ссылка на просмотр: {stream.get('watch_url', 'N/A')}
            """.strip()
        
        return info
    
    def save_meeting_data(self, meeting_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Сохранить данные встречи в файл
        
        Args:
            meeting_data: Данные встречи
            filename: Имя файла (опционально)
        
        Returns:
            Путь к сохраненному файлу
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            meeting_id = meeting_data.get('id', 'unknown')
            filename = f"meeting_{meeting_id}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(meeting_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Данные встречи сохранены: {filename}")
        return filename
    
    def validate_meeting_data(self, meeting_data: Dict[str, Any]) -> bool:
        """
        Проверить корректность данных встречи
        
        Args:
            meeting_data: Данные для проверки
        
        Returns:
            True если данные корректны
        
        Raises:
            TelemostValidationError: При некорректных данных
        """
        required_fields = ['id', 'join_url']
        
        for field in required_fields:
            if field not in meeting_data:
                raise TelemostValidationError(f"Отсутствует обязательное поле: {field}")
        
        # Проверяем URL
        join_url = meeting_data.get('join_url', '')
        if not join_url.startswith('https://telemost.yandex.ru/'):
            raise TelemostValidationError("Некорректная ссылка на встречу")
        
        return True


def main():
    """Основная функция для демонстрации возможностей API"""
    try:
        # Инициализируем API
        api = TelemostAPI()
        
        print("🚀 Демонстрация возможностей Яндекс Телемост API")
        print("=" * 60)
        
        # 1. Создаем простую встречу
        print("\n1️⃣ Создание простой встречи...")
        simple_meeting = api.create_simple_meeting()
        print(f"✅ Встреча создана: {simple_meeting['id']}")
        print(f"🔗 Ссылка: {simple_meeting['join_url']}")
        
        # 2. Создаем встречу с трансляцией
        print("\n2️⃣ Создание встречи с трансляцией...")
        stream_meeting = api.create_meeting_with_stream(
            stream_title="Демо презентация",
            stream_description="Показываем возможности API",
            stream_access_level="PUBLIC"
        )
        print(f"✅ Встреча с трансляцией: {stream_meeting['id']}")
        print(f"👀 Ссылка на просмотр: {stream_meeting.get('live_stream', {}).get('watch_url', 'N/A')}")
        
        # 3. Получаем информацию о встрече
        print("\n3️⃣ Получение информации о встрече...")
        meeting_info = api.get_meeting_info_formatted(simple_meeting['id'])
        print(meeting_info)
        
        # 4. Сохраняем данные
        print("\n4️⃣ Сохранение данных...")
        filename1 = api.save_meeting_data(simple_meeting)
        filename2 = api.save_meeting_data(stream_meeting)
        print(f"💾 Файлы сохранены: {filename1}, {filename2}")
        
        # 5. Получаем список встреч
        print("\n5️⃣ Получение списка встреч...")
        try:
            meetings_list = api.list_meetings(limit=5)
            print(f"📋 Найдено встреч: {len(meetings_list.get('conferences', []))}")
        except TelemostAPIError as e:
            print(f"⚠️ Не удалось получить список: {e}")
        
        print("\n✨ Демонстрация завершена!")
        print("ℹ️ Для полного функционала см. examples_advanced.py")
        
    except TelemostAuthError as e:
        print(f"🔐 Ошибка авторизации: {e}")
        print("ℹ️ Проверьте токен в .env файле")
    except TelemostValidationError as e:
        print(f"⚠️ Ошибка валидации: {e}")
    except TelemostAPIError as e:
        print(f"🚫 Ошибка API: {e}")
    except Exception as e:
        logger.exception("Неожиданная ошибка")
        print(f"❌ Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
