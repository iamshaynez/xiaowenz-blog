import datetime
import time
import requests
from lxml import etree
import pandas as pd
import re
import os
from dotenv import load_dotenv
from smms import SMMS
import random

load_dotenv()

READ_FILE = './content/read/read-2025.md'
class ImageService(object):
    def __init__(self):
        self.service = SMMS(os.environ["SMMS_KEY"])

    def download(self, url, filename):
        with open(filename, 'wb') as handle:
            response = requests.get(url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    def upload(self, url, filename):
        try:
            os.remove(filename)
        except:
            pass

        self.download(url, filename)
        link = self.service.upload_image(filename)
        try:
            os.remove(filename)
        except:
            pass
        return link

def response(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
               'Cookie': os.environ["DOUBAN_COOKIE"]
               }
    resposn = requests.get(url=url, headers=headers).text
    return resposn

def process(url):
    resposn = response(url)
    etree_html = etree.HTML(resposn)
    #print(resposn)
    # parse book page html
    book_title = etree_html.xpath('.//h1/span/text()')[0]
    img_small = etree_html.xpath('.//div/a[@class="nbg"]/img/@src')

    print("Found image url {0}".format(img_small))

    # span[contains(@class, 'myclass') and normalize-space(text()) = 'qwerty']

    book_info_test = etree_html.xpath('.//div[@id="info"]')
    
    reg = re.compile("<(.*?)>")
    book_info_result = reg.sub("", etree.tostring(book_info_test[0], encoding='UTF-8').decode('UTF-8'))
    book_info_result = re.sub(' +','', book_info_result)
    book_info_result = re.sub('\n+','\n', book_info_result)
    #print(book_info_result)


    # download image to upload to cdn
    service = ImageService()

    book_img = book_title.replace("/", "")
    cdnUrl = service.upload(img_small[0], "./tmp/{0}.jpg".format(book_img))


    # print my book list format
    print(f"### {get_next_book_number(READ_FILE)}. [《{book_title}》]({url}) ★★★★★")
    print("")
    print("```go")
    print(book_info_result)
    print("```")
    print("")
    print(">")
    print("")
    print("![]({0})".format(cdnUrl))

    #downloadImage(img_small[0], "{0}.jpg".format(book_title))
def get_next_book_number(filename):
    last_number = 0
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('###'):
                    # 提取序号部分
                    parts = line.strip().split('.')
                    if len(parts) > 1:
                        try:
                            number = int(parts[0].replace('###', '').strip())
                            last_number = max(last_number, number)
                        except ValueError:
                            continue
                            
        return last_number + 1
    
    except FileNotFoundError:
        return 1
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return 1


if __name__ == "__main__":
    url = 'https://book.douban.com/subject/36488645/'

    process(url)
    #count = get_next_book_number('./content/read/read-2024.md')

    #print(f'Last number is {count}')