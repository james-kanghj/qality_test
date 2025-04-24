import pytest
import requests
import logging
from playwright.sync_api import sync_playwright
from data.jira_config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN

# ✅ 실패 로그 파일 저장 설정
logging.basicConfig(
    filename="test_failures.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def report_result_to_jira(issue_key: str, result: bool, debug_log: str = ""):
    status = "✅ Passed" if result else "❌ Failed"
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    # ✅ ADF + 로그 포함
    comment_body = [
        {
            "type": "paragraph",
            "content": [{"type": "text", "text": f"Playwright 테스트 결과: {status}"}]
        }
    ]
    if debug_log:
        comment_body.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": f"📄 로그: {debug_log}"}]
        })

    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": comment_body
        }
    }

    try:
        response = requests.post(url, headers=headers, auth=auth, json=payload)
        print(f"[{issue_key}] 결과 Jira에 기록됨: {response.status_code}, 응답: {response.text}")
    except Exception as e:
        print(f"[{issue_key}] Jira 댓글 등록 중 예외 발생: {e}")

    # 실패 시 로그 기록
    if not result:
        logging.info(f"[{issue_key}] ❌ 테스트 실패")
        logging.info(f"📄 로그 내용: {debug_log}")

    transition_issue(issue_key, result)

def transition_issue(issue_key: str, result: bool):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    try:
        res = requests.get(url, headers=headers, auth=auth)
        if res.status_code != 200:
            print(f"[{issue_key}] 전환 목록 실패: {res.status_code}, {res.text}")
            return

        transitions = res.json().get("transitions", [])
        print(f"[{issue_key}] 가능한 전환 상태 목록:")
        for t in transitions:
            print(f"- {t['name']} (ID: {t['id']})")

        target_status = "완료" if result else "Failed"
        transition_id = next((t["id"] for t in transitions if t["name"] == target_status), None)

        if not transition_id:
            print(f"[{issue_key}] '{target_status}' 전환 ID를 찾을 수 없습니다.")
            return

        payload = { "transition": { "id": transition_id } }
        r = requests.post(url, headers=headers, auth=auth, json=payload)
        print(f"[{issue_key}] 상태 전환 응답: {r.status_code}, {r.text}")
    except Exception as e:
        print(f"[{issue_key}] 상태 전환 중 예외 발생: {e}")

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        yield browser
        browser.close()

def test_keyword_input(browser):
    issue_key = "QAP-1"
    keyword = "날씨"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    search_input = page.get_by_placeholder("검색어를 입력해 주세요.")
    search_input.wait_for()
    search_input.fill(keyword)
    search_input.press("Enter")

    result = keyword in search_input.input_value()
    debug_log = f"입력값: {keyword}, 실제값: {search_input.input_value()}"
    report_result_to_jira(issue_key, result, debug_log)
    assert result

def test_korean_encoding(browser):
    issue_key = "QAP-2"
    keyword = "날씨"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    search_input = page.get_by_placeholder("검색어를 입력해 주세요.")
    search_input.wait_for()
    search_input.fill(keyword)
    search_input.press("Enter")
    page.wait_for_load_state("networkidle")

    result = keyword in search_input.input_value()
    debug_log = f"입력값: {keyword}, 실제값: {search_input.input_value()}"
    report_result_to_jira(issue_key, result, debug_log)
    assert result

def test_search_redirect(browser):
    issue_key = "QAP-3"
    keyword = "Playwright"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    try:
        search_input = page.get_by_placeholder("검색를 입력해 주세요.")
        search_input.wait_for()
        search_input.fill(keyword)
        search_input.press("Enter")
        page.wait_for_load_state("networkidle")

        result = "query=" in page.url
        debug_log = f"현재 URL: {page.url}"
        report_result_to_jira(issue_key, result, debug_log)
        assert result
    except Exception as e:
        debug_log = f"예외 발생: {str(e)}"
        report_result_to_jira(issue_key, False, debug_log)
        raise