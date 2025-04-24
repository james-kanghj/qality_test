import pytest
from playwright.sync_api import sync_playwright
from jira.jira_reporter import report_result_to_jira


# Playwright 브라우저 초기화
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)                       # UI 안 보이도록 설정
        #browser = p.chromium.launch(headless=False, slow_mo=300)        # UI 보이도록 설정
        yield browser
        browser.close()

# QAP-1: 네이버에서 '날씨' 검색 후 입력값 확인
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

# QAP-2: 한글 검색어 인코딩 처리 확인 (오류를 강제로 발생시킴)
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

    result = False  # 강제로 테스트 실패 처리
    debug_log = f"강제 오류 발생 - 입력값: {keyword}, 실제값: {search_input.input_value()}"
    report_result_to_jira(issue_key, result, debug_log)
    assert result

# QAP-3: 검색 후 URL 쿼리 확인 (리디렉션 여부)
def test_search_redirect(browser):
    issue_key = "QAP-3"
    keyword = "Playwright"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    try:
        search_input = page.get_by_placeholder("검색어를 입력해 주세요.")
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
