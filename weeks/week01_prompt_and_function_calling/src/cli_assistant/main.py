from assistant import Assistant

if __name__ == "__main__":
    assistant = Assistant()
    while True:
        user_input = input("请输入：")
        result = assistant.chat(user_input)
        print(result)