import re

def 到大写字母(要操作的文本, 起始位置=None, 转换字母数=None):
    # 我是人才 其实不应该这样写的
    缓冲区长度 = len(要操作的文本)
    偏移 = 1
    # 判断
    if 起始位置 is None:
        起始位置 = 1

    # 判断转换字母数是否为空
    if 转换字母数 is None:
        转换字母数 = len(要操作的文本) - 起始位置 + 1
    偏移 = 起始位置 - 1

    # 循环处理
    for _ in range(转换字母数):
        if 偏移 >= 缓冲区长度:
            break
        if ord(要操作的文本[偏移]) > 128:
            偏移 += 2
        else:
            if 96 < ord(要操作的文本[偏移]) < 123:
                要操作的文本 = 要操作的文本[:偏移] + chr(ord(要操作的文本[偏移]) & 95) + 要操作的文本[偏移 + 1:]
            偏移 += 1
    return 要操作的文本

def 字数到位置(要操作的文本, 字数):
    偏移 = 1
    缓冲区长度 = len(要操作的文本)

    for _ in range(字数 - 1):
        if 偏移 > 缓冲区长度:
            break
        if ord(要操作的文本[偏移 - 1]) > 128:
            偏移 += 2
        else:
            偏移 += 1
    return 偏移

def 到小写字母(要操作的文本, 起始位置=None, 转换字母数=None):
    缓冲区长度 = len(要操作的文本)
    偏移 = 0
    if 起始位置 is None:
        起始位置 = 1
    偏移 = 字数到位置(要操作的文本, 起始位置) - 1

    if 转换字母数 is None:
        转换字母数 = 缓冲区长度 - 偏移

    # 转换字母
    for _ in range(转换字母数):
        if 偏移 >= 缓冲区长度:
            break
        if ord(要操作的文本[偏移]) > 128:
            偏移 += 2
        elif 64 < ord(要操作的文本[偏移]) < 91:
            缓冲区列表 = list(要操作的文本)
            缓冲区列表[偏移] = chr(ord(要操作的文本[偏移]) | 32)
            要操作的文本 = ''.join(缓冲区列表)
            偏移 += 1
        else:
            偏移 += 1
    return 要操作的文本

def 删首空格(要操作的文本):
    # 使用lstrip方法 左
    删除空格后的文本 = 要操作的文本.lstrip(' ')
    return 删除空格后的文本

def 删尾空格(要操作的文本):
    # 使用rstrip方法 右
    删除空格后的文本 = 要操作的文本.rstrip(' ')
    return 删除空格后的文本

def 删除全部空格(要操作的文本): 
    # 使用正则表达 全部
    删除空格后的文本 = re.sub(r'\s+', '', 要操作的文本)
    return 删除空格后的文本

# 更改写法
# def 写出到文件(文件名):
#     内存内容 = []
#     with open(文件名, 'wb') as 文件句柄:
#         文件句柄.seek(0)
#         文件句柄.write(内存内容.encode('utf-8')) 
#     return True

def 读取文本每行(文件路径):
    """
        读取指定路径的文本文件，并返回每行的内容（去除前后空白字符）。
        
        参数:
        文件路径 (str): 要读取的文本文件的路径。
        
        返回:
        list: 包含每行文本内容的列表。
    """
    文本内容 = []
    try:
        with open(文件路径, 'r', encoding='utf-8') as 文件:
            for 行 in 文件:
                文本内容.append(行.strip())
    except FileNotFoundError:
        print(f"文件 {文件路径} 未找到。")
    except UnicodeDecodeError:
        print(f"文件 {文件路径} 编码错误，请确保文件编码为UTF-8。")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
    return 文本内容

def 写出到文本(文件名, 文本):
    """
        将文本列表写入指定的文件。

        参数:
        文件名 (str): 要写入的文件路径和名称。
        文本 (list): 要写入文件的文本行列表。
    """
    try:
        with open(文件名, 'w', encoding='utf-8') as 文件:
            文件.write('\n'.join(文本))
    except Exception as e:
        print(f"写入文件时发生错误: {e}")