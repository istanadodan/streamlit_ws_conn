import streamlit as st
from core.session import ChatSession
from core.websocket_client import WSClient
import queue
from service.rag_svc import call_rag_api
from core.logging import setup_logging
import time
from pprint import pformat

# 로거 초기화
logger = setup_logging()


# websocket connection을 cache로 저장하는 함수
@st.cache_resource
def get_ws_client():
    q = queue.Queue()

    def on_ws_msg(msg: str):
        # 큐에 적재 (백그라운드 스레드)
        q.put(msg)
        logger.info(f"[WS 콜백] 메시지 수신: {msg[:100]}...")

    client = WSClient(
        "ws://rag-api.local/rag-api/ws?client_id=1&role=alarm", on_text=on_ws_msg
    )
    return client, q


def format_message(msg):
    """메시지 포맷팅 - pprint로 깔끔하게 출력"""
    try:
        return pformat(msg, width=80, compact=False)
    except Exception as e:
        logger.warning(f"메시지 포맷팅 실패: {e}")
        return str(msg)


def main():
    st.set_page_config(page_title="LLM WS Demo")

    # session_state 초기화
    if "chat" not in st.session_state:
        st.session_state.chat = ChatSession()
        st.session_state.chat.start()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    ws, msg_queue = get_ws_client()

    # UI 구성
    st.title("LLM WebSocket Demo")

    uploaded = st.file_uploader("PDF/파일 업로드")
    query = st.text_area("질문 입력", height=100)

    col1, col2 = st.columns([1, 3])
    with col1:
        submit_btn = st.button("질의", type="primary")
    with col2:
        if st.button("초기화"):
            st.session_state.messages = []
            # 큐 비우기
            while not msg_queue.empty():
                try:
                    msg_queue.get_nowait()
                except queue.Empty:
                    break
            st.rerun()

    # 질의 버튼 클릭 처리
    if submit_btn and query.strip():
        file_path = None
        if uploaded:
            file_path = f"/tmp/{uploaded.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded.read())

        payload = {"query": query, "file": file_path}

        try:
            ws.send_text(str(payload))
            call_rag_api(query)
            logger.info(f"질의 전송: {query}")
        except Exception as e:
            st.error(f"전송 실패: {str(e)}")
            logger.error(f"전송 오류: {e}")

    # 메시지 수신 처리 (버튼 클릭과 무관하게 항상 확인)
    messages_received = []
    while not msg_queue.empty():
        try:
            msg = msg_queue.get_nowait()
            formatted = format_message(msg)
            messages_received.append(formatted)
            logger.info(f"메시지 처리: {formatted[:50]}...")
        except queue.Empty:
            break

    # 새 메시지가 있으면 추가하고 rerun
    if messages_received:
        st.session_state.messages.extend(messages_received)
        st.rerun()

    # 답변 표시
    if st.session_state.messages:
        st.divider()
        st.subheader(f"📝 답변 ({len(st.session_state.messages)}개 메시지)")

        # 전체 답변
        combined = "\n\n" + "=" * 50 + "\n\n".join(st.session_state.messages)
        st.text_area("전체 내용", combined, height=400)

        # 개별 메시지
        with st.expander("📦 개별 메시지 보기", expanded=False):
            for idx, msg in enumerate(st.session_state.messages, 1):
                st.text_area(f"메시지 #{idx}", msg, height=150, key=f"msg_{idx}")

    # 사이드바
    with st.sidebar:
        st.header("⚙️ 상태")
        st.metric("수신된 메시지", len(st.session_state.messages))
        st.metric("큐 대기 중", msg_queue.qsize())

        # 자동 새로고침 설정
        auto_refresh = st.checkbox("자동 새로고침", value=True)
        if auto_refresh:
            refresh_interval = st.slider("새로고침 간격 (초)", 0.5, 5.0, 1.0, 0.5)

            if msg_queue.qsize() > 0:
                st.info("📬 새 메시지 대기 중...")
            else:
                st.info("🔄 메시지 확인 중...")

            time.sleep(refresh_interval)
            st.rerun()
        else:
            if st.button("수동 새로고침"):
                st.rerun()


if __name__ == "__main__":
    main()
