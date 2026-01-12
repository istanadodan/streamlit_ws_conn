import streamlit as st
import queue
import logging
from core.websocket.client import WSClient
from core.config import settings

logger = logging.getLogger(__name__)


@st.cache_resource
def get_client(client_id=1, role="alarm") -> WSClient:
    q = queue.Queue()

    def on_ws_msg(msg: dict):
        # 큐에 적재 (백그라운드 스레드)
        logger.info(f"[WS 콜백] 메시지 수신: {msg}...")
        q.put(msg["value"])

    endpoint = f"{settings.websocket_url}?{client_id=}&{role=}"
    return WSClient(endpoint, q=q, on_text=on_ws_msg)
