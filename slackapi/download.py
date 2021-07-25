import requests
from slackapi import config


def download(url, name):
    with open(f'{name}', 'wb') as f:
        response = requests.get(url, headers={
            'Authorization': 'Bearer ' + config.SLACK_TOKEN
        })
        f.write(response.content)
