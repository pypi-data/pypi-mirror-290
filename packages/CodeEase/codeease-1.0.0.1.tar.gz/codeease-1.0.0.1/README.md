# CodeEase

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CodeEase(易码),是一个中文函数库，给出了同等函数的翻译，实现在Python平台中文也能实现开发。

## 项目描述

CodeEase(易码) 项目提供了一个对照表，列出了Python的中文对应的标准异常和内置函数，以帮助开发者更好地理解和使用 Python 语言。

## 特性

- 提供对等的 Python 标准异常和内置函数的中英文对照。
- 帮助开发者快速查找和理解在使用CodeEase(易码)中的错误类型和函数。


## 使用方法

要使用 CodeEase，你可以简单地将项目克隆到本地，然后查看对照表。

```bash
git clone https://github.com/yourusername/codeease.git
cd codeease

## 异常和内置函数对照表

以下是 Python 的一些标准异常和内置函数，以及它们的中文名称：

  ## 时间函数
  获取当前时间戳  格式化时间戳 暂停 
  获取当前本地时间 获取当前UTC时间 格式化时间

  ## 访问函数 - 等待后续更新
  网页_访问 
    """
    网页访问函数，模拟子程序网页访问功能。
    
    参数:
    网址: str, 完整的网页地址，必须包含http://或者https://
    访问方式: int, 0=GET, 1=POST, 2=HEAD, 3=PUT, 4=OPTIONS, 5=DELETE
    提交信息: str, POST专用，表单提交数据
    提交Cookies: dict, 设置提交时的cookie
    返回Cookies: dict, 返回的Cookie
    附加协议头: str, 附加的协议头，一行一个请用换行符隔开
    返回协议头: dict, 返回的协议头
    禁止重定向: bool, 默认不禁止网页重定向
    字节集提交: bytes, 提交字节集数据
    代理地址: str, 代理地址，格式为:ip:port,例如:8.8.8.8:88
    是否自动合并更新Cookie: bool, 默认为真，自动合并更新
    是否补全必要协议头: bool, 当附加协议头为空时自动添加必要的UA协议头
    是否处理协议头大小写: bool, 将协议头中的键名首字母处理为大写
    
    返回:
    返回网页访问的字节集，如果访问失败则返回None
    """
    ## 异常函数 + 内置函数 等待后续更新
    | 英文异常/函数 | 中文名称       |
    |----------------|----------------|
    |print  | 调试输出      |
    |ArithmeticError  | 算术错误      |
    |AssertionError  | 断言错误      |
    |AttributeError  | 属性错误      |
    |BaseException  | 基础异常      |
    |BlockingIOError  | 阻塞IO错误      |
    |BrokenPipeError  | 管道破裂错误      |
    |BufferError  | 缓冲区错误      |
    |BytesWarning  | 字节警告      |
    |ChildProcessError  | 子进程错误      |
    |ConnectionAbortedError  | 连接中止错误      |
    |ConnectionError  | 连接错误      |
    |ConnectionRefusedError  | 连接被拒绝错误      |
    |ConnectionResetError  | 连接重置错误      |
    |DeprecationWarning  | 弃用警告      |
    |EOFError  | 文件结束错误      |
    |EnvironmentError  | 环境错误      |
    |Exception  | 异常      |
    |FileExistsError  | 文件已存在错误      |
    |FileNotFoundError  | 文件未找到错误      |
    |FloatingPointError  | 浮点错误      |
    |FutureWarning  | 未来警告      |
    |GeneratorExit  | 生成器退出      |
    |IOError  | IO错误      |
    |ImportError  | 导入错误      |
    |ImportWarning  | 导入警告      |
    |IndentationError  | 缩进错误      |
    |IndexError  | 索引错误      |
    |InterruptedError  | 中断错误      |
    |IsADirectoryError  | 是一个目录错误      |
    |KeyError  | 键错误      |
    |KeyboardInterrupt  | 键盘中断      |
    |LookupError  | 查找错误      |
    |MemoryError  | 内存错误      |
    |ModuleNotFoundError  | 模块未找到错误      |
    |NameError  | 名称错误      |
    |NotADirectoryError  | 不是一个目录错误      |
    |NotImplementedError  | 尚未实现错误      |
    |OSError  | 操作系统错误      |
    |OverflowError  | 溢出错误      |
    |PendingDeprecationWarning  | 待弃用警告      |
    |PermissionError  | 权限错误      |
    |ProcessLookupError  | 进程查找错误      |
    |RecursionError  | 递归错误      |
    |ReferenceError  | 引用错误      |
    |ResourceWarning  | 资源警告      |
    |RuntimeError  | 运行时错误      |
    |RuntimeWarning  | 运行时警告      |
    |StopAsyncIteration  | 停止异步迭代      |
    |StopIteration  | 停止迭代      |
    |SyntaxError  | 语法错误      |
    |SyntaxWarning  | 语法警告      |
    |SystemError  | 系统错误      |
    |SystemExit  | 系统退出      |
    |TabError  | 制表符错误      |
    |TimeoutError  | 超时错误      |
    |TypeError  | 类型错误      |
    |UnboundLocalError  | 未绑定本地错误      |
    |UnicodeDecodeError  | Unicode解码错误      |
    |UnicodeEncodeError  | Unicode编码错误      |
    |UnicodeError  | Unicode错误      |
    |UnicodeTranslateError  | Unicode翻译错误      |
    |UnicodeWarning  | Unicode警告      |
    |UserWarning  | 用户警告      |
    |ValueError  | 值错误      |
    |Warning  | 警告      |
    |WindowsError  | Windows错误      |
    |ZeroDivisionError  | 除零错误      |
    |__build_class__  | 构建类      |
    |__import__  | 导入      |
    |__loader__  | 加载器      |
    |abs  | 绝对值      |
    |all  | 全部      |
    |any  | 任一      |
    |ascii  | ASCII码      |
    |bin  | 二进制      |
    |bool  | 布尔值      |
    |breakpoint  | 断点      |
    |bytearray  | 字节数组      |
    |bytes  | 字节      |
    |callable  | 可调用      |
    |chr  | 字符      |
    |classmethod  | 类方法      |
    |compile  | 编译      |
    |complex  | 复数      |
    |copyright  | 版权      |
    |credits  | 信誉      |
    |delattr  | 删除属性      |
    |dict  | 字典      |
    |dir  | 目录      |
    |divmod  | 除余      |
    |enumerate  | 枚举      |
    |eval  | 评估      |
    |exec  | 执行      |
    |exit  | 退出      |
    |filter  | 过滤      |
    |float  | 浮点数      |
    |format  | 格式化      |
    |frozenset  | 冻结集合      |
    |getattr  | 获取属性      |
    |globals  | 全局变量      |
    |hasattr  | 有属性      |
    |hash  | 哈希      |
    |help  | 帮助      |
    |hex  | 十六进制      |
    |id  | ID      |
    |input  | 输入      |
    |int  | 整数      |
    |isinstance  | 实例      |
    |issubclass  | 子类      |
    |iter  | 迭代      |
    |len  | 长度      |
    |license  | 许可证      |
    |list  | 列表      |
    |locals  | 局部变量      |
    |map  | 映射      |
    |max  | 最大值      |
    |memoryview  | 内存视图      |
    |min  | 最小值      |
    |next  | 下一个      |
    |object  | 对象      |
    |oct  | 八进制      |
    |open  | 打开      |
    |ord  | 序号      |
    |pow  | 幂      |
    |property  | 属性      |
    |quit  | 退出      |
    |range  | 范围      |
    |repr  | 表示      |
    |reversed  | 反转      |
    |round  | 四舍五入      |
    |set  | 集合      |
    |setattr  | 设置属性      |
    |slice  | 切片      |
    |sorted  | 排序      |
    |staticmethod  | 静态方法      |
    |str  | 字符串      |
    |sum  | 求和      |
    |super  | 超类      |
    |tuple  | 元组      |
    |type  | 类型      |
    |vars  | 变量      |
    |zip  | 压缩      |

