from zhtools.langconv import *


def t2s(sentence):
    """
    Traditional2Simplified
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    """
    sentence = Converter('zh-hans').convert(sentence)
    return sentence


def s2t(sentence):
    """
    Simplified2Traditional
    将sentence中的简体字转为繁体字
    :param sentence: 待转换的句子
    :return: 将句子中简体字转换为繁体字之后的句子
    """
    sentence = Converter('zh-hant').convert(sentence)
    return sentence


if __name__ == "__main__":
    simplified_sentence = '忧郁的台湾乌龟'
    traditional_sentence = s2t(simplified_sentence)
    print(traditional_sentence)

    '''
    输出结果：
        憂郁的臺灣烏龜
    '''

    traditional_sentence = '憂郁的臺灣烏龜'
    simplified_sentence = t2s(traditional_sentence)
    print(simplified_sentence)

    '''
    输出结果：
        忧郁的台湾乌龟
    '''
