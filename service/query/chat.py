import streamlit as st
from core.websocket import get_ws_client
from service.rag_svc import call_rag_api
import logging

logger = logging.getLogger(__name__)


def on_chat(query: str, top_k, llm, retriever: str):
    if not query:
        st.warning("질문을 입력해주세요")
        return

    query = query.strip()
    ws_client = get_ws_client()
    try:
        ws_client.send_text("[LLM 질의] " + query)
        # RAG 서비스 호출
        call_rag_api(query, top_k, llm, retriever)

    except Exception as e:
        st.session_state.ui_state.change_waiting_state(False)
        st.error(f"전송 실패: {str(e)}")
        logger.error(f"전송 오류: {e}")
