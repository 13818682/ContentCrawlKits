---
name: machine-migration
description: 迁移到新电脑的计划与 Claude Code 环境清单（GitHub 私有仓库 ContentCrawlKits）
metadata: 
  node_type: memory
  type: project
  originSessionId: def5d2de-c606-4c61-a075-c999db6c642c
  modified: 2026-08-29T15:56:38.554Z
---

2026-08 决定把本项目迁移到另一台电脑。已在 GitHub 创建私有仓库 `ContentCrawlKits`。目标：平衡切换、少损失、少时间成本。

**迁移三线：**
1. 项目主体（CLAUDE.md、docs/、1.设计思路及规划/、scripts/、txt 源文件）→ git + GitHub 私有仓库
2. Claude Code 环境 → 打包 zip 搬运：
   - 全局配置 `~/.claude/settings.json`（含 DeepSeek `ANTHROPIC_AUTH_TOKEN`，**勿入 git**）、`settings.local.json`、`agents/`、`skills/`（源头在 `~/.agents/skills/`，49 个技能约 2.9MB）
   - 插件 `~/.claude/plugins/`（installed_plugins.json、known_marketplaces.json、data/）
   - 全局 MCP 定义在 `~/.claude.json`：firecrawl / context7 带密钥，其余 npx 自动装
   - 项目级 MCP：content-production、better-writer
3. 记忆与历史 → 私有仓库放一份 `_claude-memory/`（换机时拷回 `~/.claude/projects/<key>/memory/`）；会话 jsonl 可选打包

**关键坑：**
- auto-memory 目录名由项目路径派生（当前 `E--1-HSEE-6-ContentCrawlKits`），新机项目路径若不同，目录名会变，需把 memory/ 拷到新目录名下
- 项目 `.claude/settings.local.json` 与全局 settings 含绝对路径/权限规则，跨机可能失效
- GitHub 插件 MCP 报 400（Authorization header 格式错误）、`gh` CLI 未装 → push 用 PAT 或修复 GitHub 授权

**进度（2026-08-29）：**
- 备份已产出：`E:\1.HSEE\迁移备份\claude-env-20260829.tar.gz`（13MB，含密钥勿上传）、`project-videos-20260829.tar.gz`（134MB）
- 仓库已有首次提交 `d2f467f`（526 文件），git 身份为占位 `weiwei@users.noreply.github.com`（需确认/amend）
- 仓库内已含 `_claude-memory/`（记忆快照）、`迁移到新电脑.md`（操作手册）、`backup-claude-env.sh`
- **✅ 已 push 到 GitHub**：`https://github.com/13818682/ContentCrawlKits`，main 分支同步，凭据走 Windows 凭据管理器
- **日常提交用 `bash sync.sh "说明"`**：自动刷新 `_claude-memory/`（本机最新记忆）→ commit → push，一步完成内容+记忆同步
- **换机后按 `迁移到新电脑.md` 还原**；新机 push/pull 凭据需另配（PAT 或凭据管理器）

关联：[[content-creation-progress]] [[file-naming-convention]] [[model-config]]
