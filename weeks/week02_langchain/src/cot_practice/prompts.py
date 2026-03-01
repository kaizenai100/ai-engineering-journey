from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.messages.base import BaseMessage

class PromptBuilder:
    @staticmethod
    def intent_prompt(input_text, context:None) -> list[BaseMessage]:
        context_block = f"\n最近对话记录：\n{context}\n" if context else ""
        return [
            SystemMessage(content="""你是意图分类器。
                            你的唯一任务是从给定选项中选择一个意图并返回。
                            严格规则：
                            - 只返回意图名称本身
                            - 不能有任何其他文字、标点、解释
                            - 必须从选项中选择，不能创造新意图"""
                          ),
            HumanMessage(content=f"""
                            {context_block}

                            用户输入：{input_text}

                            可选意图（只能从以下选项中选择一个）：
                            - 入园咨询：开放时间、携带物品、停车、交通路线等
                            - 售前咨询：票价、票种区别、优惠政策、儿童身高限制等
                            - 创建订单：根据提供信息创建订单
                            - 退票咨询：退款规则、退款金额、退款进度等
                            - 改期咨询：是否能改期、差价补扣、改期截止时间等
                            - 订单查询：订单状态、取票码、发票申请等
                            - 投诉建议：体验投诉、服务投诉、设施问题等
                            - 紧急求助：景区内走失、受伤、紧急联系等
                            - 活动咨询：当前促销活动、节假日特惠、会员权益等
                            - 闲聊：无法归类到以上意图的内容

                            注意：
                            1. 只返回意图名称，不要解释，不要加标点符号
                            2. 必须从以上选项中选择，不能返回其他内容
                            3. 如果无法判断，返回"闲聊"

                            示例：
                            用户输入：我买的票能退吗
                            返回：退票咨询

                            用户输入：明天几点开门
                            返回：入园咨询

                            用户输入：我在景区里迷路了
                            返回：紧急求助
                            """
                         )
        ]


    @staticmethod
    def extract_prompt(input_text, fields) -> HumanMessage:
        return HumanMessage(content=f"""从以下文本中提取信息，以JSON的格式返回。
    文本：{input_text}

    需要提取的字段：{fields}
只返回JSON格式的 字符串，不要其他内容，返回结果可以通过json.loads()函数解析成字典。"""
        )