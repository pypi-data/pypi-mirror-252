import click


@click.group()
def main():
    pass


@main.command(help="随机色图")
@click.option("-r", "--r18", default=0, type=int,
              help="0为非 R18，1为 R18，2为混合（在库中的分类，不等同于作品本身的 R18 标识）")
@click.option("-n", "--num", default=1, type=int,
              help="一次返回的结果数量，范围为1到20；在指定关键字或标签的情况下，结果数量可能会不足指定的数量")
@click.option("-u", "--uid", default=None, type=int, help="返回指定uid作者的作品，最多20个")
@click.option("-t", "--tag", default='萝莉,少女,白丝,黑丝', type=str,
              help="返回匹配指定标签的作品 https://api.lolicon.app/#/setu?id=tag （以逗号隔开 如 萝莉,少女,白丝,黑丝）")
@click.option("-s", "--size", default="original", type=str,
              help="返回指定图片规格的地址 https://api.lolicon.app/#/setu?id=size")
@click.option("-p", "--proxy", default="i.pixiv.re", type=str,
              help="设置图片地址所使用的在线反代服务 https://api.lolicon.app/#/setu?id=proxy")
@click.option("-e", "--excludeai", default=False, type=bool, help="排除 AI 作品")
@click.option("-d", "--download", default=True, type=bool, help="获取并下载图片")
@click.option("--path", default=".\\", type=str, help="图片下载地址")
def setu(r18, num, uid, tag, size, proxy, excludeai, download, path):
    from .setu import get_setu
    from colorama import Fore, Back
    data = get_setu(
        r18=r18,
        num=num,
        uid=uid,
        tag=tag.split(","),
        size=size,
        proxy=proxy,
        exCludeAI=excludeai
    )
    print(f"{Fore.BLACK}{Back.LIGHTBLUE_EX} -- 获取数据 -- {Fore.RESET}{Back.RESET}")
    print(
        data
    )
    for image in data.data:
        print(f"{Fore.BLACK}{Back.LIGHTYELLOW_EX} -- 图片{image.pid} -- {Fore.RESET}{Back.RESET}")
        print(f"画师：{image.author}{image.uid}")
        print(f"标题：{image.title}")
        print(f"标签：{image.tags}")
        if r18:
            print(f"成人图（不安全）")
        else:
            print("未成年图（安全）")
        print(image.urls[size])

        if download:
            from os.path import join, exists
            from os import makedirs
            if not exists(path):
                makedirs(path)
            with open(join(path, f"{image.pid}.{image.ext}"), "wb+") as img:
                try:
                    print(f"{Fore.BLACK}{Back.LIGHTBLUE_EX}图片{image.pid} -> 下载中{Fore.RESET}{Back.RESET}")

                    from requests import get
                    img.write(
                        get(
                            image.urls[size]
                        ).content
                    )
                except:
                    print(f"{Fore.BLACK}{Back.LIGHTRED_EX}图片{image.pid} -> 下载失败{Fore.RESET}{Back.RESET}")
                else:
                    print(f"{Fore.BLACK}{Back.LIGHTGREEN_EX}图片{image.pid} -> 下载成功{Fore.RESET}{Back.RESET}")

                print()

if __name__ == '__main__':
    main()
