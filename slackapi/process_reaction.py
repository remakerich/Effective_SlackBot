import slack
from slackapi import config
from googleapi.upload import upload
from slackapi.download import download

client = slack.WebClient(token=config.SLACK_TOKEN)


def process(json_payload):
    filenames = []
    print(json_payload['event']['reaction'])
    if json_payload['event']['reaction'] == 'camera':

        targetmessage = client.conversations_history(
            channel=json_payload['event']['item']['channel'],
            inclusive=True,
            oldest=json_payload['event']['item']['ts'],
            limit=1)
        files = []
        try:
            files = targetmessage['messages'][0]['files']
        except KeyError:
            print('no files in the message')
            exit()
        for file in files:
            try:
                download(file['url_private'], file['name'])
                filenames.append(file['name'])
            except KeyError:
                pass
        print(f'Downloaded from Slack: {filenames}')
        filenames = []
        for file in files:
            try:
                upload('bot album', file['name'])
                filenames.append(file['name'])
            except KeyError:
                pass
        print(f'Uploaded to Google Photos: {filenames}')
