# websocket==0.2.1 클라이언트용 베스트
# create_connection + 내부 WebSocket 핸들링

import orjson
import threading
from websocket import create_connection, WebSocket
from typing import Callable
import logging
import time

logger = logging.getLogger(__name__)


class WSClient:
    def __init__(self, url: str, on_text: Callable):
        self.url = url
        self._callback = on_text
        self._ws: WebSocket
        self._thread = None
        self._running = False
        # 헬스체크 개시
        threading.Thread(target=self.healthcheck, daemon=True).start()

    def healthcheck(self):
        import time

        while True:
            if not self._running:
                try:
                    self._start()
                finally:
                    pass
            time.sleep(5)

    def _listen(self):
        logger.info("WS 리스닝 시작")
        while self._running:
            try:
                msg = self._ws.recv()
                if not msg:
                    continue
                if self._callback:
                    self._callback(orjson.loads(msg))
            except orjson.JSONDecodeError as e:
                logger.error(f"WS 메시지 파싱 오류: {e}")
            except Exception as e:
                logger.error(f"WS 오류: {e}")
                self._running = False
                break
        logger.info("WS 종료 후, healthcheck 중 재시작")
        self.close()

    def _start(self):
        if self._running:
            return
        logger.debug(f"WS 연결 시도: {self.url}")
        self._ws = create_connection(self.url)
        self._running = True
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def send_text(self, text: str):
        if not self._running:
            self._start()
        try:
            self._ws.send(text)
        except Exception:
            self.close()
            self._start()
            raise ConnectionError("WS 전송 실패, 재시도 필요")

    def send_json(self, payload: dict):
        self.send_text(orjson.dumps(payload).decode("utf-8"))

    def close(self):
        self._running = False
        if self._ws:
            try:
                self._ws.close()
            except:
                pass
        self._thread = None
