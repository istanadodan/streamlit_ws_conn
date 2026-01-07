import streamlit as st

st.set_page_config(page_title="LLM WebSocket Demo", layout="wide")

# 상단 타이틀
st.markdown("## LLM WebSocket Demo")

# 메인 레이아웃
left, center = st.columns([1, 3])

with left:
    st.markdown("### 설정")
    model = st.selectbox("LLM Model", ["studio", "gpt", "local"])
    top_k = st.slider("Top-k", 1, 50, 5)

    st.divider()

    st.markdown("#### 새로고침")
    auto_refresh = st.checkbox("자동 새로고침")
    st.button("수동 새로고침")

with center:
    st.markdown("### 질문 입력")
    query = st.text_area("질문", placeholder="질문을 입력하세요", height=120)

    col_q, col_reset = st.columns([1, 6])
    with col_q:
        st.button("질의", use_container_width=True)
    with col_reset:
        st.button("초기화")

    st.divider()

    st.markdown("### 응답")
    st.chat_message("assistant").write("여기에 LLM 응답 스트림 출력")

# 하단 영역
st.divider()
tab1, tab2 = st.tabs(["파일 업로드", "WebSocket 모니터"])

with tab1:
    uploaded = st.file_uploader("PDF / TXT 업로드", type=["pdf", "txt"])
    st.button("업로드")

with tab2:
    st.caption("WebSocket Stream Monitor")
    st.code("listening for incoming frames...")
