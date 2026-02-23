class OrderInfo:
    def __init__(self, order_id: str, pay_amount: float, people_num: int, order_flag: int, order_flag_desc: str, 
                 create_time: str, travel_time: str, ticket_code: str, scenic_name: str):
        self.order_id = order_id
        self.pay_amount = pay_amount
        self.people_num = people_num
        self.order_flag = order_flag
        self.order_flag_desc = order_flag_desc
        self.create_time = create_time
        self.travel_time = travel_time
        self.ticket_code = ticket_code
        self.scenic_name = scenic_name