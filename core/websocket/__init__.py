import streamlit as st
import queue, logging
from core.websocket.client import WSClient
from core.config import settings

logger = logging.getLogger(__name__)


# websocket connection을 cache로 저장하는 함수
@st.cache_resource
def get_ws_client(client_id=1, role="alarm") -> WSClient:
    q = queue.Queue()

    def on_ws_msg(msg: dict):
        # 큐에 적재 (백그라운드 스레드)
        q.put(msg["value"])
        logger.info(f"[WS 콜백] 메시지 수신: {msg}...")

    endpoint = f"{settings.websocket_url}?{client_id=}&{role=}"
    return WSClient(endpoint, q=q, on_text=on_ws_msg)


def update_msg_state(is_waiting: bool) -> None:
    if not is_waiting:
        return
    messages_received = []
    for msg in _get_ws_data():
        messages_received.append(msg)

        logger.info(f"메시지 처리: {msg}...")

        if st.session_state.ui_state.check_complete(msg):
            break

    # 새 메시지가 있으면 추가하고 rerun
    st.session_state.ui_state.messages = messages_received

    # timeout check
    st.session_state.ui_state.check_timeout(600)


def _get_ws_data():
    q = get_ws_client().queue
    while not q.empty():
        try:
            _m = q.get_nowait()
            if _m:
                yield _m
        except queue.Empty:
            break
