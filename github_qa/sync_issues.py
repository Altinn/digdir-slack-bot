import requests
import box
import os
import yaml
import math
import pprint
import typesense
from datetime import datetime

with open('github_qa/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

get_github_batch_size = 80

pp = pprint.PrettyPrinter(indent=2)

def get_latest_issues(org_repo, page_count):
    latest_key_name = f'GH_{org_repo}_ISSUES_SYNC_UPDATED_AT' 
    updated_after = datetime.utcfromtimestamp(cfg[latest_key_name])
    url = f"https://api.github.com/repos/{org_repo}/issues"
    params = {
        "state": "open",
        "per_page": get_github_batch_size,
        "sort": "updated",
        "direction": "asc", 
        "since": updated_after.isoformat()
    }
    pat = os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']
    headers = {}
    if not pat:
        print(f'GITHUB_PERSONAL_ACCESS_TOKEN environment variable not found, Github anonymous rate limits will apply.')
    else:
        headers["Authorization"] = "token " + pat
    
    # print(f'Get github issues:\n{params}')
    cur_page = 0
    while url and cur_page < page_count:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            print(f'Error requesting Github issues:\n {response.content}')
            break

        yield from response.json()
        url = response.links.get("next", {}).get("url")
        cur_page += 1


def batch_issues(org_repo, batch_size=20, page_count=3):
    batch = []
    for issue in get_latest_issues(org_repo, page_count):
        batch.append(issue)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def upload_issues_to_typesense(org_repo, max_issue_count=120):
    client = typesense.Client(cfg.TYPESENSE_CONFIG)

    for issue_batch in batch_issues(org_repo, 40, math.ceil(max_issue_count / get_github_batch_size)):
        upload_batch = []

        for issue in issue_batch:
            try:
                # print(f'Incoming issue')
                # pp.pprint(issue)

                body_trimmed = issue.get("body", "")
                if body_trimmed is None:
                    body_trimmed = ""
                related_issue_start = body_trimmed.find("## Related Issue(s)")
                if related_issue_start > -1:
                    body_trimmed = body_trimmed[:related_issue_start]

                processed_issue = {
                    "id": str(issue["id"]),
                    "repository": issue["repository_url"].replace('https://api.github.com/repos/', ''),
                    "url": issue.get("html_url", ""),
                    "number": issue["number"],
                    "title": issue["title"],
                    "state": issue["state"],
                    "created_at": int(datetime.strptime(issue["created_at"], '%Y-%m-%dT%H:%M:%SZ').timestamp()),
                    "updated_at": int(datetime.strptime(issue["updated_at"], '%Y-%m-%dT%H:%M:%SZ').timestamp()),                    
                    "closed_at": None if issue["closed_at"] is None else int(datetime.strptime(issue["closed_at"], '%Y-%m-%dT%H:%M:%SZ').timestamp()),
                    "body": body_trimmed,
                    "labels": [label["name"] for label in issue["labels"]],
                    "is_pr": "pull_request" in issue
                }
                upload_batch.append(processed_issue)
            except Exception as e:
                print(f'Error while processing issue: {e}\n')
                pp.pprint(issue)
                continue

        if len(upload_batch) == 0:
            print(f'Empty batch, skipping...')
            continue

        results = client.collections['gh-studio-issues'].documents.import_(upload_batch, {'action': 'upsert', 'return_id': True})
        failed_results = [result for result in results if not result['success']]
        success_results = [result for result in results if result['success']]

        print(f'Github issues upserted to typesense: {len(success_results)}')

        if len(failed_results) > 0:
            print(f'The following issue IDs were not successfully upserted to typesense:\n{failed_results}')
                               
        if len(success_results) > 0:
            last_success_result_id = success_results[-1]['id']
            last_success_issue = next((issue for issue in upload_batch if issue['id'] == last_success_result_id), None)
            if last_success_issue:
                timestamp = last_success_issue['updated_at']
                store_issues_updated_at_filter(org_repo, timestamp)
                print(f'Saved GH_{org_repo}_ISSUES_SYNC_UPDATED_AT={timestamp}')


def store_issues_updated_at_filter(org_repo, timestamp):
    with open('github_qa/config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))

    # Update the value
    timestamp_key = f'GH_{org_repo}_ISSUES_SYNC_UPDATED_AT'
    cfg[timestamp_key] = timestamp

    # Write back to the file
    with open('github_qa/config.yml', 'w', encoding='utf8') as ymlfile:
        yaml.dump(cfg.to_dict(), ymlfile)

def main():
    upload_issues_to_typesense('Altinn/altinn-studio', 10)
    upload_issues_to_typesense('Altinn/app-frontend-react', 10)

if __name__ == "__main__":
    main()

