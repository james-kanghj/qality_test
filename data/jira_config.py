import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

print("🔎 BASE_URL:", repr(JIRA_BASE_URL))
print("🔎 EMAIL:", repr(JIRA_EMAIL))
print("🔎 TOKEN exists:", bool(JIRA_API_TOKEN))