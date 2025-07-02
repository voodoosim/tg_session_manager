"""
TDLib 라이브러리를 사용한 세션 관리
"""
import os
import json
import asyncio
from typing import Optional, Dict
from session_base import SessionBase
from session_utils import extract_session_name, session_to_base64, validate_session_file


class TDLibSession(SessionBase):
    """TDLib 세션 매니저"""
    
    def __init__(self, api_id: str, api_hash: str, session_dir: str):
        super().__init__(api_id, api_hash, session_dir)
        self.td_client = None
    
    async def create_session(self, phone_number: str, code_callback=None, 
                           password_callback=None) -> bool:
        """TDLib 세션 생성"""
        try:
            from telegram.client import Telegram
            
            session_name = extract_session_name(phone_number)
            db_path = os.path.join(self.session_dir, session_name)
            
            # TDLib 클라이언트 초기화
            tg = Telegram(
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone=phone_number,
                database_directory=db_path,
                files_directory=os.path.join(db_path, "files"),
                use_message_database=True,
                use_secret_chats=True,
                system_language_code='ko',
                device_model='Desktop',
                application_version='1.0'
            )
            
            # 로그인 상태 확인
            tg.login()
            
            # 인증 대기
            state = tg.get_authorization_state()
            
            if state['@type'] == 'authorizationStateWaitPhoneNumber':
                # 전화번호 입력
                tg.send_phone_number(phone_number)
                state = tg.get_authorization_state()
            
            if state['@type'] == 'authorizationStateWaitCode':
                # 인증 코드 입력
                if code_callback:
                    code = code_callback()
                    tg.send_code(code)
                    state = tg.get_authorization_state()
            
            if state['@type'] == 'authorizationStateWaitPassword':
                # 2FA 비밀번호 입력
                if password_callback:
                    password = password_callback()
                    tg.send_password(password)
                    state = tg.get_authorization_state()
            
            # 로그인 완료 확인
            if state['@type'] == 'authorizationStateReady':
                print("✓ TDLib 세션 생성 성공!")
                
                # 세션 정보 저장
                session_info = {
                    "phone_number": phone_number,
                    "api_id": self.api_id,
                    "api_hash": self.api_hash,
                    "db_path": db_path,
                    "library": "tdlib"
                }
                
                info_path = os.path.join(self.session_dir, f"{session_name}_info.json")
                with open(info_path, 'w') as f:
                    json.dump(session_info, f, indent=2)
                
                tg.stop()
                return True
            
            tg.stop()
            return False
            
        except ImportError:
            print("python-telegram 패키지가 설치되지 않았습니다.")
            print("pip install python-telegram 명령으로 설치해주세요.")
            return False
        except Exception as e:
            print(f"TDLib 세션 생성 실패: {e}")
            return False
    
    def session_to_string(self, phone_number: str) -> Optional[str]:
        """세션을 base64 문자열로 변환"""
        session_name = extract_session_name(phone_number)
        info_path = os.path.join(self.session_dir, f"{session_name}_info.json")
        return session_to_base64(info_path)
    
    def validate_session(self, phone_number: str) -> bool:
        """세션 유효성 검사"""
        session_name = extract_session_name(phone_number)
        db_path = os.path.join(self.session_dir, session_name)
        info_path = os.path.join(self.session_dir, f"{session_name}_info.json")
        
        # TDLib 데이터베이스와 정보 파일 모두 확인
        return os.path.exists(db_path) and os.path.exists(info_path)
    
    def get_session_info(self, phone_number: str) -> Optional[Dict]:
        """세션 정보 조회"""
        if self.validate_session(phone_number):
            session_name = extract_session_name(phone_number)
            info_path = os.path.join(self.session_dir, f"{session_name}_info.json")
            
            try:
                with open(info_path, 'r') as f:
                    info = json.load(f)
                    info['valid'] = True
                    return info
            except:
                pass
        
        return None
