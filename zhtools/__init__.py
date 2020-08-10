from .langconv import Converter

T2S = Converter('zh-hans').convert


def t2s(text):
    '''繁体转简体'''

    return T2S(text.strip())
