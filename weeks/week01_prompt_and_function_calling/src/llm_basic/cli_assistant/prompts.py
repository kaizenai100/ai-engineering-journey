class PromptBuilder:
    """统一管理提示词构建"""

    @staticmethod
    def intent(input_text):
        return f"""判断以下用户输入的意图。
    用户输入：{input_text}

    可选意图：
    - 查天气
    - 提取信息
    - 闲聊
    - 投诉

    只返回意图名称，不要解释。"""

    @staticmethod
    def extract(input_text, fields):
        return f"""从以下文本中提取信息，以JSON的格式返回。

    文本：{input_text}

    提取的字段全部选项：{fields}

    注意：文本中可能包含用户的问题，请根据问题意图只提取相关字段，而不是提取全部字段。
    只返回JSON格式的字符串，不要其他内容，返回结果可以通过json.loads()函数解析成字典。"""
