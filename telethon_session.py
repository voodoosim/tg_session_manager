"""
Telethon 라이브러리를 사용한 세션 관리
"""
import os
from typing import Optional, Dict
from session_base import SessionBase
from session_utils import extract_session_name, session_to_base64, validate_session_file


class TelethonSession(SessionBase):
    """Telethon 세션 매니저"""
    
    async def create_session(self, phone_number: str, code_callback=None, 
                           password_callback=None) -> bool:
        """Telethon 세션 생성"""
        try:
            from telethon import TelegramClient
            from telethon.errors import SessionPasswordNeededError
            
            session_name = extract_session_name(phone_number)
            session_path = os.path.join(self.session_dir, session_name)
            
            client = TelegramClient(session_path, int(self.api_id), self.api_hash)
            
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.send_code_request(phone_number)
                
                # 인증 코드 입력
                if code_callback:
                    code = code_callback()
                    try:
                        await client.sign_in(phone_number, code)
                    except SessionPasswordNeededError:
                        # 2FA 처리
                        if password_callback:
                            password = password_callback()
                            await client.sign_in(password=password)
            
            await client.disconnect()
            return True
            
        except Exception as e:
            print(f"Telethon 세션 생성 실패: {e}")
            return False
    
    def session_to_string(self, phone_number: str) -> Optional[str]:
        """세션을 base64 문자열로 변환"""
        session_name = extract_session_name(phone_number)
        session_path = os.path.join(self.session_dir, f"{session_name}.session")
        return session_to_base64(session_path)
    
    def validate_session(self, phone_number: str) -> bool:
        """세션 유효성 검사"""
        session_name = extract_session_name(phone_number)
        session_path = os.path.join(self.session_dir, f"{session_name}.session")
        return validate_session_file(session_path)
    
    def get_session_info(self, phone_number: str) -> Optional[Dict]:
        """세션 정보 조회"""
        if self.validate_session(phone_number):
            return {
                "library": "telethon",
                "phone": phone_number,
                "valid": True
            }
        return None
