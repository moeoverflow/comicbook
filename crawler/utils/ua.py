import random
import os


def get_random_ua(uafile=os.path.dirname(os.path.abspath(__file__))+"/user_agents.txt"):
    uas = []
    with open(uafile, 'r') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)

    return uas[random.randint(0, len(uas)-1)]
