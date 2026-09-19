# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## MCP Tool Dispatch Rules (Session-Standing, Take Precedence)

These rules govern every session in this repository. All MCP tools are automatically chained per task phase.

### 1. Information Priority

```
claude-mem (long-term memory) > local files (fs / docx-reader / doc-convert) > firecrawl (web search)
```

- Never re-fetch the same URL or re-read the same file within a session.
- Check claude-mem first for prior research before hitting the network.

### 2. Task-Phase → MCP Mapping

| Phase / Need | MCP Tool | Constraint |
|---|---|---|
| Industry, competitor, or compliance research gaps | `firecrawl` | Max 3 effective pages per search; extract only core conclusions, do NOT carry full page text into context |
| Word / PDF business source materials | `docx-reader` / `doc-convert` | Parse and fuse with original business requirements |
| Architecture, performance, or component spec verification | `context7` | Quantified, actionable metrics from official docs |
| Output documents: market analysis, PRD, technical design | `mcp-docs` | Write to `./docs/` with Markdown hierarchy and YAML version header |
| Simple file reads, temp attachments | `fs` | Do NOT use `mcp-docs` for plain file I/O |

### 3. Closed-Loop Workflow

- **Phase 1 (Market Research)** complete → auto-archive conclusions to `claude-mem` long-term memory.
- **Phase 2 (Business PRD)** complete → auto self-check for completeness: quantitative metrics, acceptance criteria, priority ordering, compliance constraints.
- **Phase 3 (Technical Design)** — every technical decision must bind to a corresponding PRD business section, ensuring bidirectional traceability and full requirement coverage.

### 4. Token Throttling

- Full webpages, PDFs, and raw business files do NOT persist in context.
- After each major phase, trim redundant content; retain only core conclusions.
- No unbounded loop tool calls — each invocation must have a clear termination condition.

### 5. Tool Isolation

- `mcp-docs` → professional Markdown document editing only
- `context7` → technical specification / API / library documentation queries only
- `firecrawl` → web research only
- `fs` → plain file reads and temporary attachment handling only
- Each tool stays in its lane; never substitute one for another's purpose.

---

## Project Overview

深圳中考志愿填报垂直AI自动化内容平台 — a vertical AI-automated content creation platform targeting the Shenzhen high school exam volunteer application (中考志愿填报) niche. The platform covers the full content lifecycle: multi-platform scraping → semantic deduplication & classification → AI content generation with RAG → multi-modal production → cross-platform distribution → data-driven iteration.

**Current phase:** Planning and design. No code has been written yet.

## Repository Structure

**权威设计源**：`1.设计思路及规划/` —— 完整方案(7模块) / 可复制执行清单 / MediaCrawler 介绍+部署 / 建设方案(可行性&成本) / 8周验证SOP。该目录是下列内容的唯一权威出处：模块规格、工具采购清单、各平台 AI 提示词模板(小红书/抖音/公众号/头条/B站)、内容标签分类、7天执行 SOP、版权合规清单、MediaCrawler 部署细节。

```
CLAUDE.md                            # 本文件
HSEE-Content-Script（内容创作）.txt     # 原始需求书
1.设计思路及规划/                      # 见上「权威设计源」
docs/                                # 结构化产出（mcp-docs 管理）
├── 00-产品-平台PRD与技术/            # 01-PRD 业务说明书 / 02-tech-design 技术方案
├── 01-策划-内容策略与生产方案/         # 03 内容策略合订本 / 05 政策日历 / 06 学校变形指南 / 07 竞品调研 / 09 工具链手册 / 10 发布素材自动化 / 11 视频制作分发SOP / 12 专区规划
├── 02-规范-平台文案与发布约束/         # 04 合规清单 / 04A 公众号搜一搜 / 08 九大平台文案 / 13-1~13-5 各平台提示词模板 / 16 跨平台复用边界 / 17 知乎纪律 / 19 一稿多载体发布规范
├── 03-内容创作/                     # 创作工作区·**城市一级维度**：SZ深圳/ DG东莞/ GZ广州/ FS佛山/ + 00-城市域说明.md
│   └── SZ深圳/                      # 深圳全部创作资产（1407 文件）：P1-政策解码器 / P2-降分通道 / P3-数据择校地图 / P4-志愿填报作战室 / P5-录取后行动指南 / S1-基本态势 / 问答专区
├── 12-专区/                         # 细分市场专区索引（配合 策划目录 12-专区规划）
├── 14-运营管理/                     # A-已办结存档-主体注册 / B-策划与决策 / C-日常运营；入口 00-运营路线图-总览.md
└── 15-运营数据/                     # 运营数据归档（**按城市/周**：SZ深圳/ DG东莞/ GZ广州/ FS佛山/ _统一号/）
```

## Architecture (from design docs)

The platform is designed as a 7-module pipeline:

1. **采集层 (Collection)** — Multi-source scraping via MediaCrawler (open-source, Python+Playwright) covering 小红书/抖音/B站/知乎/微博/视频号/快手, plus official education bureau websites
2. **清洗语义分析层 (Cleaning & Semantic Analysis)** — Text cleaning, dual-layer dedup (URL + semantic vector similarity >0.7), auto-clustering via K-Means, three-level tag system
3. **选题库管理层 (Topic Library)** — Notion/飞书多维表格 for managing topics, content gaps, and production status
4. **AI内容生成层 (AI Generation)** — Batch generation via 豆包/智谱 API with RAG on a Shenzhen-specific knowledge base (policies, school tiers, historical admission scores)
5. **多模态制作层 (Multi-modal Production)** — Auto-generate images, short videos (剪映/腾讯智影 digital human), platform-specific format adaptation
6. **全域分发层 (Distribution)** — One-click multi-platform publishing via 蚁小二/易媒助手 API
7. **数据反馈层 (Feedback Loop)** — Engagement data collection → topic weight adjustment → content optimization

## Two Implementation Paths

- **Path A (Low-code):** Commercial SaaS tools (熊猫工坊, 优采云, Kimi/豆包, 剪映, 蚁小二) — ~¥500/month, 1 person can operate 30+ accounts
- **Path B (Self-built):** MediaCrawler + self-deployed NLP (tao-8k embeddings) + LLM API + RAG + custom admin panel — full data ownership, can be commercialized as SaaS

## Key Design Decisions

- Content is organized into a **three-phase lifecycle**: 前期政策科普 (Mar-May) → 中期填报实操 (Jun-Jul) → 后期录取复盘 (Jul-Aug)
- **Three-level tag system**: Phase tag → Business topic tag (e.g., B03 冲稳保梯度) → Platform+format tag (e.g., XHS-tip, DY-template)
- **70/30 content split**: AI generates 70% skeleton, human editors add 30% local data and real cases
- **Compliance is critical**: Semantic similarity vs source must stay below 30%, scraped content is for reference only, never directly republished

## 运营管理与数据归档（自 2.内容管理及运营 并入）

本仓现在同时承担**内容生产侧**（docs/ 的00-产品-平台PRD与技术 / 01-策划-内容策略与生产方案 / 02-规范-平台文案与发布约束 / 03-内容创作，深圳内容在 `03-内容创作/SZ深圳/`，见上）与**运营管理侧**（docs/14-运营管理、docs/15-运营数据）。原 `E:\1.HSEE\2.内容管理及运营` 已并入，统一知识、记忆与 git 版本管理。

**多城市（2026-09-19 起）**：创作域与运营数据域均已立**城市一级维度**（`SZ深圳 / DG东莞 / GZ广州 / FS佛山`）。
- **派生新城市前必读** `docs/03-内容创作/00-城市域说明.md` —— 深圳树是单城硬编码（411 个文件名带「深圳」、145 个脚本写死深圳文案、**76 个脚本写死深圳绝对输出路径**），**禁止整树复制**，否则误跑脚本会覆盖深圳已发布配图。
- **深圳迁移已完成（2026-09-19）**：旧址 `03-内容创作-深圳中考志愿填报/` 整树并入 `03-内容创作/SZ深圳/`（1407 文件无损，全仓 314 处引用已同步）。**仍挂账**：`01/02` 共享层参数化、76 个脚本拆绝对路径——见 `00-城市域说明.md` §五。

**权威运营文档**（docs/14-运营管理/，先读 `00-运营路线图-总览.md` 再动笔）：
- 变现主体策略：**个体户先行 → 主体变更升级为公司**（走「主体变更」保 AppID/OpenID/用户数据，勿走「主体迁移」；变更前个体户保持存续不注销）
- 多城市扩张：深圳先行（跑通闭环）→ 东莞 → 广州，**原定 3 城**；用户 2026-09-19 提出**四城并联（加佛山）**——但 `方案-2026-006` 排期仍是三城且佛山不在其列，**该变更待经营者拍板，本仓不代为变更**（见 `docs/03-内容创作/FS佛山/00-FS佛山-城市清单.md`）
- 关键数字：第一年成本 ¥2000–8000；深圳个体户注册 ¥1000–2500；盈亏平衡 15–50 付费用户/年
- 9 平台矩阵：公众号/B站/小红书/抖音/头条/微博/知乎/快手/百度贴吧

**运营数据归档**（docs/15-运营数据/，**按城市/周分目录**：`SZ深圳/ DG东莞/ GZ广州/ FS佛山/ _统一号/`，见 `00-运营数据归档说明.md`）：
- 每周分析报告（跨平台对比 + 平台适配性 + 发布时间建议），报告即模板，下周围绕同口径对比
- 北极星指标：**抖音完播率**、**小红书获粉转化率**（首周基线：抖音完播 6%、小红书观看 2,746→净增粉 42）
- **北极星按城独立建基线**——深圳现值（抖音完播 3.1%、小红书主页访客 23/周）**只对深圳成立，不可套用其他城市**
- 战略判断（2026-08 基线）：小红书=获客主阵地；抖音=需改原生内容形态（停止图文直投）；公众号=搜一搜 SEO 资产；头条=低门槛放量；知乎=待问答化；**B站暂不做引流，设触发条件后再进**
- 每周报告归档后，将关键结论沉淀到长期记忆（weekly-operations-*）
