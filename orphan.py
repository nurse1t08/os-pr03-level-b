#!/usr/bin/env python3
"""Наблюдение смены PPID у сироты в Linux. Ребёнок завершится сам."""
import os
import time

pid = os.fork()
if pid:
    print(f'Родитель PID={os.getpid()}, ребёнок PID={pid}; родитель завершается', flush=True)
    os._exit(0)
original = os.getppid()
time.sleep(1)
print(f'Ребёнок PID={os.getpid()}: PPID до={original}, после={os.getppid()}', flush=True)
time.sleep(1)
