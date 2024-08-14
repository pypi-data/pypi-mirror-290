import json

class Json类:
    def __init__(self):
        self.json数据 = None

    def 解析(self, JSON文本: str, 为对象: bool = False) -> bool:
        """
        解析 JSON 文本为 Python 对象。
        
        参数:
        JSON文本: 文本型, 必须是标准的JSON格式。
        为对象: 逻辑型, 如果为真，则返回JSON对象，否则返回字典。
        
        返回:
        逻辑型, 如果解析成功返回真，否则返回假。
        """
        try:
            self.json数据 = json.loads(JSON文本)
            return True
        except json.JSONDecodeError:
            print("JSON文本格式不正确，请检查输入是否为标准JSON格式。")
            return False

    def 取通用属性(self, 属性名: str, 为对象: bool = False) -> str:
        """
        获取JSON数据中的属性值。
        
        参数:
        属性名: 文本型, 要获取的属性名称。
        为对象: 逻辑型, 如果为真，则属性解析为JSON对象或数组，否则解析为文本。
        
        返回:
        文本型, 属性的值，如果属性不存在或解析失败则返回空字符串。
        """
        if self.json数据 is not None and 属性名 in self.json数据:
            属性值 = self.json数据[属性名]
            if 为对象:
                return json.dumps(属性值)
            else:
                return str(属性值)
        else:
            print(f"属性'{属性名}'不存在或JSON数据未正确解析。")
            return ""




