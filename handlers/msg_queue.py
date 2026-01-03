import streamlit as st
from utils.ws_client import get_ws_data
import logging

logger = logging.getLogger(__name__)


def checking_message_queue():
    messages_received = []
    for msg in get_ws_data():
        messages_received.append(msg)

        logger.info(f"메시지 처리: {msg}...")

        if st.session_state.ui_state.check_complete(msg):
            break

    # 새 메시지가 있으면 추가하고 rerun
    st.session_state.ui_state.messages.extend(messages_received)

    # timeout check
    st.session_state.ui_state.check_timeout()
