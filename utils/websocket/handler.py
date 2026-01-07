import streamlit as st
import queue, logging
from utils.websocket.ws_client import WSClient
from core.config import settings
from pprint import pformat

logger = logging.getLogger(__name__)


# websocket connection을 cache로 저장하는 함수
@st.cache_resource
def get_ws_client() -> tuple:
    q = queue.Queue()

    def on_ws_msg(msg: dict):
        # 큐에 적재 (백그라운드 스레드)
        q.put(msg["value"])
        logger.info(f"[WS 콜백] 메시지 수신: {msg}...")

    client = WSClient(
        f"{settings.websocket_url}?client_id=1&role=alarm", on_text=on_ws_msg
    )
    return client, q


def get_ws_data():
    _, q = get_ws_client()
    while not q.empty():
        try:
            _m = q.get_nowait()
            if _m:
                yield _m
        except queue.Empty:
            break


def checking_message_queue(is_waiting: bool):
    if not is_waiting:
        return
    messages_received = []
    for msg in get_ws_data():
        messages_received.append(msg)

        logger.info(f"메시지 처리: {msg}...")

        if st.session_state.ui_state.check_complete(msg):
            break

    # 새 메시지가 있으면 추가하고 rerun
    st.session_state.ui_state.messages = messages_received

    # timeout check
    st.session_state.ui_state.check_timeout()


def format_message(msg):
    """메시지 포맷팅 - pprint로 깔끔하게 출력"""
    try:
        return pformat(msg, width=80, compact=False)
    except Exception as e:
        logger.warning(f"메시지 포맷팅 실패: {e}")
        return str(msg)
