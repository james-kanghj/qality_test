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
        "body": f"*Playwright 테스트 결과*\n결과: {status}"
    }
    response = requests.post(url, headers=headers, auth=auth, json=payload)
    print(f"[{issue_key}] 결과 Jira에 기록됨: {response.status_code}")

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

def test_keyword_input(browser):
    issue_key = "SCRUM-1"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    search_input = page.locator("input[name='query']")
    keyword = "테스트 키워드"
    search_input.fill(keyword)

    result = search_input.input_value() == keyword
    report_result_to_jira(issue_key, result)
    assert result

def test_korean_encoding(browser):
    issue_key = "SCRUM-2"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    search_input = page.locator("input[name='query']")
    korean_word = "한글 검색어"
    search_input.fill(korean_word)
    search_input.press("Enter")

    page.wait_for_load_state("networkidle")

    result_input = page.locator("input[name='query']")
    result = korean_word in result_input.input_value()
    report_result_to_jira(issue_key, result)
    assert result

def test_search_redirect(browser):
    issue_key = "SCRUM-3"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    search_input = page.locator("input[name='query']")
    keyword = "플레이라이트"
    search_input.fill(keyword)
    search_input.press("Enter")

    try:
        page.wait_for_url("**search.naver.com/**", timeout=5000)
        result = "search.naver.com" in page.url
    except:
        result = False

    report_result_to_jira(issue_key, result)
    assert result