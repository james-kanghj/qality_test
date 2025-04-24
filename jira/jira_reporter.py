import os
import logging
from dotenv import load_dotenv
from jira.jira_helper import post_comment_to_jira, get_transitions, transition_issue

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL").strip()
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN").strip()

# 문자열 양끝의 불필요한 따옴표 제거
if JIRA_EMAIL:
    JIRA_EMAIL = JIRA_EMAIL.strip('"')
if JIRA_API_TOKEN:
    JIRA_API_TOKEN = JIRA_API_TOKEN.strip('"')
    
print("")
print("🔎 BASE_URL:", os.getenv("JIRA_BASE_URL"))
print("🔎 EMAIL:", os.getenv("JIRA_EMAIL"))
print("🔎 TOKEN exists:", bool(os.getenv("JIRA_API_TOKEN")))


logging.basicConfig(filename="test_failures.log", level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

def report_result_to_jira(issue_key: str, result: bool, debug_log: str = ""):
    status = "✅ Passed" if result else "❌ Failed"
    comment_body = [
        {"type": "paragraph", "content": [{"type": "text", "text": f"Playwright 테스트 결과: {status}"}]}
    ]
    if debug_log:
        comment_body.append({"type": "paragraph", "content": [{"type": "text", "text": f"📄 로그: {debug_log}"}]})

    payload = {"body": {"type": "doc", "version": 1, "content": comment_body}}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    try:
        response = post_comment_to_jira(issue_key, headers, auth, payload)
        print(f"[{issue_key}] 결과 Jira에 기록됨: {response.status_code}, 응답: {response.text}")
    except Exception as e:
        print(f"[{issue_key}] Jira 댓글 등록 중 예외 발생: {e}")

    if not result:
        logging.info(f"[{issue_key}] ❌ 테스트 실패\n📄 로그: {debug_log}")

    try:
        transitions = get_transitions(issue_key, headers, auth)
        if transitions.status_code != 200:
            print(f"[{issue_key}] 전환 목록 실패: {transitions.status_code}, {transitions.text}")
            return

        target_status = "완료" if result else "Failed"
        transition_id = next((t["id"] for t in transitions.json()["transitions"] if t["name"] == target_status), None)

        if transition_id:
            r = transition_issue(issue_key, transition_id, headers, auth)
            print(f"[{issue_key}] 상태 전환 응답: {r.status_code}, {r.text}")
        else:
            print(f"[{issue_key}] 상태 '{target_status}' 전환 ID를 찾을 수 없습니다.")
    except Exception as e:
        print(f"[{issue_key}] 상태 전환 중 예외 발생: {e}")
