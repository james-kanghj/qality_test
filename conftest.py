# pytest에서 테스트 실행 전 공통으로 실행되는 환경 설정 파일

import sys
import os
from dotenv import load_dotenv

# 루트 디렉토리를 sys.path에 추가하여 상위 디렉토리 모듈(jira 등)을 import 가능하게 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# .env 파일에서 환경 변수 불러오기 (.env는 루트 디렉토리에 위치)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# 환경 변수에서 Jira 인증 및 베이스 URL을 불러와 사용할 수 있도록 변수 설정
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
