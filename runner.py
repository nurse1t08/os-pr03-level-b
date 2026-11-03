#!/usr/bin/env python3
"""N дочерних процессов: fork + execvp; родитель ожидает каждый."""
import argparse
import os
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', '-n', type=int, default=3)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    cmd = args.command
    if cmd and cmd[0] == '--':
        cmd = cmd[1:]
    if args.count < 1 or not cmd:
        parser.error('нужны --count N и команда: --count 3 -- sleep 2')
    started = {}
    for i in range(args.count):
        now = time.monotonic()
        pid = os.fork()
        if pid == 0:
            try:
                os.execvp(cmd[0], cmd)
            except OSError as exc:
                print(f'Ошибка exec: {exc}', file=__import__('sys').stderr, flush=True)
                os._exit(127)
        started[pid] = now
        print(f'Запущен дочерний процесс {i+1}: PID={pid}', flush=True)
    while started:
        pid, status = os.wait()
        elapsed = time.monotonic() - started.pop(pid)
        code = os.waitstatus_to_exitcode(status)
        print(f'PID={pid} code={code} elapsed={elapsed:.3f} с', flush=True)


if __name__ == '__main__':
    main()
