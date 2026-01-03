import streamlit as st
import logging

logger = logging.getLogger(__name__)


# 응답 출력
def print_messages():
    messages = st.session_state.ui_state.messages
    if not messages:
        return

    st.divider()
    st.subheader(f"📝 답변 ({len(messages)}개 메시지)")

    # 전체 답변
    combined = "\n\n".join([_parse_msg(msg) for msg in messages]) if messages else ""
    st.text_area("전체 내용", combined, height=200, disabled=True)

    # 개별 메시지
    with st.expander("📦 개별 메시지 보기", expanded=False):
        for idx, msg in enumerate(messages, 1):
            st.text_area(f"메시지 #{idx}", msg, height=50, key=f"msg_{idx}")


def _parse_msg(msg: str | dict) -> str:
    if isinstance(msg, dict):
        return msg.get("answer", "no answer")
    else:
        return msg
