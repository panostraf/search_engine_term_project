
from scrapy.cmdline import execute
import os, sys
from techradar.settings import save_paths
from techradar.spiders.uploader import upload_article
import scrapy
from scrapy.crawler import CrawlerProcess

from techradar.spiders.reviews import ReviewsSpider

def run_app():
    process = CrawlerProcess(settings = {
        "FEEDS": {
            "items.json": {
                "format": "json"
            },
        },
    })

    process.crawl(ReviewsSpider)
    process.start() # the script will block here until the crawling is finished
    # TODO works for small files but crashes on larger ones. Try azure file share instead of blob

    # UNCOMMENT NEXT LINE TO SAVE TO AZURE
    # upload_article(source_name = save_paths, target_name='articles_2020.xml')

if __name__=="__main__":
    run_app()
    # print(save_paths)
    # test = open(save_paths,'r').read()
    # print(test)
    # upload_article(source_name = save_paths, target_name='articles_2020.xml')
# if __name__ == "__main__":
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy', 'crawl', 'reviews'])