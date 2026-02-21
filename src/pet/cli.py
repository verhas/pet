import sys
import time
import argparse
import shutil
from pathlib import Path
from pet.processor import process_template


def cmd_init(args):
    macros_src = Path(__file__).parent / "macros"
    dest = Path(".pet")
    if dest.exists():
        print("'.pet/' already exists. Skipping.")
        return
    shutil.copytree(macros_src, dest,
                    ignore=shutil.ignore_patterns("__init__.py", "__pycache__"))
    (dest / ".status").mkdir()
    print("Initialized '.pet/' directory with macro library.")


def cmd_watch(args):
    input_file = args.input
    output_file = args.output
    interval = args.interval

    print(f"Watching '{input_file}' for changes. Press Ctrl+C to stop.")
    process_template(input_file, output_file)

    last_mtime = Path(input_file).stat().st_mtime

    try:
        while True:
            time.sleep(interval)
            try:
                mtime = Path(input_file).stat().st_mtime
                if mtime != last_mtime:
                    last_mtime = mtime
                    print(f"Change detected, regenerating...")
                    process_template(input_file, output_file)
            except FileNotFoundError:
                print(f"Warning: '{input_file}' not found, waiting...")
    except KeyboardInterrupt:
        print("\nStopped watching.")


def main():
    # Shorthand: `pet input.md.pet output.md`
    if len(sys.argv) == 3 and sys.argv[1] not in ('process', 'init', 'watch', '-h', '--help'):
        process_template(sys.argv[1], sys.argv[2])
        return

    parser = argparse.ArgumentParser(
        prog="pet",
        description="Program Enhanced Text — documentation automation tool",
    )
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("process", help="Process a .pet template file")
    p.add_argument("input", help="Input .pet template file")
    p.add_argument("output", help="Output file")

    sub.add_parser("init", help="Initialize .pet/ macro directory in current project")

    w = sub.add_parser("watch", help="Watch a .pet file and reprocess on every change")
    w.add_argument("input", help="Input .pet template file")
    w.add_argument("output", help="Output file")
    w.add_argument("--interval", type=float, default=0.5,
                   metavar="SECONDS", help="Polling interval in seconds (default: 0.5)")

    args = parser.parse_args()

    if args.command == "process":
        process_template(args.input, args.output)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "watch":
        cmd_watch(args)
    else:
        parser.print_help()
