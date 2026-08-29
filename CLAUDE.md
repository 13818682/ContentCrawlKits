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

```
.
├── CLAUDE.md                                          # This file
├── HSEE-Content-Script（内容创作）.txt                  # Original project brief / requirements
├── script.txt                                         # Empty (placeholder)
├── 1.设计思路及规划/                                    # Design & planning documents
│   ├── 深圳中考志愿填报垂直AI自动化创作平台完整方案.md    # Full platform architecture (7 modules)
│   ├── 深圳中考志愿填报AI自动化内容平台落地全套可复制执行清单.md  # Executable checklist, tool lists, prompt templates
│   ├── MediaCrawler（NanmiCoder_MediaCrawler）完整介绍文档.md  # MediaCrawler tool introduction
│   ├── MediaCrawler 全解：支持采集范围、完整部署步骤、实操采集流程.md  # MediaCrawler deployment & usage guide
│   ├── 建设方案-自媒体内容自动化创作平台-完整方案.md   # Construction plan with feasibility & cost estimation
│   └── 验证阶段-低成本试跑实施细则.md               # 8-week validation SOP with tool comparison & HSEE data integration
└── docs/                                              # Structured output documents (mcp-docs managed)
    ├── 01-PRD-深圳中考志愿填报AI自动化内容平台.md         # Business PRD with competitor analysis, P0-P2, metrics, compliance
    ├── 02-tech-design-深圳中考志愿填报AI自动化内容平台.md  # Technical design with DB, API, architecture, deployment
    ├── 03-内容策略与创作框架-深圳中考志愿填报（合订本）.md  # Content strategy & creation framework: 5 pillars × 35+ topics × keyword map × annual calendar (merged from 03+03A)
    └── 03-内容创作-深圳中考志愿填报/                    # Content writing workspace: 1 overview + 3 phases (24 dirs), each topic dir stores draft articles
    ├── 04-内容发布合规检查清单.md                        # AI content labeling regulations, content red lines, pre-publish checklist
    ├── 05-2026深圳中考政策变化与热点日历.md              # Monthly policy calendar with content topic planning for the full year
    ├── 06-学校介绍内容变形指南.md                        # How to transform 180 school MD files into platform-specific content, data enhancement SOP
    └── 07-竞品内容生态调研.md                           # Competitor content landscape scan across 5 platforms, gap analysis, differentiation strategy
    ├── 08-九大平台文案撰写要求说明书.md                    # 9-platform copywriting guide: user profiles, writing rules, title formulas, tone, and ready-to-use AI prompts per platform
    ├── 09-工具链使用手册-市场调研与文案撰写.md              # MCP toolchain & skills handbook: two-scenario command reference with D类家长 case study
    ├── 10-发布素材自动化方案.md                            # Publish-asset automation plan: draft MD → 9-platform publish assets (copy/data-chart/cover/video), per-platform checklist, tool selection, cost
    ├── 11-视频制作与分发SOP.md                             # Video production & distribution SOP: 口播脚本→剪映/智影→蚁小二, per-platform script params, publish schedule
    ├── 12-细分市场内容专区规划.md                            # Segment content zones: 4 audience zones (D类/临界生/区域/AC类), tag+index organization, 四象限话术矩阵
    ├── 13-1-公众号内容生产提示词模板（精简版·极简版·长图·插图）.md  # WeChat template: 精简版/极简版/长图/插图 prompt templates with naming rules & verification
    ├── 13-2-今日头条号内容生产提示词模板（长文·微头条·长图·插图）.md  # Toutiao template: 长文/微头条/配图 prompt templates, file naming rules, docx via external tool
    ├── 13-3-小红书内容生产提示词模板（合集规划·笔记·配图·合规）.md  # XHS template: 合集规划/单篇笔记/首图配图/合规, S1合集12篇
    └── 13-4-抖音口播视频内容生产提示词模板（口播脚本·视频制作·分发）.md  # Douyin template: 口播脚本/剪映图文成片/智影数字人/蚁小二, S1合集10条
    └── 13-5-知乎内容生产提示词模板（回答·想法·配图·合规）.md  # Zhihu template: 回答+想法双件套, 心理旅程撰写思路, 1600×900/1080×1080配图
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

## Working with Design Docs

The planning documents in `1.设计思路及规划/` are the authoritative source for:
- Full platform module specifications
- Tool procurement and configuration lists
- AI prompt templates for each platform (小红书, 抖音, 公众号, 头条, B站)
- Content tag taxonomies
- 7-day execution SOP
- Copyright compliance checklists
- MediaCrawler deployment and configuration details
