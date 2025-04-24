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

    # Atlassian Document Format (ADF) 구조
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Playwright 테스트 결과: {status}"
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(comment_url, headers=headers, auth=auth, json=payload)
    print(f"[{issue_key}] 결과 Jira에 기록됨: {response.status_code}, 응답: {response.text}")

    # 상태도 함께 변경
    transition_issue(issue_key, result)


def transition_issue(issue_key: str, result: bool):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"

    res = requests.get(url, headers=headers, auth=auth)
    if res.status_code != 200:
        print(f"[{issue_key}] 상태 전환 목록 조회 실패: {res.status_code}, {res.text}")
        return

    transitions = res.json().get("transitions", [])
    print(f"[{issue_key}] 전환 가능한 상태 목록:")
    for t in transitions:
        print(f"  - {t['id']}: {t['name']}")

    # 자동 탐색 우선순위로 상태 이름 지정 (Jira 워크플로우에 맞게 조정 가능)
    preferred_names = ["Done", "완료", "Complete"] if result else ["In Progress", "진행 중", "Working"]

    transition_id = None
    for name in preferred_names:
        for t in transitions:
            if t["name"].lower() == name.lower():
                transition_id = t["id"]
                print(f"[{issue_key}] '{name}' 상태로 전환 ID 찾음 → {transition_id}")
                break
        if transition_id:
            break

    if not transition_id:
        print(f"[{issue_key}] 원하는 상태로 전환 가능한 ID를 찾지 못했습니다.")
        return

    payload = {
        "transition": {
            "id": transition_id
        }
    }

    response = requests.post(url, headers=headers, auth=auth, json=payload)
    print(f"[{issue_key}] 상태 전환 결과: {response.status_code}, 응답: {response.text}")
