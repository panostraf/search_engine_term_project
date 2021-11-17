import nltk
import scrapy
from ..items import TechradarItem
import time
import random
import re
from bs4 import BeautifulSoup
from techradar.spiders.preprocess import PreprocessArticle
from techradar.spiders.uploader import upload_article
import os
from ..settings import save_paths
from collections import defaultdict
from nltk import word_tokenize
from nltk.corpus import stopwords
# print(stopwords.words('english'))


class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    
    month = 1
    year = 2020
    start_urls = [f'https://www.techradar.com/reviews/archive/{year}/{month}/']
    fpath = os.getcwd()
    output = f"""articles_{str(month)}_{str(year)}.xml"""
    
    save_as = f"""{fpath}/articles_{str(month)}_{str(year)}.xml"""
    # word_counter = defaultdict(lambda: 0)
    # if not os.path.isfile(save_as):
    #     with open(save_as,'a') as f:
    #         pass

    def parse(self, response, **kwargs):
        
        all_links = []
        items = TechradarItem()
        # xpath to extract the links from each page
        scrapped_links = response.xpath('//div/a/@href').getall()
        scrapped_links2 = response.xpath('//li/a/@href').getall()
        all_links.extend(scrapped_links)
        all_links.extend(scrapped_links2)
        scrapped_links = []
        
        # self.month += 1
        ReviewsSpider.month += 1 # increment month for link pagination
        next_page = f'https://www.techradar.com/reviews/archive/{str(ReviewsSpider.year)}/{str(ReviewsSpider.month)}/'
        
        for link in all_links:
            if not re.search("https://www.techradar.com/reviews/archive/.*", link): # filter unnessacary links (eg archive)
                
                try:
                    print(link)
                    print(response)
                    print('\n\n\n')
                    # Get only the links from news or reviews using regex
                    if len(re.findall(r"https://www.techradar.com/(reviews|news)/.", link)) > 0:
                        if link not in scrapped_links:
                            scrapped_links.append(link)
                            time.sleep(random.randint(0,1))
                            yield scrapy.Request(link, callback = self.parse_link_contents)
                        
                            
                        # items['links'] = link
                        # yield items

                except IndexError:
                    # response.follow(next_page, callback=self.parse)
                    pass

                except Exception as e:
                    print(e)
                    pass

        time.sleep(random.randint(1,3)) # Sleep before the next request

        if (ReviewsSpider.month) <= 2:
            # Callback on it's self to visit next link (archives of months)
            yield response.follow(next_page, callback=self.parse)
        
        # time.sleep(5)
        # upload_article(source_name = save_paths, target_name='articles_2020.xml')

        # else:
        #     # UPLOADE TO AZURE
        #     try:
        #         upload_article(source_name = save_paths, target_name='articles_2020.xml')
        #         # os.remove(ReviewsSpider.save_as)
        #     except Exception as e:
        #         print(e)
            
            

        
    def parse_link_contents(self,response,**kwargs):
        # full_art = response.meta.get('full_art')
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        content = soup.prettify()
        link_name = response.url.split('/')[-2] + "_" +response.url.split('/')[-1]
        title = response.url.split('/')[-1]
      
        with open(save_paths,'a') as f:
            f.write(PreprocessArticle().parse_paragraphs(content,link_name,title))
        f.close()

    




# TODO Proxy rotation - (if needed)
# TODO save file to Azure File server and remove file 
# connect GoogleDrive API as FileServer
