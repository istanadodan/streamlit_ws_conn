import streamlit as st
from core.logging import setup_logging
import queue
from utils.ws_client import get_ws_client
from handlers import msg_queue, chat
from ui import sidebar, session, answers
import time

# 로거 초기화
logger = setup_logging()


def main():
    st.set_page_config(page_title="LLM WS Demo")
    st.markdown(
        """
    <style>
    .block-container {
        padding-top: 1rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    # UI 구성
    st.title("LLM WebSocket Demo")

    session.initailize_ss_state()

    _, q = get_ws_client()
    is_waiting = st.session_state.ui_state.is_waiting

    # 사이드바
    with st.sidebar:
        sidebar.load_sidebar(q)

    # 입력항목 - chat 질의문
    query = st.text_area("질문 입력", height=100)
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("질의", type="primary", disabled=is_waiting):
            chat.on_chat(query)

    with col2:
        if st.button("초기화"):
            st.session_state.ui_state.initialize()
            # 큐 비우기
            while not q.empty():
                try:
                    q.get_nowait()
                except queue.Empty:
                    break

    # 수신대기 상태 중, 큐확인 및 화면갱신
    if is_waiting:
        msg_queue.checking_message_queue()

    # 화면 출력 처리
    if st.session_state.ui_state.messages:
        st.divider()
        answers.print_messages(st.session_state.ui_state.messages)

    if st.session_state.is_rerun:
        time.sleep(st.session_state.refresh_interval)
        st.rerun()


if __name__ == "__main__":

    main()
