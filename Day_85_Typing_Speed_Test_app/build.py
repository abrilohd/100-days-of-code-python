import os
import shutil
import subprocess
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
BUILD = os.path.join(ROOT, "build")
WEB_DIR = os.path.join(ROOT, "web")
DATA_DIR = os.path.join(ROOT, "data")


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)


def main() -> None:
    # Clean previous builds
    for p in (DIST, BUILD):
        if os.path.exists(p):
            shutil.rmtree(p, ignore_errors=True)

    entry = os.path.join(ROOT, "app_webview.py")

    # PyInstaller --add-data uses ";" on Windows, ":" on macOS/Linux
    sep = os.pathsep
    add_web = f"{WEB_DIR}{sep}web"
    add_data = f"{DATA_DIR}{sep}data"

    run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--onefile",
            "--name",
            "TypingSpeedTestPro",
            "--add-data",
            add_web,
            "--add-data",
            add_data,
            entry,
        ]
    )

    print("\nBuild complete.")
    print(f"EXE: {os.path.join(DIST, 'TypingSpeedTestPro.exe')}")


if __name__ == "__main__":
    main()
