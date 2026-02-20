import sys
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
    shutil.copytree(macros_src, dest)
    print("Initialized '.pet/' directory with macro library.")


def main():
    # Shorthand: `pet input.md.pet output.md`
    if len(sys.argv) == 3 and sys.argv[1] not in ('process', 'init', '-h', '--help'):
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

    args = parser.parse_args()

    if args.command == "process":
        process_template(args.input, args.output)
    elif args.command == "init":
        cmd_init(args)
    else:
        parser.print_help()
