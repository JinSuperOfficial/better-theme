#!/usr/bin/env python3
"""检查 better-theme 仓库的文档卫生。

跑法（仓库根目录）：

    python3 scripts/check-refs.py

检查项：
1. 交叉引用：文档里出现的 `xxx.md` / 路径引用，文件是否真实存在
   （依次按「引用者所在目录」「仓库根目录」「references/」「references/cases/」解析）
2. 换行符：Markdown 一律 LF，发现 CRLF 报警
3. 行尾空白与文件末尾多余空行
4. YAML frontmatter：能否解析、name 是否 kebab-case、description 是否存在
   （有 PyYAML 时做严格解析，没有时退化为关键字检查）
5. 语言表：根目录与 readme/ 下的 README 必须带 `## Language` 表，
   列出全部语言版本，且各表按字符数对齐（跑 --fix 自动对齐）

退出码：0 全绿，1 有问题。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # 没有 PyYAML 也能跑，只是退化为关键字检查
    yaml = None

ROOT = Path(__file__).resolve().parent.parent

# 只看文档，跳过素材
SKIP_DIRS = {".git", ".obsidian", "asset", "node_modules", "scripts"}

# 反引号里的内容 / Markdown 链接目标
INLINE_CODE = re.compile(r"`([^`\n]+)`")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# 长得像仓库内文件引用的：以 .md 结尾，或 references/ 开头的路径
PATH_LIKE = re.compile(r"^(?:\.{0,2}/)?(?:[\w./-]*/)?[\w.-]+\.md$")

# frontmatter 里的技能名必须是 kebab-case
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# 多语言 README 全家族：每个入口的语言表都要列全这些文件
LANG_TABLE = re.compile(r"^##\s+Language\b")
LANG_READMES = (
    "README.md",
    "README-EN.md",
    "README-CN-HANT.md",
    "README-JP.md",
    "README-ES.md",
)

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


def check_frontmatter(path: Path, text: str) -> list[str]:
    """校验 SKILL.md / 参考文档的 YAML frontmatter。"""
    if not text.startswith("---\n"):
        return []
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return ["  frontmatter 没有闭合的 --- 分隔线"]
    raw = parts[1]
    if yaml is None:
        problems = []
        if not re.search(r"^name:\s*\S", raw, re.M):
            problems.append("  frontmatter 缺少 name")
        if not re.search(r"^description:\s*\S", raw, re.M):
            problems.append("  frontmatter 缺少 description")
        return problems
    try:
        data = yaml.safe_load(raw) or {}
    except Exception as exc:  # noqa: BLE001
        first = str(exc).splitlines()[0]
        return [f"  frontmatter 不是合法 YAML：{type(exc).__name__} {first}"]
    problems = []
    if path.name == "SKILL.md":
        # 技能入口必须有可路由的 name + description
        name = data.get("name")
        if not name:
            problems.append("  frontmatter 缺少 name")
        elif not KEBAB.match(str(name)):
            problems.append(f"  name 不是 kebab-case：{name!r}")
        if not data.get("description"):
            problems.append("  frontmatter 缺少 description")
    for key, value in data.items():
        if value in (None, "", [], {}):
            problems.append(f"  frontmatter 的 {key} 是空值")
    return problems


def align_table(rows: list[list[str]]) -> list[str]:
    """把表格按字符数对齐，分隔行用 :--- 左对齐，风格与编辑器格式化一致。"""
    if not rows:
        return []
    widths = [max(len(cell) for cell in col) for col in zip(*rows)]
    out = ["| " + " | ".join(c.ljust(w) for c, w in zip(rows[0], widths)) + " |"]
    out.append("| " + " | ".join(":" + "-" * (w - 1) for w in widths) + " |")
    for row in rows[1:]:
        out.append("| " + " | ".join(c.ljust(w) for c, w in zip(row, widths)) + " |")
    return out


def normalize_language_table(text: str) -> str:
    """返回语言表对齐后的文本；找不到语言表就原样返回。"""
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if LANG_TABLE.match(line)), None)
    if start is None:
        return text
    i = start + 1
    while i < len(lines) and not lines[i].startswith("|"):
        i += 1
    rows: list[list[str]] = []
    j = i
    while j < len(lines) and lines[j].startswith("|"):
        cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
        if not all(set(c) <= set(":- ") for c in cells):  # 跳过已有的分隔行
            rows.append(cells)
        j += 1
    if not rows:
        return text
    return "\n".join(lines[:i] + align_table(rows) + lines[j:])


def check_language_table(path: Path, text: str) -> list[str]:
    """根目录与 readme/ 下的 README 必须带一张列全所有语言的语言表。"""
    if not path.name.startswith("README"):
        return []
    if not (path.parent == ROOT or path.parent.name == "readme"):
        return []
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if LANG_TABLE.match(line)), None)
    if start is None:
        return ["  缺少 `## Language` 语言表"]
    section: list[str] = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        section.append(line)
    blob = "\n".join(section)
    problems = []
    missing = [name for name in LANG_READMES if name not in blob]
    if missing:
        problems.append("  语言表缺少条目：" + "、".join(missing))
    if normalize_language_table(text) != text:
        problems.append("  语言表未对齐（跑 python3 scripts/check-refs.py --fix 自动对齐）")
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


def readme_family_frontmatter(path: Path, text: str) -> tuple[str, ...] | None:
    """README 家族的 frontmatter 键集合，用于比对各语言版本是否一致。"""
    if not path.name.startswith("README"):
        return None
    if not (path.parent == ROOT or path.parent.name == "readme"):
        return None
    if not text.startswith("---\n"):
        return ()
    parts = text.split("---\n", 2)
    if len(parts) < 3 or yaml is None:
        return ()
    data = yaml.safe_load(parts[1]) or {}
    return tuple(sorted(data))


def main() -> int:
    fix = "--fix" in sys.argv[1:]
    failed = False
    files = md_files()
    family: dict[str, tuple[str, ...]] = {}
    if fix:
        changed = []
        for path in files:
            text = path.read_text(encoding="utf-8")
            fixed = normalize_language_table(text)
            if fixed != text:
                path.write_text(fixed, encoding="utf-8", newline="\n")
                changed.append(str(path.relative_to(ROOT)))
        print("已对齐语言表：" + ("、".join(changed) if changed else "无需改动"))
        print()
    for path in files:
        text = path.read_text(encoding="utf-8")
        keys = readme_family_frontmatter(path, text)
        if keys is not None:
            family[str(path.relative_to(ROOT))] = keys
        problems = (
            check_refs(path, text)
            + check_hygiene(path, text)
            + check_frontmatter(path, text)
            + check_language_table(path, text)
        )
        if problems:
            failed = True
            print(f"✗ {path.relative_to(ROOT)}")
            print("\n".join(problems))
    if len(set(family.values())) > 1:
        failed = True
        print("✗ README 家族 frontmatter 不一致")
        for name, keys in sorted(family.items()):
            print(f"  {name}: {list(keys)}")
    print(f"\n扫描 {len(files)} 个 Markdown 文件：{'有问题' if failed else '全部通过 ✅'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
