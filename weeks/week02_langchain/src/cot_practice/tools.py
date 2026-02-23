from domain.order_info import OrderInfo
from langchain_core.tools import tool

@tool
def get_scenic_desc(scenic_name: str) -> str:
    """从数据库中直接获取相关景区的描述信息"""
    if scenic_name == "寒山寺":
        return "寒山寺介绍..."
    elif scenic_name == "拙政园":
        return "拙政园介绍..."

@tool
def create_order(username: str, phone: str, scenic_name: str, travel_date: str, ticket_num: int) -> str:
    """创建订单"""
    return "订单创建成功"

@tool
def get_order_detail(order_id: str) -> str:
    """获取景区的订单详情"""
    print(f"正在查询订单号：{order_id}的订单详情")
    order_info = _get_order_info(order_id)
    return f"""
        订单号：{order_id}
        支付金额：{order_info.pay_amount}元
        出游人数：{order_info.people_num}人
        景点名称：{order_info.scenic_name}
        订单状态：{order_info.order_flag_desc}
        订单创建时间：{order_info.create_time}
        出游时间：{order_info.travel_time}
        取票码：{order_info.ticket_code}
    """

@tool
def get_refund_amount(order_id: str, deduct_ratio: float) -> float:
    """获取可退金额"""
    order_info = _get_order_info(order_id)
    return order_info.pay_amount * (1 - deduct_ratio)

@tool
def refund_order(order_id: str) -> str:
    """申请退款"""
    return f"已申请退款，订单号：{order_id}"

# 内部辅助函数，不暴露给 LLM
def _get_order_info(order_id: str) -> OrderInfo:
    return OrderInfo(order_id, 20, 2, 2, "预定成功", "2026-02-01 10:00:00", "2026-02-27", "123456", "寒山寺")