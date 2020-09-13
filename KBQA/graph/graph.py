import json

from KBQA.utils.similar_string import similarity as similarity_ratio


class Graph:
    def __init__(self, kbqa):
        self.kbqa = kbqa
        self.entity = dict()  # 名称到属性的映射
        self.relation = dict()  # 暂时未用到

        self.entity_list = []
        self.relation_list = []

        self.entity_name_set = set()  # 保存所有节点名称

        self.init_entity()
        self.init_relation()

    def init_entity(self):
        """
        # 读取图谱文件，构建图谱对象
        """
        with open(self.kbqa.config["entity_file"], "r", encoding="utf-8") as f:
            self.entity_list = json.load(f)
        for e in self.entity_list:
            self.entity.setdefault(e["name"], [])
            self.entity[e["name"]].append(e)
            self.entity_name_set.add(str(e["name"]))

    def init_relation(self):
        with open(self.kbqa.config["relation_file"], "r", encoding="utf-8") as f:
            self.relation_list = json.load(f)
        for r in self.relation_list:
            self.relation[r["name"]] = r

    def find_name(self, name):
        """
        在self.entity中查找
        """
        entity = self.entity.get(name)
        return entity

    def find_similar(self, query, ratio_threshold=0.5):
        """
        返回{name: attribute}的格式
        """
        answer = []
        similar_entities = dict()
        # for entity in self.entity_list:  # 相似度大于阈值或名称有包含
        #     ratio = similarity_ratio(query, entity["name"])
        #     if ratio >= ratio_threshold or (entity["name"] in query or query in entity["name"]):
        #         similar_entities.setdefault(ratio, [])
        #         similar_entities[ratio].append(entity)
        #
        # for score, entity_list in sorted(similar_entities.items(), key=lambda x: -x[0]):
        #     for entity in entity_list:
        #         attribute = entity["attribute"]
        #         attribute["经名"] = entity["name"]
        #         answer.append(attribute)
        #     if score == 1:  # 有相符的就只返回相符的
        #         break
        for name in self.entity_name_set:  # 相似度大于阈值或名称有包含
            # print(query, name)
            ratio = similarity_ratio(query, name)
            if ratio >= ratio_threshold or (name in query or query in name):
                similar_entities.setdefault(ratio, [])
                similar_entities[ratio].append(name)

        for score, entity_list in sorted(similar_entities.items(), key=lambda x: -x[0]):
            for entity in entity_list:
                answer.append(entity)
            if score == 1:  # 有相符的就只返回相符的
                break
        return answer

    def find_answer(self, query):
        """
        查找逻辑：
        一、精确匹配到一个节点：
        节点attribute:
        1.有地址译者
        2.有部数
        3.空attribute:找孩子节点，如“大藏经”

        二、模糊匹配到多个节点：
        按一循环

        三、返回的节点，如果是叶子节点，不用处理
        如果是中间节点，点击后返回叶子节点
        """
        from pprint import pprint
        answers = []  # [{地址，经名，译者}, ..., {}]
        similar = self.find_similar(query=query)
        for s in similar:
            entities = self.find_name(s)
            # pprint(entities)
            for entity in entities:
                if not entity["attribute"].get("地址"):
                    # 地址为空,表示不是经书节点，要继续找子节点
                    children = self.kbqa.graph_arango.find_children_by_name(graph="tripitaka", name=entity["name"])
                    print(entity)
                    pprint(children)
                    # print(children["name"])
                    answer = self.format_answer(children)
                    starter = self.format_answer([entity])
                    answer.insert(0, starter[0])
                    answers.append(answer)
                else:  # 是经书节点，直接format_answer
                    answer = self.format_answer([entity])
                    answers.append(answer)
        # pprint(answers)
        self.kbqa.response = answers

    @staticmethod
    def format_answer(nodes):
        formatted_answer = []
        for node in nodes:
            attribute = node["attribute"]
            attribute["经名"] = node["name"]
            # 如果没有地址，a标签的链接地址应该再次以这个name找子节点
            formatted_answer.append(attribute)
        return formatted_answer

