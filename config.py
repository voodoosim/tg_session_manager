"""
환경 설정 및 상수 관리 모듈
"""
import os
from typing import Dict

# 기본 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")
BASE64_DIR = os.path.join(BASE_DIR, "base64_strings")
API_CONFIG_FILE = os.path.join(BASE_DIR, "api_configs.json")

# 라이브러리별 세션 디렉토리
SESSION_DIRS: Dict[str, str] = {
    "telethon": os.path.join(SESSIONS_DIR, "telethon"),
    "pyrogram": os.path.join(SESSIONS_DIR, "pyrogram"),
    "telegram-bot": os.path.join(SESSIONS_DIR, "telegram-bot"),
    "tdlib": os.path.join(SESSIONS_DIR, "tdlib")
}

# 라이브러리별 Base64 문자열 저장 디렉토리
BASE64_DIRS: Dict[str, str] = {
    "telethon": os.path.join(BASE64_DIR, "telethon"),
    "pyrogram": os.path.join(BASE64_DIR, "pyrogram"),
    "telegram-bot": os.path.join(BASE64_DIR, "telegram-bot"),
    "tdlib": os.path.join(BASE64_DIR, "tdlib")
}

# 기본 설정값
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 60

# 디렉토리 생성
for dir_path in list(SESSION_DIRS.values()) + list(BASE64_DIRS.values()):
    os.makedirs(dir_path, exist_ok=True)
