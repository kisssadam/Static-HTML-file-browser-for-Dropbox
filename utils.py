def sizeof_fmt(num):
    """
    Convert file size to human readable format.
    """
    if num == "-":
        return num

    num = float(num)
    for x in ['bytes','KB','MB','GB','TB',"PB","EX"]:
        if num < 1024.0 and x == 'bytes':
            return int(num)
        elif num < 1024.0:
            return "{0:.2f}&nbsp;{1}".format(num, x)
        num /= 1024.0
