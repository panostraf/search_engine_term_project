import bs4
import os

path = """techradar/spiders/downloads/"""
arr = os.listdir(path)

article = open(path + arr[1],'r').read()


def parse_paragraphs(article):
    print(arr[0])
    # print(article)
    soup = bs4.BeautifulSoup(article,'html.parser')
    ps = soup.find_all('p')
    i = 0
    paragraphs = ""
    for p in ps:
        # print(i)
        # i +=1
        # print('<p>',p.get_text().strip().replace(r'\t','').replace(r'\r',''),'</p>')
        paragraphs += '<p>'+p.get_text().strip().replace(r'\t','').replace(r'\r','').replace(r'\n','').replace('  ',' ')+'</p>'
    # for item in ps:
        # soup.find_all('p')
    print(paragraphs)

parse_paragraphs(article=article)