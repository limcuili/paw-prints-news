import os
import secrets_file
from query_api import Query

LOGFILE = os.environ.get("LOGFILE", "C:/temp/slack_news_log")
NEWS_API_KEY = secrets_file.NEWS_API_KEY
SLACK_BOT_TOKEN = secrets_file.SLACK_BOT_TOKEN
DEFAULT_WEBHOOK = secrets_file.WEBHOOK
SLACK_BOT_NAME = 'Paw Prints'
SLACK_ICON_EMOJI = ':paw_prints:'
DEFAULT_SLACK_CHANNEL = '#paw-prints-news'
TIMEZONE = 'Europe/London'

QUERIES = [
    Query(
        name='TechRadar',
        sources='techradar',
        headline_limit=3
    ),
    Query(
        name='IGN',
        sources='ign',
        headline_limit=3
    ),
    Query(
        name='TechCrunch',
        sources='techcrunch',
        headline_limit=3
    ),
]