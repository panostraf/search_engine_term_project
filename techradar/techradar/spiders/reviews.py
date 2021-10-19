import scrapy
from ..items import TechradarItem
import time
import random
import re

class ReviewsSpider(scrapy.Spider):
    

    name = 'reviews'
    # allowed_domains = ['https://www.techradar.com/']
    start_urls = [f'https://www.techradar.com/reviews/archive/2020/1/']
    month = 2
    # year = 2020
    # def __init__(self):
    #     self.year = 2020
    #     self.month = 1
    

    def parse(self, response, **kwargs):
        items = TechradarItem()
        scrapped_links = response.xpath('//div/a/@href').extract()
        self.month += 1
        print(response)
        
        
        ReviewsSpider.month += 1
        next_page = f'https://www.techradar.com/reviews/archive/2020/{str(ReviewsSpider.month)}/'
        # print(next_page)
        for link in scrapped_links:
            try:
                if len(re.findall(r"https://www.techradar.com/(review|news)/.*", link)) > 0:
                    
                    # if link not in items['links']:
                    items['links'] = link
                    print(link)
                    yield items

            except IndexError:
                print('ERROR---------------------')
                # response.follow(next_page, callback=self.parse)
                pass

        
        time.sleep(random.randint(1,4))
        if (ReviewsSpider.month) < 12:
            yield response.follow(next_page, callback=self.parse)


# Proxy rotation
# Follow links
# Replace csv with sql

# def parse(self, response):
#         months = response.xpath('//table//tr//a/@href').re(r'/archive/year-\d+,month-\d+.cms')
#         for month in months:
#             self.logger.info(month)