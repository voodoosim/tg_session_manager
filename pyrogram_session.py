"""
Pyrogram 라이브러리를 사용한 세션 관리
"""
import os
from typing import Optional, Dict
from session_base import SessionBase
from session_utils import extract_session_name, session_to_base64, validate_session_file


class PyrogramSession(SessionBase):
    """Pyrogram 세션 매니저"""
    
    async def create_session(self, phone_number: str, code_callback=None, 
                           password_callback=None) -> bool:
        """Pyrogram 세션 생성"""
        try:
            from pyrogram import Client
            from pyrogram.errors import SessionPasswordNeeded
            
            session_name = extract_session_name(phone_number)
            
            app = Client(
                session_name,
                api_id=int(self.api_id),
                api_hash=self.api_hash,
                workdir=self.session_dir,
                phone_number=phone_number
            )
            
            await app.connect()
            
            if not await app.is_user_authorized():
                sent_code = await app.send_code(phone_number)
                
                # 인증 코드 입력
                if code_callback:
                    code = code_callback()
                    try:
                        await app.sign_in(phone_number, sent_code.phone_code_hash, code)
                    except SessionPasswordNeeded:
                        # 2FA 처리
                        if password_callback:
                            password = password_callback()
                            await app.check_password(password)
            
            await app.disconnect()
            return True
            
        except Exception as e:
            print(f"Pyrogram 세션 생성 실패: {e}")
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
                "library": "pyrogram",
                "phone": phone_number,
                "valid": True
            }
        return None
