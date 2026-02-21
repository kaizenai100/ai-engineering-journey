def format_number(number: int) -> str:
    if number > 0 and number < 100:
        return "50+"
    elif number >= 100 and number < 1000:
        return f"{(number / 100) * 100}+"
    elif number >= 1000 and number < 10000:
        if number % 1000 == 0:
            return str(number / 1000) + "千+"
        return f"{number / 1000:.1f}千+"
    elif number >= 10000 and number < 1000000:
        if number % 10000 == 0:
            return str(number / 10000) + "万+"
        return f"{number / 10000:.1f}万+"
    elif number >= 1000000:
        return "100万+"
    else:
        return ""
    
if __name__ == "__main__":
    print(format_number(100))
    print(format_number(1000))
    print(format_number(10000))
    print(format_number(100000))
    print(format_number(1000000))
    print(format_number(10000000))
    print(format_number(100000000))
    print(format_number(1000000000))