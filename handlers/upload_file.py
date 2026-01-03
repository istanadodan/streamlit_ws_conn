import streamlit as st
import time, logging
from service.rag_svc import call_rag_pipeline_api
from utils.ws_client import get_ws_client

logger = logging.getLogger(__name__)


def on_upload_file(uploaded):
    # 이벤트 처리
    if not uploaded:
        st.warning("업로드할 파일을 선택하세요.")
    else:
        st.session_state.waiting_start_time = time.time()
        # file_path = f"/tmp/{uploaded.name}"
        # with open(file_path, "wb") as f:
        #     f.write(uploaded.read())

        ws_client, _ = get_ws_client()
        try:
            ws_client.send_text("[upload file] " + uploaded.name)
            # RAG 파이프라인 서비스 호출
            call_rag_pipeline_api(upload_file=uploaded)

            st.session_state.ui_state.change_waiting_state(True)
            logger.info(f"파일 업로드 전송: {uploaded.name}")

        except Exception as e:
            st.session_state.ui_state.change_waiting_state(False)
            st.error(f"업로드 전송 실패: {str(e)}")
            logger.error(f"업로드 전송 오류: {e}")
