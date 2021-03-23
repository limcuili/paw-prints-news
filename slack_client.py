import logging
import pytz
import datetime
import dateutil.parser
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import config
import requests


INTRO_TEXT = 'Hello! This is Paw Prints News :paw_prints: \nHere are some top headlines today!\n'


class SlackClient(object):

    def __init__(self, token=config.SLACK_BOT_TOKEN, default_channel=config.DEFAULT_SLACK_CHANNEL,
                 default_webhook_url=config.DEFAULT_WEBHOOK, bot_name=config.SLACK_BOT_NAME,
                 icon_emoji=config.SLACK_ICON_EMOJI,):
        self.token = token
        self.default_channel = default_channel
        self.default_webhook_url = default_webhook_url
        self.bot_name = bot_name
        self.client = WebClient(token=token)
        self.icon_emoji = icon_emoji


    def submit_post(self, blocks, channel=None, webhook=None):
        """ Posts a message to slack using JSON blocks https://api.slack.com/reference/block-kit/block-elements
        Uses slack client to do so https://slack.dev/python-slack-sdk/web/index.html
        Play around here: https://app.slack.com/block-kit-builder

        :param blocks: Lists of fields and values that describe the JSON that apps can use to generate each block.
            A series of components that can be combined to create visually rich and compellingly interactive messages.
        :param channel: slack channel to send the message to.

        ## If you'd like to use the Slack API instead of webhook, use the below in the 'try' clause.
        response = self.client.chat_postMessage(
            channel=channel,
            text='Paws printing soon...',
            blocks=blocks,
            username=self.bot_name,
            icon_emoji=self.icon_emoji
        )
        """
        try:
            webhook_url = webhook or self.default_webhook_url
            response = requests.post(
                webhook_url, json={"blocks": blocks},
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code != 200:
                raise ValueError(
                    'Request to slack returned an error %s, the response is:\n%s'
                    % (response.status_code, response.text)
                )
        except SlackApiError as error:
            logging.error(f"Slack API error: {error.response['error']}")
            raise error

        return response


    def _prepare_posts(self, headlines, n=4):
        logging.info('Grouping posts...')
        final_messages_keys = [headlines[i:i+n] for i in range(0, len(headlines), n)]
        return final_messages_keys


    def send_messages(self, name, headlines, channel=None, webhook=None, n=4):
        channel = channel or self.default_channel
        final_headlines = self._prepare_posts(headlines, n=n)
        logging.info(f"Sending {len(final_headlines)} to Slack.")

        for index, headlines in enumerate(final_headlines):
            print(f"{index}, {headlines}")
            logging.info(f"{index}, {headlines}\n")
            if index == 0:
                message = self.create_layout(name, headlines, cont=False)
            else:
                message = self.create_layout(name, headlines, cont=True)
            slack_response = self.submit_post(message, channel, webhook)
            logging.info(f"Sent {index+1}/{len(final_headlines)} to Slack.:\n{slack_response}")


    def format_divider_block(self):
        return {"type": "divider"}


    def format_button_block(self, url):
        return {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Read the Full Article",
                    },
                    "value": "article_link",
                    "url": url
                }
            ]
        }


    def format_headline_block(self, headline, description, source, publishing_time, image_url):
        tzone = pytz.timezone(config.TIMEZONE)
        tz_dt = publishing_time.replace(tzinfo=pytz.utc).astimezone(tzone)
        dt_string = tz_dt.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{headline}*\n{source} | {dt_string}\n{description}."
            },
            "accessory": {
                "type": "image",
                "image_url": f"{image_url}",
                "alt_text": "alt text for image"
            }
        }


    def parse_datetime(self, datetime_string):
        try:
            datetime_object = datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            datetime_object = dateutil.parser.parse(datetime_string)
        return datetime_object.replace(tzinfo=pytz.utc)


    def format_headline_blocks(self, headlines):
        blocks = [self.format_divider_block()]

        for headline in headlines:
            title = headline["title"]
            description = headline["description"]
            url = headline["url"]
            image_url = headline["urlToImage"]
            source = headline["source"]["name"]
            publishing_time = self.parse_datetime(headline["publishedAt"])
            headline_block = self.format_headline_block(
                title, description, source, publishing_time, image_url)
            button_block = self.format_button_block(url)
            blocks.append(headline_block)
            blocks.append(button_block)

        return blocks


    def format_header_block(self, name, cont=False):
        first_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": INTRO_TEXT if not cont else "More to come..."
            }
        }
        if not cont:
            header = {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{name}"
                }
            }
            return [header, first_block]
        else:
            return [first_block]


    def create_layout(self, name, headlines, cont=False):
        blocks = self.format_header_block(name, cont)
        blocks.extend(self.format_headline_blocks(headlines))
        return blocks

