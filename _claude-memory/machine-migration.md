---
name: machine-migration
description: 迁移到新电脑的计划与 Claude Code 环境清单（GitHub 私有仓库 ContentCrawlKits）
metadata: 
  node_type: memory
  type: project
  originSessionId: def5d2de-c606-4c61-a075-c999db6c642c
  modified: 2026-08-29T15:31:53.938Z
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

关联：[[content-creation-progress]] [[file-naming-convention]] [[model-config]]
