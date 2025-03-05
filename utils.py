def unparse(data:bytes) -> list[str]:
    nb = data[0]
    elements = data[1+nb:]
    count = 1+nb
    out = []
    for i in range(nb):
        size = data[i+1]
        out.append(elements[count:count+size].decode("utf-8"))
        count += size
    return out

def parser(id:int,data:list[str]) -> bytes:
    prefix = [id]
    parsed_data = []
    prefix.append(len(data))
    for e in data:
        prefix.append(len(e))
        parsed_data.append(e.encode("utf-8"))
    return bytes(prefix)+b"".join(parsed_data)