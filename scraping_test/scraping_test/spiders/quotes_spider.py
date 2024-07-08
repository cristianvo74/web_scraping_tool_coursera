import scrapy
import os

# current_dir = os.path.dirname(__file__)
# url = os.path.join(current_dir, 'index.html')


class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        tables = response.xpath('//div[@class="quote"]')

        quotes_lst = []

        for table in tables:
            quote = table.xpath('.//span[@class="text" and @itemprop="text"]/text()').get()
            author = table.xpath('.//span /small[@class="author" and @itemprop="author"]/text()').get()

            quotes_lst.append((author, quote))

        for quote in quotes_lst:
            yield {
                'author': quote[0],
                'quote': quote[1]
            }
        # Extract the link to the next page and follow it
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(next_page_link, callback=self.parse)