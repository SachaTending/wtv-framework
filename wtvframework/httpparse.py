def parsehttp(d: str):
    d1 = d.split("\n")
    data: str = ""
    #print(d1[0])
    out = {
        "type": d1[0].removesuffix("\r").split(" ", 1)[0],
        "url": d1[0].removesuffix("\r").split(" ", 1)[1].split("?",1)[0],
        'headers': {},
        "data": ""
    }
    del d1[0]
    dataStart = False
    amogus = []
    # Skip headers, and get data
    for i in d1:
        if i == '\r' or i == '\r\n':
            dataStart = True # After headers is data
        elif dataStart:
            amogus.append(i.removesuffix("\r"))
        else:
            #print(i.split(":"))
            out['headers'][i.split(":", 1)[0]] = i.split(":", 1)[1].removeprefix(" ").removesuffix("\r")
    data = "\n".join(amogus)
    out['data'] = data
    return out
