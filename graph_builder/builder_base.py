import json

from itertools import repeat


class Base:
    def __init__(self, name, start_id, prefix):
        self.name = name
        self.start_id = start_id
        self.prefix = prefix

        self.entity_keys = ["name", "_key", "_id", "attribute"]
        self.relation_keys = ["name", "_key", "_id", "_from", "_to"]

        self.entity_list = []
        self.relation_list = []

        self.entity_count = 0
        self.relation_count = 0

        self.known_entities = {}
        self.known_relations = {}

    def json_template(self, kind):
        keys = self.entity_keys if kind == "entity" else self.relation_keys
        return dict(zip(keys, repeat("")))

    def generate_entity(self, **kwargs):
        if kwargs.get("check_exist") and kwargs["name"] in self.known_entities:
            return self.known_entities[kwargs["name"]]
        kwargs.pop("check_exist", None)
        entity = self.json_template("entity")
        for k in kwargs:
            entity[k] = kwargs.get(k)
        entity["_key"] = "{}".format(self.start_id + self.entity_count)
        entity["_id"] = "{}_entity/{}".format(self.prefix, self.start_id + self.entity_count)

        self.known_entities[kwargs["name"]] = entity
        self.entity_list.append(entity)
        self.entity_count += 1
        return entity

    def generate_relation(self, **kwargs):
        relation = self.json_template("relation")
        for k in kwargs:
            relation[k] = kwargs.get(k)
        relation["_key"] = "{}".format(self.start_id + self.relation_count)
        relation["_id"] = "{}_relation/{}".format(self.prefix, self.start_id + self.relation_count)

        self.known_relations[kwargs["name"]] = relation
        self.relation_list.append(relation)
        self.relation_count += 1
        return relation

    def save_json(self, path):
        json_format = dict(ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
        entity_file = '{}/{}_entity.json'.format(path, self.prefix)
        relation_file = '{}/{}_relation.json'.format(path, self.prefix)
        print("saved to:")
        print(entity_file, len(self.entity_list))
        print(relation_file, len(self.relation_list))
        with open(entity_file, "w", encoding="utf-8") as f:
            json.dump(self.entity_list, f, **json_format)
        with open(relation_file, "w", encoding="utf-8") as f:
            json.dump(self.relation_list, f, **json_format)
