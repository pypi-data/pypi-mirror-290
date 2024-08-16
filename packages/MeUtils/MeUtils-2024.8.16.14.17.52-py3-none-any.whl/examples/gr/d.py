#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : d
# @Time         : 2024/8/16 14:07
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *



def download(url, filename: Optional[str] = None):
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url)
        with open(filename or Path(url).name, 'wb') as f:
            f.write(response.content)


# 使用示例
url = "https://fluxpro.art/api/view/clzwako9n01l6e2zoy3q5mpfe/3.webp"

download(url)
