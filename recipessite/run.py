#!/usr/bin/env python

"""
Desktop launcher for recipessite (SQLite) with GUI.

Окно с кнопкой Stop и терминалом. Закрытие окна корректно
останавливает Django runserver. Запускается из loader.exe.
"""

import os
import sys
import queue
import threading
import time
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

import tkinter as tk
from tkinter import ttk

HOST = '127.0.0.1'
PORT = 8000
URL = f'http://{HOST}:{PORT}/'

RUN_MIGRATE = os.getenv('RUN_MIGRATE', '0') == '1'

server_process = None


def get_base_dir() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent


def setup_environment(base_dir: Path):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipessite.settings')
    os.environ['DESKTOP_MODE'] = '1'
    if str(base_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))


def create_window():
    root = tk.Tk()
    root.title("recipessite Desktop Launcher")
    root.geometry("900x560")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(main_frame, text="🍳 recipessite", font=("Arial", 15, "bold"))
    title_label.pack(anchor=tk.W, pady=(0, 8))

    control_frame = ttk.Frame(main_frame)
    control_frame.pack(fill=tk.X, pady=(0, 8))

    status_label = tk.Label(control_frame, text="Starting...", font=("Arial", 10))
    status_label.pack(side=tk.LEFT, padx=(0, 10))

    url_label = tk.Label(control_frame, text=URL, font=("Arial", 10), fg="blue", cursor="hand2")
    url_label.pack(side=tk.LEFT, padx=(0, 10))
    url_label.bind("<Button-1>", lambda e: webbrowser.open(URL))
    url_label.config(state="disabled")

    progress_bar = ttk.Progressbar(control_frame, mode='indeterminate', length=150)
    progress_bar.pack(side=tk.LEFT, padx=(0, 10))
    progress_bar.start()

    terminal_frame = ttk.LabelFrame(main_frame, text="Terminal Output", padding="5")
    terminal_frame.pack(fill=tk.BOTH, expand=True)

    terminal_text = tk.Text(terminal_frame, wrap=tk.WORD, font=("Consolas", 9),
                            bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
                            relief=tk.FLAT, borderwidth=0,
                            selectbackground="#264f78", selectforeground="white")
    terminal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(terminal_frame, orient=tk.VERTICAL, command=terminal_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    terminal_text.config(yscrollcommand=scrollbar.set)

    terminal_text.tag_configure("INFO", foreground="#4ec9b0")
    terminal_text.tag_configure("ERROR", foreground="#f48771")
    terminal_text.tag_configure("WARNING", foreground="#ce9178")
    terminal_text.tag_configure("SUCCESS", foreground="#6a9955")

    is_shutting_down = False

    def append_to_terminal(message, tag="INFO"):
        def _append():
            terminal_text.insert(tk.END, message, tag)
            terminal_text.see(tk.END)
            terminal_text.yview_moveto(1.0)

        root.after(0, _append)

    def update_status(text, enable_url=False, stop_progress=False):
        def _update():
            status_label.config(text=text)
            if enable_url:
                url_label.config(state="normal")
            if stop_progress:
                progress_bar.stop()
                progress_bar.pack_forget()

        root.after(0, _update)

    def shutdown_app():
        nonlocal is_shutting_down
        if is_shutting_down:
            return
        is_shutting_down = True

        append_to_terminal("\n" + "=" * 50 + "\n", "INFO")
        append_to_terminal("🛑 Shutting down...\n", "WARNING")
        append_to_terminal("=" * 50 + "\n", "INFO")

        global server_process
        if server_process and server_process.poll() is None:
            append_to_terminal("Stopping Django...\n", "INFO")
            try:
                server_process.terminate()
                server_process.wait(timeout=5)
            except Exception:
                try:
                    server_process.kill()
                except Exception:
                    pass

        append_to_terminal("✅ Shutdown complete\n", "SUCCESS")
        try:
            root.destroy()
        except Exception:
            pass
        os._exit(0)

    stop_button = tk.Button(control_frame, text="Stop", command=shutdown_app,
                            bg="#ff4444", fg="white", padx=20, pady=4)
    stop_button.pack(side=tk.RIGHT)
    stop_button.config(state="disabled")

    root.protocol("WM_DELETE_WINDOW", shutdown_app)

    startup_queue = queue.Queue()

    def run_startup():
        base_dir = get_base_dir()
        setup_environment(base_dir)

        logs_dir = base_dir / 'logs'
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_path = logs_dir / f'recipessite_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        log_file = open(log_path, 'w', encoding='utf-8', buffering=1)

        append_to_terminal(f"Base dir: {base_dir}\n")
        append_to_terminal(f"Log file: {log_path}\n")

        if RUN_MIGRATE:
            append_to_terminal("Applying migrations...\n")
            r = subprocess.run(
                [sys.executable, 'manage.py', 'migrate', '--noinput'],
                cwd=str(base_dir), capture_output=True, text=True,
            )
            log_file.write(r.stdout or '')
            log_file.write(r.stderr or '')
            log_file.flush()
            if r.returncode != 0:
                append_to_terminal("❌ migrate failed\n", "ERROR")
                startup_queue.put("STARTUP_FAILED")
                return
            append_to_terminal("✅ migrations applied\n", "SUCCESS")

        cmd = [
            sys.executable, '-m', 'django', 'runserver',
            '--noreload', f'{HOST}:{PORT}',
        ]

        creationflags = 0
        if sys.platform == 'win32':
            creationflags = 0x08000000  # CREATE_NO_WINDOW

        append_to_terminal(f"Starting: {' '.join(cmd)}\n")
        log_file.write(f"Starting: {' '.join(cmd)}\n")
        log_file.flush()

        global server_process
        try:
            server_process = subprocess.Popen(
                cmd,
                cwd=str(base_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                creationflags=creationflags,
                text=True,
                encoding='utf-8',
                errors='replace',
            )
        except Exception as e:
            append_to_terminal(f"❌ Failed to start runserver: {e}\n", "ERROR")
            log_file.write(f"Failed to start runserver: {e}\n")
            startup_queue.put("STARTUP_FAILED")
            return

        def pump_output(proc, log):
            for line in iter(proc.stdout.readline, ''):
                if line:
                    log.write(line)
                    log.flush()
                    tag = "ERROR" if ('Error' in line or 'Traceback' in line) else "INFO"
                    append_to_terminal(line, tag)

        threading.Thread(target=pump_output, args=(server_process, log_file), daemon=True).start()

        time.sleep(2.0)
        try:
            webbrowser.open(URL)
        except Exception:
            pass

        append_to_terminal(f"\n✅ SERVER READY! {URL}\n", "SUCCESS")
        startup_queue.put("SERVER_READY")

    threading.Thread(target=run_startup, daemon=True).start()

    def check_queue():
        try:
            msg = startup_queue.get_nowait()
            if msg == "SERVER_READY":
                update_status("Running", enable_url=True, stop_progress=True)
                stop_button.config(state="normal")
            elif msg == "STARTUP_FAILED":
                update_status("Failed!", stop_progress=True)
                stop_button.config(state="normal")
        except queue.Empty:
            pass
        finally:
            root.after(100, check_queue)

    root.after(100, check_queue)
    root.mainloop()


def main():
    try:
        create_window()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        global server_process
        if server_process and server_process.poll() is None:
            try:
                server_process.terminate()
                server_process.wait(timeout=5)
            except Exception:
                try:
                    server_process.kill()
                except Exception:
                    pass


if __name__ == '__main__':
    main()