
# from scrapy.cmdline import execute
# import os, sys
# from techradar.techradar.settings import save_paths
# from techradar.techradar.spiders.uploader import upload_article
# import scrapy
# from scrapy.crawler import CrawlerProcess
# from techradar import *

# # from techradar.techradar.spiders.reviews import ReviewsSpider




# process = CrawlerProcess(settings = {
#       "FEEDS": {
#          "items.json": {
#             "format": "json"
#          },
#       },
#    })

# process.crawl(ReviewsSpider)
# process.start() # the script will block here until the crawling is finished
# upload_article(source_name = save_paths, target_name='articles_2020.xml')
# # if __name__ == "__main__":
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy', 'crawl', 'reviews'])