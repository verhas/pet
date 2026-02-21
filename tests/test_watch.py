import argparse
from pathlib import Path
from pet.cli import cmd_watch


def make_args(input_file, output_file, interval=0.1):
    args = argparse.Namespace()
    args.input = str(input_file)
    args.output = str(output_file)
    args.interval = interval
    return args


def test_watch_processes_immediately(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).parent.parent)
    t = tmp_path / "in.pet"
    t.write_text("{% print('hello') %}")
    out = tmp_path / "out.txt"

    # Stop after the first sleep (one loop iteration)
    def fake_sleep(seconds):
        raise KeyboardInterrupt

    monkeypatch.setattr("pet.cli.time.sleep", fake_sleep)
    cmd_watch(make_args(t, out))

    assert "hello" in out.read_text()


def test_watch_reprocesses_on_change(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).parent.parent)
    t = tmp_path / "in.pet"
    t.write_text("{% print('version1') %}")
    out = tmp_path / "out.txt"

    call_count = 0

    def fake_sleep(seconds):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # Modify the file so the next mtime check detects a change
            t.write_text("{% print('version2') %}")
        else:
            raise KeyboardInterrupt

    monkeypatch.setattr("pet.cli.time.sleep", fake_sleep)
    cmd_watch(make_args(t, out, interval=0.1))

    assert "version2" in out.read_text()
