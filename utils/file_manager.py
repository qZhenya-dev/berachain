
def txt_to_list(name):
    resp = []

    try:
        with open(f"data/{name}.txt", "r", encoding="utf-8") as f:
            resp = f.read().split("\n")
    except:
        pass

    return [item for item in resp if item]

def append_to_txt(name, message):
    with open(f"data/{name}.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

