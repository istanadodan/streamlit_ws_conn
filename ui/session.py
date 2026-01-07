import streamlit as st
from core.session import ChatSession
from service.state_manager import UIState


# session_state 초기화
def initailize_ss_state():
    if "ui_state" not in st.session_state:
        st.session_state.ui_state = UIState()

    # session_state 초기화
    if "chat" not in st.session_state:
        st.session_state.chat = ChatSession()
        st.session_state.chat.start()

    if "is_rerun" not in st.session_state:
        st.session_state.is_rerun = False

    if "refresh_interval" not in st.session_state:
        st.session_state.refresh_interval = 0

    if "auto_refresh" not in st.session_state:
        st.session_state.auto_refresh = False

    if (
        "_enable_auto_refresh" in st.session_state
        and st.session_state._enable_auto_refresh
    ):
        st.session_state.auto_refresh = True
    else:
        st.session_state.auto_refresh = False
