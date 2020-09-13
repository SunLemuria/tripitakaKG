import os
import json

from KBQA.kbqa_abs import KBQAAbs
from KBQA.graph.graph import Graph
from KBQA.graph.graph_arango_utils import ArangoGraph
from KBQA.config.config import Config


pwd = os.path.dirname(os.path.abspath(__file__))
conf_file = pwd + "/config/base.json"


class KBQAMain(KBQAAbs):
    def __init__(self):
        self.config = Config()
        self.graph = None
        self.graph_arango = None
        self.response = {}
        self.parse_config()
        self.init_obj()

    def parse_config(self):
        with open(conf_file, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def init_obj(self):
        self.graph = Graph(kbqa=self)
        self.graph_arango = ArangoGraph(kbqa=self)

    def run(self, request):
        self.graph.find_answer(query=request.get("query"))
