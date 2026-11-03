#!/usr/bin/env python3
"""Дерево процессов своего UID через /proc (не вызываем ps). Linux only."""
from pathlib import Path
import os


def processes():
    found = {}
    for p in Path('/proc').iterdir():
        if not p.name.isdigit():
            continue
        try:
            info = {}
            for line in (p / 'status').read_text().splitlines():
                key, sep, value = line.partition(':')
                if sep:
                    info[key] = value.strip()
            if int(info['Uid'].split()[0]) != os.getuid():
                continue
            found[int(p.name)] = {
                'ppid': int(info['PPid']),
                'name': info.get('Name', '?'),
                'state': info.get('State', '?'),
                'rss': info.get('VmRSS', '0 kB'),
            }
        except (FileNotFoundError, ProcessLookupError, PermissionError, KeyError, ValueError):
            continue  # процесс мог завершиться между чтениями
    return found


def main():
    if not Path('/proc').is_dir():
        raise SystemExit('Эта программа требует Linux с /proc (например, Ubuntu).')
    items = processes()
    children = {}
    for pid, item in items.items():
        children.setdefault(item['ppid'], []).append(pid)
    def show(pid, depth=0):
        p = items[pid]
        print(f"{'  '*depth}{pid} {p['name']} | {p['state']} | RSS={p['rss']}")
        for child in sorted(children.get(pid, [])):
            show(child, depth + 1)
    for pid in sorted(items):
        if items[pid]['ppid'] not in items:
            show(pid)


if __name__ == '__main__':
    main()
