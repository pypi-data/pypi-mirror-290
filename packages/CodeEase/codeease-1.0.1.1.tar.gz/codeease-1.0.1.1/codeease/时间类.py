import time

获取当前时间戳 = time.time()

def 格式化时间戳(时间戳):
    return time.ctime(时间戳)

def 暂停(秒数):
    time.sleep(秒数)

def 获取当前本地时间():
    return time.asctime(time.localtime())

def 获取当前UTC时间():
    return time.gmtime()

def 格式化时间(时间戳):
    return time.localtime(时间戳)

