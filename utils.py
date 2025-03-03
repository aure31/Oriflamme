def unparse(data:bytes) -> list[str]:
    i=0
    sizes = []
    while data[i] != 0b0:
        sizes.append(data[i])
        i+=1
    i+=1
    data = data[i:]
    count = 0
    out = []
    for e in sizes:
        out.append(data[count:count+e].decode("utf-8"))
        count += e
    return out

def parser(id:int,data:list[str]) -> bytes:
    prefix = [id]
    data = []
    for e in data:
        prefix.append(len(e))
        data.append(e.encode("utf-8"))
    prefix.append(0)
    return bytes(prefix)+b"".join(data)