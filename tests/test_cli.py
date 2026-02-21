import argparse
from pathlib import Path
from pet.cli import cmd_init


def make_init_args():
    return argparse.Namespace()


def test_init_creates_pet_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cmd_init(make_init_args())
    assert (tmp_path / ".pet").is_dir()


def test_init_copies_macros(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cmd_init(make_init_args())
    assert (tmp_path / ".pet" / "counters.py").exists()
    assert (tmp_path / ".pet" / "snippet.py").exists()
    assert (tmp_path / ".pet" / "include.py").exists()
    assert (tmp_path / ".pet" / "number.py").exists()
    assert (tmp_path / ".pet" / "pipe.py").exists()


def test_init_creates_status_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cmd_init(make_init_args())
    assert (tmp_path / ".pet" / ".status").is_dir()


def test_init_does_not_copy_package_artifacts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cmd_init(make_init_args())
    assert not (tmp_path / ".pet" / "__init__.py").exists()
    assert not (tmp_path / ".pet" / "__pycache__").exists()


def test_init_skips_if_already_exists(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".pet").mkdir()
    cmd_init(make_init_args())
    assert "already exists" in capsys.readouterr().out
    assert not (tmp_path / ".pet" / ".status").exists()
