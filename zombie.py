#!/usr/bin/env python3
"""Кратковременный zombie; родитель всегда вызывает waitpid в finally."""
import os
import subprocess
import time

pid = os.fork()
if pid == 0:
    os._exit(0)
try:
    time.sleep(0.4)
    print(f'Ребёнок PID={pid} завершился, но ещё не был ожидаем:', flush=True)
    subprocess.run(['ps', '-o', 'pid,ppid,stat,cmd', '-p', str(pid)], check=False)
finally:
    os.waitpid(pid, 0)
print('waitpid вызван, zombie убран из таблицы процессов.')
