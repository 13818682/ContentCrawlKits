#!/usr/bin/env bash
# 备份 Claude Code 环境 + 项目媒体（含 API 密钥，请勿上传公开仓库）
# 用法：bash backup-claude-env.sh
# 产出：E:/1.HSEE/迁移备份/claude-env-<日期>.tar.gz   （Claude Code 环境 + 记忆 + 会话）
#       E:/1.HSEE/迁移备份/project-videos-<日期>.tar.gz（docs 下 mp4 等媒体，不入 git）
set -euo pipefail

STAMP="$(date +%Y%m%d)"
BACKUP_ROOT="E:/1.HSEE/迁移备份"
STAGE="$BACKUP_ROOT/_staging_$STAMP"
ENV_ARC="$BACKUP_ROOT/claude-env-$STAMP.tar.gz"
MEDIA_ARC="$BACKUP_ROOT/project-videos-$STAMP.tar.gz"
PROJ="E:/1.HSEE/6.ContentCrawlKits"
PM="$HOME/.claude/projects/E--1-HSEE-6-ContentCrawlKits"

mkdir -p "$STAGE/claude-config/plugins" "$STAGE/project-memory" "$STAGE/project-sessions"

# --- 1) Claude Code 全局配置 ---
cp "$HOME/.claude/settings.json"          "$STAGE/claude-config/settings.json"
cp "$HOME/.claude/settings.local.json"    "$STAGE/claude-config/settings.local.json"
cp "$HOME/.claude/.mcp.json"              "$STAGE/claude-config/.mcp.json"
cp "$HOME/.claude.json"                   "$STAGE/claude-config/claude-json-full-backup.json"
[ -d "$HOME/.claude/agents" ] && cp -r "$HOME/.claude/agents" "$STAGE/claude-config/agents"
[ -d "$HOME/.claude/skills" ] && cp -r "$HOME/.claude/skills" "$STAGE/claude-config/skills"
[ -d "$HOME/.agents/skills" ] && cp -r "$HOME/.agents/skills" "$STAGE/claude-config/agents-skills"
[ -d "$HOME/.claude/rules" ] && cp -r "$HOME/.claude/rules" "$STAGE/claude-config/rules"
[ -f "$HOME/.claude/plugins/installed_plugins.json" ] && cp "$HOME/.claude/plugins/installed_plugins.json" "$STAGE/claude-config/plugins/"
[ -f "$HOME/.claude/plugins/known_marketplaces.json" ] && cp "$HOME/.claude/plugins/known_marketplaces.json" "$STAGE/claude-config/plugins/"
[ -d "$HOME/.claude/plugins/data" ] && cp -r "$HOME/.claude/plugins/data" "$STAGE/claude-config/plugins/data"
# 备用模型档位配置
for f in "$HOME"/.claude/settings\ -\*.json; do
  [ -e "$f" ] && cp "$f" "$STAGE/claude-config/" || true
done

# --- 2) 本项目记忆与会话历史 ---
cp -r "$PM/memory" "$STAGE/project-memory/memory"
cp "$PM"/*.jsonl "$STAGE/project-sessions/" 2>/dev/null || true

# --- 3) 打环境包 ---
cd "$BACKUP_ROOT"
tar -C "$STAGE" -czf "claude-env-$STAMP.tar.gz" .

# --- 4) 打媒体包（docs 下的视频，不入 git） ---
cd "$PROJ"
find docs -type f \( -iname '*.mp4' -o -iname '*.mp3' -o -iname '*.mov' -o -iname '*.avi' -o -iname '*.mkv' \) > "$STAGE/media-list.txt"
cd "$BACKUP_ROOT"
if [ -s "$STAGE/media-list.txt" ]; then
  tar -C "$PROJ" -czf "project-videos-$STAMP.tar.gz" -T "$STAGE/media-list.txt"
else
  echo "（无媒体文件，跳过媒体包）"
  touch "project-videos-$STAMP.tar.gz"
fi

rm -rf "$STAGE"
echo ""
echo "备份完成："
ls -lh "$BACKUP_ROOT/claude-env-$STAMP.tar.gz" "$BACKUP_ROOT/project-videos-$STAMP.tar.gz"
echo ""
echo "提示：备份含 API 密钥，仅限本机使用，勿上传任何公开位置。"
