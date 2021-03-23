import logging
import config
from news_api import NewsApi
from slack_client import SlackClient

logging.basicConfig(
    filename=config.LOGFILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main(news_api, slack_client):
    for query in config.QUERIES:
        result = news_api.obtain_top_headlines(query)
        headlines = result['articles'][:query.headline_limit]
        slack_client.send_messages(
            query.name,
            headlines,
            query.webhook_url
        )


if __name__ == "__main__":
    main(NewsApi(), SlackClient())

