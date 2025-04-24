# Jira API 호출을 직접 수행하는 저수준 함수들을 정의한 모듈

import requests
from data.jira_config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN
import logging

# 로깅 설정 (이미 되어 있다면 생략)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 이슈에 코멘트를 등록하는 함수
def post_comment_to_jira(issue_key: str, headers: dict, auth: tuple, payload: dict):
    """
    Jira 이슈에 ADF 형식의 코멘트를 등록합니다.
    - issue_key: "QAP-1" 형태의 이슈 키
    - headers: API 요청에 필요한 헤더 정보
    - auth: (이메일, API 토큰) 형태의 인증 정보
    - payload: ADF 문서 형식의 댓글 데이터
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    logger.debug(f"[{issue_key}] POST 코멘트 인증 정보: {auth}")        # 디버깅 용도, 실제 배포 전에는 제거 또는 logging으로 대체
    return requests.post(url, headers=headers, auth=auth, json=payload)

# 전환 가능한 상태(Transition 목록)를 가져오는 함수
def get_transitions(issue_key: str, headers: dict, auth: tuple):
    """
    Jira 이슈의 상태 전환 목록을 조회합니다.
    - issue_key: 상태를 전환하고 싶은 이슈의 키
    - headers: 요청 헤더
    - auth: 인증 정보
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    logger.debug(f"[{issue_key}] GET 전환 목록 인증 정보: {auth}")        # 디버깅 용도, 실제 배포 전에는 제거 또는 logging으로 대체
    return requests.get(url, headers=headers, auth=auth)

# 이슈 상태를 전환하는 함수
def transition_issue(issue_key: str, transition_id: str, headers: dict, auth: tuple):
    """
    Jira 이슈의 상태를 전환합니다.
    - issue_key: 이슈 키 (예: QAP-1)
    - transition_id: 전환할 상태 ID (예: 완료 상태의 ID)
    - headers: 요청 헤더
    - auth: 인증 정보
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    payload = {"transition": {"id": transition_id}}
    logger.debug(f"[{issue_key}] POST 상태 전환 인증 정보: {auth}")        # 디버깅 용도, 실제 배포 전에는 제거 또는 logging으로 대체
    return requests.post(url, headers=headers, auth=auth, json=payload)
