import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    """
    use this command to run
    scrapy crawl quotes -o quotes-humor.json -a tag=humor
    
    allows to search only those quotes having 'humor' as one of the tags
    """

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        # if a tag is entered, this will output only the quotes related to that tag
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)