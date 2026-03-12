import hashlib
import sys
import time
import argparse
import shutil
from importlib.metadata import version
from pathlib import Path
from pet.processor import process_template


def _pet_hash(pet_dir: Path) -> str:
    """MD5 of all files under pet_dir (alphabetical, excluding .hash itself)."""
    md5 = hashlib.md5()
    for path in sorted(pet_dir.rglob("*")):
        if path.is_file() and path.name != ".hash":
            md5.update(str(path.relative_to(pet_dir)).encode())
            md5.update(path.read_bytes())
    return md5.hexdigest()


def _create_pet_dir(macros_src: Path, dest: Path):
    shutil.copytree(macros_src, dest,
                    ignore=shutil.ignore_patterns("__init__.py", "__pycache__"))
    (dest / ".status").mkdir()
    (dest / ".hash").write_text(_pet_hash(dest))


def cmd_init(args):
    macros_src = Path(__file__).parent / "macros"
    dest = Path(".pet")
    hash_file = dest / ".hash"

    if dest.exists():
        if args.force:
            shutil.rmtree(dest)
            _create_pet_dir(macros_src, dest)
            print("Forced reinitialisation of '.pet/' directory.")
        else:
            stored = hash_file.read_text().strip() if hash_file.exists() else None
            if stored is None:
                print("'.pet/' exists with no .hash — skipping (delete it manually or use -f to reinitialise).")
            elif stored == _pet_hash(dest):
                shutil.rmtree(dest)
                _create_pet_dir(macros_src, dest)
                print("Regenerated '.pet/' with updated macro library.")
            else:
                print("'.pet/' has local modifications — skipping (use -f to overwrite).")
    else:
        _create_pet_dir(macros_src, dest)
        print("Initialized '.pet/' directory with macro library.")

    if getattr(args, "target", None) == "for_claude":
        _install_claude_skill()


def _install_claude_skill():
    pkg = Path(__file__).parent
    skills = [
        (pkg / "SKILL.md",           Path(".claude") / "skills" / "pet"          / "SKILL.md"),
        (pkg / "AUTHORING_SKILL.md", Path(".claude") / "skills" / "pet-authoring" / "SKILL.md"),
    ]
    for src, dest in skills:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"Installed {dest}")



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
        description=f"Program Enhanced Text {version('pet-doc')} — documentation automation tool",
    )
    parser.add_argument("--version", "-V", action="version",
                        version=f"pet {version('pet-doc')}")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("process", help="Process a .pet template file")
    p.add_argument("input", help="Input .pet template file")
    p.add_argument("output", help="Output file")

    p_init = sub.add_parser("init",
                            help="Initialize .pet/ macro directory in current project. "
                                 "Use 'init for_claude' to also install the pet skill into Claude Code.")
    p_init.add_argument("target", nargs="?", choices=["for_claude"],
                        help="'for_claude' also installs the pet skill into Claude Code")
    p_init.add_argument("-f", "--force", action="store_true",
                        help="Overwrite .pet/ even if it has local modifications")

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
