"""
메인 CLI 애플리케이션 - 전체 플로우 관리
"""
import asyncio
import sys
import os
from typing import List, Dict
from api_manager import APIManager
from session_factory import SessionFactory
from config import MAX_RETRY_ATTEMPTS, SESSION_DIRS
from logger import SessionLogger
from session_utils import backup_existing_session, extract_session_name


class TelegramSessionManager:
    """텔레그램 세션 관리 메인 클래스"""
    
    def __init__(self):
        self.api_manager = APIManager()
        self.results: List[Dict] = []
        self.logger = SessionLogger()
        
    def print_colored(self, text: str, color: str = "white"):
        """색상 출력 (선택적)"""
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "reset": "\033[0m"
        }
        print(f"{colors.get(color, '')}{text}{colors['reset']}")
    
    def select_or_register_api(self) -> Dict[str, str]:
        """API 선택 또는 등록"""
        apis = self.api_manager.list_apis()
        
        if apis:
            self.print_colored("\n📋 등록된 API 목록:", "cyan")
            for i, api_name in enumerate(apis, 1):
                print(f"  {i}. {api_name}")
            print(f"  {len(apis) + 1}. 새 API 등록")
            
            choice = input("\n선택하세요: ")
            if choice.isdigit() and 1 <= int(choice) <= len(apis):
                api_name = apis[int(choice) - 1]
                return self.api_manager.get_api(api_name)
        
        # 새 API 등록
        self.print_colored("\n🔑 새 API 등록", "yellow")
        name = input("API 이름: ")
        api_id = input("API ID: ")
        api_hash = input("API Hash: ")
        
        self.api_manager.register_api(name, api_id, api_hash)
        self.logger.log_api_registered(name)
        self.print_colored("✅ API 등록 완료!", "green")
        return {"api_id": api_id, "api_hash": api_hash}
    
    def select_libraries(self) -> List[str]:
        """사용할 라이브러리 선택"""
        selected = []
        
        self.print_colored("\n📚 사용할 라이브러리를 선택하세요 (쉼표로 구분):", "cyan")
        print("  1. Telethon (유저 세션)")
        print("  2. Pyrogram (유저 세션)")
        print("  3. python-telegram-bot (봇 전용)")
        print("  4. TDLib (고성능 C++ 기반)")
        
        choices = input("\n선택 (예: 1,2): ").split(',')
        
        library_map = {
            '1': 'telethon',
            '2': 'pyrogram', 
            '3': 'telegram-bot',
            '4': 'tdlib'
        }
        
        for choice in choices:
            lib = library_map.get(choice.strip())
            if lib:
                selected.append(lib)
        
        if selected:
            self.print_colored(f"✅ 선택된 라이브러리: {', '.join(selected)}", "green")
        
        return selected
    
    def input_phone_numbers(self) -> List[str]:
        """전화번호 입력"""
        self.print_colored("\n📱 전화번호를 입력하세요 (쉼표로 구분):", "cyan")
        print("   예) +821012345678, +821087654321")
        phones = input("\n입력: ")
        phone_list = [phone.strip() for phone in phones.split(',') if phone.strip()]
        
        if phone_list:
            self.print_colored(f"✅ 입력된 번호: {len(phone_list)}개", "green")
        
        return phone_list
    
    async def create_sessions(self, api_config: Dict[str, str], 
                            libraries: List[str], phones: List[str]):
        """세션 생성 메인 로직"""
        total_tasks = len(libraries) * len(phones)
        current_task = 0
        
        self.print_colored(f"\n🚀 총 {total_tasks}개 세션 생성 시작...", "magenta")
        print("="*60)
        
        for library in libraries:
            for phone in phones:
                current_task += 1
                self.print_colored(f"\n[{current_task}/{total_tasks}] 처리 중...", "blue")
                
                success = await self._create_single_session(
                    api_config, library, phone
                )
                
                self.results.append({
                    "library": library,
                    "phone": phone,
                    "success": success
                })
    
    async def _create_single_session(self, api_config: Dict[str, str], 
                                   library: str, phone: str) -> bool:
        """단일 세션 생성"""
        manager = SessionFactory.create_session_manager(
            library, api_config['api_id'], api_config['api_hash']
        )
        
        if not manager:
            self.print_colored(f"❌ {library} 매니저 생성 실패", "red")
            return False
        
        # 기존 세션 확인 및 백업
        session_name = extract_session_name(phone)
        session_path = os.path.join(SESSION_DIRS[library], f"{session_name}.session")
        
        if os.path.exists(session_path):
            self.print_colored(f"⚠️  기존 세션 발견: {session_name}", "yellow")
            backup_path = backup_existing_session(session_path)
            if backup_path:
                self.print_colored(f"💾 백업 완료: {os.path.basename(backup_path)}", "green")
                self.logger.log_backup(session_path, backup_path)
        
        print(f"\n🔄 [{library}] {phone} 세션 생성 중...")
        
        for attempt in range(MAX_RETRY_ATTEMPTS):
            try:
                def code_callback():
                    code = input(f"📲 인증 코드 입력 ({attempt + 1}/{MAX_RETRY_ATTEMPTS}): ")
                    self.logger.log_authentication(phone, attempt + 1, bool(code))
                    return code
                
                def password_callback():
                    return input(f"🔐 2FA 비밀번호 입력 ({attempt + 1}/{MAX_RETRY_ATTEMPTS}): ")
                
                success = await manager.create_session(
                    phone, code_callback, password_callback
                )
                
                if success:
                    self.print_colored("✅ 세션 생성 성공!", "green")
                    self.logger.log_session_created(library, phone, True)
                    
                    # Base64 문자열 생성
                    base64_str = manager.session_to_string(phone)
                    if base64_str:
                        self.print_colored(f"🔤 Base64: {base64_str[:50]}...", "cyan")
                    
                    return True
                    
            except Exception as e:
                self.print_colored(f"❌ 시도 {attempt + 1} 실패: {e}", "red")
                self.logger.log_error(str(e))
        
        self.print_colored(f"❌ {phone} 세션 생성 실패 (최대 시도 횟수 초과)", "red")
        self.logger.log_session_created(library, phone, False)
        return False
    
    def print_results(self):
        """전체 결과 출력"""
        print("\n" + "="*60)
        self.print_colored("📊 전체 결과 요약", "magenta")
        print("="*60)
        
        success_count = sum(1 for r in self.results if r['success'])
        total_count = len(self.results)
        fail_count = total_count - success_count
        
        # 성공률 계산
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        
        # 요약 정보
        self.print_colored(f"\n✅ 성공: {success_count}개", "green")
        self.print_colored(f"❌ 실패: {fail_count}개", "red")
        self.print_colored(f"📈 성공률: {success_rate:.1f}%", "cyan")
        
        # 라이브러리별 통계
        print("\n📚 라이브러리별 통계:")
        lib_stats = {}
        for result in self.results:
            lib = result['library']
            if lib not in lib_stats:
                lib_stats[lib] = {'success': 0, 'fail': 0}
            if result['success']:
                lib_stats[lib]['success'] += 1
            else:
                lib_stats[lib]['fail'] += 1
        
        for lib, stats in lib_stats.items():
            total = stats['success'] + stats['fail']
            print(f"  • {lib}: {stats['success']}/{total} 성공")
        
        # 상세 결과
        print("\n📋 상세 결과:")
        print("-" * 60)
        print(f"{'상태':^6} | {'라이브러리':^15} | {'전화번호':^20}")
        print("-" * 60)
        
        for result in self.results:
            status = "✅" if result['success'] else "❌"
            color = "green" if result['success'] else "red"
            self.print_colored(
                f"{status:^6} | {result['library']:^15} | {result['phone']:^20}",
                color
            )
        print("-" * 60)
    
    async def run(self):
        """메인 실행 함수"""
        self.print_colored("🚀 텔레그램 멀티 세션 관리자 v1.0", "magenta")
        print("="*60)
        
        try:
            # 1. API 선택/등록
            api_config = self.select_or_register_api()
            
            # 2. 라이브러리 선택
            libraries = self.select_libraries()
            if not libraries:
                self.print_colored("⚠️  라이브러리를 선택하지 않았습니다.", "yellow")
                return
            
            # 3. 전화번호 입력
            phones = self.input_phone_numbers()
            if not phones:
                self.print_colored("⚠️  전화번호를 입력하지 않았습니다.", "yellow")
                return
            
            # 4. 세션 생성
            await self.create_sessions(api_config, libraries, phones)
            
            # 5. 결과 출력
            self.print_results()
            
        except KeyboardInterrupt:
            self.print_colored("\n\n⚠️  사용자에 의해 중단되었습니다.", "yellow")
            self.logger.log_error("사용자 중단")
        except Exception as e:
            self.print_colored(f"\n❌ 오류 발생: {e}", "red")
            self.logger.log_error(str(e))
        
        self.print_colored("\n👋 프로그램을 종료합니다.", "cyan")


if __name__ == "__main__":
    # Windows 환경에서 컬러 출력 활성화
    if sys.platform.startswith('win'):
        os.system('color')
    
    manager = TelegramSessionManager()
    asyncio.run(manager.run())
