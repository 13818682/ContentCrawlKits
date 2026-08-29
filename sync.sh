#!/usr/bin/env bash
# 一键同步：刷新记忆快照(_claude-memory/) → git add → commit → push
# 用法：bash sync.sh "可选的提交说明"
#       不带参数时用默认说明；push 失败时改动已留在本地，重跑即可。
set -euo pipefail

PROJ="$(cd "$(dirname "$0")" && pwd)"
MSG="${*:-sync: 内容与记忆更新}"

cd "$PROJ"

# 1) 找到本机该项目对应的 auto-memory 目录（目录名由项目路径编码生成，用模糊匹配）
MEMDIR="$(find "$HOME/.claude/projects" -maxdepth 2 -type d -path '*ContentCrawlKits*memory*' 2>/dev/null | head -1 || true)"
if [ -n "$MEMDIR" ]; then
  rm -rf _claude-memory
  mkdir -p _claude-memory
  cp -r "$MEMDIR/." _claude-memory/
  echo "✓ 记忆快照已更新（$(cygpath -w "$MEMDIR" 2>/dev/null || echo "$MEMDIR")）"
else
  echo "! 未找到本机 auto-memory 目录，跳过记忆同步"
fi

# 2) 暂存全部改动（含 sync.sh 自身、docs、_claude-memory 等）
git add -A

# 3) 无改动则退出
if git diff --cached --quiet; then
  echo "工作区已是最新，无需提交。"
  exit 0
fi

# 4) 提交并推送
git commit -q -m "$MSG"
echo "✓ 已提交：$MSG"
if git push -q origin HEAD; then
  echo "✓ 已推送 origin/$(git branch --show-current)"
else
  echo "! push 失败：改动已本地提交，稍后重跑 bash sync.sh 或检查网络/凭据。"
  exit 1
fi
