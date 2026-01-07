import streamlit as st
from core.logging import setup_logging
import queue
from utils.websocket import handler as ws_handler
from handlers import chat
from ui import sidebar, session, answers
import time
from handlers import upload_file

# 로거 초기화
logger = setup_logging()


def main():
    st.set_page_config(page_title="LLM WS Demo", layout="wide", page_icon="🤖")
    st.markdown(
        """
    <style>
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    # UI 구성
    st.title("LLM WebSocket Demo")

    session.initailize_ss_state()

    _, q = ws_handler.get_ws_client()
    is_waiting = st.session_state.ui_state.is_waiting
    if (
        len(st.session_state.ui_state.messages) > 0
        and "hits" in st.session_state.ui_state.messages[:-1]
    ):
        logger.info(f"UI State: {st.session_state.ui_state.__dict__}")

    # ---------- sidebar ----------
    with st.sidebar:
        sidebar.load_sidebar(q)

    # ---------- 입력항목 - chat 질의문 ----------
    query = st.text_area("질문 입력", height=80)
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("질의", type="primary", disabled=is_waiting):
            chat.on_chat(
                query,
                st.session_state.top_k,
                st.session_state.llm_model,
                st.session_state.retriever,
            )
            st.session_state.ui_state.change_waiting_state(True)
            st.session_state.ui_state.reset_messages()
            st.session_state._enable_auto_refresh = True
            st.rerun()

    with col2:
        if st.button("초기화", disabled=is_waiting):
            st.session_state.ui_state.initialize()
            # 큐 비우기
            while not q.empty():
                try:
                    q.get_nowait()
                except queue.Empty:
                    break
            st.rerun()

    # ---------- 수신대기 상태 중, 큐확인 및 화면갱신 ----------
    ws_handler.checking_message_queue(is_waiting)

    # ---------- 화면 출력 처리 ----------
    answers.print_messages()

    # ---------- Bottom Area ----------
    st.divider()
    tab1, tab2 = st.tabs(["파일 업로드", "WebSocket 모니터"])

    with tab1:
        # 입력항목 - 파일업로드
        uploaded = st.file_uploader(
            "PDF / TXT 업로드", type=["pdf", "txt"], accept_multiple_files=False
        )
        if st.button(
            "업로드", type="primary", disabled=st.session_state.ui_state.is_waiting
        ):
            upload_file.on_upload_file(uploaded)

    with tab2:
        st.caption("WebSocket Stream Monitor")
        st.code("listening for incoming frames...")
        if q.qsize() > 0:
            st.info(f"큐에 남은 메시지: {q.qsize()}")
        else:
            st.info("📬 새 메시지 대기 중...")

    # ---------- Rerun timer ----------
    if st.session_state.is_rerun:
        time.sleep(st.session_state.refresh_interval)
        st.rerun()


if __name__ == "__main__":

    main()
