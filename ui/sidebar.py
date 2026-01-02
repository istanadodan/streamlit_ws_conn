import streamlit as st
import queue
from handlers import upload_file


def load_sidebar(mq: queue.Queue):
    st.header("⚙️ 상태")
    st.metric("수신된 메시지", len(st.session_state.ui_state.messages))
    st.metric("큐 대기 중", mq.qsize())

    # 자동 새로고침 설정
    auto_refresh = st.checkbox("자동 새로고침", value=False)
    st.session_state.is_rerun = False
    st.session_state.refresh_interval = 0
    if auto_refresh:
        st.session_state.refresh_interval = st.slider(
            "새로고침 간격 (초)", 0.5, 5.0, 1.0, 0.5
        )

        if mq.qsize() > 0:
            st.info("📬 새 메시지 대기 중...")
        else:
            st.info("🔄 메시지 확인 중...")

        st.session_state.is_rerun = True

    else:
        if st.button("수동 새로고침"):
            st.session_state.is_rerun = True

    # 입력항목 - 파일업로드
    uploaded = st.file_uploader("PDF/파일 업로드")
    if st.button(
        "업로드", type="primary", disabled=st.session_state.ui_state.is_waiting
    ):
        upload_file.on_upload_file(uploaded)
