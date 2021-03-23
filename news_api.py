from newsapi import NewsApiClient
import config
import logging

class NewsApi(object):

    def __init__(self, my_api_key=config.NEWS_API_KEY):
        self.client = NewsApiClient(api_key=my_api_key)

    def obtain_top_headlines(self, query):
        """ Check out https://newsapi.org/docs/client-libraries/python

        :param query: Query object
        :return: headlines from api
        """
        logging.info(f"Querying top headlines for {query}...")
        top_headlines = self.client.get_top_headlines(
            q=query.query,
            language=query.language,
            country=query.country,
            category=query.category,
            sources=query.sources,
            page_size=100
        )
        logging.info(f"We have got {len(top_headlines['articles'])} headlines for this query.")
        print(top_headlines)

        return top_headlines

