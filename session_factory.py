"""
세션 팩토리 - 라이브러리명에 따라 적절한 세션 매니저 인스턴스 생성
"""
from typing import Optional
from session_base import SessionBase
from telethon_session import TelethonSession
from pyrogram_session import PyrogramSession
from telegram_bot_session import TelegramBotSession
from tdlib_session import TDLibSession
from config import SESSION_DIRS


class SessionFactory:
    """세션 매니저 팩토리 클래스"""
    
    @staticmethod
    def create_session_manager(library: str, api_id: str, api_hash: str) -> Optional[SessionBase]:
        """라이브러리명에 따라 세션 매니저 인스턴스 생성"""
        library = library.lower()
        
        if library not in SESSION_DIRS:
            print(f"지원하지 않는 라이브러리: {library}")
            return None
        
        session_dir = SESSION_DIRS[library]
        
        if library == "telethon":
            return TelethonSession(api_id, api_hash, session_dir)
        elif library == "pyrogram":
            return PyrogramSession(api_id, api_hash, session_dir)
        elif library == "telegram-bot":
            return TelegramBotSession(api_id, api_hash, session_dir)
        elif library == "tdlib":
            return TDLibSession(api_id, api_hash, session_dir)
        
        return None
