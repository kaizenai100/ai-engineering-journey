import json
from datetime import date
import os
from dotenv import load_dotenv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cot_practice.prompts import PromptBuilder
from commons.llm_client import OpenAIClient
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from cot_practice.tools import get_scenic_desc, get_order_detail, get_refund_amount, create_order



class CustomerAgent():
    """客服智能体，负责意图识别和任务分发，主要处理门票相关业务问题
    """

    EXTRACT_FIELDS = ["订单号", "景点名称"]
    def __init__(self):
        load_dotenv()
        today = date.today().strftime("%Y-%m-%d")
        self.current_flow = None  # 当前进行中的流程
        self.llm = OpenAIClient()
        self.get_scenic_desc = get_scenic_desc
        self.get_order_detail = get_order_detail
        self.get_refund_amount = get_refund_amount
        self.create_order = create_order
        self.history = [SystemMessage(f"""你是一个门票OTA平台的智能客服，你需要根据用户的意图进行智能处理，安抚用户的情绪并高质量的解决用户的问题。
            
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
            """)
        ]

    def classify_intent(self, user_input):
        """意图识别"""
        recent_history = self.history[-4:] if len(self.history) > 4 else self.history[1:]
        context = "\n".join(f"{m.type}: {m.content}" for m in recent_history if m.type != "system")
        messages = PromptBuilder.intent_prompt(user_input, context)
        return self.llm.call(messages)
    

    def _execute_single_tool_call(self, user_input, tools, tool_executes:list):
        """调 LLM → 解析 tool_call → 执行函数 → 回传结果 → 再调 LLM"""
        messages = list(self.history)
        messages.append(HumanMessage(user_input))
        return self.llm.func_call(history=messages, tools=tools, executes=tool_executes)
        
    
    def scenic_desc_handle(self, user_input):
        """景区信息相关问题处理"""
        tools = [self.get_scenic_desc]
        tool_executes = {"get_scenic_desc":self.get_scenic_desc}
        return self._execute_single_tool_call(user_input, tools,tool_executes)
        
    def create_order_handle(self, user_input):
        """创建订单相关问题处理"""
        tools = [self.create_order]
        tool_executes = {"create_order":self.create_order}
        return self._execute_single_tool_call(user_input, tools,tool_executes)
        
    def order_detail_handle(self, user_input):
        """订单详情相关问题处理"""
        tools = [self.get_order_detail]
        tool_executes = {"get_order_detail":self.get_order_detail}
        return self._execute_single_tool_call(user_input, tools,tool_executes)

    def refund_handle(self, user_input):
        """退款相关问题处理"""
        tools = [self.get_order_detail,self.get_refund_amount,self.get_scenic_desc]
        # 关键：复制 history，在循环外初始化，循环内持续累积
        messages = list(self.history)
        messages.append(HumanMessage(user_input))
        
        executors = {
            "get_order_detail": self.get_order_detail,
            "get_refund_amount": self.get_refund_amount,
            "get_scenic_desc": self.get_scenic_desc,
        }
        return self.llm.func_call(history=messages, tools=tools, executes=executors)
    
    def handle_chat(self, user_input):
        """闲聊处理"""
        messages = list(self.history)
        messages.append(HumanMessage(user_input))
        return self.llm.call(messages)
    
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
        print(f"意图：{intent}")
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
        self.history.append(HumanMessage(user_input))
        self.history.append(AIMessage(result))
        return result