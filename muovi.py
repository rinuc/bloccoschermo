#!/usr/bin/env python3
"""
move_mouse_until.py
Sposta il mouse in modo casuale fino all’orario stabilito e,
al termine, tenta di bloccare lo schermo.

Dipendenze:
    pip install pyautogui

Su alcune distro/desktop X11 PyAutoGUI richiede anche:
    sudo apt install scrot python3-xlib python3-tk
"""

import datetime as dt
import random
import subprocess
import sys
import time

try:
    import pyautogui
except ImportError:
    sys.exit("‼  Devi prima installare pyautogui (pip install pyautogui).")

pyautogui.FAILSAFE = False           # disabilita il failsafe (angolo alto-sx)

def parse_time(t: str) -> dt.datetime:
    """Parsa l'input HH:MM e restituisce l'oggetto datetime target per oggi
    (o per domani se l'ora è già passata)."""
    try:
        h, m = map(int, t.strip().split(":"))
        now = dt.datetime.now()
        target = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if target <= now:
            target += dt.timedelta(days=1)
        return target
    except Exception:
        sys.exit("Formato ora non valido: usa HH:MM (es. 18:45)")

def random_move():
    """Piccolo spostamento casuale del cursore."""
    dx = random.randint(-100, 100)
    dy = random.randint(-100, 100)
    duration = random.uniform(0.05, 0.3)
    pyautogui.moveRel(dx, dy, duration)

def lock_screen() -> bool:
    """Prova una serie di comandi di lock; restituisce True se uno funziona."""
    commands = [
        ("gnome-screensaver-command", "-l"),
        ("xdg-screensaver", "lock"),
        ("loginctl", "lock-session"),
        ("dm-tool", "lock"),
    ]
    for cmd in commands:
        try:
            subprocess.run(cmd, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False

def main():
    target_input = input("Fino a che ora vuoi muovere il mouse? (HH:MM) ➜ ")
    target_time = parse_time(target_input)
    print(f"Inizio a muovere il mouse fino alle {target_time.strftime('%H:%M')}...")
    try:
        while dt.datetime.now() < target_time:
            random_move()
            time.sleep(random.uniform(5, 20))   # aspetta 5-20 s
    except KeyboardInterrupt:
        print("\nInterrotto manualmente.")
        sys.exit(0)

    print("⌛ Orario raggiunto, provo a bloccare lo schermo...")
    if lock_screen():
        print("✅ Schermo bloccato.")
    else:
        print("⚠  Non sono riuscito a bloccare lo schermo: fallo manualmente.")

if __name__ == "__main__":
    main()
