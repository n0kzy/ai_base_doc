#!/usr/bin/env python3
"""
Lightweight duplicate-block scanner (no third-party deps).
Finds repeated consecutive normalized line sequences across files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

DEFAULT_EXTENSIONS = {
    "py",
    "js",
    "jsx",
    "ts",
    "tsx",
    "go",
    "rs",
    "java",
    "kt",
    "cs",
    "rb",
    "php",
    "vue",
    "svelte",
    "css",
    "scss",
    "html",
    "md",
}

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "out",
    "target",
    ".next",
    ".nuxt",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
    ".agents",
    "vendor",
    ".turbo",
    ".cache",
    "duplication-jscpd",
}


@dataclass
class Region:
    path: str
    start_line: int  # 1-based
    end_line: int  # 1-based inclusive


@dataclass
class Cluster:
    block_hash: str
    lines: list[str]
    regions: list[Region] = field(default_factory=list)

    @property
    def line_count(self) -> int:
        return len(self.lines)

    @property
    def impact_score(self) -> int:
        """Higher = more waste (lines × extra copies beyond first)."""
        n = len(self.regions)
        if n < 2:
            return 0
        return self.line_count * (n - 1)

    def snippet(self, max_len: int = 72) -> str:
        text = " ".join(self.lines[:2]).strip()
        if len(text) > max_len:
            return text[: max_len - 3] + "..."
        return text or "(empty)"


def normalize_line(line: str, ext: str) -> str | None:
    s = line.strip()
    if not s:
        return None
    # Drop full-line comments (rough; good enough for duplication detection)
    if ext in {"py"}:
        if s.startswith("#"):
            return None
    elif ext in {"js", "jsx", "ts", "tsx", "java", "go", "rs", "cs", "kt", "php", "rb"}:
        if s.startswith("//"):
            return None
    elif ext in {"css", "scss"}:
        if s.startswith("/*") or s.startswith("*"):
            return None
    # Strip end-of-line comments (simple)
    s = re.sub(r"\s*//.*$", "", s)
    s = re.sub(r"\s*#(?!!).*$", "", s)  # python; avoid shebang
    s = re.sub(r"\s+", " ", s).strip()
    return s if s else None


def iter_source_files(
    root: Path,
    extensions: set[str],
    exclude_dirs: set[str],
) -> Iterator[tuple[Path, str]]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.parts)
        if parts & exclude_dirs:
            continue
        if any(part in exclude_dirs for part in path.parts):
            continue
        ext = path.suffix.lstrip(".").lower()
        if ext not in extensions:
            continue
        yield path, ext


def normalized_lines(path: Path, ext: str) -> list[tuple[int, str]]:
    """Returns (original_line_number, normalized_text) for non-empty logical lines."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"warn: skip {path}: {e}", file=sys.stderr)
        return []
    out: list[tuple[int, str]] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        norm = normalize_line(raw, ext)
        if norm is not None:
            out.append((i, norm))
    return out


def block_key(lines: list[str]) -> str:
    payload = "\n".join(lines)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def find_clusters(
    root: Path,
    extensions: set[str],
    exclude_dirs: set[str],
    min_lines: int,
    min_tokens: int,
) -> list[Cluster]:
    # hash -> list of (path, start_orig_line, end_orig_line, block_lines)
    buckets: dict[str, list[tuple[str, int, int, list[str]]]] = defaultdict(list)

    for path, ext in iter_source_files(root, extensions, exclude_dirs):
        rel = str(path.relative_to(root)).replace("\\", "/")
        seq = normalized_lines(path, ext)
        if len(seq) < min_lines:
            continue
        # Map normalized index -> original line number
        orig_lines = [o for o, _ in seq]
        norms = [n for _, n in seq]

        for i in range(len(norms) - min_lines + 1):
            block = norms[i : i + min_lines]
            if min_tokens > 0:
                token_count = sum(len(line.split()) for line in block)
                if token_count < min_tokens:
                    continue
            h = block_key(block)
            start_orig = orig_lines[i]
            end_orig = orig_lines[i + min_lines - 1]
            buckets[h].append((rel, start_orig, end_orig, block))

    clusters: list[Cluster] = []
    for h, entries in buckets.items():
        if len(entries) < 2:
            continue
        # Deduplicate identical regions (same file, same span)
        seen: set[tuple[str, int, int]] = set()
        regions: list[Region] = []
        block_lines = entries[0][3]
        for rel, start, end, bl in entries:
            key = (rel, start, end)
            if key in seen:
                continue
            seen.add(key)
            regions.append(Region(rel, start, end))
        if len(regions) < 2:
            continue
        clusters.append(Cluster(block_hash=h, lines=block_lines, regions=regions))

    clusters.sort(key=lambda c: (-c.impact_score, -c.line_count, c.regions[0].path))
    return clusters


def format_markdown_report(
    root: Path,
    clusters: list[Cluster],
    min_lines: int,
    top: int,
) -> str:
    shown = clusters[:top]
    total_waste = sum(c.impact_score for c in clusters)
    lines: list[str] = [
        "# Duplication report",
        "",
        f"- **Root:** `{root.resolve()}`",
        f"- **Threshold:** `{min_lines}` consecutive normalized lines",
        f"- **Clusters found:** {len(clusters)}",
        f"- **Estimated duplicate line-equivalents:** {total_waste}",
        "",
        "## Top clusters",
        "",
        "| Rank | Impact | Lines | Copies | Snippet | Locations |",
        "|------|--------|-------|--------|---------|-----------|",
    ]
    for rank, c in enumerate(shown, start=1):
        locs = "; ".join(f"`{r.path}:{r.start_line}-{r.end_line}`" for r in c.regions[:4])
        if len(c.regions) > 4:
            locs += f" (+{len(c.regions) - 4} more)"
        lines.append(
            f"| {rank} | {c.impact_score} | {c.line_count} | {len(c.regions)} | "
            f"{c.snippet()} | {locs} |"
        )
    lines.extend(["", "## Sample blocks", ""])
    for rank, c in enumerate(shown[:10], start=1):
        lines.append(f"### Cluster {rank} (impact {c.impact_score})")
        lines.append("")
        lines.append("```")
        lines.extend(c.lines)
        lines.append("```")
        lines.append("")
        lines.append("**Locations:**")
        for r in c.regions:
            lines.append(f"- `{r.path}` lines {r.start_line}-{r.end_line}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan for duplicated code blocks.")
    parser.add_argument("root", type=Path, help="Project root directory")
    parser.add_argument("--min-lines", type=int, default=6, help="Min lines per block")
    parser.add_argument("--min-tokens", type=int, default=0, help="Min tokens in block")
    parser.add_argument(
        "--extensions",
        type=str,
        default=",".join(sorted(DEFAULT_EXTENSIONS)),
        help="Comma-separated file extensions without dot",
    )
    parser.add_argument(
        "--exclude",
        type=str,
        default="",
        help="Comma-separated extra directory names to exclude",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout")
    parser.add_argument("--stdout", action="store_true", help="No duplication-report.md")
    parser.add_argument("--top", type=int, default=30, help="Clusters in markdown report")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Report path (default: <root>/duplication-report.md)",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 1

    extensions = {e.strip().lower() for e in args.extensions.split(",") if e.strip()}
    exclude_dirs = set(DEFAULT_EXCLUDE_DIRS)
    if args.exclude:
        exclude_dirs.update(x.strip() for x in args.exclude.split(",") if x.strip())

    clusters = find_clusters(
        root, extensions, exclude_dirs, args.min_lines, args.min_tokens
    )

    if args.json:
        payload = {
            "root": str(root),
            "min_lines": args.min_lines,
            "cluster_count": len(clusters),
            "clusters": [
                {
                    "hash": c.block_hash,
                    "line_count": c.line_count,
                    "impact_score": c.impact_score,
                    "snippet": c.snippet(),
                    "lines": c.lines,
                    "regions": [
                        {
                            "path": r.path,
                            "start_line": r.start_line,
                            "end_line": r.end_line,
                        }
                        for r in c.regions
                    ],
                }
                for c in clusters
            ],
        }
        print(json.dumps(payload, indent=2))
        return 0

    report = format_markdown_report(root, clusters, args.min_lines, args.top)
    if args.stdout:
        print(report)
    else:
        out_path = args.output or (root / "duplication-report.md")
        out_path.write_text(report, encoding="utf-8")
        print(f"Wrote {out_path} ({len(clusters)} clusters)")

    # Brief stdout summary
    print(f"\nSummary: {len(clusters)} clusters, top impact:", file=sys.stderr)
    for c in clusters[:5]:
        print(
            f"  [{c.impact_score}] {c.line_count}L x{len(c.regions)} — {c.snippet()}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
