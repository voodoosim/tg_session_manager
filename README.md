# 📱 텔레그램 멀티 세션 관리자 v1.0

텔레그램의 여러 라이브러리(Telethon, Pyrogram, TDLib, python-telegram-bot)를 사용하여 
복수 계정의 세션을 효율적으로 생성하고 관리하는 도구입니다.

## 🚀 주요 기능

- ✅ **다중 라이브러리 지원**: Telethon, Pyrogram, TDLib, python-telegram-bot
- ✅ **복수 계정 동시 처리**: 여러 전화번호를 한 번에 입력하여 세션 생성
- ✅ **2FA 지원**: 인증코드와 2차 비밀번호 모두 처리 (3회 재시도)
- ✅ **세션 백업**: 기존 세션 덮어쓰기 시 자동 백업
- ✅ **Base64 변환**: 세션 파일을 문자열로 변환하여 이동/공유 가능
- ✅ **로깅 시스템**: 모든 작업 내역 자동 기록
- ✅ **보안 고려**: .gitignore로 민감 정보 보호

## 📋 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/tg_session_manager.git
cd tg_session_manager
```

### 2. 가상환경 생성 (권장)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

## 🔧 사용 방법

### 1. 프로그램 실행
```bash
python main.py
```

### 2. 실행 흐름
1. **API 설정**: 처음 실행 시 API ID와 Hash 등록
2. **라이브러리 선택**: 사용할 라이브러리 선택 (복수 선택 가능)
3. **전화번호 입력**: 세션을 생성할 전화번호 입력 (쉼표로 구분)
4. **인증 진행**: 각 번호별로 인증코드 입력
5. **결과 확인**: 전체 결과 요약 표시

### 3. 예시
```
텔레그램 멀티 세션 관리자 v1.0
==================================================

등록된 API 목록:
1. MyAPI
2. 새 API 등록

선택하세요: 1

사용할 라이브러리를 선택하세요 (쉼표로 구분):
1. Telethon (유저 세션)
2. Pyrogram (유저 세션)
3. python-telegram-bot (봇 전용)
4. TDLib (고성능 C++ 기반)

선택 (예: 1,2): 1,2

전화번호를 입력하세요 (쉼표로 구분):
예) +821012345678, +821087654321: +821012345678

[telethon] +821012345678 세션 생성 중...
인증 코드 입력 (1/3): 12345
✓ 세션 생성 성공!
Base64: U2Vzc2lvbkZpbGVDb250ZW50cy4uLg==...
```

## 📁 디렉토리 구조
```
tg_session_manager/
├── sessions/              # 세션 파일 저장
│   ├── telethon/         # Telethon 세션
│   ├── pyrogram/         # Pyrogram 세션
│   ├── telegram-bot/     # Bot 세션
│   └── tdlib/           # TDLib 세션
├── logs/                 # 로그 파일
├── api_configs.json      # API 설정 (자동 생성)
└── *.py                  # 소스 코드
```

## ⚠️ 주의사항

1. **API 보안**: `api_configs.json` 파일은 절대 공유하지 마세요
2. **세션 보안**: 세션 파일은 계정 접근 권한과 동일하므로 안전하게 보관하세요
3. **2FA 계정**: 2차 비밀번호가 설정된 계정은 추가 입력이 필요합니다
4. **백업 관리**: 자동 백업된 파일은 수동으로 정리해주세요

## 🔐 보안 권장사항

1. 프로덕션 환경에서는 환경변수 사용:
```bash
export TELEGRAM_API_ID=your_api_id
export TELEGRAM_API_HASH=your_api_hash
```

2. 세션 파일 권한 설정:
```bash
chmod 600 sessions/*/*
```

3. 정기적인 세션 검증 및 갱신

## 🐛 문제 해결

### 인증 실패 시
- 전화번호 형식 확인 (+국가코드 포함)
- API ID/Hash 정확성 확인
- 네트워크 연결 상태 확인

### 패키지 설치 오류 시
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📄 라이선스

MIT License

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
