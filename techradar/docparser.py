import bs4
import os
import re
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


def clean_text(text):
    text = text.strip()
    text = re.sub("\s\s+" , " ", text)
    text = re.sub(r"\t","",text)
    text = re.sub(r"\r","",text)
    text = re.sub(r"\n","",text)
    return text

    


def parse_paragraphs(article):
    
    soup = bs4.BeautifulSoup(article,'html.parser')

    paragraphs_raw = soup.find_all('p')
    pp = [clean_text(p.get_text()) for p in paragraphs_raw]
    pars = ''.join(pp)
    pars = "<p>" + pars + "</p>"

    lists_raw = soup.find_all('li')
    li = [clean_text(li.get_text()) for li in lists_raw]
    lists = '\n'.join(li)
    lists = "<li>" + lists + "</li>"

    h2_raw = soup.find_all('h2')
    h2 = [clean_text(h2.get_text()) for h2 in h2_raw]
    headers = '\n'.join(h2)
    headers = "<h2>" + headers + "</h2>"

    art = "<article>" + "\n" + pars + "\n" + lists + "\n" + headers + "\n" + "</article>"
    return art


def upload_article(article):
    # Create a blob client using the local file name as the name for the blob
    blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=articlesdata;AccountKey=qbsGGNzP6w9guZd7weDt/ycWa/ULRIoHHK44P4BuuYQKV5+tkJIBYkffAi876aWMc3vzlP7oi5AM+FfKsB6i3A==;EndpointSuffix=core.windows.net')
    blob_client = blob_service_client.get_blob_client(container='articles', blob='test2')

    # print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open('test_file.xml', "r") as data:
        blob_client.upload_blob(data)
    data.close()

def download_blob():
    article_name = 'articles_2020.xml'
    # download_file_path = "term_project/techradar/"#test_download.xml"
    download_file_path = os.getcwd() +"/"+ article_name
    print(download_file_path)
    # exit(-1)

    print("\nDownloading blob to \n\t" + download_file_path)

    with open(download_file_path, "wb") as download_file:
        blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=articlesdata;AccountKey=qbsGGNzP6w9guZd7weDt/ycWa/ULRIoHHK44P4BuuYQKV5+tkJIBYkffAi876aWMc3vzlP7oi5AM+FfKsB6i3A==;EndpointSuffix=core.windows.net')
        blob_client = blob_service_client.get_blob_client(container='articles', blob=article_name)

        download_file.write(blob_client.download_blob().readall())
    print('check ',download_file_path)



if __name__ == '__main__':
    # path = """techradar/spiders/downloads/"""
    # arr = os.listdir(path)

    # article = open(path + arr[10],'r').read()
    # art = parse_paragraphs(article=article)
    # with open('test_file.xml','w') as f:
    #     f.write(art)
    # f.close()
    # upload_article(art)
    download_blob()
    # print(art)