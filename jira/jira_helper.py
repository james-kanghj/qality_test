import requests
from data.jira_config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN

def post_comment_to_jira(issue_key: str, headers: dict, auth: tuple, payload: dict):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    print(auth)
    return requests.post(url, headers=headers, auth=auth, json=payload)

def get_transitions(issue_key: str, headers: dict, auth: tuple):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    print(auth)
    return requests.get(url, headers=headers, auth=auth)

def transition_issue(issue_key: str, transition_id: str, headers: dict, auth: tuple):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    payload = {"transition": {"id": transition_id}}
    print(auth)
    return requests.post(url, headers=headers, auth=auth, json=payload)
