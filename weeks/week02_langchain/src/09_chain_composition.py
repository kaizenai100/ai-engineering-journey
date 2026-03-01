from langchain_core.output_parsers import StrOutputParser, JsonOutputParser, PydanticOutputParser
from commons.configs import Configs
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableBranch
from pydantic import BaseModel, Field
from cot_practice.prompts import PromptBuilder
import os
from dotenv import load_dotenv

def get_llm():
    load_dotenv()
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-5.2"),
        temperature=0.0,
        max_tokens=1024,
        base_url=os.environ["OPENAI_BASE_URL"],
        default_headers=Configs.IKUN_API_HEADERS
    )


def get_scenic_desc(query:str) -> str:
    """从数据库中直接获取相关景区的描述信息，如果是模糊名称匹配到多个景区时，直接将所有景区信息返回给大模型，交由大模型去处理"""

    print(f"景区：{query}")
    if query == "寒山寺":
        return f"""
            寒山寺介绍：
            票价：10元/人
            特惠政策
            【免费政策】
                身高1.4米（含）以下；
                老人：65岁(含）以上（凭身份证）；
                特殊人群：现役军人、退役军人（凭有效证件）、消防救援人员、皈依证、医务人员免费（仅限每年8月19日中国医师节、5月12日国际护士节当天起7日内免票）
                【优惠政策】
                全日制大学本科及以下学历在校生凭有效证件；
                老人：60（含）-64（含）周岁（凭身份证）。
            注：上述优惠政策需至景区自行购买。

            以上信息仅供参考，具体以景区公示为准。

            温馨提示
            ①预订票型包含寺内景点有:大雄宝殿，寒山铜钟，寒拾殿，碑廊等；
            ②本产品仅限成人预订，儿童请至景区购买。景区统一限购，每个手机号码每天至多可订3张，如需预订更多，请更换手机号码预订；
            ③景区严禁带宠物入园，请严格遵守，谢谢；
            ④购票优待政策的游客需主动出示有效证件，享受免票政策的游客请持有效证件直接到检票口验证入园；
            ⑤大雄宝殿每天参观时间：8:00-16:00 ,如遇特殊情况，根据现场实际情况执行。
            ⑥景区大门票不包含寺内敲钟项目。

            景区紧急联系电话：400-888-6666

            退改规则：
            1.出游前7天取消订单，不收取取消手续费。
            2.出游前3天取消订单，收取50%的取消手续费。
            3.出游当日取消订单，收取80%的取消手续费。
            4.过出游日期后取消，收取100%的取消手续费。

            改期规则：门票一经售出，不支持改期，如需改期可先申请退票后重新购买。
        
            """
    elif query == "拙政园":
        return f"""
            拙政园介绍：
                票价：30元/人
                特惠政策
                【免费政策】
                ①儿童：身高1.4米（含）以下，或6周岁（含）以下，凭有效证件免费入园；
                ②老人：年龄70周岁（含）以上，凭有效居民身份证或《高龄证》免费入园；
                ③军人：中华人民共和国现役军人凭军人证等有效证件、退役军人、军队离退休干部凭离退休干部证免费入园；
                ④残疾人：残疾人员凭《残疾证》免费入园，重度残疾人员需要陪护的，可由一名陪护人员免费陪同入园。
                【优待政策】
                ①儿童：6周岁（不含）-18周岁（含），凭身份证/户口本等有效证件半价；
                ②学生：全日制大学本科及以下学历在校学生，凭居民身份证/学生证等有效证件半价；
                ③老人：60周岁（含）-70周岁（不含），凭有效居民身份证或《老年人优待证》半价；
                ④其他：法律、法规规定的其他门票价格优惠政策。
                请凭预留身份证至检票处刷身份证验证后方可入园（需携带有效证件进行核验），请按照预约时间段入园。
                以上信息仅供参考，具体以景区公示为准。
                温馨提示
                【温馨提示】

                每年3月1日-10月31日：07:30开始检票入园，17:00停止检票入园，17:30开始清园；其中清明、五一、中秋、十一期间延迟半小时闭园，18:00闭园。

                每年11月1日-次年2月底：07:30开始检票入园，16:30停止检票入园，17:00开始清园。

                游客游览需提前网上预约购票，请携带本人身份证等有效证件验证入园。已开通支付宝功能的购票游客也可选择人脸识别审核入园。
                【预订须知】

                1.游客必须填写本人有效身份证件，实名预约景区门票。

                2.网络预订票最早可提前7日购票，预定门票一经使用不可退订；网络门票预订成功后，不得改期；如需改期，请申请取消订单后重新预订。请勿在多个平台重复购票。

                3.游览日前一日24:00前退票，不计爽约；游览当日预约时段后退票记爽约一次，一周内累计爽约2次，从第2次爽约的次日起，30日内将无法预约门票。

                4.为保证入园顺利，预订时请务必填写入园游览者真实姓名、身份证号、手机号码等信息，游客需持本人有效证件验证入园。

                5.如需开具景区发票（包含联票），请至各景区售票窗口登记。如已离开，请联系客服登记开票信息，景区开具电子发票发送至游客邮箱。

                6.未使用的门票可随时申请退款。

                7.如有问题，请至景区综合服务窗口咨询。

                8.【优惠对象】无需购票，凭本人相关有效证件验证入园。

                ①中华人民共和国现役军人凭军人证等有效证件、军队离退休干部凭离退休干部证免费入园。

                ②退役军人和其他优抚对象凭中华人民共和国退役军人优待证、中华人民 共和国烈士、因公牺牲军人、病故军人遗属优待证，免费参观游览苏州园林景区，园中园、园内收费及夜游项目除外。

                ③残疾人员凭残疾证免费入园，重度残疾人员需要陪护的，可由一名陪护人员免费陪同入园。

                ④70周岁（含70周岁）以上老人，凭有效居民身份证或高龄证免费入园。

                ⑤身高1.4米（含1.4米）以下，6周岁（含6周岁）以下儿童，免费入园。

                ⑥法律、法规规定的其他门票价格优惠政策。

                【入园方式】

                1.购买全价票的游客，刷本人身份证或者人脸识别审核入园；

                2.购买半价票与优惠对象预约票的游客，请出示相关有效证件，景区审核通过后，刷本人身份证或者人脸识别审核入园。

                最佳游玩时间
                四季皆宜

                景区旺季：4月、5月、7月、8月、9月、10月，淡季：1月、2月、3月、6月、11月、12月

                游览推荐：3-5月杜鹃花展览，6月上旬-10月中旬荷花展，9-10月菊花展（具体活动以为景区实时公布为准）

                建议游玩时长
                2-3小时

                景区紧急联系电话：400-888-8888

            退改规则：
                1.出游前7天取消订单，不收取取消手续费。
                2.出游前3天取消订单，收取50%的取消手续费。
                3.出游当日取消订单，收取80%的取消手续费。
                4.过出游日期后取消，收取100%的取消手续费。

            改期规则：门票一经售出，不支持改期，如需改期可先申请退票后重新购买。
                """

def extract_keywords(query:str) -> str:
    llm = get_llm() 
    prompt = ChatPromptTemplate.from_template("""从以下文本中提取关键字信息信息。
    文本：{query}

    举例：
    上海的天气怎么样 输出=>上海
    拙政园今天开园吗 输出=>拙政园
    上海的景点有哪些 输出=>上海

    只返回一个关键词就可以了。""")
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"query": query})
    print(f"关键词：{result}")
    return result


def logger(query:str):
    print(f"query={query}")
    return query


def runnable_passthrough(query):
    llm = get_llm() 
    prompt = ChatPromptTemplate.from_template("请根据上下文回答问题：{query}\n上下文：{context}")
    chain = (RunnablePassthrough.assign(keywords=extract_keywords) 
             | RunnablePassthrough.assign(context=lambda k:get_scenic_desc(k["keywords"]))
             | prompt | llm | StrOutputParser())

    return chain.invoke({"query": query})



def classify_intent(query:str) -> str:
    """意图识别"""
    messages = PromptBuilder.intent_prompt(input_text=query, context='')
    llm = get_llm()
    return llm.invoke(messages).content

def runnable_lambda(query):
    llm = get_llm() 
    prompt = ChatPromptTemplate.from_template("请根据上下文回答问题：{query}\n上下文：{context}")
    chain = (RunnableLambda(logger) | RunnablePassthrough.assign(keywords=lambda k: extract_keywords(k["query"])) 
             | RunnableLambda(logger) | RunnablePassthrough.assign(context=lambda k:get_scenic_desc(k["keywords"]))
             | RunnableLambda(logger) | prompt | llm | StrOutputParser())

    return chain.invoke({"query": query})

def runnable_branch(query):
    prompt = ChatPromptTemplate.from_template(
        "请根据上下文回答问题：{query}\n上下文：{context}"
    )
    llm = get_llm()

    # 查票价/攻略链
    info_chain = (
        RunnablePassthrough.assign(keywords=lambda k: extract_keywords(k["query"]))
        | RunnablePassthrough.assign(context=lambda k: get_scenic_desc(k["keywords"]))
        | prompt | llm | StrOutputParser()
    )

    # 闲聊兜底链
    chat_prompt = ChatPromptTemplate.from_template("你是一个友好的旅游助手，请回答：{query}")
    chat_chain = chat_prompt | llm | StrOutputParser()

    branch = RunnableBranch(
        (lambda x: "入园咨询" in x["intent"], info_chain),
        (lambda x: "票价" in x["intent"], info_chain),
        chat_chain  # 兜底
    )

    chain = RunnablePassthrough.assign(intent=lambda x: classify_intent(x["query"])) | branch
    return chain.invoke({"query": query})
if __name__ == "__main__":
    print(runnable_branch("寒山寺票价"))
