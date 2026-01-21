import streamlit as st
from ui.message import get_client
from service.rag_svc import rag_query_svc, agent_query_svc
import logging

logger = logging.getLogger(__name__)


def call_chat_api(query: str, top_k, llm, retriever: str):
    if not query:
        st.warning("질문을 입력해주세요")
        return

    ws = get_client()
    try:
        ws.send_text("[LLM 질의] " + query)
        # RAG 서비스 호출
        rag_query_svc(query, top_k, llm, retriever)

    except Exception as e:
        st.session_state.ui_state.change_waiting_state(False)
        st.error(f"전송 실패: {str(e)}")
        logger.error(f"전송 오류: {e}")


def call_agent_api(query: str):
    if not query:
        st.warning("질문을 입력해주세요")
        return

    try:
        return agent_query_svc(query)
    except Exception as e:
        st.session_state.ui_state.change_waiting_state(False)
        st.error(f"전송 실패: {str(e)}")
        logger.error(f"전송 오류: {e}")
