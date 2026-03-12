import re
import glob as _glob
from pathlib import Path
from fnmatch import fnmatch
from typing import Dict, List, Optional, Union


class snippet:
    """
    Collect named code snippets from directories or glob patterns.

    Snippets are defined by:
    - Start: a line containing "snippet <name>" where <name> is an identifier
    - End: a line containing "end snippet" (with optional spaces between words)
    """

    def __init__(self, source: Union[str, List[str]], exclude=None):
        """
        Args:
            source: a directory path, a glob pattern, or a list of either.
                    Directories are scanned recursively; globs select files directly.
            exclude: filename, glob pattern, or list of either to skip during scan.
        """
        self._sources = list(source) if isinstance(source, (list, tuple)) else [source]

        if exclude is None:
            self._exclude = []
        elif isinstance(exclude, str):
            self._exclude = [exclude]
        else:
            self._exclude = list(exclude)

        self.snippets: Dict[str, str] = {}
        self._scan()

    def _files(self) -> List[Path]:
        """Resolve all sources to a deduplicated, exclusion-filtered list of files."""
        seen = set()
        result = []
        for source in self._sources:
            p = Path(source)
            if p.is_dir():
                candidates = sorted(p.rglob('*'))
            else:
                candidates = sorted(Path(f) for f in _glob.glob(source, recursive=True))
            for f in candidates:
                key = str(f.resolve())
                if f.is_file() and key not in seen:
                    seen.add(key)
                    if not any(fnmatch(f.name, pat) or fnmatch(str(f), pat) for pat in self._exclude):
                        result.append(f)
        return result

    def _scan(self):
        for file_path in self._files():
            try:
                self._extract_snippets_from_file(str(file_path))
            except (UnicodeDecodeError, PermissionError):
                continue

    def _extract_snippets_from_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            snippet_name = self._match_snippet_start(lines[i].strip())
            if snippet_name:
                content = []
                i += 1
                while i < len(lines):
                    if self._match_snippet_end(lines[i].strip()):
                        if snippet_name in self.snippets:
                            raise ValueError(
                                f"Snippet '{snippet_name}' already exists "
                                f"(second occurrence in '{file_path}')"
                            )
                        self.snippets[snippet_name] = ''.join(content)
                        break
                    content.append(lines[i])
                    i += 1
                else:
                    raise ValueError(
                        f"Snippet '{snippet_name}' is not terminated in '{file_path}'"
                    )
            i += 1

    def _match_snippet_start(self, line: str) -> Optional[str]:
        m = re.search(r'.*snippet\s+([a-zA-Z_][a-zA-Z0-9_]*)', line, re.IGNORECASE)
        return m.group(1) if m else None

    def _match_snippet_end(self, line: str) -> bool:
        return bool(re.search(r'.*end\s+snippet.*', line, re.IGNORECASE))

    def get(self, name: str) -> Optional[str]:
        return self.snippets.get(name)

    def __call__(self, name: str) -> Optional[str]:
        return self.get(name)

    def names(self) -> list:
        return list(self.snippets.keys())

    def contains(self, name: str) -> bool:
        return name in self.snippets

    def size(self) -> int:
        return len(self.snippets)

    def __str__(self) -> str:
        return ''

    def __repr__(self) -> str:
        return f"snippet(sources={self._sources!r}, snippets={list(self.snippets.keys())})"
