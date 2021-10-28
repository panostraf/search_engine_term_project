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
        text = re.sub(r"\t","",text)
        text = re.sub(r"\r","",text)
        text = re.sub(r"\n","",text)
        return text

    def parse_paragraphs(self,article,link,title):
        soup = bs4.BeautifulSoup(article,'html.parser')
        title = "<title>" + title + "</title>"
        link = '<link>' + link + '</link>'

        paragraphs_raw = soup.find_all('p')
        pp = [self.clean_text(p.get_text()) for p in paragraphs_raw]
        pars = ''.join(pp)
        pars = "<p>" + pars + "</p>"

        lists_raw = soup.find_all('li')
        li = [self.clean_text(li.get_text()) for li in lists_raw]
        lists = '\n'.join(li)
        lists = "<li>" + lists + "</li>"

        h2_raw = soup.find_all('h2')
        h2 = [self.clean_text(h2.get_text()) for h2 in h2_raw]
        headers = '\n'.join(h2)
        headers = "<h2>" + headers + "</h2>"

        art = "<article>" + "\n" + link + "\n" + title + "\n"+ headers + "\n" + lists + "\n" + pars + "\n" + "</article>\n"
        return art

    def tf_idf(articles):
        from nltk import word_tokenize
        from nltk.corpus import stopwords
        import math
        global_words = DefaultDict(lambda:0)
        articles = defaultdict()
        for article in articles:
            article_words = defaultdict(lambda: 0)
            words = [w for w in word_tokenize(article) if w not in stopwords]
            
            for word in words:
                global_words[word] +=1
                article_words[word]+=1
                
            articles[article] = article_words
        
        for article in articles:
            for word,frequency in dict(article).items():
                article[word] = math.log(frequency/global_words[word])
                
        for word in global_words.keys():
            pass

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
    