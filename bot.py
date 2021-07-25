import threading
from slackapi import config
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slackapi.process_reaction import process

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    config.SIGNING_SECRET, '/slack/events', app)


@slack_event_adapter.on('reaction_added')
def reaction_added(json_payload):
    threading.Thread(
        target=process,
        args=(json_payload,)
    ).start()
    return


if __name__ == "__main__":
    app.run(debug=False)
