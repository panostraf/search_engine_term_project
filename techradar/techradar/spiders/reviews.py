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
import bs4
# print(stopwords.words('english'))


class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    
    # month = 1
    # year = 2020
    start_urls = [f'https://www.techradar.com/reviews/archive/2020/1/',
                    "https://www.techradar.com/reviews/archive/2021/1/",
                    "https://www.techradar.com/reviews/archive/2019/1/",
                    "https://www.cnet.com/"]

    allowed_domains = ["www.techradar.com",
                        "www.cnet.com"]
                    # "https://www.cnet.com/"]
    # fpath = os.getcwd()
    # output = f"""articles_{str(month)}_{str(year)}.xml"""
    
    # save_as = f"""{fpath}/articles_{str(month)}_{str(year)}.xml"""
    # word_counter = defaultdict(lambda: 0)
    # if not os.path.isfile(save_as):
    #     with open(save_as,'a') as f:
    #         pass
    all_links = []
    

    def __init__(self):
        self.all_links = []
        self.scrapped_links = []

    def parse(self, response, **kwargs):
        
        # print(response.url)
        # print(response)
        # print("\n\n\n")
        # time.sleep(1)
        
        current_links = []
        items = TechradarItem()
        # xpath to extract the links from each page
        scrapped_links1 = response.xpath('//div/a/@href').getall()
        scrapped_links2 = response.xpath('//li/a/@href').getall()

        current_links.extend(scrapped_links1)
        current_links.extend(scrapped_links2)

        # for link in current_links:
        #     print(link)
        title,content = PreprocessArticle().parse_paragraphs(response=response)
        saved_content = PreprocessArticle().save_paragraphs(content = content,link=response.url,title = title)
        
        with open(save_paths,'a') as f:
            f.write(saved_content)
        f.close()
        
        self.scrapped_links.append(response.url)
        
        for link in current_links:
            if re.search(r"^/", link):
                link = response.url + str(link)[1:]
                self.all_links.append(link)
                
            if re.search(r"^(https://www.cnet.com/|https://www.techradar.com/).*", link): # filter unnessacary links (eg archive)
                
                if link not in self.scrapped_links:
                
                    self.all_links.append(link)
        
        # time.sleep(3)
        # self.all_links.remove(response.url)
        for link in self.all_links:
            # time.sleep(1)
            try:
                self.all_links.remove(link)
            except Exception as e:
                print(e)
            yield response.follow(link,self.parse)
        # ReviewsSpider.scrapped_links = []
        
        # self.month += 1
        # ReviewsSpider.month += 1 # increment month for link pagination
        # next_page = f'https://www.techradar.com/reviews/archive/{str(ReviewsSpider.year)}/{str(ReviewsSpider.month)}/'

        
    #     for link in all_links:
    #         if re.search(r"^/", link):
    #             link = response.url + str(link)[1:]

    #         if re.search(r"(https://www.cnet.com/|https://www.techradar.com/).*", link): # filter unnessacary links (eg archive)
                
    #             try:
    #                 print(link)
    #                 print(response)
    #                 print('\n\n\n')
    #                 # Get only the links from news or reviews using regex
    #                 if link not in scrapped_links:
    #                     # Scrape links here
    #                     soup = bs4.BeautifulSoup(response.text,'html.parser')
    #                     title = soup.find_all('title')[0].get_text()
                        
    #                     paragraphs_raw = soup.find_all('p')
                        
    #                     paragraphs = [p.get_text() for p in paragraphs_raw]
    #                     content = ''.join(paragraphs)

    #                     content = PreprocessArticle().clean_text(content)
                        

    #                     with open(save_paths,'a') as f:
    #                         f.write(PreprocessArticle().parse_paragraphs(content,link,title))
    #                     f.close()
                        
    #                     scrapped_links.append(link)
    #                     time.sleep(random.randint(0,1))
    #                     yield scrapy.Request(link, callback = self.parse)

    #             except IndexError:
    #                 pass

    #             except Exception as e:
    #                 print(e)
    #                 pass
    # #     time.sleep(random.randint(1,3)) # Sleep before the next request

    # #     if (ReviewsSpider.month) <= 2:
    # #         # Callback on it's self to visit next link (archives of months)
    # #         yield response.follow(next_page, callback=self.parse)
        
    # #     # time.sleep(5)
    # #     # upload_article(source_name = save_paths, target_name='articles_2020.xml')

    # #     # else:
    # #     #     # UPLOADE TO AZURE
    # #     #     try:
    # #     #         upload_article(source_name = save_paths, target_name='articles_2020.xml')
    # #     #         # os.remove(ReviewsSpider.save_as)
    # #     #     except Exception as e:
    # #     #         print(e)
            
            

        
    # # def parse_link_contents(self,response,**kwargs):
    # #     # full_art = response.meta.get('full_art')
    # #     content = response.text
    # #     soup = BeautifulSoup(content, 'html.parser')
    # #     content = soup.prettify()
    # #     link_name = response.url.split('/')[-2] + "_" +response.url.split('/')[-1]
    # #     title = response.url.split('/')[-1]
      
    # #     with open(save_paths,'a') as f:
    # #         f.write(PreprocessArticle().parse_paragraphs(content,link_name,title))
    # #     f.close()

    




# TODO Proxy rotation - (if needed)
# TODO save file to Azure File server and remove file 
# connect GoogleDrive API as FileServer
