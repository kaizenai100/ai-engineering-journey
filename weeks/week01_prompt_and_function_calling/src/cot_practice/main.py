from customer_agent import CustomerAgent

if __name__ == "__main__":
    customer_agent = CustomerAgent()
    while True:
        user_input = input("请输入：")
        result = customer_agent.chat(user_input)
        print(result)