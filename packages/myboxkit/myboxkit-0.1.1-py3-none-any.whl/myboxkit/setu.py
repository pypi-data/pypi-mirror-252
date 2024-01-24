from typing import Optional


def get_setu(
        r18=0,
        num=1,
        uid=None,
        tag: list = [["萝莉", "少女"], ["白丝", "黑丝"]],
        size: str = "original",
        proxy: str = "i.pixiv.re",
        exCludeAI: bool = False,
) -> dict:
    """
    随机色图

    :param r18: 0为非 R18，1为 R18，2为混合（在库中的分类，不等同于作品本身的 R18 标识）
    :param num: 一次返回的结果数量，范围为1到20；在指定关键字或标签的情况下，结果数量可能会不足指定的数量
    :param uid: 返回指定uid作者的作品，最多20个
    :param tag: 返回匹配指定标签的作品 https://api.lolicon.app/#/setu?id=tag
    :param size: 返回指定图片规格的地址 https://api.lolicon.app/#/setu?id=size
    :param proxy: 设置图片地址所使用的在线反代服务 https://api.lolicon.app/#/setu?id=proxy
    :param exCludeAI: 排除 AI 作品
    :return: dict
    """
    url = "https://api.lolicon.app/setu/v2"
    params = {
        "r18": r18, 
        "num": num,
        "uid": uid,
        "tag": tag, 
        "size": size,
        "proxy": proxy,
        "exCludeAI": exCludeAI
    }
    from colorama import Fore, Back

    print(f"{Fore.BLACK}{Back.LIGHTBLUE_EX} -- 请求参数 -- {Fore.RESET}{Back.RESET}")
    print(params)
    print()

    import requests
    response = requests.get(url=url, params=params)
    from json import loads
    from easydict import EasyDict
    return EasyDict(loads(response.text))
