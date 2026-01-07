import streamlit as st
from core.session import ChatSession
from core.llm_client import LLMClient
from utils.websocket.ws_client import WSClient
import queue
from service.rag_svc import call_rag_api
from core.logging import setup_logging
import time
import orjson

logger = setup_logging()


# websocket connection을 cache로 저장하는 함수
@st.cache_resource
def get_ws_client():
    q = queue.Queue()

    def on_ws_msg(msg: str):
        # 여기서는 오직 Queue 에만 적재 (백그라드 스레드)
        q.put(msg)

    client = WSClient(
        "ws://rag-api.local/rag-api/ws?client_id=1&role=alarm", on_text=on_ws_msg
    )
    return client, q


def main():
    st.set_page_config(page_title="LLM WS Demo")

    if "chat" not in st.session_state:
        st.session_state.chat = ChatSession()
        st.session_state.chat.start()

    if "last_answer" not in st.session_state:
        st.session_state.last_answer = []

    if "is_waiting" not in st.session_state:
        st.session_state.is_waiting = False

    ws, msg_queue = get_ws_client()
    uploaded = st.file_uploader("PDF/파일 업로드")
    query = st.text_area("질문 입력")

    # if st.button("연결"):
    #     ws.start()

    if st.button("질의"):

        file_path = None
        if uploaded:
            file_path = f"/tmp/{uploaded.name}"
            # with open(file_path, "wb") as f:
            #     f.write(uploaded.read())

        payload = {"query": query, "file": file_path}
        ws.send_text(str(payload))
        call_rag_api(query)

        st.session_state.is_waiting = True

    if st.session_state.is_waiting:

        st.info("📬 대기 중...")
        # 메시지 수신 처리 (한 번만)
        while not msg_queue.empty():
            try:
                msg = msg_queue.get()
                try:
                    recv_msg = orjson.loads(msg)
                    if "value" in recv_msg:
                        st.session_state.is_waiting = False
                except orjson.JSONDecodeError:
                    recv_msg = msg

                st.session_state.last_answer.append(recv_msg)
                logger.info(f"메시지 처리: {recv_msg}")
                st.rerun()
            except queue.Empty:
                st.session_state.last_answer = ""
                st.session_state.is_waiting = False
                break

    # UI 출력
    if st.session_state.last_answer:
        with st.expander("📝 답변 보기", expanded=True):
            for idx, msg in enumerate(st.session_state.last_answer, 1):
                st.text_area(f"메시지 #{idx}", msg, height=150, key=f"msg_{idx}")

    if st.session_state.is_waiting:
        time.sleep(1)  # 1초 후 자동 재실행
        st.rerun()


if __name__ == "__main__":
    main()
