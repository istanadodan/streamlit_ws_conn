import streamlit as st
from core.config import settings
import asyncpg
import asyncio
from datetime import datetime
import json
from core.logging import get_logger

logger = get_logger(__name__)

queue = asyncio.Queue()


async def subscribe_pipeline_completed(callback=None):
    """pipeline_completed pg_notify 채널 구독"""
    logger.info("pipeline_completed 채널 구독 시작")
    conn = None
    try:
        conn = await asyncpg.connect(settings.SUPABASE_DB_URL)

        async def listen():
            await conn.add_listener(
                "pipeline_completed", callback or handle_pipeline_event
            )
            st.balloons()
            st.success("✅ pipeline_completed 채널 구독 시작")

        await listen()
        # await asyncio.Event().wait()
        await asyncio.sleep(60 * 3)  # 3분 대기

    except asyncio.CancelledError:
        pass
    except Exception as e:
        st.error(f"❌ 구독 오류: {e}")
    finally:
        if conn:
            await conn.close()


def handle_pipeline_event(conn, pid, channel, payload):
    """pipeline_completed 이벤트 핸들러"""
    logger.info(f"{conn}, {pid}, {channel}, {payload}")
    try:
        event_data = json.loads(payload)
        event = {
            "channel": channel,
            "id": event_data.get("id"),
            "content": (
                event_data.get("content", "")[:200] + "..."
                if len(event_data.get("content", "")) > 200
                else event_data.get("content", "")
            ),
            "meta": event_data.get("meta"),
            "created_at": event_data.get("created_at"),
            "received_at": datetime.now().isoformat(),
        }

        queue.put_nowait(event)

    except json.JSONDecodeError:
        st.session_state.error_payload = payload
        st.rerun()
