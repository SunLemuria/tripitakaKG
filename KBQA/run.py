from pprint import pprint
from KBQA.kbqa_main import KBQAMain


def run():
    while 1:
        query = input("input query: ")
        request = {"query": query}

        kbqa.run(request)
        pprint(kbqa.response)


if __name__ == '__main__':
    kbqa = KBQAMain()
    run()
