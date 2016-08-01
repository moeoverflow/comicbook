import random

def getRandomUA(uafile="user_agents.txt"):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)

    return uas[random.randint(0, len(uas))]
