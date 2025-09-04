from urllib.parse import quote
from pathlib import Path
import argparse
import json
import sys

REPO = "tenstorrent/tt-metal"
STATE_FILE = Path.home() / ".tt-badges.json"

WORKFLOWS = [
    ("All post-commit tests",                "all-post-commit-workflows.yaml"),
    ("Blackhole post-commit tests",          "blackhole-post-commit.yaml"),
    ("(Single-card) Demo tests",             "single-card-demo-tests.yaml"),
    ("(Single-card) Model perf tests",       "perf-models.yaml"),
    ("(T3K) T3000 demo tests",               "t3000-demo-tests.yaml"),
    ("(T3K) T3000 frequent tests",           "t3000-frequent-tests.yaml"),
    ("(T3K) T3000 perplexity tests",         "t3000-perplexity-tests.yaml"),
    ("(T3K) T3000 unit tests",               "t3000-unit-tests.yaml"),
    ("(TG) TG DeepSeek tests",               "tg-deepseek-tests.yaml"),
    ("(TG) TG demo all-post-commit tests",   "tg-demo-all-post-commit.yaml"),
]

# Defaults: first two ON, others OFF
DEFAULT_SELECTED = [True, True] + [False] * (len(WORKFLOWS) - 2)


def build_badge(repo: str, workflow: str, title: str, branch: str) -> str:
    enc_branch = quote(branch, safe="")
    return (
        f"[![{title}]"
        f"(https://github.com/{repo}/actions/workflows/{workflow}/badge.svg?branch={enc_branch})]"
        f"(https://github.com/{repo}/actions/workflows/{workflow})"
    )


def load_saved_selection():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        sel = data.get("selected", [])
        if not isinstance(sel, list):
            return None
        out = list(map(bool, sel))[: len(WORKFLOWS)]
        if len(out) < len(WORKFLOWS):
            out.extend([False] * (len(WORKFLOWS) - len(out)))
        return out
    except Exception:
        return None


def save_selection(selected):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"selected": list(map(bool, selected))}, f)
    except Exception:
        pass  # non-fatal


def digit_to_index(ch: str):
    """Map keys '1'..'9' to indices 0..8, and '0' to last index."""
    if ch in "123456789":
        return int(ch) - 1
    if ch == "0":
        return len(WORKFLOWS) - 1
    return None


def index_to_label(idx: int):
    """Display labels as 1..9, then 0 for the last item."""
    return str(idx + 1) if idx < len(WORKFLOWS) - 1 else "0"


def apply_digit_toggles(selected, digits: str):
    for ch in digits:
        idx = digit_to_index(ch)
        if idx is not None:
            selected[idx] = not selected[idx]


def clear_screen():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()


def print_menu(branch, selected):
    clear_screen()
    print("GitHub badge picker (press digits 0–9 to toggle, Enter to finish)\n")
    print(f"Branch: {branch}\n")
    for idx, (title, _) in enumerate(WORKFLOWS):
        lbl = index_to_label(idx)
        mark = "X" if selected[idx] else " "
        print(f"{lbl}: [{mark}] {title}")
    print(
        "\nPress 0-9 to toggle tests. Press Enter to generate GitHub badges for selected tests.\n"
    )


def read_single_key():
    """Read one keypress without waiting for Enter (cross-platform)."""
    try:
        import msvcrt  # Windows

        ch = msvcrt.getwch()
        if ch in ("\r", "\n"):
            return "\n"
        return ch
    except ImportError:
        import termios, tty  # POSIX

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return "\n" if ch == "\r" else ch


def interactive_toggle(branch, selected):
    print_menu(branch, selected)
    while True:
        ch = read_single_key()
        if ch == "\n":  # Enter
            break
        idx = digit_to_index(ch)
        if idx is not None:
            selected[idx] = not selected[idx]
            print_menu(branch, selected)
        # ignore other keys
    return selected


def main():
    parser = argparse.ArgumentParser(
        description="Print tt-metal workflow badge markdown."
    )
    parser.add_argument(
        "-b", "--branch", help="Branch name (e.g., main or feature/foo)"
    )
    parser.add_argument(
        "-s",
        "--select",
        help="Digits (1–9, 0 for last) to pre-toggle and skip interaction.",
    )
    args = parser.parse_args()

    branch = args.branch
    while not branch:
        branch = input("Enter branch name (e.g., main or feature/foo): ").strip()

    if args.select is not None:
        selected = DEFAULT_SELECTED.copy()
        apply_digit_toggles(selected, args.select)
    else:
        selected = load_saved_selection() or DEFAULT_SELECTED.copy()
        if sys.stdin.isatty() and sys.stdout.isatty():
            try:
                selected = interactive_toggle(branch, selected)
            except KeyboardInterrupt:
                print("\nAborted.")
                return

    save_selection(selected)

    any_printed = False
    for (title, wf), is_on in zip(WORKFLOWS, selected):
        if is_on:
            any_printed = True
            print(build_badge(REPO, wf, title, branch))
    if not any_printed:
        print("No badges selected. Nothing to output.")
    print()


if __name__ == "__main__":
    main()

