# QAlity - Playwright Test

This project automates the Naver search test based on Jira (QAlity) test cases using Playwright and Python.

## 📦 Requirements

- Python 3.11+
- `uv` (optional but recommended)
- Jira Cloud (with API access enabled)
- Playwright

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/james-kanghj/qality_test.git
cd qality_test
```

### 2. Create virtual environment (if using `uv`)

```bash
uv venv .venv
source .venv/bin/activate
```

Or using traditional Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Create a `.env` file in the root directory:

```
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token
```

> ✅ The `.env` file is used to load Jira credentials for API calls.

## 🚀 Run Tests

```bash
pytest -s tests/
```

Tests will automatically:
- Open Chromium browser (default: headless = False if configured)
- Perform search on Naver
- Report results as comments to corresponding Jira issues
- Attempt to transition Jira issue status based on test outcome (e.g., to "완료" or "진행 중")

## 🛠 Configuration

To run tests with visible browser:
```python
# In conftest.py or test setup
browser = p.chromium.launch(headless=False)
```

## 📄 Notes
- Jira API requires ADF (Atlassian Document Format) for comments.
- Ensure Jira user has access to the project and permission to comment and transition issues.
- `.env` must be placed at the project root.

---

Happy Testing! 🚀