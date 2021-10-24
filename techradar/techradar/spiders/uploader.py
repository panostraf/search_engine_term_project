from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os



def upload_article(source_name,target_name):
    print(os.path.abspath(__name__))
    # exit(-1)
    # source_name = "/Users/panos/Documents/term_project/articles_2020.xml"
    # Create a blob client using the local file name as the name for the blob
    con_string = 'DefaultEndpointsProtocol=https;AccountName=articlesdata;AccountKey=qbsGGNzP6w9guZd7weDt/ycWa/ULRIoHHK44P4BuuYQKV5+tkJIBYkffAi876aWMc3vzlP7oi5AM+FfKsB6i3A==;EndpointSuffix=core.windows.net'
    #DefaultEndpointsProtocol=https;AccountName=articlesdata;AccountKey=qbsGGNzP6w9guZd7weDt/ycWa/ULRIoHHK44P4BuuYQKV5+tkJIBYkffAi876aWMc3vzlP7oi5AM+FfKsB6i3A==;EndpointSuffix=core.windows.net
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=con_string)
    blob_client = blob_service_client.get_blob_client(container='articles', blob=target_name)

    print("\nUploading to Azure Storage as blob:\n\t" + target_name)

    # Upload the created file

    data = open(source_name, "r").read()
    try:
        blob_client.upload_blob(data)
    except:
        # instead of rename delete the file and re-upload it
        blob_client = blob_service_client.get_blob_client(container='articles', blob=target_name + "2")
        blob_client.upload_blob(data)


if __name__ == '__main__':

    save_paths = "/Users/panos/Documents/term_project/articles_2020.xml"
    upload_article(save_paths,'save_paths = "articles_2020.xml')