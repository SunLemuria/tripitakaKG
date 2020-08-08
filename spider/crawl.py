import re
import time
import random
import threading

import requests
import pandas as pd

from lxml import etree

from proxy import proxies
from user_agents import agents


class GDEduCrawler:
    def __init__(self):
        self.main_url = "http://bskk.net"
        self.read_url = "http://gdedulscg.cn/home/bill/billdetails/billGuid/{}.html"  # 填入see_info的值,阅读页面

        self.detail_patt = re.compile(r"see_info\((\d+)\)")

        self.columns = ["分部", "部数", "经名", "译者", "分卷", "地址"]
        self.result_df = pd.DataFrame(columns=self.columns)

        self.lock = threading.Lock()

    def crawl(self, html_data):
        self.get_main(html_data=html_data)
        self.result_df.to_excel("./data/books_info.xlsx")

    def send_request(self, url, referer):
        user_agent = random.choice(agents)

        # method = random.choice(["http", "https"])
        method = random.choice(["https"])
        proxy_url = random.choice(proxies[method])
        proxy = {method: proxy_url}
        print(proxy_url)

        headers = {"User-Agent": user_agent, "Referer": referer} if referer else {"User-Agent": user_agent}
        try:
            response = requests.get(url, headers=headers, proxies=proxy)
        except Exception as e:
            print(e)
            return ""

        # print(response.text)
        print(response.url)
        # print(response.encoding)
        print(response.status_code)
        # print(response.content)
        # print("=" * 80)

        return response.text

    def get_main(self, html_data):  # 分页发送请求，获取详情页url列表
        if not html_data:
            url = self.main_url
            content = self.send_request(url=url, referer="")
            self.parse_main(content, '')
        else:
            self.parse_main('', html_data)

    def parse_main(self, content, html_data):
        """
        # 获取首页信息
        :param content: response.content,是html
        :return:
        """
        if content:
            html = etree.HTML(content)
        else:
            html = etree.HTML(html_data)
        divisions = html.xpath('//*/dl')
        for div in divisions:
            division_name = div.xpath('dt/div/text()')  # 部名如“大乘般若部”
            books = div.xpath('dd')  # 本部下包含的书的标签
            for book in books:
                self.parse_book(division_name, book, len(books))

    def parse_book(self, division_name, book, books_count):
        """
        有分卷和无分卷的分开处理
        解析译者
        :param division_name:
        :param book:
        :param books_count:分部下有多少部经
        :return:
        保存信息：分部名,分部下有多少部经，经名，译者，分卷，经文地址
        """
        save_info = {
            "分部": division_name[0].strip(),
            "部数": books_count
        }
        translator = book.xpath('*/span/text()')
        if translator:
            save_info['译者'] = translator[0]
        volumes = book.xpath('div/div/ul/li')
        # 没有分卷时volumes为空列表
        if volumes:
            book_name = book.xpath('div[@class="left pull-left"]/text()')
            # print(book_name, volumes)
            for i, vol in enumerate(volumes):
                link = vol.xpath('a/@href')
                vol_name = vol.xpath('a/text()')
                if vol_name:
                    save_info["分卷"] = vol_name[0].strip()
                else:
                    save_info["分卷"] = i + 1
                save_info["经名"] = book_name[0].strip()
                save_info["地址"] = self.main_url + link[0].strip()
                self.save_information(**save_info)
        else:
            book_name = book.xpath('div[@class="left pull-left"]/a/text()')
            link = book.xpath('div[@class="left pull-left"]/a/@href')
            save_info["经名"] = book_name[0].strip()
            save_info["地址"] = self.main_url + link[0].strip()
            self.save_information(**save_info)

    def save_information(self, **kwargs):
        """
        保存到xls
        :return:
        """
        print(kwargs)
        # if not kwargs.get("经名"):
        #     print(kwargs)
        self.lock.acquire()
        self.result_df = self.result_df.append(kwargs, ignore_index=True)
        self.lock.release()


if __name__ == '__main__':
    file = "./data/乾隆大藏经-地藏论坛.html"
    crawler = GDEduCrawler()
    crawler.crawl(html_data='')
