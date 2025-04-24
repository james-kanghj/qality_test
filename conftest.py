# pytest에서 테스트 실행 전 공통으로 실행되는 환경 설정 파일

import sys
import os
from dotenv import load_dotenv
from data.jira_config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN

# 루트 디렉토리를 sys.path에 추가하여 상위 디렉토리 모듈(jira 등)을 import 가능하게 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))