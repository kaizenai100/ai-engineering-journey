from domain.order_info import OrderInfo
class ScenicDescTool:
    """景区说明工具，获取根据景区名称获取该景区的详细信息"""

    def get_scenic_desc(self, scenic_name):
        """从数据库中直接获取相关景区的描述信息，如果是模糊名称匹配到多个景区时，直接将所有景区信息返回给大模型，交由大模型去处理"""

        if scenic_name == "寒山寺":
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
        elif scenic_name == "拙政园":
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
    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": "get_scenic_desc",
                "description": "查询景区详细信息，包括景点介绍、门票价格、开放时间、景点地址、景点电话、景点门票使用条件、景点门票退换条件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scenic_name": {
                            "type": "string",
                            "description": "景点名称"
                        }
                    },
                    "required": ["scenic_name"]
                }
            }
        }
    def execute(self, func_name, func_args):
        mapping = {
            "get_scenic_desc": self.get_scenic_desc
        }
        return mapping[func_name](**func_args)



class CreateOrderTool:
    """创建订单"""

    def create_order(self, username, phone, scenic_name, travel_date, ticket_num):
        """获取景区的订单信息"""
        return "订单创建成功"
        
    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": "create_order",
                "description": "创建订单，需要提供用户名和手机号",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "用户名"
                        },
                        "phone": {
                            "type": "string",
                            "description": "用户手机号"
                        },
                        "scenic_name": {
                            "type": "string",
                            "description": "景区名称"
                        },
                        "travel_date": {
                            "type": "string",
                            "description": "出游日期，格式：yyyy-MM-dd"
                        },
                        "ticket_num": {
                            "type": "integer",
                            "description": "出游人数"
                        }
                    },
                    "required": ["username", "phone","scenic_name", "travel_date", "ticket_num"]
                }
            }
        }
    def execute(self, func_name, func_args):
        mapping = {
            "create_order": self.create_order
        }
        return mapping[func_name](**func_args)


class OrderDetailTool:
    """查询订单详细信息工具，根据订单号查询订单详细信息"""

    @staticmethod
    def get_order_info(order_id) -> OrderInfo:
        """获取景区的订单信息"""
        return OrderInfo(order_id,20,2,2,"预定成功","2026-02-01 10:00:00","2026-02-27","123456","寒山寺")
        

    def get_order_detail(self, order_id):
        """获取景区的订单详情"""
        print(f"正在查询订单号：{order_id}的订单详情")
        order_info = OrderDetailTool.get_order_info(order_id)
        return f"""
                订单号：{order_id}：
                支付金额：{order_info.pay_amount}元
                出游人数：{order_info.people_num}人
                景点名称：{order_info.scenic_name}
                订单状态：{order_info.order_flag_desc}
                订单创建时间：{order_info.create_time}
                出游时间：{order_info.travel_time}
                取票码：{order_info.ticket_code}
                """
    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": "get_order_detail",
                "description": "查询订单详细信息，包括订单号、支付金额、出游人数、景点名称、订单状态、订单创建时间、出游时间、取票码",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "订单号"
                        }
                    },
                    "required": ["order_id"]
                }
            }
        }
    def execute(self, func_name, func_args):
        mapping = {
            "get_order_detail": self.get_order_detail
        }
        return mapping[func_name](**func_args)


class RefundAmountTool:
    """计算退票金额"""

    def get_refund_amount(self, order_id, deduct_ratio):
        """获取可退金额"""
        order_info = OrderDetailTool.get_order_info(order_id)
        order_amount = order_info.pay_amount
        deduct_amount = order_amount * deduct_ratio
        return deduct_amount
    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": "get_refund_amount",
                "description": "查询订单可退金额，根据订单号和退票比例计算可退金额",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "订单号"
                        },
                        "deduct_ratio": {
                            "type": "number",
                            "description": "手续费比例，根据退改规则和出游日期获取手续费比例，例：出游前3天取消订单，收取50%的取消手续费，手续费比例就是0.5"
                        }
                    },
                    "required": ["order_id"]
                }
            }
        }
    def execute(self, func_name, func_args):
        mapping = {
            "get_refund_amount": self.get_refund_amount
        }
        return mapping[func_name](**func_args)
        

class RefundOrderTool:
    """申请退款"""

    def refund_order(self, order_id):
        """申请退款"""
        return f"已申请退款，订单号：{order_id}"
    
    def definition(self):
        return {
            "type":"function",
            "function":{
                "name":"refund_order",
                "description":"发起退款申请",
                "parameters":{
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "订单号"
                        }
                    },
                    "required": ["order_id"]
                }
            }

        }