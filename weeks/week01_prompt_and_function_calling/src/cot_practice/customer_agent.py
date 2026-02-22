import json
from datetime import date
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
        today = date.today().strftime("%Y-%m-%d")
        self.current_flow = None  # 当前进行中的流程
        self.llm = OpenAIClient()
        self.scenic_desc_tool = ScenicDescTool()
        self.order_detail_tool = OrderDetailTool()
        self.refund_detail_tool = RefundAmountTool()
        self.create_order_tool = CreateOrderTool()
        self.history = [
            {
            "role": "system",
            "content": f"""你是一个门票OTA平台的智能客服，你需要根据用户的意图进行智能处理，安抚用户的情绪并高质量的解决用户的问题。
            
            当前日期：{today}
            
            关于退款：如果用户需要退款：
            1. 必须先获取用户的订单号，如果用户没有提供订单号，请先向用户索要
            2. 根据订单中的出游日期和当前日期（{today}）计算距离出游还有几天
            3. 从景区信息中查看退改规则，结合天数计算扣款比例
            4. 最后计算可退金额
            示例：
            退改规则：
                - 出游前7天（含）以上取消：免费退，手续费0%
                - 出游前3天（含）至7天以内取消：收取50%手续费  
                - 出游前3天以内取消：收取80%手续费
                - 出游当日及之后：不可退

                出游日2026-02-27
                - 2026-02-20及之前取消 → 0%
                - 2026-02-21至2026-02-24取消 → 50%
                - 2026-02-25至2026-02-26取消 → 80%
                - 2026-02-27当日 → 不可退
            
            关于改期：如果用户需要改期，你要先从景区信息中确认景区是否支持改期
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
        recent_history = self.history[-4:] if len(self.history) > 4 else self.history[1:]
        context = "\n".join(f"{m['role']}: {m['content']}" for m in recent_history if m["role"] != "system")
        prompt = PromptBuilder.intent_prompt(user_input, context)
        msg = self.llm.chat(prompt)
        return msg.strip()
    

    def _execute_single_tool_call(self, user_input, tools, tool_execute):
        """调 LLM → 解析 tool_call → 执行函数 → 回传结果 → 再调 LLM"""
        msg, messages = self.llm.call(prompt=user_input, tools=tools, history=self.history)
        if msg.tool_calls:
            messages.append(msg)
            tool_call = msg.tool_calls[0]
            print(f"fun_args_str：{tool_call.function.arguments}")
            func_args = json.loads(tool_call.function.arguments)
            func_name = tool_call.function.name
            result = self.scenic_desc_tool.execute(func_name, func_args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            )
            msg, _ = self.llm.call(prompt='', history=messages)
            return msg.content
        else:
            return msg.content
    
    def scenic_desc_handle(self, user_input):
        """景区信息相关问题处理"""
        tools = [self.scenic_desc_tool.definition]
        return self._execute_single_tool_call(user_input, tools,self.scenic_desc_tool.definition)
        
    def create_order_handle(self, user_input):
        """创建订单相关问题处理"""
        tools = [self.create_order_tool.definition]
        return self._execute_single_tool_call(user_input, tools,self.create_order_tool.definition)
        
    def order_detail_handle(self, user_input):
        """订单详情相关问题处理"""
        tools = [self.order_detail_tool.definition]
        return self._execute_single_tool_call(user_input, tools,self.order_detail_tool.definition)

    def refund_handle(self, user_input):
        """退款相关问题处理"""
        tools = [self.order_detail_tool.definition,self.refund_detail_tool.definition,self.scenic_desc_tool.definition]
        # 关键：复制 history，在循环外初始化，循环内持续累积
        messages = list(self.history)
        messages.append({"role": "user", "content": user_input})
        
        executors = {
            "get_order_detail": self.order_detail_tool,
            "get_refund_amount": self.refund_detail_tool,
            "get_scenic_desc": self.scenic_desc_tool,
        }
        for i in range(5):
            msg, _ = self.llm.call(prompt=None, tools=tools, history=messages)
            messages.append(msg)
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    func_args = json.loads(tool_call.function.arguments)
                    func_name = tool_call.function.name
                    func = executors.get(func_name)

                    print(f"{func_name} agrs:{func_args}")
                    order_detail = func.execute(func_name, func_args)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": order_detail
                        }
                    )
            else:
                return msg.content
        return "抱歉，处理超时，请稍后重试"

    def extract_handle(self, user_input):
        """提取数据"""
        prompt = PromptBuilder.extract(user_input, self.EXTRACT_FIELDS)
        msg = self.llm.call(prompt=prompt, response_format=self.extract_json_schema, history=self.history)
        return json.loads(msg)
    
    def handle_chat(self, user_input):
        """闲聊处理"""
        msg, _ = self.llm.call(prompt=user_input, history=self.history)
        return msg.content
    
    def handle(self, intent, user_input):
        handlers = {
            "入园咨询": self.scenic_desc_handle,
            "售前咨询": self.scenic_desc_handle,
            "退票咨询": self.refund_handle,
            "改期咨询": self.scenic_desc_handle,
            "订单查询": self.order_detail_handle,
            "投诉建议": self.handle_chat,
            "紧急求助": self.scenic_desc_handle,
            "活动咨询": self.scenic_desc_handle,
            "创建订单": self.create_order_handle,
            "闲聊": self.handle_chat,
        }
        handler = handlers.get(intent, self.handle_chat)
        if handler:
            return handler(user_input)
        else:
            return "很抱歉，没能理解您的意思！"
        
    def dispatch(self, intent, user_input):
        if intent == "退票咨询":
            self.current_flow = "退票咨询"
            result = self.refund_handle(user_input)
            # 流程结束后清除状态
            if result and "退款" in result and ("元" in result or "成功" in result):
                self.current_flow = None
            return result
        else:
            return self.handle(intent=intent, user_input=user_input)

    def chat(self, user_input):
        # 如果有进行中的流程，直接继续，不重新分类
        if self.current_flow:
            intent = self.current_flow
        else:
            intent = self.classify_intent(user_input)
        result = self.dispatch(intent=intent, user_input=user_input)
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": result})
        return result