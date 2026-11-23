import os
import subprocess
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    entry_path = os.path.join(out_dir, "entry.txt")
    if os.path.exists(entry_path):
        os.remove(entry_path)
    os.makedirs(out_dir, exist_ok=True)

    result = subprocess.run(
        [sys.executable, "main.py"],
        env={**os.environ, "MAKEFUN_OUTPUT_DIR": out_dir},
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(f"main.py failed: {result.returncode}\n{result.stdout}\n{result.stderr}")

    if not os.path.exists(entry_path):
        raise SystemExit(f"missing {entry_path}")

    with open(entry_path, "r", encoding="utf-8") as f:
        content = f.read()

    if len(content) == 0:
        raise SystemExit("entry is empty")
    if any(ch.isspace() for ch in content):
        raise SystemExit(f"entry contains whitespace: {content!r}")
    if not any(ch.isalpha() for ch in content):
        raise SystemExit(f"entry has no letters: {content!r}")
    words = content.split()
    if len(words) != 1:
        raise SystemExit(f"expected exactly one word, got: {content!r}")
    if words[0] != content:
        raise SystemExit(f"entry has surrounding content: {content!r}")

    print("PASS")


if __name__ == "__main__":
    main()
