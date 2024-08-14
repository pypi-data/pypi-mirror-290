def READ_API(BotUserName,filie_path=r"D:\downloads\Python\Projects\Secrets\TelebotApiKeys.txt"):
    with open(filie_path) as f:
        apikeys=f.readlines()
    for line in apikeys:
        line=line.rstrip()
        if BotUserName==line.split("~")[0]:
            return line.split("~")[1]