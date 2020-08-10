import re
import json
import time
import random
import threading

import requests
import pandas as pd

from lxml import etree

from spider.proxy import proxies
from spider.user_agents import agents
from zhtools.converters import t2s


class Crawler:
    def __init__(self):
        self.main_url = "http://buddhaspace.org/dict/dfb/data/"

        self.result = {}

    def crawl(self, h_data):
        self.get_main(h_data=h_data)
        self.save_result()

    @staticmethod
    def send_request(url, referer):
        user_agent = random.choice(agents)

        # method = random.choice(["http", "https"])
        method = random.choice(["https"])
        # proxy_url = random.choice(proxies[method])
        # proxy = {method: proxy_url}
        # print(proxy_url)

        headers = {"User-Agent": user_agent, "Referer": referer} if referer else {"User-Agent": user_agent}
        print(url)
        try:
            # response = requests.get(url, headers=headers, proxies=proxy)
            response = requests.get(url, headers=headers)
            response.encoding = 'big5'
        except Exception as e:
            print(e)
            return ""

        # print(response.text)
        # print(response.url)
        # print(response.encoding)
        print(response.status_code)
        # print(response.content)
        # print("=" * 80)

        return response.text

    def get_main(self, h_data):  # 分页发送请求，获取详情页url列表
        if not html_data:
            url = self.main_url
            content = self.send_request(url=url, referer="")
            self.parse_main(content, '')
        else:
            self.parse_main('', h_data)

    def parse_main(self, content, h_data):
        """
        # 获取首页信息
        :param content: response.content,是html
        :param h_data: html文件名
        :return:
        """
        # print('parse_main, ', h_data)
        if content:
            content = content.encode("ISO-8859-1").decode("utf-8")
            html = etree.HTML(content)
        else:
            with open(h_data, "r") as f:
                content = "".join(f.readlines())
            html = etree.HTML(content)
            # print(html)
        entities = html.xpath('//*/li')
        # print(entities)
        for entity in entities:
            entity_name = entity.xpath('a/text()')[0]  # 实体名如“一行三昧”
            entity_link = entity.xpath('a/@href')[0]  # 详情链接
            entity_name_sim, entity_link = t2s(entity_name), t2s(entity_link)
            # print(entity_name, entity_name_sim, entity_link)
            if not entity_name.startswith("丁福保"):
                self.result[entity_name] = [entity_name_sim, entity_link]

    def save_result(self):
        json_format = dict(ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
        file = "./data/dfb.json"

        with open(file, "w") as f:
            json.dump(self.result, f, **json_format)
        print("saved to {}.".format(file))


if __name__ == '__main__':
    html_data = "./data/dfb.html"
    crawler = Crawler()
    crawler.crawl(h_data=html_data)
