import os
from pathlib import Path

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

mcp = MCPServer("search-local-docs")

ROOTS_FILE = Path(__file__).resolve().parent / "search_roots.txt"
TEXT_SUFFIXES = {".md", ".markdown", ".txt"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".cursor"}
MAX_MATCHES = 5
MAX_FILE_BYTES = 1_000_000
EXCERPT_LIMIT = 180


def load_roots() -> list[Path]:
    """Read the folders the user listed. Relative paths are based on this file."""
    if not ROOTS_FILE.is_file():
        return []
    roots: list[Path] = []
    for line in ROOTS_FILE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        path = Path(stripped).expanduser()
        if not path.is_absolute():
            path = ROOTS_FILE.parent / path
        roots.append(path)
    return roots


def keywords_for(query: str) -> list[str]:
    seen: set[str] = set()
    keywords: list[str] = []
    for word in query.casefold().split():
        if word not in seen:
            seen.add(word)
            keywords.append(word)
    return keywords


def excerpt_for(text: str, keywords: list[str]) -> str:
    lines = text.splitlines() or [text]

    def line_key(line: str) -> tuple[int, int]:
        folded = line.casefold()
        hits = sum(folded.count(keyword) for keyword in keywords)
        return (hits, len(" ".join(line.split())))

    compact = " ".join(max(lines, key=line_key).split())
    if not compact:
        compact = " ".join(text.split())
    folded = compact.casefold()
    index = min((folded.find(keyword) for keyword in keywords if keyword in folded), default=0)
    if len(compact) <= EXCERPT_LIMIT:
        return compact
    start = max(0, index - 40)
    end = min(len(compact), start + EXCERPT_LIMIT)
    start = max(0, end - EXCERPT_LIMIT)
    snippet = compact[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(compact):
        snippet = snippet + "..."
    return snippet


def iter_documents(root: Path):
    resolved_root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [
            name
            for name in dirnames
            if name not in SKIP_DIRS and not name.startswith(".")
        ]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() not in TEXT_SUFFIXES or path.is_symlink():
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
                resolved = path.resolve()
                resolved.relative_to(resolved_root)
                text = resolved.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeError, ValueError):
                continue
            yield resolved, text


def search_files(query: str) -> str:
    keywords = keywords_for(query)
    if not keywords:
        return 'Pass a keyword query, such as "setup instructions" or "course notes".\n'

    roots = load_roots()
    if not roots:
        return (
            "No search folders are configured. Add one absolute folder path per line to "
            f"{ROOTS_FILE}. Only those folders are searched, and they can sit outside "
            "this project.\n"
        )

    warnings: list[str] = []
    found: list[tuple[int, Path, str]] = []
    for root in roots:
        if not root.exists():
            warnings.append(f"Skipped missing folder: {root}")
            continue
        if not root.is_dir():
            warnings.append(f"Skipped path that is not a folder: {root}")
            continue
        for path, text in iter_documents(root):
            folded = text.casefold()
            if any(keyword not in folded for keyword in keywords):
                continue
            hits = sum(folded.count(keyword) for keyword in keywords)
            found.append((hits, path, excerpt_for(text, keywords)))

    found.sort(key=lambda item: (-item[0], str(item[1]).casefold()))
    total = len(found)
    shown = found[:MAX_MATCHES]
    if total == 0:
        lines = [f'No matches for "{query}".']
    else:
        if total > len(shown):
            header = f'Showing {len(shown)} of {total} matches for "{query}".'
        elif total == 1:
            header = f'1 match for "{query}".'
        else:
            header = f'{total} matches for "{query}".'
        lines = [header, ""]
        for _hits, path, snippet in shown:
            lines.extend([str(path), snippet, ""])
    if warnings:
        if lines and lines[-1] != "":
            lines.append("")
        lines.extend(warnings)
    return "\n".join(lines).rstrip() + "\n"


@mcp.tool(
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def search_local_docs(query: str) -> str:
    """Find old project specs, setup instructions, and course notes in local files.

    Use this when the user asks where a spec, setup guide, or course note lives on
    disk, including notes kept outside the current project. Pass a short keyword
    query such as "database setup" or "week 3 notes". Every keyword must appear.
    The search is case-insensitive.

    Returns up to five matches from the folders listed in search_roots.txt. Each
    match has the file path and a short excerpt showing the matching text. Returns
    a no-match message when nothing in those folders matches. Read-only.
    """
    return search_files(query)


if __name__ == "__main__":
    mcp.run(transport="stdio")
