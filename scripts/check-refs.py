#!/usr/bin/env python3
"""检查 better-theme 仓库的文档卫生。

跑法（仓库根目录）：

    python3 scripts/check-refs.py

检查项：
1. 交叉引用：文档里出现的 `xxx.md` / 路径引用，文件是否真实存在
   （依次按「引用者所在目录」「仓库根目录」「references/」「references/cases/」解析）
2. 换行符：Markdown 一律 LF，发现 CRLF 报警
3. 行尾空白与文件末尾多余空行

退出码：0 全绿，1 有问题。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 只看文档，跳过素材
SKIP_DIRS = {".git", ".obsidian", "asset", "node_modules", "scripts"}

# 反引号里的内容 / Markdown 链接目标
INLINE_CODE = re.compile(r"`([^`\n]+)`")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# 长得像仓库内文件引用的：以 .md 结尾，或 references/ 开头的路径
PATH_LIKE = re.compile(r"^(?:\.{0,2}/)?(?:[\w./-]*/)?[\w.-]+\.md$")

def md_files() -> list[Path]:
    return sorted(
        p
        for p in ROOT.rglob("*.md")
        if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts)
    )


def check_refs(path: Path, text: str) -> list[str]:
    problems: list[str] = []
    candidates = INLINE_CODE.findall(text) + MD_LINK.findall(text)
    for raw in candidates:
        target = raw.split("#", 1)[0].strip()
        if not target or not PATH_LIKE.match(target):
            continue
        # 锚点/外链跳过
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        # 引用可能是相对自身、相对仓库根，或只写了 references/ 里的裸文件名
        bases = (path.parent, ROOT, ROOT / "references", ROOT / "references" / "cases")
        if not any((base / target).exists() for base in bases):
            problems.append(f"  引用不存在：`{target}`")
    return problems


def check_hygiene(path: Path, text: str) -> list[str]:
    rel = path.relative_to(ROOT)
    problems: list[str] = []
    if "\r\n" in text:
        n = text.count("\r\n")
        problems.append(f"  CRLF 换行 {n} 处（应统一 LF）")
    for i, line in enumerate(text.split("\n"), 1):
        # 行尾恰好两个空格是 Markdown 硬换行，属于有效语法，不报警
        if line.endswith("  "):
            line = line[:-2]
        if line != line.rstrip(" \t"):
            problems.append(f"  第 {i} 行行尾空白")
    if text.endswith("\n\n"):
        problems.append("  文件末尾有多余空行")
    return problems


def main() -> int:
    failed = False
    files = md_files()
    for path in files:
        text = path.read_text(encoding="utf-8")
        problems = check_refs(path, text) + check_hygiene(path, text)
        if problems:
            failed = True
            print(f"✗ {path.relative_to(ROOT)}")
            print("\n".join(problems))
    print(f"\n扫描 {len(files)} 个 Markdown 文件：{'有问题' if failed else '全部通过 ✅'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
