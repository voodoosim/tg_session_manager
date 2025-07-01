"""
API 정보 관리 모듈 - api_id/api_hash 등록, 조회, 저장
"""
import json
import os
from typing import Dict, List, Optional
from config import API_CONFIG_FILE


class APIManager:
    """텔레그램 API 정보를 관리하는 클래스"""
    
    def __init__(self):
        self.api_configs: Dict[str, Dict[str, str]] = self._load_configs()
    
    def _load_configs(self) -> Dict[str, Dict[str, str]]:
        """JSON 파일에서 API 설정 로드"""
        if os.path.exists(API_CONFIG_FILE):
            try:
                with open(API_CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"API 설정 로드 실패: {e}")
        return {}
    
    def save_configs(self) -> None:
        """API 설정을 JSON 파일에 저장"""
        try:
            with open(API_CONFIG_FILE, 'w') as f:
                json.dump(self.api_configs, f, indent=2)
        except Exception as e:
            print(f"API 설정 저장 실패: {e}")
    
    def register_api(self, name: str, api_id: str, api_hash: str) -> bool:
        """새로운 API 정보 등록"""
        self.api_configs[name] = {
            "api_id": api_id,
            "api_hash": api_hash
        }
        self.save_configs()
        return True
    
    def get_api(self, name: str) -> Optional[Dict[str, str]]:
        """등록된 API 정보 조회"""
        return self.api_configs.get(name)
    
    def list_apis(self) -> List[str]:
        """등록된 모든 API 이름 반환"""
        return list(self.api_configs.keys())
