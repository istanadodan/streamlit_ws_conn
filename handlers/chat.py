import streamlit as st
import time
from utils.ws_client import get_ws_client
from service.rag_svc import call_rag_api
import logging

logger = logging.getLogger(__name__)


def on_chat(query: str):
    if not query:
        st.warning("질문을 입력해주세요")
        return

    query = query.strip()
    st.session_state.waiting_start_time = time.time()
    ws, _ = get_ws_client()
    try:
        ws.send_text("[LLM 질의] " + query)
        # RAG 서비스 호출
        call_rag_api(query)

        st.session_state.ui_state.change_waiting_state(True)
        logger.info(f"질의 전송: {query}")

    except Exception as e:
        st.session_state.ui_state.change_waiting_state(False)
        st.error(f"전송 실패: {str(e)}")
        logger.error(f"전송 오류: {e}")
