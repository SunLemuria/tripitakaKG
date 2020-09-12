import json

from KBQA.utils.similar_string import similarity as similarity_ratio


class Graph:
    def __init__(self, kbqa):
        self.kbqa = kbqa
        self.entity = dict()  # 名称到属性的映射
        self.relation = dict()  # 暂时未用到

        self.entity_list = []
        self.relation_list = []

        self.init_entity()
        self.init_relation()

    def init_entity(self):
        """
        # 读取图谱文件，构建图谱对象
        """
        import os
        print(os.getcwd())
        with open(self.kbqa.config["entity_file"], "r", encoding="utf-8") as f:
            self.entity_list = json.load(f)
        for e in self.entity_list:  # TODO 网页数据问题，暂时在这里处理
            if e["attribute"].get('地址') in ['http://bskk.net/Index/detail/id/662.html',
                                            'http://bskk.net/Index/detail/id/663.html']:
                e["name"] = "佛顶尊胜陀罗尼经"
            self.entity.setdefault(e["name"], [])
            self.entity[e["name"]].append(e)

    def init_relation(self):
        with open(self.kbqa.config["relation_file"], "r", encoding="utf-8") as f:
            self.relation_list = json.load(f)
        for r in self.relation_list:
            self.relation[r["name"]] = r

    def find_similar(self, query, ratio_threshold):
        """
        返回{name: attribute}的格式
        """
        answer = []
        similar_entities = dict()
        for entity in self.entity_list:  # 相似度大于阈值或名称有包含
            ratio = similarity_ratio(query, entity["name"])
            if ratio >= ratio_threshold or (entity["name"] in query or query in entity["name"]):
                similar_entities.setdefault(ratio, [])
                similar_entities[ratio].append(entity)

        for score, entity_list in sorted(similar_entities.items(), key=lambda x: -x[0]):
            for entity in entity_list:
                attribute = entity["attribute"]
                attribute["经名"] = entity["name"]
                answer.append(attribute)
            if score == 1:  # 有相符的就只返回相符的
                break
        return answer
