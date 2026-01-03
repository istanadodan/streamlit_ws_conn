import time
import logging
import streamlit as st

logger = logging.getLogger(__name__)


class UIState:
    def __init__(self):
        self.initialize()

    def initialize(self):
        """
        Initialize the UI state.
        """
        self.is_waiting = False
        self.waiting_start_time = 0.0
        self.messages = []
        self.message_count = 0
        self.message_queue = []

    def check_timeout(self, timeout_sec: int = 1800):
        if self.is_waiting and self.waiting_start_time + timeout_sec < time.time():
            logger.info(
                f"Timeout: {self.waiting_start_time + timeout_sec*1000} < {time.time()}"
            )
            self.is_waiting = False
            self.waiting_start_time = 0.0

    def check_complete(self, msg) -> bool:
        """
        Check if the message is complete.
        """
        if isinstance(msg, dict) and "hits" in msg and msg["hits"]:
            # 답변 메시지인 경우, 완료처리
            self.change_waiting_state(False)
            return True
        return False

    def change_waiting_state(self, is_waiting: bool):
        """
        Change the waiting state of the UI.
        """
        self.is_waiting = is_waiting
        if self.is_waiting and self.waiting_start_time == 0.0:
            self.waiting_start_time = time.time()

    def update_ui_state(self, **kwargs):
        """
        Update the UI state.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
