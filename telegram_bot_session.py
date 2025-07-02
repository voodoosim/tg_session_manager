"""
python-telegram-bot 공식 라이브러리를 사용한 세션 관리
"""

import asyncio
import json
import os
from typing import Dict, Optional

from session_base import SessionBase
from session_utils import extract_session_name, session_to_base64


class TelegramBotSession(SessionBase):
    """python-telegram-bot 세션 매니저"""

    async def create_session(
        self, phone_number: str, code_callback=None, password_callback=None
    ) -> bool:
        """python-telegram-bot은 주로 봇용이므로 유저 세션 미지원"""
        # pylint: disable=unused-argument
        print("python-telegram-bot은 주로 봇 개발용 라이브러리입니다.")
        print("유저 세션 생성은 Telethon 또는 Pyrogram을 사용하세요.")

        # 비동기 입력을 위한 헬퍼 함수
        async def async_input(prompt: str) -> str:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, input, prompt)

        # 대신 봇 토큰으로 세션 정보 저장 가능
        token = await async_input("봇 토큰을 입력하세요 (선택사항, Enter로 건너뛰기): ")
        if token:
            session_name = extract_session_name(phone_number)
            session_path = os.path.join(self.session_dir, f"{session_name}.json")

            session_data = {
                "bot_token": token,
                "phone_number": phone_number,
                "api_id": self.api_id,
                "api_hash": self.api_hash,
                "type": "bot",
            }

            try:
                # 비동기 파일 쓰기
                await self._async_write_json(session_path, session_data)
                print("✓ 봇 세션 정보 저장 완료")
                return True
            except (IOError, OSError) as e:
                print(f"세션 저장 실패: {e}")

        return False

    async def _async_write_json(self, filepath: str, data: dict) -> None:
        """비동기로 JSON 파일 쓰기"""
        loop = asyncio.get_event_loop()

        def write_json():
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        await loop.run_in_executor(None, write_json)

    async def _async_read_json(self, filepath: str) -> dict:
        """비동기로 JSON 파일 읽기"""
        loop = asyncio.get_event_loop()

        def read_json():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)

        return await loop.run_in_executor(None, read_json)

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
                with open(session_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return "bot_token" in data
            except (json.JSONDecodeError, IOError, OSError) as e:
                print(f"세션 검증 실패: {e}")
                return False
        return False

    def get_session_info(self, phone_number: str) -> Optional[Dict]:
        """세션 정보 조회"""
        if self.validate_session(phone_number):
            return {
                "library": "python-telegram-bot",
                "phone": phone_number,
                "type": "bot",
                "valid": True,
            }
        return None
