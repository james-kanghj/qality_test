import pytest
import requests
from playwright.sync_api import sync_playwright
from data.jira_config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN


def report_result_to_jira(issue_key: str, result: bool):
    status = "✅ Passed" if result else "❌ Failed"
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
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
    response = requests.post(url, headers=headers, auth=auth, json=payload)
    print(f"[{issue_key}] 결과 Jira에 기록됨: {response.status_code}")

    transition_issue(issue_key, result)

def transition_issue(issue_key: str, result: bool):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    # 가능한 전환 목록 가져오기
    res = requests.get(url, headers=headers, auth=auth)
    if res.status_code != 200:
        print(f"[{issue_key}] 전환 목록 가져오기 실패: {res.status_code}, {res.text}")
        return

    transitions = res.json().get("transitions", [])
    target_status = "완료" if result else "진행 중"
    
    transition_id = next((t["id"] for t in transitions if t["name"] == target_status), None)
    if not transition_id:
        print(f"[{issue_key}] 상태 '{target_status}' 전환 ID를 찾지 못했습니다.")
        return

    payload = { "transition": { "id": transition_id } }
    r = requests.post(url, headers=headers, auth=auth, json=payload)
    print(f"[{issue_key}] 상태 전환 응답: {r.status_code}, {r.text}")

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        yield browser
        browser.close()

def test_keyword_input(browser):
    print("BASE_URL:", JIRA_BASE_URL)
    print("EMAIL:", JIRA_EMAIL)
    print("TOKEN exists:", bool(JIRA_API_TOKEN))

    issue_key = "QAP-1"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    keyword = "날씨"
    search_input = page.get_by_placeholder("검색어를 입력해 주세요.")
    search_input.wait_for()
    search_input.fill(keyword)
    search_input.press("Enter")

    result = keyword in search_input.input_value()
    report_result_to_jira(issue_key, result)
    assert result

def test_korean_encoding(browser):
    print("BASE_URL:", JIRA_BASE_URL)
    print("EMAIL:", JIRA_EMAIL)
    print("TOKEN exists:", bool(JIRA_API_TOKEN))

    issue_key = "QAP-2"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    keyword = "날씨"
    search_input = page.get_by_placeholder("검색어를 입력해 주세요.")
    search_input.wait_for()
    search_input.fill(keyword)
    search_input.press("Enter")

    page.wait_for_load_state("networkidle")

    result = keyword in search_input.input_value()
    report_result_to_jira(issue_key, result)
    assert result

def test_search_redirect(browser):
    print("BASE_URL:", JIRA_BASE_URL)
    print("EMAIL:", JIRA_EMAIL)
    print("TOKEN exists:", bool(JIRA_API_TOKEN))

    issue_key = "QAP-3"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    keyword = "Playwright"
    search_input = page.get_by_placeholder("검색어를 입력해 주세요.")
    search_input.wait_for()
    search_input.fill(keyword)
    search_input.press("Enter")

    page.wait_for_load_state("networkidle")
    result = "query=" in page.url
    report_result_to_jira(issue_key, result)
    assert result