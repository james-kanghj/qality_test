import requests
from data.jira_config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN

auth = (JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def report_result_to_jira(issue_key: str, result: bool):
    status = "✅ Passed" if result else "❌ Failed"
    comment_url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    payload = {
        "body": f"*Playwright 테스트 결과*\n결과: {status}"
    }
    res = requests.post(comment_url, headers=headers, auth=auth, json=payload)
    print(f"[{issue_key}] 결과 Jira에 기록됨: {res.status_code}")

    # 상태도 함께 변경
    transition_issue_status(issue_key, result)

def transition_issue_status(issue_key: str, result: bool):
    transitions_url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    res = requests.get(transitions_url, headers=headers, auth=auth)
    transitions = res.json().get("transitions", [])

    target_status = "완료" if result else "진행 중"
    transition_id = next((t["id"] for t in transitions if t["name"] == target_status), None)

    if transition_id:
        payload = {"transition": {"id": transition_id}}
        res = requests.post(transitions_url, headers=headers, auth=auth, json=payload)
        print(f"[{issue_key}] 상태 변경 → '{target_status}' ({res.status_code})")
    else:
        print(f"[{issue_key}] 상태 '{target_status}'로 변경 불가. 전환 가능 상태: {[t['name'] for t in transitions]}")