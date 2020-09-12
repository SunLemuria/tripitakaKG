import difflib


def similarity(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


if __name__ == '__main__':
    print(similarity("文殊师利所说", "文殊师利所说摩诃般若波罗蜜经"))
    print(similarity("文殊师利所说", "文殊师利所说"))
