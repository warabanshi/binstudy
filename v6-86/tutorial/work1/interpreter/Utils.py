def convNum(byteList, byteNum):
    if len(byteList) < byteNum:
        return 0

    result = 0
    for i in range(byteNum):
        result = (result << 8) | ord(byteList[i])

    return result
