import streamlit as st
import queue


def load_sidebar(mq: queue.Queue):
    st.header("⚙️ 설정")
    # st.caption("### LLM MODEL")
    st.session_state.llm_model = st.selectbox(
        "LLM Model",
        ["studio", "openai"],
        index=0,
    )
    st.session_state.top_k = st.slider("Top-k", 1, 5, 1)
    st.session_state.retriever = st.selectbox(
        "Retriever",
        ["qdrant", "multiQuery", "selfQuery"],
        index=0,
    )

    col1, col2 = st.columns(2)
    col1.metric("수신된 메시지", len(st.session_state.ui_state.messages))
    col2.metric("큐 대기 중", mq.qsize())

    # 자동 새로고침 설정
    refresh_container = st.container(border=True, width="stretch")
    with refresh_container:
        st.markdown("### 새로고침 설정")
        auto_refresh = st.checkbox("자동 새로고침", key="auto_refresh")
        st.session_state.is_rerun = False
        st.session_state.refresh_interval = 0
        if auto_refresh:
            st.session_state.refresh_interval = st.slider(
                "새로고침 간격 (초)", 0.5, 5.0, 1.0, 0.5
            )

            st.session_state.is_rerun = True

        else:
            if st.button("수동 새로고침"):
                st.session_state.is_rerun = True
