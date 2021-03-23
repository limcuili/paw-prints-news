### newsapi test 1

from newsapi import NewsApiClient
import config

api_key = config.NEWS_API_KEY
client = NewsApiClient(api_key=api_key)
# sources = client.get_sources()
result = client.get_top_headlines(
    language=None,
    country=None,
    category=None,
    sources='bbc-news',
    page_size=100
)

### newsapi test 2

from query_api import Query

query = Query(
    name='BBC News',
    sources='bbc-news'
)

top_headlines = client.get_top_headlines(
            q=query.query,
            language=query.language,
            country=query.country,
            category=query.category,
            sources=query.sources,
            page_size=100
        )

headlines = result['articles']

final_messages_keys = [headlines[i:i+4] for i in range(0, len(headlines), 4-1)]

for headline in headlines:
    print(headline["description"])

### slack test 1
import config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

print(config.DEFAULT_SLACK_CHANNEL)
token=config.SLACK_BOT_TOKEN
client = WebClient(token=token)
client.chat_postMessage(
                channel='#paw-prints-news',
                text='Paw prints printing soon...',
                username=config.SLACK_BOT_NAME,
                icon_emoji=config.SLACK_ICON_EMOJI
            )

## slack test 2
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import config

INTRO_TEXT = 'Hello! Hope you are having a wonderful day!\n'
class SlackClient(object):

    def __init__(self, token=config.SLACK_BOT_TOKEN, default_channel=config.DEFAULT_SLACK_CHANNEL,
                 bot_name=config.SLACK_BOT_NAME, icon_emoji=config.SLACK_ICON_EMOJI):
        self.token=token
        print(f"token: {self.token}")
        self.default_channel=default_channel
        print(f"default_channel: {self.default_channel}")
        self.bot_name=bot_name
        print(f"bot_name: {self.bot_name}")
        self.client=WebClient(token=token)
        self.icon_emoji=icon_emoji


    def submit_post(self, channel=None):
        channel = channel or self.default_channel
        try:
            print(f"HERE!... {channel}")
            response = self.client.chat_postMessage(
                channel=channel,
                text='Paws printing soon...',
                username=self.bot_name,
                icon_emoji=self.icon_emoji
            )
        except SlackApiError as error:
            logging.error(f"Slack API error: {error.response['error']}")
            raise error

        return response