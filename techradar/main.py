
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
    upload_article(source_name = save_paths, target_name='articles_2020.xml')

run_app()
# if __name__ == "__main__":
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy', 'crawl', 'reviews'])