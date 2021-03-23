class Query(object):

    def __init__(self, name, query=None, category=None, country=None,
                 sources=None, language=None, slack_channel=None, webhook_url=None, headline_limit=8):
        """ Taken directly out of the newsapi docs at https://newsapi.org/docs/endpoints/top-headlines

        :param name: Slack name for this query.
        :param query: Keywords or a phrase to search for.
        :param category: The category you want to get headlines for. Possible options:
                        business, entertainment, general, health, science, sports, technology.
                        Note: you can't mix this param with the sources param.
        :param country: The 2-letter ISO 3166-1 code of the country you want to get headlines for.
                        Note: you can't mix this param with the sources param.
        :param sources: A comma-seperated string of identifiers for the news sources or blogs you want headlines from.
                        Use the /sources endpoint to locate these programmatically or look at the sources index.
                        Note: you can't mix this param with the country or category params.
        :param language: The 2-letter ISO-639-1 code of the language you want to get headlines in.
        :param slack_channel: The channel name where these will be posted.
        :param headline_limit: The maximum number of headlines to send to slack.
        """
        if sources is not None and (country is not None or category is not None):
            raise ValueError('Check your country,category, source parameters...')

        self.name = name
        self.query = query
        self.category = category
        self.country = country
        self.sources = sources
        self.language = language
        self.slack_channel = slack_channel
        self.webhook_url = webhook_url
        self.headline_limit = headline_limit

    def __str__(self):
        return (
            f"Query(name={self.name}, query={self.query}, category={self.category}, "
            f"country={self.country}, sources={self.sources}, language={self.language}, "
            f"channel={self.slack_channel}, webhook_url={self.webhook_url})"
        )

