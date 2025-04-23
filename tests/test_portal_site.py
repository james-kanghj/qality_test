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

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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