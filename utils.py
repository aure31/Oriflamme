def unparse(data:bytes) -> tuple[int,list[str]]:
    print("unparse : in ",data)
    id = data[0]
    nb = data[1]
    elements = data[2+nb:]
    count = 0
    out = []
    for i in range(nb):
        size = data[i+2]
        out.append(elements[count:count+size].decode("utf-8"))
        count += size
    return id,out

def parser(id:int,data:list[str]) -> bytes:
    print("parser : ",data)
    prefix = [id]
    parsed_data = []
    prefix.append(len(data))
    for e in data:
        prefix.append(len(e))
        parsed_data.append(e.encode("utf-8"))
    return bytes(prefix)+b"".join(parsed_data)


def test():
    print("parser : out : ",parser(0,["test","test2"]))
    print(unparse(parser(0,["test","test2"])))

#test()