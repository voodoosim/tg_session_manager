"""텔레그램 세션 관리 패키지"""

# 실제 import를 통해 __all__ 정의
from .api_manager import APIManager
from .logger import SessionLogger
from .session_base import SessionBase
from .session_factory import SessionFactory
from .session_utils import (
    backup_existing_session,
    base64_to_session,
    extract_session_name,
    session_to_base64,
    validate_session_file,
)

# 세션 구현체들
try:
    from .telethon_session import TelethonSession
except ImportError:
    TelethonSession = None

try:
    from .pyrogram_session import PyrogramSession
except ImportError:
    PyrogramSession = None

try:
    from .telegram_bot_session import TelegramBotSession
except ImportError:
    TelegramBotSession = None

try:
    from .tdlib_session import TDLibSession
except ImportError:
    TDLibSession = None

__all__ = [
    "APIManager",
    "SessionBase",
    "SessionFactory",
    "TelethonSession",
    "PyrogramSession",
    "TelegramBotSession",
    "TDLibSession",
    "SessionLogger",
    "extract_session_name",
    "session_to_base64",
    "base64_to_session",
    "validate_session_file",
    "backup_existing_session",
]
