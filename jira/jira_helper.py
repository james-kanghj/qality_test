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
    transition_issue(issue_key, result)


def transition_issue(issue_key: str, transition_id: str):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    payload = {
        "transition": {
            "id": transition_id
        }
    }
    response = requests.post(url, headers=headers, auth=auth, json=payload)
    print(f"[{issue_key}] 상태 전환 결과: {response.status_code}")