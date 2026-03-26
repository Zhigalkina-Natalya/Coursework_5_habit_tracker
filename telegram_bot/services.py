import logging

import requests

from config import settings

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message) -> None:
    """Отправляет сообщение пользователю Telegram."""

    url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage"

    params = {
        "chat_id": chat_id,
        "text": message,
    }
    logger.info("Попытка отправки Telegram сообщения. chat_id=%s", chat_id)

    try:
        response = requests.post(url, json=params, timeout=10)
        if not response.ok:
            logger.error("Telegram API вернул ошибку: %s", response.text)

        logger.info("Ответ Telegram API: status=%s, body=%s", response.status_code, response.text)
        response.raise_for_status()

        logger.info("Сообщение успешно отправлено. chat_id=%s", chat_id)

    except requests.RequestException as error:

        logger.error(
            "Ошибка Telegram. chat_id=%s, error=%s, response=%s",
            chat_id,
            error,
            getattr(error.response, "text", None),
        )
