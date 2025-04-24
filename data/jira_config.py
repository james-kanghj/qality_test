# .env 파일에서 Jira 연동을 위한 환경변수를 로드하고 전역 변수로 설정합니다.

import os
from dotenv import load_dotenv  # .env 파일의 내용을 환경 변수로 불러오기 위한 모듈

# 현재 파일의 위치 기준으로 상위 디렉토리에 있는 .env 파일 경로를 지정하고 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# 환경 변수에서 Jira 연동에 필요한 값들을 읽어옵니다.
JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL")        # ex: https://jamescompanykr.atlassian.net
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")              # ex: jamescompanykr@gmail.com  
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")      # Atlassian에서 발급한 API 토큰

# 불러온 값들을 확인용으로 출력 (개발 시 확인용, 실제 배포 시에는 보안을 위해 제거 권장)
print("🔎 BASE_URL:", repr(JIRA_BASE_URL))             # URL 문자열이 제대로 로드되었는지 확인
print("🔎 EMAIL:", repr(JIRA_EMAIL))                   # 이메일 형식 확인
print("🔎 TOKEN exists:", bool(JIRA_API_TOKEN))        # 토큰은 민감하므로 값의 존재 여부만 출력