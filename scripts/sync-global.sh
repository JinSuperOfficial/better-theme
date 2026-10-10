#!/usr/bin/env bash
# 把本仓库同步到全局 DSH 技能目录，随时可用（默认 ~/.dsh/skills/better-theme）
#
#   ./scripts/sync-global.sh            # 同步
#   ./scripts/sync-global.sh --dry-run  # 只看会改哪些文件
#   DSH_SKILLS_DIR=/path/to/skills ./scripts/sync-global.sh
#
# 只做同步，不删除源仓库内容；--delete 仅清理目标目录里的残留文件。
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${DSH_SKILLS_DIR:-$HOME/.dsh/skills}"
DEST="$SKILLS_DIR/better-theme"
DRY=0
[[ "${1:-}" == "--dry-run" ]] && DRY=1

if ! grep -q '^name: better-theme' "$SRC/SKILL.md"; then
  echo "✗ $SRC/SKILL.md 的 frontmatter 不是 better-theme，中止" >&2
  exit 1
fi

echo "源  ：$SRC"
echo "目标：$DEST"

RSYNC=(rsync -a --delete --exclude '.git/' --exclude '.obsidian/')

if (( DRY )); then
  "${RSYNC[@]}" --dry-run --itemize-changes "$SRC/" "$DEST/"
  echo "（dry-run：未写入任何文件）"
  exit 0
fi

mkdir -p "$DEST"
"${RSYNC[@]}" "$SRC/" "$DEST/"

# 同步后跑一遍文档卫生检查，避免把断链装进全局
if command -v python3 >/dev/null 2>&1; then
  python3 "$DEST/scripts/check-refs.py"
fi

echo "✅ 已同步到 $DEST（DSH 会热加载，技能列表无需重启）"
