def unparse(data:bytes) -> tuple[int,list[str]]:
    print("unparse : in ",data)
    id = data[0]
    if len(data) == 1:
        return id,[]
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
        encode = e.encode("utf-8")
        prefix.append(len(encode))
        parsed_data.append(encode)
    return bytes(prefix)+b"".join(parsed_data)


def test():
    print("parser : out : ",parser(0,["test","test2"]))
    print(unparse(parser(0,["test","test2"])))

#test()