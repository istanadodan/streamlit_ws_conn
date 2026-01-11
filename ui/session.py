import streamlit as st
from core.state_manager import UIState


# session_state 초기화
def initailize_ss_state():
    if "ui_state" not in st.session_state:
        st.session_state.ui_state = UIState()

    if "is_rerun" not in st.session_state:
        st.session_state.is_rerun = False

    if "refresh_interval" not in st.session_state:
        st.session_state.refresh_interval = 0

    if "auto_refresh" not in st.session_state:
        st.session_state.auto_refresh = False

    if "_enable_auto_refresh" not in st.session_state:
        st.session_state._enable_auto_refresh = False


def get_ui_state():
    if "ui_state" in st.session_state and st.session_state.ui_state:
        return st.session_state.ui_state
