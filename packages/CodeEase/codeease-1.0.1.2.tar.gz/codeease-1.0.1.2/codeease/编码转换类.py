import base64
from base64 import b64encode, b64decode
import ctypes
import platform

def base64编码(欲转换的数据: str) -> str:
    """
        将输入的字符串数据转换为 Base64 编码形式.

        参数:
            data (str): 要进行 Base64 编码的字符串数据.

        返回:
            str: 返回编码后的 Base64 字符串.
    """
    encoded_bytes = base64.b64encode(欲转换的数据.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def base64解码(欲转换的数据: str) -> str:
    """
        将输入的字符串数据转换为 Base64 编码形式.

        参数:
            data (str): 要进行 Base64 解码的字符串数据.

        返回:
            str: 返回解码后的 Base64 字符串.
    """
    decoded_bytes = base64.b64decode(欲转换的数据.encode('utf-8'))
    return decoded_bytes.decode('utf-8')

def BASE64编码API(欲转换的数据: bytes, dwFlags: int = None):
    """
        将字节数据编码为 Base64 字符串。

        Args:
            data (bytes): 需要编码的字节数据。
            flags (int, optional): 编码标志位。如果为 1 则执行 Base64 编码,否则返回空字节串。默认为 0。

        Returns:
            bytes: 编码后的 Base64 字节数据。
    """
    if dwFlags is None:
        dwFlags = 1 
    try:
        if dwFlags & 1: 
            encoded_data = b64encode(欲转换的数据)
            return encoded_data
        else:
            return b''
    except Exception as e:
        return b''

def BASE64解码API(欲转换的数据: bytes, dwFlags: int = None):
    """
        将给定的 bytes 对象解码为 Base64 格式。

        参数:
            data (bytes): 需要解码的 bytes 对象。
            flags (int, optional): 解码标志位。
                如果 flags 的第一位为 1，则执行 Base64 解码;
                否则返回空 bytes 对象。
                默认值为 0。

        返回:
            bytes: 解码后的 bytes 对象。
    """
    if dwFlags is None:
        dwFlags = 1 
    
    try:
        if dwFlags & 1: 
            decoded_data = b64decode(欲转换的数据)
            return decoded_data
        else:
            return b''
    except Exception as e:
        return b''

## RC4加密-解密-算法
def RC4加密(明文: bytes, 密钥: str) -> bytes:
    """
        使用 RC4 算法对明文进行加密。

        参数:
            plaintext (bytes): 需要加密的明文数据。
            key (str): 用于加密的密钥。

        返回:
            bytes: 加密后的密文数据。
    """
    return 校验_取rc4(明文, 密钥)

def RC4解密(密文: bytes, 密钥: str) -> bytes:
    """
        使用 RC4 算法对密文进行解密。

        参数:
            plaintext (bytes): 需要解密的密文数据。
            key (str): 用于解密的密钥。

        返回:
            bytes: 解密后的密文数据。
    """
    return 校验_取rc4(密文, 密钥)

# 实现RC4加密算法
def 校验_取rc4(data: bytes, key: str) -> bytes:
    def KSA(key):
        key_length = len(key)
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + ord(key[i % key_length])) % 256
            S[i], S[j] = S[j], S[i]
        return S

    def PRGA(S):
        i = j = 0
        while True:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            yield K

    def RC4(data, key):
        S = KSA(key)
        return bytes([data[i] ^ next(PRGA(S)) for i in range(len(data))])

    return RC4(data, key)

# 检测操作系统
is_windows = platform.system() == 'Windows'

# 如果是Windows，导入相关的库和定义函数
if is_windows:
    import base64
    from base64 import b64encode, b64decode
    kernel32 = ctypes.WinDLL('kernel32')

    # 简体繁体互换 只支持Win 因为调用的是Win的API
    # 利用kernel32.dll 实现简体繁体互换
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    kernel32.LCMapStringA.argtypes = [
        ctypes.c_int,                  # Locale
        ctypes.c_int,                  # dwMapFlags
        ctypes.c_char_p,               # lpSrcStr
        ctypes.c_int,                  # cchSrc
        ctypes.c_char_p,               # lpDestStr
        ctypes.c_int                   # cchDest
    ]
    kernel32.LCMapStringA.restype = ctypes.c_int

    def 简体到繁体(text):
        """
            将简体中文转换为繁体中文。

            Args:
                text (str): 需要转换的简体中文字符串。

            Returns:
                str: 转换后的繁体中文字符串。
        """
        # 简体中文转繁体中文
        locale = 2052  # 中文GBK/CP936编码
        flags = 67108864  # 转换为繁体
        src_len = len(text.encode('cp936'))
        dst_len = src_len * 2 
        src_buffer = ctypes.create_string_buffer(text.encode('cp936'))
        dst_buffer = ctypes.create_string_buffer(dst_len)

        # 调用LCMapStringA
        ret = kernel32.LCMapStringA(locale, flags, src_buffer, src_len, dst_buffer, dst_len)

        if ret == 0:
            raise ctypes.WinError(ctypes.get_last_error())

        return dst_buffer.value.decode('cp936')

    def 繁体到简体(text):
        """
            将繁体中文转换为简体中文。

            Args:
                text (str): 需要转换的繁体中文字符串。

            Returns:
                str: 转换后的简体中文字符串。
        """
        # 繁体中文转简体中文
        locale = 2052  # 中文GBK/CP936编码
        flags = 33554432  # 转换为简体
        src_len = len(text.encode('cp936'))
        dst_len = src_len * 2
        src_buffer = ctypes.create_string_buffer(text.encode('cp936'))
        dst_buffer = ctypes.create_string_buffer(dst_len)

        ret = kernel32.LCMapStringA(locale, flags, src_buffer, src_len, dst_buffer, dst_len)

        if ret == 0:
            raise ctypes.WinError(ctypes.get_last_error())

        return dst_buffer.value.decode('cp936')
else:
    # 如果不是Windows，定义空函数或者抛出异常
    def 简体到繁体(text):
        raise NotImplementedError("该功能仅支持Windows操作系统。")

    def 繁体到简体(text):
        raise NotImplementedError("该功能仅支持Windows操作系统。")