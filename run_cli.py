#!/usr/bin/env python3
"""CLI 애플리케이션 실행 스크립트"""
import sys
import os
import asyncio

# pylint: disable=wrong-import-position
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from tg_session_manager.cli.main import TelegramSessionManager

if __name__ == "__main__":
    manager = TelegramSessionManager()
    asyncio.run(manager.run())
