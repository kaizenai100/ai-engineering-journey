class WeatherTool:
    """天气工具，封装工具定义和执行"""

    def get_weather(self, city):
        return f"{city} 晴转多云，东风3-4级，空气质量优，18-25度，温度适宜。"
    
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "查询天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    def execute(self, func_name, func_args):
        mapping = {
            "get_weather": self.get_weather
        }
        return mapping[func_name](**func_args)
