from flask import Blueprint, request, jsonify
from src.telemost_api import TelemostAPI, TelemostAPIError, TelemostAuthError, TelemostValidationError
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

meetings_bp = Blueprint('meetings', __name__)

# Инициализация API клиента
try:
    telemost_client = TelemostAPI()
    logger.info("Telemost API client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Telemost API client: {e}")
    telemost_client = None

@meetings_bp.route('/meetings', methods=['POST'])
def create_meeting():
    """Создание новой встречи"""
    if not telemost_client:
        return jsonify({'error': 'Telemost API client not available'}), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Извлекаем параметры
        waiting_room_level = data.get('waiting_room_level', 'PUBLIC')
        title = data.get('title', '')
        description = data.get('description', '')
        live_stream = data.get('live_stream')
        
        logger.info(f"Creating meeting with params: waiting_room_level={waiting_room_level}, title={title}")
        
        # Создаем встречу
        result = telemost_client.create_meeting(
            waiting_room_level=waiting_room_level,
            live_stream=live_stream
        )
        
        # Формируем ответ
        response_data = {
            'id': result.get('id'),
            'join_url': result.get('join_url'),
            'waiting_room_level': result.get('waiting_room_level'),
            'created_at': result.get('created_at'),
            'title': title,
            'description': description
        }
        
        if live_stream:
            response_data['live_stream'] = result.get('live_stream')
        
        logger.info(f"Meeting created successfully: {result.get('id')}")
        return jsonify(response_data), 201
        
    except TelemostValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except TelemostAuthError as e:
        logger.error(f"Auth error: {e}")
        return jsonify({'error': 'Authentication failed'}), 401
    except TelemostAPIError as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@meetings_bp.route('/meetings/<meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    """Получение информации о встрече"""
    if not telemost_client:
        return jsonify({'error': 'Telemost API client not available'}), 500
    
    try:
        result = telemost_client.get_meeting(meeting_id)
        logger.info(f"Retrieved meeting: {meeting_id}")
        return jsonify(result), 200
        
    except TelemostValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except TelemostAPIError as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@meetings_bp.route('/meetings', methods=['GET'])
def list_meetings():
    """Получение списка встреч"""
    if not telemost_client:
        return jsonify({'error': 'Telemost API client not available'}), 500
    
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        result = telemost_client.list_meetings(limit=limit, offset=offset)
        logger.info(f"Retrieved meetings list: limit={limit}, offset={offset}")
        return jsonify(result), 200
        
    except TelemostValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except TelemostAPIError as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@meetings_bp.route('/meetings/<meeting_id>', methods=['PATCH'])
def update_meeting(meeting_id):
    """Обновление настроек встречи"""
    if not telemost_client:
        return jsonify({'error': 'Telemost API client not available'}), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        waiting_room_level = data.get('waiting_room_level')
        live_stream = data.get('live_stream')
        
        result = telemost_client.update_meeting(
            meeting_id=meeting_id,
            waiting_room_level=waiting_room_level,
            live_stream=live_stream
        )
        
        logger.info(f"Meeting updated: {meeting_id}")
        return jsonify(result), 200
        
    except TelemostValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except TelemostAPIError as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@meetings_bp.route('/meetings/<meeting_id>', methods=['DELETE'])
def delete_meeting(meeting_id):
    """Удаление встречи"""
    if not telemost_client:
        return jsonify({'error': 'Telemost API client not available'}), 500
    
    try:
        result = telemost_client.delete_meeting(meeting_id)
        logger.info(f"Meeting deleted: {meeting_id}")
        return jsonify(result), 200
        
    except TelemostValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except TelemostAPIError as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@meetings_bp.route('/send-meeting', methods=['POST'])
def send_meeting_to_contacts():
    """Отправка ссылки на встречу выбранным контактам"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        meeting_data = data.get('meeting_data')
        contacts = data.get('contacts', [])
        custom_message = data.get('custom_message')
        
        if not meeting_data:
            return jsonify({'error': 'Meeting data is required'}), 400
        
        if not contacts:
            return jsonify({'error': 'At least one contact is required'}), 400
        
        logger.info(f"Sending meeting {meeting_data.get('id')} to {len(contacts)} contacts")
        
        # Импортируем функцию отправки
        from src.telegram_bot import send_meeting_to_contacts as send_to_telegram
        
        # Отправляем через Telegram Bot API
        result = send_to_telegram(contacts, meeting_data, custom_message)
        
        if result.get('simulated'):
            return jsonify({
                'success': True,
                'sent_count': result['sent_count'],
                'message': f'Simulation: Meeting link would be sent to {result["sent_count"]} contacts',
                'note': 'Telegram bot token not configured - this is a simulation'
            }), 200
        
        return jsonify({
            'success': result['success'],
            'sent_count': result['sent_count'],
            'failed_count': result['failed_count'],
            'message': f'Meeting link sent to {result["sent_count"]} contacts',
            'errors': result.get('errors', [])
        }), 200
        
    except Exception as e:
        logger.error(f"Error sending meeting to contacts: {e}")
        return jsonify({'error': 'Failed to send meeting to contacts'}), 500

@meetings_bp.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния API"""
    status = {
        'status': 'healthy',
        'telemost_api': 'available' if telemost_client else 'unavailable'
    }
    
    return jsonify(status), 200


@meetings_bp.route('/bot-status', methods=['GET'])
def bot_status():
    """Проверка статуса Telegram бота"""
    try:
        from src.telegram_bot import check_bot_status
        status = check_bot_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error checking bot status: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to check bot status'
        }), 500

