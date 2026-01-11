from pprint import pformat
import logging

logger = logging.getLogger(__name__)


def format_message(msg):
    """메시지 포맷팅 - pprint로 깔끔하게 출력"""
    try:
        return pformat(msg, width=80, compact=False)
    except Exception as e:
        logger.warning(f"메시지 포맷팅 실패: {e}")
        return str(msg)
