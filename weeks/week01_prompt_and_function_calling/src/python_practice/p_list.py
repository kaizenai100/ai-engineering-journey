def list_derivation():
    """
    range params:left close right open
    """
    list = [x*2 for x in range(5,15)]
    for num in list:
        print(num)  

if __name__ == "__main__":
    list_derivation()
