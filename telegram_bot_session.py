"""
python-telegram-bot 공식 라이브러리를 사용한 세션 관리
"""
import os
import json
from typing import Optional, Dict
from session_base import SessionBase
from session_utils import extract_session_name, session_to_base64, validate_session_file


class TelegramBotSession(SessionBase):
    """python-telegram-bot 세션 매니저"""
    
    async def create_session(self, phone_number: str, code_callback=None, 
                           password_callback=None) -> bool:
        """python-telegram-bot은 주로 봇용이므로 유저 세션 미지원"""
        print("python-telegram-bot은 주로 봇 개발용 라이브러리입니다.")
        print("유저 세션 생성은 Telethon 또는 Pyrogram을 사용하세요.")
        
        # 대신 봇 토큰으로 세션 정보 저장 가능
        token = input("봇 토큰을 입력하세요 (선택사항, Enter로 건너뛰기): ")
        if token:
            session_name = extract_session_name(phone_number)
            session_path = os.path.join(self.session_dir, f"{session_name}.json")
            
            session_data = {
                "bot_token": token,
                "phone_number": phone_number,
                "api_id": self.api_id,
                "api_hash": self.api_hash,
                "type": "bot"
            }
            
            try:
                with open(session_path, 'w') as f:
                    json.dump(session_data, f, indent=2)
                print("✓ 봇 세션 정보 저장 완료")
                return True
            except Exception as e:
                print(f"세션 저장 실패: {e}")
        
        return False
    
    def session_to_string(self, phone_number: str) -> Optional[str]:
        """세션을 base64 문자열로 변환"""
        session_name = extract_session_name(phone_number)
        session_path = os.path.join(self.session_dir, f"{session_name}.json")
        return session_to_base64(session_path)
    
    def validate_session(self, phone_number: str) -> bool:
        """세션 유효성 검사"""
        session_name = extract_session_name(phone_number)
        session_path = os.path.join(self.session_dir, f"{session_name}.json")
        
        if os.path.exists(session_path):
            try:
                with open(session_path, 'r') as f:
                    data = json.load(f)
                    return 'bot_token' in data
            except:
                pass
        return False
    
    def get_session_info(self, phone_number: str) -> Optional[Dict]:
        """세션 정보 조회"""
        if self.validate_session(phone_number):
            return {
                "library": "python-telegram-bot",
                "phone": phone_number,
                "type": "bot",
                "valid": True
            }
        return None
