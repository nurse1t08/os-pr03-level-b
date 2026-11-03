#!/usr/bin/env python3
"""Copy-on-write после fork: RSS вместе с Private_Dirty из smaps_rollup."""
from pathlib import Path
import argparse
import os
import sys


def fields():
    result = {}
    for filename in ('/proc/self/status', '/proc/self/smaps_rollup'):
        try:
            for line in Path(filename).read_text().splitlines():
                key, colon, val = line.partition(':')
                if colon and key in ('VmRSS', 'Rss', 'Pss', 'Private_Dirty'):
                    result[key] = val.strip()
        except OSError:
            pass
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mb', type=int, default=64)
    args = parser.parse_args()
    if args.mb <= 0:
        parser.error('--mb должен быть положительным')
    buffer = bytearray(args.mb * 1024 * 1024)
    for i in range(0, len(buffer), 4096):
        buffer[i] = 1  # создаём физические страницы
    print('Родитель до fork:', fields(), flush=True)
    pid = os.fork()
    if pid == 0:
        try:
            print('Ребёнок сразу после fork:', fields(), flush=True)
            for i in range(0, len(buffer), 4096):
                buffer[i] = 2  # требует собственных COW-страниц
            print('Ребёнок после изменения:', fields(), flush=True)
        finally:
            os._exit(0)
    os.waitpid(pid, 0)
    print('Родитель после wait:', fields(), flush=True)


if __name__ == '__main__':
    main()
