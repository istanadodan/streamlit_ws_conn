import streamlit as st
import queue
import time
import ui.message as message
from core.logging import setup_logging
from service.pipeline import upload_file as pipeline_svc
from service.query import chat as chat_svc

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
    message.session.initailize_ss_state()

    q = message.get_client().queue
    is_waiting = st.session_state.ui_state.is_waiting

    # ---------- sidebar ----------
    with st.sidebar:
        message.sidebar.load_sidebar(q)

    tab_llm, tab_agt = st.tabs(["LLM Chat", "LLM Agent"])
    with tab_llm:
        # ---------- 입력항목 - chat 질의문 ----------
        query1 = st.text_area("질문 입력", height=80, key="llm_query_txt").strip()
        col11, col12 = st.columns([10, 1])
        with col11:
            if st.button("RAG 질의", type="primary", disabled=is_waiting or not query1):
                if query1:
                    chat_svc.call_chat_api(
                        query1,
                        st.session_state.top_k,
                        st.session_state.llm_model,
                        st.session_state.retriever,
                    )
                    st.session_state.ui_state.change_waiting_state(True)
                    st.session_state.ui_state.reset_messages()
                    st.rerun()
                else:
                    st.warning("질의를 입력해주세요.")

        with col12:
            if st.button("초기화", disabled=is_waiting):
                st.session_state.ui_state.initialize()
                # 큐 비우기
                while not q.empty():
                    try:
                        q.get_nowait()
                    except queue.Empty:
                        break
                st.rerun()
    with tab_agt:
        query2 = st.text_area("질의 입력", height=80).strip()
        col21, col22 = st.columns([10, 1])
        with col21:
            if st.button(
                "Agent 질의", type="primary", disabled=is_waiting or not query2
            ):
                if query2:
                    response = chat_svc.call_agent_api(query2)
                    st.session_state.ui_state.messages.append(
                        dict(answer=str(response))
                    )
                    st.rerun()
                else:
                    st.warning("질의를 입력해주세요.")
        with col22:
            if st.button("재시작", disabled=is_waiting):
                st.session_state.ui_state.initialize()
                st.rerun()

    # ---------- 수신대기 상태 중, 큐확인 및 화면갱신 ----------
    message.update_msg_state(is_waiting)

    # ---------- 화면 출력 처리 ----------
    message.answers.print_messages()

    # ---------- Bottom Area ----------
    st.divider()
    tab1, tab2 = st.tabs(["파일 업로드", "WebSocket 모니터"])

    with tab1:
        # 입력항목 - 파일업로드
        file = st.file_uploader(
            "PDF / TXT 업로드", type=["pdf", "txt"], accept_multiple_files=False
        )
        if st.button(
            "업로드", type="primary", disabled=st.session_state.ui_state.is_waiting
        ):
            st.session_state.ui_state.change_waiting_state(True)
            pipeline_svc.call_pipeline_api(file)

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
