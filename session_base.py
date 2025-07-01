"""
세션 관리 추상 클래스 - 라이브러리별 인터페이스 정의
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict


class SessionBase(ABC):
    """세션 관리를 위한 추상 기반 클래스"""
    
    def __init__(self, api_id: str, api_hash: str, session_dir: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_dir = session_dir
    
    @abstractmethod
    async def create_session(self, phone_number: str, code_callback=None, 
                           password_callback=None) -> bool:
        """세션 생성 - 구현 필수"""
        pass
    
    @abstractmethod
    def session_to_string(self, phone_number: str) -> Optional[str]:
        """세션을 base64 문자열로 변환"""
        pass
    
    @abstractmethod
    def validate_session(self, phone_number: str) -> bool:
        """세션 유효성 검사"""
        pass
    
    @abstractmethod
    def get_session_info(self, phone_number: str) -> Optional[Dict]:
        """세션 정보 조회"""
        pass
