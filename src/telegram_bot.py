import os
import requests
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramBotError(Exception):
    """Базовый класс для ошибок Telegram Bot API"""
    pass


class TelegramBot:
    """Класс для работы с Telegram Bot API"""
    
    def __init__(self, bot_token: Optional[str] = None):
        """Инициализация бота
        
        Args:
            bot_token: Токен бота. Если не указан, берется из переменной окружения
        """
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        if not self.bot_token:
            logger.warning("TELEGRAM_BOT_TOKEN не найден в переменных окружения")
    
    def _make_request(self, method: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Базовый метод для выполнения запросов к Telegram API
        
        Args:
            method: Метод API
            data: Данные для отправки
        
        Returns:
            Ответ API
        
        Raises:
            TelegramBotError: При ошибках API
        """
        if not self.bot_token:
            raise TelegramBotError("Bot token not configured")
        
        url = f"{self.base_url}/{method}"
        
        try:
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            if not result.get('ok'):
                error_msg = result.get('description', 'Unknown error')
                raise TelegramBotError(f"Telegram API error: {error_msg}")
            
            return result.get('result', {})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {e}")
            raise TelegramBotError(f"Network error: {e}")
    
    def send_message(
        self, 
        chat_id: str, 
        text: str, 
        parse_mode: str = 'HTML',
        disable_web_page_preview: bool = True
    ) -> Dict[str, Any]:
        """Отправка сообщения
        
        Args:
            chat_id: ID чата или username
            text: Текст сообщения
            parse_mode: Режим парсинга (HTML, Markdown)
            disable_web_page_preview: Отключить превью ссылок
        
        Returns:
            Информация об отправленном сообщении
        """
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_web_page_preview
        }
        
        logger.info(f"Sending message to {chat_id}")
        return self._make_request('sendMessage', data)
    
    def send_meeting_invitation(
        self,
        chat_id: str,
        meeting_data: Dict[str, Any],
        custom_message: str = None
    ) -> Dict[str, Any]:
        """Отправка приглашения на встречу
        
        Args:
            chat_id: ID чата или username
            meeting_data: Данные встречи
            custom_message: Пользовательское сообщение
        
        Returns:
            Информация об отправленном сообщении
        """
        meeting_id = meeting_data.get('id', 'N/A')
        join_url = meeting_data.get('join_url', '')
        title = meeting_data.get('title', 'Встреча в Telemost')
        description = meeting_data.get('description', '')
        
        # Формируем сообщение
        if custom_message:
            message = custom_message
        else:
            message = f"🎥 <b>Приглашение на встречу</b>\n\n"
            
            if title:
                message += f"📋 <b>Название:</b> {title}\n"
            
            if description:
                message += f"📝 <b>Описание:</b> {description}\n"
            
            message += f"\n🔗 <b>Ссылка для подключения:</b>\n{join_url}\n"
            message += f"\n💡 Нажмите на ссылку, чтобы присоединиться к встрече"
        
        return self.send_message(chat_id, message)
    
    def get_me(self) -> Dict[str, Any]:
        """Получение информации о боте"""
        return self._make_request('getMe')
    
    def send_bulk_invitations(
        self,
        contacts: List[Dict[str, Any]],
        meeting_data: Dict[str, Any],
        custom_message: str = None
    ) -> Dict[str, Any]:
        """Массовая отправка приглашений
        
        Args:
            contacts: Список контактов
            meeting_data: Данные встречи
            custom_message: Пользовательское сообщение
        
        Returns:
            Статистика отправки
        """
        if not self.bot_token:
            logger.warning("Bot token not configured, simulating send")
            return {
                'success': True,
                'sent_count': len(contacts),
                'failed_count': 0,
                'simulated': True
            }
        
        sent_count = 0
        failed_count = 0
        errors = []
        
        for contact in contacts:
            try:
                # Пытаемся отправить по username, если есть
                chat_id = contact.get('username', '').replace('@', '')
                if not chat_id:
                    # Если нет username, используем ID (если есть)
                    chat_id = contact.get('id')
                
                if not chat_id:
                    logger.warning(f"No chat_id for contact: {contact}")
                    failed_count += 1
                    continue
                
                self.send_meeting_invitation(chat_id, meeting_data, custom_message)
                sent_count += 1
                logger.info(f"Invitation sent to {contact.get('name', chat_id)}")
                
            except TelegramBotError as e:
                logger.error(f"Failed to send to {contact.get('name', 'unknown')}: {e}")
                failed_count += 1
                errors.append(str(e))
            except Exception as e:
                logger.error(f"Unexpected error sending to {contact.get('name', 'unknown')}: {e}")
                failed_count += 1
                errors.append(str(e))
        
        return {
            'success': sent_count > 0,
            'sent_count': sent_count,
            'failed_count': failed_count,
            'errors': errors[:5]  # Показываем только первые 5 ошибок
        }


# Глобальный экземпляр бота
telegram_bot = TelegramBot()


def send_meeting_to_contacts(
    contacts: List[Dict[str, Any]], 
    meeting_data: Dict[str, Any],
    custom_message: str = None
) -> Dict[str, Any]:
    """Удобная функция для отправки встречи контактам
    
    Args:
        contacts: Список контактов
        meeting_data: Данные встречи
        custom_message: Пользовательское сообщение
    
    Returns:
        Результат отправки
    """
    return telegram_bot.send_bulk_invitations(contacts, meeting_data, custom_message)


def check_bot_status() -> Dict[str, Any]:
    """Проверка статуса бота"""
    try:
        if not telegram_bot.bot_token:
            return {
                'status': 'not_configured',
                'message': 'Bot token not configured'
            }
        
        bot_info = telegram_bot.get_me()
        return {
            'status': 'active',
            'bot_info': bot_info
        }
    except TelegramBotError as e:
        return {
            'status': 'error',
            'message': str(e)
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f"Unexpected error: {e}"
        }

