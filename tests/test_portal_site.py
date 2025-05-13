# Playwright 기반 UI 테스트 케이스

import pytest
from playwright.sync_api import sync_playwright
from jira.jira_reporter import report_result_to_jira  # 테스트 결과를 Jira에 기록하는 함수

# 세션 단위로 브라우저를 초기화하여 테스트 간 브라우저 재사용
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        headless=True # 브라우저 UI를 보여주지 않음.
        browser = p.chromium.launch(headless=True)
        # headless=False: 브라우저 UI를 보여줌, slow_mo로 동작 속도를 늦춰 시각적 확인 가능
        # browser = p.chromium.launch(headless=False, slow_mo=300)
        yield browser
        browser.close()

# QAP-1: 네이버에서 '날씨' 키워드를 입력하고 입력값이 제대로 반영됐는지 확인
def test_keyword_input(browser):
    issue_key = "QAP-1"  # Jira 이슈 키
    keyword = "날씨"     # 입력할 검색어
    page = browser.new_page()
    page.goto("https://www.naver.com")

    search_input = page.get_by_placeholder("검색어를 입력해 주세요.")
    search_input.wait_for()
    search_input.fill(keyword)
    search_input.press("Enter")

    # 입력값과 필드에 실제 입력된 값 비교
    result = keyword in search_input.input_value()
    debug_log = f"입력값: {keyword}, 실제값: {search_input.input_value()}"
    report_result_to_jira(issue_key, result, debug_log)
    assert result  # 입력값이 반영되었는지 검증

# QAP-2: 인코딩 오류 케이스를 시뮬레이션 하기 위해 일부러 실패 유도
def test_korean_encoding(browser):
    issue_key = "QAP-2"
    keyword = "날씨"
    page = browser.new_page()
    page.goto("https://www.naver.com")

    search_input = page.get_by_placeholder("검색어를 입력해 주세요.")
    search_input.wait_for()
    search_input.fill(keyword)
    search_input.press("Enter")
    page.wait_for_load_state("networkidle")  # 페이지 로딩이 끝날 때까지 대기

    # 테스트 실패를 유도하여 Jira 상태 전환/코멘트 로직을 검증
    result = False
    debug_log = f"강제 오류 발생 - 입력값: {keyword}, 실제값: {search_input.input_value()}"
    report_result_to_jira(issue_key, result, debug_log)
    assert result

# QAP-3: 검색 후 리디렉션된 페이지의 URL에 쿼리 파라미터가 포함됐는지 확인
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

        # URL에 "query=" 파라미터가 있는지 확인 → 검색 결과 페이지인지 판단
        result = "query=" in page.url
        debug_log = f"현재 URL: {page.url}"
        report_result_to_jira(issue_key, result, debug_log)
        assert result
    except Exception as e:
        # 예외가 발생하더라도 Jira에는 실패로 기록되도록 처리
        debug_log = f"예외 발생: {str(e)}"
        report_result_to_jira(issue_key, False, debug_log)
        raise


def test_aaaa(browser):
    issue_key = "QAP-4"
    keyword = "Playwright"
    page = browser.new_page()
    
    try:
        page.goto("https://naver.com")  # 실제 페이지 주소로 수정 필요

        # 검색 input 요소에 검색어 입력
        page.fill('#query', keyword)  # 또는 'input[name="query"]'

        result = "query=" in page.url
        # 필요한 후속 처리 (예: 결과 대기)
        page.wait_for_timeout(3000)  # 결과 확인을 위한 대기 시간
        report_result_to_jira(issue_key, result, debug_log)
    except Exception as e:
        # 예외가 발생하더라도 Jira에는 실패로 기록되도록 처리
        debug_log = f"예외 발생: {str(e)}"
        report_result_to_jira(issue_key, False, debug_log)
        raise
