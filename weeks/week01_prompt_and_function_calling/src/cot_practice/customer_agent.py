import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cot_practice.tools import ScenicDescTool, OrderDetailTool, RefundAmountTool, CreateOrderTool
from cot_practice.prompts import PromptBuilder
from commons.llm_client import OpenAIClient


class CustomerAgent():
    """客服智能体，负责意图识别和任务分发，主要处理门票相关业务问题
    """

    EXTRACT_FIELDS = ["订单号", "景点名称"]
    def __init__(self):
        self.llm = OpenAIClient()
        self.scenic_desc_tool = ScenicDescTool()
        self.order_detail_tool = OrderDetailTool()
        self.refund_detail_tool = RefundAmountTool()
        self.create_order_tool = CreateOrderTool()
        self.history = [
            {
                "role": "system",
                "content": """你是一个门票OTA平台的智能客服，你需要根据用户的意图进行智能处理，安抚用户的情绪并高质量的解决用户的问题。
                
                关于退款：如果用户需要退款，你需要从景区信息中查看退改规则，然后结合订单信息进行计算需要扣除的手续费金额

                关于改期：如果用户需要改期，你要先从景区信息中确认改景区是否支持改期
                
                """
            }
        ]
        self.extract_json_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "extract_result",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "scenic_name": {
                            "type": "string", 
                            "description": "景点名称"
                        },
                        "order_id": {
                            "type": "string",
                            "description": "订单号"
                        }
                    },
                    "required": [],
                    "additionalProperties": False
                }
            }
        }

    
    def classify_intent(self, user_input):
        """意图识别"""
        prompt = PromptBuilder.intent_prompt(user_input)
        msg = self.llm.chat(prompt)
        return msg.strip()
    

    
    def scenic_desc_handel(self, user_input):
        """景区信息相关问题处理"""
        tools = [self.scenic_desc_tool.definition]
        msg, messages = self.llm.call(prompt=user_input, tools=tools, history=self.history)
        if msg.tool_calls:

            messages.append(msg)
            tool_call = msg.tool_calls[0]
            print(f"fun_args_str：{tool_call.function.arguments}")
            func_args = json.loads(tool_call.function.arguments)
            func_name = tool_call.function.name
            scenic_desc = self.scenic_desc_tool.execute(func_name, func_args)
            if not scenic_desc:
                return "没有找到该景点信息"
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": scenic_desc
                }
            )
            msg, _ = self.llm.call(prompt='', history=messages)
            return msg.content
        else:
            return msg.content
        
    def create_order_handel(self, user_input):
        """创建订单相关问题处理"""
        tools = [self.create_order_tool.definition]
        msg, messages = self.llm.call(prompt=user_input, tools=tools, history=self.history)
        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            func = self.create_order_tool.execute(func_name, func_args)
            messages.append(msg)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": func
                }
            )
            msg, messages = self.llm.call(prompt='', history=messages)
            return msg.content
        else:
            return msg.content
        
    def order_detail_handel(self, user_input):
        """订单详情相关问题处理"""
        tools = [self.order_detail_tool.definition]
        msg, messages = self.llm.call(prompt=user_input, tools=tools, history=self.history)
        if msg.tool_calls:
            messages.append(msg)
            tool_call = msg.tool_calls[0]
            func_args = json.loads(tool_call.function.arguments)
            func_name = tool_call.function.name
            order_detail = self.order_detail_tool.execute(func_name, func_args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": order_detail
                }
            )
            msg, _ = self.llm.call(prompt='',history=messages)
            return msg.content
        else:
            return msg.content

    def refund_handel(self, user_input):
        """退款相关问题处理"""
        tools = [self.order_detail_tool.definition,self.refund_detail_tool.definition]
        for i in range(5):
            msg, messages = self.llm.call(prompt=user_input, tools=tools, history=self.history)
            print(msg.content)
            messages.append(msg.tool_calls)
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    func_args = json.loads(tool_call.function.arguments)
                    func_name = tool_call.function.name
                    if func_name == "get_order_detail":
                        print(f"get_order_detail agrs:{func_args}")
                        order_detail = self.order_detail_tool.execute(func_name, func_args)
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": order_detail
                            }
                        )
                    elif func_name == "get_refund_amount":
                        print(f"get_refund_amount agrs:{func_args}")
                        refund_amount = self.refund_detail_tool.execute(func_name, func_args)
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": refund_amount
                            }
                        )
                    elif func_name == "get_scenic_desc":
                        print(f"get_scenic_desc agrs:{func_args}")
                        scenic_desc = self.scenic_desc_tool.execute(func_name, func_args)
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": scenic_desc
                            }
                        )
            else:
                return msg.content

    def extract_handel(self, user_input):
        """提取数据"""
        prompt = PromptBuilder.extract(user_input, self.EXTRACT_FIELDS)
        msg = self.llm.call(prompt=prompt, response_format=self.extract_json_schema, history=self.history)
        return json.loads(msg)
    
    def handle_chat(self, user_input):
        """闲聊处理"""
        msg, _ = self.llm.call(prompt=user_input, history=self.history)
        return msg.content
    
    def handle(self, user_input):
        intent = self.classify_intent(user_input)
        print(f"意图：{intent}")

        handlers = {
            "入园咨询": self.scenic_desc_handel,
            "售前咨询": self.scenic_desc_handel,
            "退票咨询": self.refund_handel,
            "改期咨询": self.scenic_desc_handel,
            "订单查询": self.order_detail_handel,
            "投诉建议": self.handle_chat,
            "紧急求助": self.scenic_desc_handel,
            "活动咨询": self.scenic_desc_handel,
            "创建订单": self.create_order_handel,
            "闲聊": self.handle_chat,
        }
        handler = handlers.get(intent, self.handle_chat)
        if handler:
            return handler(user_input)
        else:
            return "很抱歉，没能理解您的意思！"
        

    def chat(self, user_input):
        result = self.handle(user_input)
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": result})
        return result