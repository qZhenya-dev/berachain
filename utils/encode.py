
def byte64(text=""):
    text = str(text).replace("0x", "")
    return ("0" * (64 - len(str(text)))) + str(text) if text else "0"*64

def get_data_byte64(func, *args):
    data = str(func)
    for arg in args:
        data += byte64(arg)

    return data



