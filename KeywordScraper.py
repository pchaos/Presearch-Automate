# -*- coding: utf-8 -*- #
import time
import random
import requests
from bs4 import BeautifulSoup


def add_plus(keywords):
    keywords = keywords.split()
    keyword_edited = ""
    for i in keywords:
        keyword_edited += i + "+"
    keyword_edited = keyword_edited[:-1]
    return keyword_edited


class KeywordScraper:
    def __init__(self, keyword):
        self.keyword = keyword
        plusified_keyword = add_plus(keyword)
        self.keywords_scraped = []
        self.search_string = [
            "https://www.google.co.uk/search?q=" + plusified_keyword,
            "https://www.google.co.jp/search?q=" + plusified_keyword,
            "https://www.google.co.ke/search?q=" + plusified_keyword,
            "https://www.google.co.in/search?q=" + plusified_keyword
        ]

    def scrape_SERP(self):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        proxy_host = "127.0.0.1"
        proxy_port = "1081"
        proxy_auth = ":"
        proxies = {
            "https":
            "socks5://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
            "http":
            "socks5://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
        }

        content = requests.get(random.choice(self.search_string),
                               headers=headers,
                               proxies=proxies).text
        soup = BeautifulSoup(content, "html.parser")
        related_keyword_section = soup.find("div", {"class": "card-section"})
        if related_keyword_section:
            try:
                keywords_cols = related_keyword_section.find_all(
                    "div", {"class": "brs_col"})
                for col in keywords_cols:
                    list_of_keywords = col.find_all("p", {"class": "nVcaUb"})
                    for i in list_of_keywords:
                        self.keywords_scraped.append(i.find("a").text)
            except Exception as e:
                print(
                    f'related_keyword_section error:{related_keyword_section}')

    def write_to_file(self):
        for keyword in self.keywords_scraped:
            with open("scraped keywords.txt", "a") as f:
                f.write(keyword + "\n")
        print("keywords related to '" + self.keyword +
              "' scraped successfully")


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def randomDelay(i: int):
    """ delay for response timeout
    """
    if i % 5 == 0:
        # random sleep
        time.sleep(random.randint(130, 300) / 100)
    else:
        time.sleep(random.randint(40, 100) / 100)
    print("|", end='')


keywords = ['AMD']
keywords = ['machine learning']
keywords = ['learning kid']
keywords = ['kids']
keywords = ['movies']
keywords = ['showgirl']
keywords = ['girl']
keywords = ['telnet']
keywords = ['openwrt router']
keywords = ['stock']
i = j = 0
while i < len(keywords):
    key = keywords[i]
    if not isEnglish(key):
        i += 1
        print(f"not english:{key}")
        #  time.sleep(0.5)
        randomDelay(i)
        continue
    print(f'"{key}"', end=',')
    s = KeywordScraper(key)
    s.scrape_SERP()
    print(f'keywords:{s.keywords_scraped} {i}/{j}/{len(keywords)}')
    if len(s.keywords_scraped) > 0:
        # 删除非英语关键字
        for k in range(len(s.keywords_scraped), 0, -1):
            if not isEnglish(s.keywords_scraped[k - 1]):
                print(f'del {s.keywords_scraped[k - 1]}', end=" ")
                del s.keywords_scraped[k - 1]
        if j < 100:
            keywords.extend(s.keywords_scraped)
    s.write_to_file()
    i += 1
    j += 1
    time.sleep(2)
    randomDelay(j)
