# Playwright 테스트 결과를 Jira에 기록하고 상태를 변경하는 고수준 로직을 처리하는 파일

import os
import logging
from data.jira_config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN

# 테스트 실패 결과를 기록할 로컬 로그 설정
logging.basicConfig(
    filename="test_failures.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# 테스트 결과를 Jira에 코멘트로 남기고, 상태 전환까지 처리하는 핵심 함수
def report_result_to_jira(issue_key: str, result: bool, debug_log: str = ""):
    status = "✅ Passed" if result else "❌ Failed"

    # Atlassian Document Format(ADF) 형식의 코멘트 내용 구성
    comment_body = [
        {"type": "paragraph", "content": [{"type": "text", "text": f"Playwright 테스트 결과: {status}"}]}
    ]
    if debug_log:
        comment_body.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": f"📄 로그: {debug_log}"}]
        })

    # 코멘트 전송에 필요한 payload 및 인증 정보 구성
    payload = {"body": {"type": "doc", "version": 1, "content": comment_body}}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    # Jira 코멘트 등록 시도
    try:
        response = post_comment_to_jira(issue_key, headers, auth, payload)
        print(f"[{issue_key}] 결과 Jira에 기록됨: {response.status_code}, 응답: {response.text}")
    except Exception as e:
        print(f"[{issue_key}] Jira 댓글 등록 중 예외 발생: {e}")

    # 실패한 테스트는 로컬 로그에도 기록
    if not result:
        logging.info(f"[{issue_key}] ❌ 테스트 실패\n📄 로그: {debug_log}")

    # 상태 전환 처리 시도 ('완료' 또는 'Failed'로 전환)
    try:
        transitions = get_transitions(issue_key, headers, auth)
        if transitions.status_code != 200:
            print(f"[{issue_key}] 전환 목록 실패: {transitions.status_code}, {transitions.text}")
            return

        # 전환 가능한 상태 목록 중에서 목표 상태를 찾음
        target_status = "완료" if result else "Failed"
        transition_id = next(
            (t["id"] for t in transitions.json()["transitions"] if t["name"] == target_status),
            None
        )

        if transition_id:
            r = transition_issue(issue_key, transition_id, headers, auth)
            print(f"[{issue_key}] 상태 전환 응답: {r.status_code}, {r.text}")
        else:
            print(f"[{issue_key}] 상태 '{target_status}' 전환 ID를 찾을 수 없습니다.")
    except Exception as e:
        print(f"[{issue_key}] 상태 전환 중 예외 발생: {e}")
