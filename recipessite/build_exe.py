#!/usr/bin/env python

"""
Build script for recipessite.exe - маленький загрузчик, который запускает Python из venv.

Адаптировано под проект recipessite:
- БД SQLite (db.sqlite3), PostgreSQL НЕ бандлится;
- venv лежит в PROJECT_ROOT.parent / '.venv' (или PROJECT_ROOT / '.venv');
- копируются: manage.py, run.py, recipessite/, recipes/, users/, templates/,
  static/, media/, db.sqlite3, .env, requirements.txt;
- collectstatic по умолчанию ОТКЛЮЧЁН (в settings.py STATIC_ROOT = BASE_DIR/'static/',
  чтобы не затереть исходную static/). При необходимости: --with-static.
"""

import argparse
import os
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / 'dist'
BUILD_DIR = PROJECT_ROOT / 'build'
EXE_NAME = 'recipessite'


def remove_readonly(func, path, excinfo):
    """Remove read-only attribute from files."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def play_sound(success=True, enabled=True):
    """Play sound notification when build completes."""
    if not enabled:
        return
    try:
        if sys.platform == 'win32':
            import winsound
            if success:
                winsound.Beep(800, 500)
                winsound.Beep(1000, 300)
            else:
                winsound.Beep(400, 300)
                winsound.Beep(300, 300)
        else:
            print('\a' * 3, end='', flush=True)
    except Exception as e:
        print(f"  Could not play sound: {e}")


def _progress(copied, total, start_time, prefix=''):
    """Ручной прогресс-бар (fallback без tqdm)."""
    if total <= 0:
        return
    elapsed = max(time.time() - start_time, 1e-6)
    percent = (copied / total) * 100
    speed = copied / elapsed
    eta_seconds = (total - copied) / speed if speed > 0 else 0
    if eta_seconds < 60:
        eta_str = f"{eta_seconds:.0f} сек"
    elif eta_seconds < 3600:
        eta_str = f"{eta_seconds // 60:.0f} мин {eta_seconds % 60:.0f} сек"
    else:
        eta_str = f"{eta_seconds // 3600:.0f} ч {(eta_seconds % 3600) // 60:.0f} мин"
    bar_length = 30
    filled = int(bar_length * copied // total)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(
        f"\r   {prefix}[{bar}] {copied}/{total} ({percent:.1f}%) | "
        f"{elapsed:.0f}с прошло | осталось: {eta_str} | {speed:.0f} файлов/сек",
        end='', flush=True,
    )


def _resolve_paths(args):
    """Резолвит путь к venv из аргументов/env с фолбэками."""
    if args.venv:
        venv = Path(args.venv)
    elif os.environ.get('VENV_DIR'):
        venv = Path(os.environ['VENV_DIR'])
    else:
        candidates = [
            PROJECT_ROOT.parent / '.venv',
            PROJECT_ROOT / '.venv',
            PROJECT_ROOT.parent / 'venv',
            PROJECT_ROOT / 'venv',
        ]
        venv = next((c for c in candidates if c.exists()), candidates[0])
    return venv


def check_prerequisites(args, venv):
    """Проверяет предусловия сборки. Возвращает True если всё ок."""
    ok = True

    if sys.version_info < (3, 10):
        print(f"❌ Python 3.10+ required, got {sys.version_info.major}.{sys.version_info.minor}")
        ok = False

    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("❌ PyInstaller not installed. Run: pip install pyinstaller")
        ok = False

    if not (PROJECT_ROOT / 'manage.py').exists():
        print(f"❌ manage.py not found at {PROJECT_ROOT / 'manage.py'}")
        ok = False

    if not (PROJECT_ROOT / 'recipessite').exists():
        print(f"❌ recipessite/ not found at {PROJECT_ROOT / 'recipessite'}")
        ok = False

    # run.py ОБЯЗАТЕЛЕН: без него loader.exe не запустит приложение
    if not (PROJECT_ROOT / 'run.py').exists():
        print(f"❌ run.py not found at {PROJECT_ROOT / 'run.py'}. "
              f"loader.exe won't work without it. Build aborted.")
        ok = False

    if not venv.exists():
        print(f"❌ venv not found at {venv}. Set VENV_DIR env or --venv.")
        ok = False
    elif not (venv / 'Scripts' / 'python.exe').exists():
        print(f"❌ venv python.exe not found at {venv / 'Scripts' / 'python.exe'}")
        ok = False

    return ok


def clean_build_files():
    """Remove old build artifacts."""
    print("\n🗑️ Cleaning old build files...")

    if sys.platform == 'win32':
        subprocess.run(f'taskkill /F /IM {EXE_NAME}.exe', shell=True, capture_output=True, check=False)
        print("  ✅ taskkill executed (if process existed)")
        time.sleep(1)

    if DIST_DIR.exists():
        for attempt in range(3):
            try:
                shutil.rmtree(DIST_DIR, onerror=remove_readonly, ignore_errors=True)
                if not DIST_DIR.exists():
                    print("  ✅ Removed dist folder")
                    break
            except Exception as e:
                print(f"  ⚠️ Attempt {attempt + 1} failed: {e}")
                time.sleep(2)
        else:
            subprocess.run(f'rmdir /s /q "{DIST_DIR}"', shell=True, check=False)
            print("  ✅ Force removed dist folder (rmdir)")

    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR, onerror=remove_readonly, ignore_errors=True)
        print("  ✅ Removed build folder")


def collect_static_files():
    """Run collectstatic to gather all static files into STATIC_ROOT."""
    print("\n📦 Collecting static files...")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipessite.settings')

    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    manage_py = PROJECT_ROOT / 'manage.py'
    cmd = [
        sys.executable, str(manage_py), 'collectstatic',
        '--noinput', '--clear', '--verbosity=1',
    ]

    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)

    if result.returncode != 0:
        print("⚠️ collectstatic failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False

    print("✅ Static files collected successfully")
    return True


def create_loader_script():
    """Создает загрузчик loader.py."""
    loader_content = '''#!/usr/bin/env python

"""Загрузчик recipessite - запускает run.py через python из venv"""

import subprocess
import os
import sys
from pathlib import Path


def main():
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).parent

    venv_python = base_path / '.venv' / 'Scripts' / 'python.exe'
    run_script = base_path / 'run.py'

    if not venv_python.exists():
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Ошибка", "Виртуальное окружение не найдено!")
        except Exception:
            print("ERROR: Virtual environment not found!")
        return 1

    if not run_script.exists():
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Ошибка", "run.py не найден!")
        except Exception:
            print("ERROR: run.py not found!")
        return 1

    startupinfo = None
    creationflags = 0

    if sys.platform == 'win32':
        creationflags = 0x08000000  # CREATE_NO_WINDOW
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0

    try:
        process = subprocess.Popen(
            [str(venv_python), str(run_script)],
            creationflags=creationflags,
            startupinfo=startupinfo,
        )
        process.wait()
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
'''

    loader_path = PROJECT_ROOT / 'loader.py'
    with open(loader_path, 'w', encoding='utf-8') as f:
        f.write(loader_content)
    print("✅ Created loader.py")
    return loader_path


def build_loader():
    """Собирает загрузчик в exe."""
    print("\n" + "=" * 50)
    print(f"Building {EXE_NAME}.exe")
    print("=" * 50)

    loader_path = create_loader_script()

    output_dir = DIST_DIR / EXE_NAME
    output_dir.mkdir(parents=True, exist_ok=True)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--noconsole',
        '--name', EXE_NAME,
        '--noconfirm',
        '--distpath', str(output_dir),
        '--workpath', str(BUILD_DIR),
        '--specpath', str(BUILD_DIR),
        str(loader_path),
    ]

    result = subprocess.run(cmd, cwd=PROJECT_ROOT)

    if result.returncode != 0:
        print("\n❌ Loader build failed!")
        return False

    final_exe = output_dir / f'{EXE_NAME}.exe'
    if final_exe.exists():
        print(f"✅ Loader built: {final_exe}")
        return True

    print(f"❌ Loader not found at {final_exe}")
    return False


def _venv_exclude(rel_parts, item):
    """Возвращает True, если файл venv надо исключить."""
    if '__pycache__' in rel_parts:
        return True
    if item.suffix.lower() in ('.pyc', '.pyo'):
        return True

    if any(part in ('tests', 'test', 'testing') for part in rel_parts):
        return True

    if item.suffix.lower() in ('.dist-info', '.egg-info'):
        return True

    if any(part in ('docs', 'doc') for part in rel_parts):
        return True

    always_exclude = {
        'pyinstaller', '_pyinstaller_hooks_contrib', 'pyinstaller_hooks_contrib',
        'altgraph', 'pefile', 'pywin32_ctypes',
        'pip', 'wheel',
        'debug_toolbar',
        'playwright', 'selenium', 'googleapiclient', 'google',
        'winpty', 'wcwidth', 'trio', '_pytest', 'aiohttp',
        'openpyxl', 'joblib',
    }
    if any(part in always_exclude for part in rel_parts):
        return True

    return False


def copy_venv_and_files(venv, args):
    """Копирует venv и все необходимые файлы в dist."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading

    exe_dir = DIST_DIR / EXE_NAME
    exe_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Copying files to: {exe_dir}")

    # ===== venv =====
    dest_venv = exe_dir / '.venv'
    if venv.exists():
        if dest_venv.exists():
            shutil.rmtree(dest_venv, onerror=remove_readonly, ignore_errors=True)

        print("📦 Preparing to copy venv...")
        files_to_copy = []
        for item in venv.rglob('*'):
            if not item.is_file():
                continue
            rel = item.relative_to(venv)
            rel_parts = [p.lower() for p in rel.parts]

            if _venv_exclude(rel_parts, item):
                continue

            files_to_copy.append((item, dest_venv / rel))

        total_files = len(files_to_copy)
        total_size_mb = sum(f[0].stat().st_size for f in files_to_copy) / (1024 * 1024)
        print(f"📦 Copying {total_files} files ({total_size_mb:.1f} MB) from venv using 8 threads...")

        for _, dst in files_to_copy:
            dst.parent.mkdir(parents=True, exist_ok=True)

        copied = 0
        lock = threading.Lock()
        start_time = time.time()

        def copy_file(src_dst):
            src, dst = src_dst
            try:
                shutil.copy2(src, dst)
                return True
            except Exception:
                return False

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(copy_file, (src, dst)) for src, dst in files_to_copy]
            for _ in as_completed(futures):
                with lock:
                    copied += 1
                    if copied % 100 == 0 or copied == total_files:
                        _progress(copied, total_files, start_time, prefix='venv ')

        print()
        elapsed_total = time.time() - start_time
        print(f"✅ Copied venv ({total_files} files) за {elapsed_total:.1f} сек")
    else:
        print(f"❌ venv not found at {venv}")
        return False

    # ===== project files =====
    def copy_item(src, dst, name, ignore_pycache=True):
        if not src.exists():
            print(f"⚠️ {name} not found at {src}")
            return
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst, onerror=remove_readonly, ignore_errors=True)
            else:
                dst.unlink()
        if src.is_dir():
            ignore = shutil.ignore_patterns('*.pyc', '__pycache__') if ignore_pycache else None
            shutil.copytree(src, dst, ignore=ignore)
        else:
            shutil.copy2(src, dst)
        print(f"✅ Copied {name}")

    copy_item(PROJECT_ROOT / 'manage.py', exe_dir / 'manage.py', 'manage.py')
    copy_item(PROJECT_ROOT / 'run.py', exe_dir / 'run.py', 'run.py')
    copy_item(PROJECT_ROOT / 'recipessite', exe_dir / 'recipessite', 'recipessite')
    copy_item(PROJECT_ROOT / 'recipes', exe_dir / 'recipes', 'recipes')
    copy_item(PROJECT_ROOT / 'users', exe_dir / 'users', 'users')
    copy_item(PROJECT_ROOT / 'templates', exe_dir / 'templates', 'templates')
    copy_item(PROJECT_ROOT / 'static', exe_dir / 'static', 'static')
    copy_item(PROJECT_ROOT / 'media', exe_dir / 'media', 'media')

    db_file = PROJECT_ROOT / 'db.sqlite3'
    if db_file.exists():
        copy_item(db_file, exe_dir / 'db.sqlite3', 'db.sqlite3')
    else:
        print(f"⚠️ db.sqlite3 not found at {db_file}, skipped")

    env_file = PROJECT_ROOT / '.env'
    if env_file.exists():
        copy_item(env_file, exe_dir / '.env', '.env')
    else:
        print(f"⚠️ .env not found at {env_file}, skipped")

    req_file = PROJECT_ROOT.parent / 'requirements.txt'
    if req_file.exists():
        copy_item(req_file, exe_dir / 'requirements.txt', 'requirements.txt')
    else:
        print(f"ℹ️ requirements.txt not found at {req_file}, skipped")

    logs_dir = exe_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)
    print("✅ Created logs folder")

    total_size = 0
    file_count = 0
    for item in exe_dir.rglob('*'):
        if item.is_file():
            total_size += item.stat().st_size
            file_count += 1

    print(f"\n📊 Copied {file_count} files, total size: {total_size // (1024 * 1024)} MB")
    return True


def parse_args():
    parser = argparse.ArgumentParser(description=f'Build {EXE_NAME}.exe')
    parser.add_argument('--with-static', action='store_true',
                        help='Run collectstatic (WARNING: STATIC_ROOT=static/ will be overwritten)')
    parser.add_argument('--venv', default=None, help='Path to venv dir')
    parser.add_argument('--no-sound', action='store_true', help='Disable build sound')
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 60)
    print(f"🚀 {EXE_NAME}.exe BUILDER (venv loader mode, SQLite)")
    print("=" * 60)
    print()

    venv = _resolve_paths(args)

    print(f"  PROJECT_ROOT : {PROJECT_ROOT}")
    print(f"  VENV_DIR     : {venv}")
    print()

    if not check_prerequisites(args, venv):
        print("❌ Prerequisites failed. Aborting.")
        play_sound(success=False, enabled=not args.no_sound)
        sys.exit(1)

    print("\nStep 1: Cleaning build files...")
    clean_build_files()

    build_success = True

    if args.with_static:
        print("\nStep 2: Collecting static files...")
        if not collect_static_files():
            build_success = False

    if build_success:
        print("\nStep 3: Building loader...")
        if not build_loader():
            build_success = False

    if build_success:
        print("\nStep 4: Copying venv and files...")
        if not copy_venv_and_files(venv, args):
            build_success = False

    print("\n" + "=" * 60)
    if build_success:
        print("✅ BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n📁 All files are in: {DIST_DIR}/{EXE_NAME}/")
        print(f"   - {EXE_NAME}.exe (маленький загрузчик)")
        print("   - .venv/ (без тестов, .dist-info, PyInstaller, pip, debug_toolbar)")
        print("   - run.py (обязателен для loader.exe)")
        print("   - db.sqlite3 (если был найден)")
        print("   - manage.py, recipessite/, recipes/, users/, templates/, static/, media/")
        print("   - .env (если был в корне проекта)")
        print(f"\nTo run: double-click {EXE_NAME}.exe")
        play_sound(success=True, enabled=not args.no_sound)
    else:
        print("❌ BUILD FAILED!")
        print("=" * 60)
        play_sound(success=False, enabled=not args.no_sound)
        sys.exit(1)


if __name__ == '__main__':
    main()