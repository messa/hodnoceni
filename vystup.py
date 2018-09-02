#!/usr/bin/env python3

import json


def main():
    regs = load_regs()
    ev_data = load_evaluations()
    data = [(reg, ev_data[reg['id']]) for reg in regs]
    for reg, ev in data:
        score = 2 + sum(ev.values())
        print(','.join([
            #str(reg['id']),
            #reg['timestamp'],
            str(score),
            #' '.join('{}:{}'.format(k, v) for k, v in ev.items()),
        ]))



def load_regs():
    with open('registrace.json') as f:
        return json.load(f)


def load_evaluations():
    with open('evaluations.json') as f:
        ev_data = json.load(f)
    return {int(k): v for k, v in ev_data.items()}



if __name__ == '__main__':
    main()
