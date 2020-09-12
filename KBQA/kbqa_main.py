import os
import json

from KBQA.kbqa_abs import KBQAAbs
from KBQA.graph.graph import Graph
from KBQA.config.config import Config


pwd = os.path.dirname(os.path.abspath(__file__))
conf_file = pwd + "/config/base.json"


class KBQAMain(KBQAAbs):
    def __init__(self):
        self.config = Config()
        self.graph = None
        self.response = {}
        self.parse_config()
        self.init_obj()

    def parse_config(self):
        """
        将配置读到context中
        """
        with open(conf_file, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def init_obj(self):
        """
        从context中取出配置，初始化
        """
        self.graph = Graph(kbqa=self)

    def run(self, request):
        self.response = self.graph.find_similar(request.get("query"), ratio_threshold=0.5)
