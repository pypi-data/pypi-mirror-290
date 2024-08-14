from codeease import *


url = ""
网页数据 = 网页_访问(url)
测试 = Json类()
测试.解析(网页数据)
信息 = 测试.取通用属性("msg")
print(信息)
