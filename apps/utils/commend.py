import json
from rest_framework.response import Response


def test():
    aItem = {}
    aItem["id"] = "2203"
    aItem["title"] = "title"
    aItem["subTitle"] = "sub title"
    bItem = {}
    bItem["id"] = "2842"
    bItem["title"] = "b标题"
    bItem["subTitle"] = "b副标题"
    bItem["content"] = "内容"
    bItem["list"] = ["a", "a 2", "b", "bb"]
    aJson = json.dumps(aItem)
    bJson = json.dumps(bItem, ensure_ascii=False)
    print(aItem)
    return aJson
