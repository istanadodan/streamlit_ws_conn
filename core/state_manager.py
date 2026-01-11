import time
import logging

logger = logging.getLogger(__name__)


class UIState:
    _messages: list
    _message_queue: list
    waiting_start_time: float
    is_waiting: bool

    def __init__(self):
        self.initialize()

    def initialize(self):
        """
        Initialize the UI state.
        """
        self.is_waiting = False
        self.waiting_start_time = 0.0
        self._messages = []
        self._message_queue = []

    @property
    def messages(self):
        return self._messages

    @property
    def queue(self):
        return self._message_queue

    @messages.setter
    def messages(self, messages):
        self._messages.extend(messages)
        self._message_queue.extend(messages)

    def reset_messages(self):
        self._messages = []

    def check_timeout(self, timeout_sec: int = 300):
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
        if isinstance(msg, dict) and all([key in msg for key in ["answer", "hits"]]):
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
