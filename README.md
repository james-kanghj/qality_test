# 🧲 QAlity - Playwright Test Automation with Jira Integration

This project automates Naver search tests based on Jira (QAlity) issues using [Playwright](https://playwright.dev/) and Python. Test results are posted as Jira comments and issue statuses can be transitioned automatically.

---

## 📁 Project Structure

```bash
qality_test/
├── tests/
│   └── test_portal_site.py     # Playwright test cases
├── jira/
│   ├── jira_helper.py          # Low-level Jira API utilities
│   └── jira_reporter.py        # High-level test result handling
├── data/
│   └── jira_config.py          # Environment variable configuration
├── conftest.py                 # Pytest environment setup
├── .env                        # Jira credentials
├── requirements.txt
└── README.md
```

---

## 📦 Requirements

- Python 3.11+
- `uv` (optional but recommended)
- Jira Cloud (with API access enabled)
- Playwright

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/james-kanghj/qality_test.git
cd qality_test
```

### 2. Create virtual environment

Using `uv` (recommended):

```bash
uv venv .venv
source .venv/bin/activate
```

Or using built-in Python venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Create a `.env` File

In the root directory, create a file named `.env` with the following:

```env
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token
```

✅ This file is used to securely load Jira credentials for API access.

### How to Get Your Jira API Token

- Go to: [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- Click **Create API token**
- Enter a label and confirm
- Copy the generated token and add it to your `.env`

---

## 🚀 Run Tests

```bash
pytest -s tests/
```

Tests will automatically:
- Launch a Chromium browser (UI visible if configured)
- Perform search actions on Naver
- Report results as Jira comments
- Transition Jira issue status (e.g., "To Do" → "Done")

---

## 🛠 Configuration

To enable browser visibility during tests:

```python
# In conftest.py or test setup
browser = p.chromium.launch(headless=False, slow_mo=300)
```

---

## ✅ Features

- Post Playwright test results to Jira issues using ADF (Atlassian Document Format)
- Log failed test results to `test_failures.log`
- Auto-transition Jira issue statuses based on outcome

---

## 📄 Test Scenarios

- **QAP-1**: Validate keyword input (e.g., "날씨")
- **QAP-2**: Force failure to test Jira integration
- **QAP-3**: Check redirected URL for query string

---

## 📊 Logging

- Failures are recorded in `test_failures.log` at the project root

---

## 📢 Contact

- Author: [James Kang](mailto:jamescompanykr@gmail.com)
- Company: James Company — Empowering QA Engineers