from pprint import pprint
from arango import ArangoClient

client = ArangoClient(hosts='http://localhost:8529')

# Connect to "_system" database as root user.
db = client.db('_system', username='root', password='rai')


class ArangoGraph:
    def __init__(self, kbqa=None):
        self.kbqa = kbqa

    def create_collection(self):
        pass

    def create_graph(self):
        pass

    def find_name(self, graph, name):
        """
        根据name字段查找单个节点，严格匹配
        """
        node = self.find_nodes(graph=graph, name=name, layer=0)
        # print(node)
        return node

    def find_children_by_name(self, graph, name):
        """
        根据name字段查找所有子节点，严格匹配
        """
        children = self.find_nodes(graph=graph, name=name, layer=1)
        # print(children)
        return children

    def find_id(self, _id):
        """
        根据_id查找，严格匹配
        """
        pass

    @staticmethod
    def find_nodes(graph, layer, name):
        aql_statement = """
        FOR c IN {graph}_entity
            FILTER c.name == "{name}"
            FOR v IN {layer}..{layer} OUTBOUND c {graph}_relation
                RETURN v
        """
        cursor = db.aql.execute(
            aql_statement.format(graph=graph, layer=layer, name=name))
        result = []
        for c in cursor:
            if c not in result:
                result.append(c)
        return result


if __name__ == '__main__':
    # find_son("tripitaka_entity/100000001")

    arango_graph = ArangoGraph()
    # 先按similar_string找到相关节点，再将这些节点放入find_son
    pprint(arango_graph.find_nodes(graph="tripitaka", layer=1, name="大乘般若部"))
