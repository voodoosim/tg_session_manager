"""
로깅 시스템 - 세션 생성/실패/삭제 등 이벤트 기록
"""

import logging
import os
from datetime import datetime
from typing import Optional

from config import BASE_DIR


class SessionLogger:
    """세션 관리 로거"""

    def __init__(self, log_file: Optional[str] = None):
        if log_file is None:
            log_dir = os.path.join(BASE_DIR, "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(
                log_dir, f"session_{datetime.now().strftime('%Y%m%d')}.log"
            )

        # 로거 설정
        self.logger = logging.getLogger("SessionManager")
        self.logger.setLevel(logging.INFO)

        # 기존 핸들러 제거
        self.logger.handlers = []

        # 파일 핸들러
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # 포맷터
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 핸들러 추가
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_session_created(self, library: str, phone: str, success: bool):
        """세션 생성 로그"""
        if success:
            self.logger.info("세션 생성 성공: %s - %s", library, phone)
        else:
            self.logger.error("세션 생성 실패: %s - %s", library, phone)

    def log_authentication(self, phone: str, attempt: int, success: bool):
        """인증 시도 로그"""
        if success:
            self.logger.info("인증 성공: %s (시도 %d)", phone, attempt)
        else:
            self.logger.warning("인증 실패: %s (시도 %d)", phone, attempt)

    def log_backup(self, original_path: str, backup_path: str):
        """백업 로그"""
        self.logger.info("세션 백업: %s -> %s", original_path, backup_path)

    def log_api_registered(self, api_name: str):
        """API 등록 로그"""
        self.logger.info("API 등록: %s", api_name)

    def log_error(self, error_msg: str):
        """에러 로그"""
        self.logger.error("에러: %s", error_msg)
