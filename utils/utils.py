clientBoundList = []
ServerBoundList = []

def unparse(data:bytes,clientbound:bool) -> list[tuple[int,list[str]]]:
    result = []
    while len(data) > 0:
        if clientbound and clientBoundList[data[0]]:
            taille = 2+sum(data[2:2+data[1]])+data[1]
            result.append(one_unparse(data[:taille]))
            data = data[taille:]
        elif clientbound and not clientBoundList[data[0]]:
            result.append(one_unparse(data[:1]))
            data = data[1:]
        elif not clientbound and ServerBoundList[data[0]]:
            taille = 2+sum(data[2:2+data[1]])+data[1]
            result.append(one_unparse(data[:taille]))
            data = data[taille:]
        elif not clientbound and not ServerBoundList[data[0]]:
            result.append(one_unparse(data[:1]))
            data = data[1:]
    return result

def one_unparse(data:bytes) -> tuple[int,list[str]]:
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