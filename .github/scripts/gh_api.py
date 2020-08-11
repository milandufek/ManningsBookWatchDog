import json
import os

import requests


GH_TOKEN = {"Authorization":
            f"token {json.loads(os.environ.get('GITHUB_CONTEXT')).get('token')}"}

# GitHub API endpoints
GH_API = {
    'ISSUES': 'https://api.github.com/repos/milandufek/ManningBooksWatchDog/issues',
    'PULLS': 'https://api.github.com/repos/milandufek/ManningBooksWatchDog/pulls',
}


def get_pr(**kwargs):
    headers = {**GH_TOKEN, **kwargs}

    return requests.get(GH_API.get('PULLS'), headers=headers)


if __name__ == '__main__':
    pulls = json.loads(get_pr().text)
    for pr in pulls:
        print(pr['title'])
