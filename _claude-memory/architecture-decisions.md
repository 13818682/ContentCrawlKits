---
name: architecture-decisions
description: 技术架构关键决策 — 技术选型、模块划分、与PRD追溯关系
metadata: 
  node_type: memory
  type: project
  originSessionId: f91804ee-7b2f-4401-a2ca-0238c3a14db0
  modified: 2026-07-31T16:22:41.157Z
---

## 技术选型

- 采集引擎: MediaCrawler (Python+Playwright)，开源多平台爬虫
- 后端: FastAPI (Python 3.11+)
- 数据库: MySQL 8.0 (业务数据) + Milvus (向量检索) + Redis 7 (缓存/队列)
- 文件存储: MinIO
- NLP: tao-8k 中文Embedding (768维)
- LLM: 豆包(主力)/智谱清言(备用)，按量计费
- 前端: Vue 3 + Vite
- 部署: Docker Compose

## 七模块架构

1. 采集调度服务 → PRD P0-01
2. 语义分析服务(去重+聚类+标签) → PRD P0-02, P0-03
3. AI内容生成引擎(RAG增强+合规标识) → PRD P0-04, P0-05, P0-07
4. 内容管理工作台 → PRD P0-06
5. 分发调度服务 → PRD P1-02
6. 数据反馈服务 → PRD P1-03
7. 管理后台(Web UI)

## 两条落地路径

- 路径A(零代码): 商用工具套装，~¥626/月，1人运营30+账号
- 路径B(自建): 开源组件+Docker部署，数据私有化，可SaaS化

**Why:** 轻量化渐进式策略——MVP用开源组件快速验证，降低初期投入；架构预留SaaS扩展能力，长期可商业化。

**How to apply:** 每个技术模块绑定对应PRD章节实现双向追溯。参见 docs/tech-design.md。[[project-overview]] [[competitor-analysis]]
