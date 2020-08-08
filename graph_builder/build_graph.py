import pandas as pd

from graph_builder.builder_base import Base


class TripitakaBuilder(Base):

    def __init__(self, name, start_id, prefix):
        Base.__init__(self, name, start_id, prefix)
        self.df = pd.DataFrame()
        self.root = self.generate_entity(name=self.name)

    def build(self, path):
        self.parse_excel(path)
        self.build_divisions()
        self.build_books()

    def parse_excel(self, path):
        xls = pd.ExcelFile(path)
        df = pd.read_excel(xls)
        df.fillna("", inplace=True)
        self.df = df

    def build_divisions(self):
        div_names = self.df[["分部", "部数"]].drop_duplicates()
        for row in div_names.iterrows():
            attribute = {"部数": row[1]["部数"]}
            entity = self.generate_entity(name=row[1]["分部"], attribute=attribute, check_exist=True)
            self.generate_relation(name="分部", _from=self.root["_id"], _to=entity["_id"])

    def build_books(self):
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            div_entity = self.generate_entity(name=row["分部"], check_exist=True)
            if not row["分卷"]:  # 没有分卷时, 地址放在书的实体中, 书是路径的最后一个节点
                attribute = {"译者": row["译者"], "地址": row["地址"]}
                book_entity = self.generate_entity(name=row["经名"], attribute=attribute)
            else:  # 有分卷时, 地址放在分卷的实体中, 分卷是路径的最后一个节点
                vol_entity = self.generate_entity(name=row["分卷"], attribute={"地址": row["地址"]})
                book_entity = self.generate_entity(name=row["经名"], check_exist=True)
                self.generate_relation(name="分卷", _from=book_entity["_id"], _to=vol_entity["_id"])
            self.generate_relation(name="经名", _from=div_entity["_id"], _to=book_entity["_id"])

    # def build_volumes(self):
    #     vol_and_addr = self.df[["经名", "分卷", "地址"]].drop_duplicates()
    #     for row in vol_and_addr:
    #         attribute = {"地址": row["地址"]}
    #         book_entity = self.generate_entity(name=row["经名"])
    #         if not row["分卷"]:
    #             name = book_entity["name"]
    #             self.known_entities[name].update(attribute)
    #         else:
    #             vol_entity = self.generate_entity(name=row["分卷"], attribute=attribute)
    #             self.generate_relation(name="经名", _from=book_entity["_id"], _to=vol_entity["_id"])


if __name__ == '__main__':
    file = "../spider/data/books_info.xlsx"
    builder = TripitakaBuilder(name="大藏经", start_id=100000001, prefix="tripitaka")
    builder.build(path=file)
    builder.save_json(path="./results")
