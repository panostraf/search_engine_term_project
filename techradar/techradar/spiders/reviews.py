import scrapy
from ..items import TechradarItem
import time
import random
import re
from bs4 import BeautifulSoup

class ReviewsSpider(scrapy.Spider):
    

    name = 'reviews'
    start_urls = [f'https://www.techradar.com/reviews/archive/2020/1/']
    month = 2
    

    def parse(self, response, **kwargs):
        all_links = []
        items = TechradarItem()
        # xpath to extract the links from each page
        scrapped_links = response.xpath('//div/a/@href').getall()
        scrapped_links2 = response.xpath('//li/a/@href').getall()
        all_links.extend(scrapped_links)
        all_links.extend(scrapped_links2)
        print(response)
        
        # self.month += 1
        ReviewsSpider.month += 1 # increment month for link pagination
        next_page = f'https://www.techradar.com/reviews/archive/2020/{str(ReviewsSpider.month)}/'
        for link in all_links:
            print(link)
        for link in all_links:
            
            
            try:
                # Get only the links from news or reviews using regex
                if len(re.findall(r"https://www.techradar.com/(reviews|news)/.*", link)) > 0:
                    
                    
                    # Here we can add a function to visit the link and extract it's text
                    time.sleep(random.randint(1,4))
                    yield scrapy.Request(link, callback = self.parse_link_contents)
                    
                    items['links'] = link
                    print(link)
                    yield items

            except IndexError:
                # response.follow(next_page, callback=self.parse)
                pass

        # Sleep before the next request
        time.sleep(random.randint(1,4))
        if (ReviewsSpider.month) < 13:
            # Callback on it's self
            yield response.follow(next_page, callback=self.parse)

    
    def parse_link_contents(self,response,**kwargs):
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        content = soup.prettify()
        link_name = response.url.split('/')[-1]
        
        print(link_name)
        
        with open(f'downloads/{link_name}.html','w') as f:
            f.write(content)
        f.close()




    # name = 'reviews'
    # start_urls = [f'https://www.techradar.com/reviews/archive/2020/1/']
    # month = 2
# TODO
# Rotate User Agent - Done
# Proxy rotation - (if needed)
# Follow links - Done
# Replace csv with sql
# connect GoogleDrive API as FileServer

# def parse(self, response):
#         months = response.xpath('//table//tr//a/@href').re(r'/archive/year-\d+,month-\d+.cms')
#         for month in months:
#             self.logger.info(month)