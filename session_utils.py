"""
세션 유틸리티 - 세션명 추출, base64 변환, 유효성 검사
"""
import base64
import os
import shutil
from datetime import datetime
from typing import Optional


def extract_session_name(phone_number: str) -> str:
    """전화번호에서 세션명 추출 (뒷 8자리)"""
    # 숫자만 추출
    numbers_only = ''.join(filter(str.isdigit, phone_number))
    # 뒷 8자리 반환, 8자리 미만이면 전체 반환
    return numbers_only[-8:] if len(numbers_only) >= 8 else numbers_only


def session_to_base64(session_file_path: str) -> Optional[str]:
    """세션 파일을 base64 문자열로 변환"""
    try:
        if os.path.exists(session_file_path):
            with open(session_file_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"세션 파일 변환 실패: {e}")
    return None


def base64_to_session(base64_string: str, output_path: str) -> bool:
    """base64 문자열을 세션 파일로 복구"""
    try:
        session_data = base64.b64decode(base64_string)
        with open(output_path, 'wb') as f:
            f.write(session_data)
        return True
    except Exception as e:
        print(f"세션 복구 실패: {e}")
        return False


def save_base64_string(base64_string: str, output_path: str) -> bool:
    """base64 문자열을 파일로 저장"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(base64_string)
        return True
    except Exception as e:
        print(f"Base64 저장 실패: {e}")
        return False


def validate_session_file(session_file_path: str) -> bool:
    """세션 파일 유효성 검사"""
    # 파일 존재 여부와 크기 확인
    if os.path.exists(session_file_path):
        file_size = os.path.getsize(session_file_path)
        return file_size > 0
    return False


def backup_existing_session(session_file_path: str) -> Optional[str]:
    """기존 세션 파일 백업"""
    if os.path.exists(session_file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{session_file_path}.backup_{timestamp}"
        try:
            shutil.copy2(session_file_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"세션 백업 실패: {e}")
    return None
