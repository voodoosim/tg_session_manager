#!/usr/bin/env python3
"""GUI 애플리케이션 실행 스크립트"""
import sys
import os

# pylint: disable=wrong-import-position
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from tg_session_manager.gui.qt_main import main

if __name__ == "__main__":
    main()
