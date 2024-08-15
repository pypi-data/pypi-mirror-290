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

    def 取成员(self, json_list, 成员索引=None):
        """
            从JSON列表中获取指定索引的成员，并将其转换为JSON格式的字符串。

            参数:
            json_list: list, 一个包含JSON对象的列表。
            成员索引: int, 要获取的成员在列表中的索引位置。

            返回:
            str, 如果索引有效且json_list是列表类型，则返回指定索引处的成员的JSON字符串表示。
                如果索引无效或json_list不是列表类型，则返回None。
        """
        if isinstance(json_list, list):
            if 成员索引 is not None and 0 <= 成员索引 < len(json_list):
                return json.dumps(json_list[成员索引])
            else:
                print(f"索引{成员索引}不在有效范围内。")
                return None
        else:
            print("提供的JSON数据不是列表类型。")
            return None

    def 取成员文本(self, json_list, 成员索引=None, 属性名=None, 为对象=False):
        """
            从JSON列表中的指定成员获取特定属性的文本表示。

            参数:
            json_list: list, 一个包含JSON对象的列表。
            成员索引: int, 要从中获取属性的成员在列表中的索引位置。
            属性名: str, 要获取的属性名称。
            为对象: bool, 如果为True，则返回属性的JSON字符串表示；否则返回属性的字符串表示。

            返回:
            str, 如果所有参数有效，则返回指定属性的文本表示。
                如果参数无效，则返回空字符串或打印错误消息。
        """
        if isinstance(json_list, list):
            if 成员索引 is not None and 0 <= 成员索引 < len(json_list):
                member = json_list[成员索引]
                if 属性名 is not None and 属性名 in member:
                    if 为对象:
                        return json.dumps(member[属性名])
                    else:
                        return str(member[属性名])
                else:
                    print(f"属性'{属性名}'不存在。")
                    return ""
            else:
                print(f"索引{成员索引}不在有效范围内。")
                return ""
        else:
            print("提供的JSON数据不是列表类型。")
            return ""

