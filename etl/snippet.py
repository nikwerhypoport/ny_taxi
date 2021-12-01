import random
from typing import Dict, Set


def seq_gen(n):
     l = list(range(1, n+1))
     l.append(random.choice(l))
     random.shuffle(l)
     return l


if __name__ == '__main__':
    result_list = seq_gen(2)

    counter: Set = set()
    for entry in result_list:

        if entry in counter:
            print(entry)
            break

        counter.add(entry)
