from collections import defaultdict
from typing import DefaultDict
import bs4
import re

class PreprocessArticle:
    def __init__(self):        
        pass

    @staticmethod
    def clean_text(text):
        text = text.strip()
        text = re.sub("\s\s+" , " ", text)
        text = re.sub(r"\t"," ",text)
        text = re.sub(r"\r"," ",text)
        text = re.sub(r"\n"," ",text)
        text = re.sub(r"\n"," ",text)
        return text

    def parse_paragraphs(self,response):
        soup = bs4.BeautifulSoup(response.text,'html.parser')
        try:
            title = soup.find_all('title')[0].get_text()
        except:
            title = "null"
        paragraphs_raw = soup.find_all('p')
        
        paragraphs = [p.get_text() for p in paragraphs_raw]
        content = ''.join(paragraphs)

        content = self.clean_text(content)
        return title,content

    def save_paragraphs(self,content,link,title):
        
        title = "<title>" + title + "</title>"
        link = '<url>' + link + '</url>'
        content = "<content>" + content + "</content>"
        art = "<article>" + "\n" + link + "\n" + title + "\n"+ content + "\n" + "</article>\n"
        return art



if __name__ == '__main__':
    import bs4
    article_path = """/Users/panos/Documents/term_project/techradar/techradar/spiders/a-small-orange.html"""
    article_path2 = """/Users/panos/Documents/term_project/techradar/techradar/spiders/abacus-expense-tracker.html"""
    article = open(article_path,'r').read()
    article2 = open(article_path2,'r').read()
    full_art = PreprocessArticle()
    full_art.parse_paragraphs(article)
    full_art.parse_paragraphs(article2)

    soup = bs4.BeautifulSoup(full_art.full_article,'html.parser')
    artss = soup.find_all('article')
    print(len(artss))
    print(artss[1].find_all('li'))
    