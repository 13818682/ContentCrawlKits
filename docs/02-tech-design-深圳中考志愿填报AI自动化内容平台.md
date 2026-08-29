---
version: "1.0"
date: "2026-08-01"
author: "HSEE Content Platform Team"
status: "draft"
category: "Technical Design"
prd_ref: "./PRD-深圳中考志愿填报AI自动化内容平台.md"
---

# 深圳中考志愿填报AI自动化内容平台 — 技术方案设计

## 文档概述

本文档为《深圳中考志愿填报AI自动化内容平台PRD》的配套技术方案。每个技术模块均绑定对应PRD章节，实现**业务需求→技术实现**双向追溯。技术选型遵循「轻量化、可私有化、渐进式」原则，优先开源组件，预留SaaS化扩展能力。

---

## 1. 总体架构

### 1.1 架构全景图

```
┌──────────────────────────────────────────────────────────────────┐
│                       管理后台 (Web UI)                           │
│         选题管理 │ 内容编辑 │ 分发配置 │ 数据看板                   │
└──────────────────────────┬───────────────────────────────────────┘
                           │ REST API (FastAPI)
┌──────────────────────────┼───────────────────────────────────────┐
│                   业务服务层 (Python)                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │采集调度   │ │语义分析   │ │AI生成引擎 │ │分发调度   │           │
│  │服务      │ │服务      │ │服务      │ │服务      │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
│       │            │            │            │                   │
│  ┌────┴────────────┴────────────┴────────────┴─────┐            │
│  │              消息队列 (Redis)                     │            │
│  └─────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────────┐
│                     数据存储层                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ MySQL    │ │ Milvus   │ │ Redis    │ │ MinIO    │           │
│  │ 业务数据 │ │ 向量存储 │ │ 缓存队列 │ │ 文件存储 │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└──────────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────────┐
│                     外部依赖层                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │MediaCrawler│ │ LLM API │ │ 蚁小二   │ │ 新榜     │           │
│  │ 采集引擎  │ │豆包/智谱 │ │ 分发API  │ │ 热点API  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 技术选型总览

| 层级 | 组件 | 选型 | 理由 | 绑定PRD |
|---|---|---|---|---|
| 采集引擎 | MediaCrawler | Python + Playwright | 开源、多平台、复用浏览器登录态、低风控 | P0-01 |
| 后端框架 | FastAPI | Python 3.11+ | 异步高性能、自动OpenAPI文档、生态成熟 | P0全模块 |
| 业务数据库 | MySQL 8.0 | 关系型 | 素材/选题/用户/发布记录的结构化存储 | P0-02~P0-06 |
| 向量数据库 | Milvus Lite | 嵌入式向量存储 | 语义去重、RAG检索，tao-8k 768维向量 | P0-02, P0-05 |
| 缓存/队列 | Redis 7 | 内存缓存+消息队列 | 采集任务队列、生成任务队列、热点数据缓存 | P0-01, P0-04 |
| 文件存储 | MinIO | 对象存储 | 图片/视频素材、导出文件 | P1-01 |
| LLM API | 豆包/智谱清言 | 按量计费 | 批量文案生成、成本可控 | P0-04 |
| 前端 | Vue 3 + Vite | SPA | 管理后台轻量化，复用MediaCrawler WebUI模式 | P0-06 |
| 部署 | Docker Compose | 容器化 | 一键部署、环境一致性 | §6 部署 |
| NLP模型 | tao-8k | 中文Embedding | 768维语义向量，本地部署，数据不外流 | P0-02 |

### 1.3 模块与PRD追溯矩阵

| 技术模块 | PRD章节 | PRD需求编号 |
|---|---|---|
| §2 采集调度服务 | §3 P0-01 多平台素材采集 | P0-01 |
| §3 语义分析服务 | §3 P0-02 语义去重与聚类、P0-03 三级标签分类 | P0-02, P0-03 |
| §4 AI内容生成引擎 | §3 P0-04 AI文案批量生成、P0-05 RAG知识库 | P0-04, P0-05 |
| §5 内容管理工作台 | §3 P0-06 人工编辑工作台 | P0-06 |
| §6 合规标识模块 | §5 合规要求 C-01~C-08 | P0-07 |
| §7 分发调度服务 | §3 P1-02 多平台一键分发 | P1-02 |
| §8 数据反馈服务 | §3 P1-03 数据反馈闭环 | P1-03 |

---

## 2. 采集调度服务 (Collection Service)

**绑定PRD**: §3 P0-01 — 多平台素材采集

### 2.1 架构设计

```
┌─────────────────────────────────────────────┐
│              Collection Scheduler            │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Cron定时  │  │ 热点触发 │  │ 手动触发 │ │
│  └─────┬─────┘  └────┬─────┘  └────┬─────┘ │
│        └──────────────┼──────────────┘       │
│                       ▼                       │
│              ┌────────────────┐              │
│              │  Task Queue    │              │
│              │  (Redis List)  │              │
│              └───────┬────────┘              │
│                      ▼                       │
│  ┌───────────────────────────────────────┐  │
│  │         MediaCrawler Adapter           │  │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ │  │
│  │  │ 小红书│ │ 抖音 │ │ B站  │ │ 知乎 │ │  │
│  │  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ │  │
│  └─────┼────────┼────────┼────────┼──────┘  │
│        └────────┼────────┼────────┘         │
│                 ▼                            │
│        ┌────────────────┐                   │
│        │  Data Pipeline │                   │
│        │  清洗→标准化→入库│                   │
│        └────────────────┘                   │
└─────────────────────────────────────────────┘
```

### 2.2 核心数据模型

```sql
-- 采集任务表
CREATE TABLE collection_tasks (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    platform    VARCHAR(20) NOT NULL COMMENT '平台: xhs/douyin/bilibili/zhihu/wechat_video',
    task_type   VARCHAR(20) NOT NULL COMMENT '类型: search/creator/detail',
    keyword     VARCHAR(200) COMMENT '搜索关键词(JSON数组)',
    creator_id  VARCHAR(100) COMMENT '博主ID',
    status      VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT 'pending/running/done/failed',
    total_count INT DEFAULT 0,
    success_count INT DEFAULT 0,
    error_msg   TEXT,
    started_at  DATETIME,
    finished_at DATETIME,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 原始素材表
CREATE TABLE raw_materials (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    platform        VARCHAR(20) NOT NULL,
    source_url      VARCHAR(500) NOT NULL,
    source_id       VARCHAR(100) NOT NULL,
    title           VARCHAR(500),
    content         LONGTEXT COMMENT '正文/字幕',
    author_name     VARCHAR(200),
    author_id       VARCHAR(100),
    publish_time    DATETIME,
    like_count      INT DEFAULT 0,
    collect_count   INT DEFAULT 0,
    comment_count   INT DEFAULT 0,
    share_count     INT DEFAULT 0,
    tags            JSON COMMENT '原始标签',
    raw_json        JSON COMMENT '原始数据完整存储',
    fetch_task_id   BIGINT,
    fetch_time      DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_source (platform, source_id)
);
```

### 2.3 采集策略配置

```python
# config/collector.py
COLLECTOR_CONFIG = {
    "platforms": ["xhs", "douyin", "bilibili", "zhihu", "wechat_video"],
    "keywords": [
        "深圳中考志愿填报", "深圳指标生政策", "深圳中考一分一段表",
        "深圳公办高中录取分数线", "深圳中考冲稳保志愿搭配"
    ],
    "request_interval": 12,        # 秒，≥10s防封
    "max_per_session": 200,        # 单次采集上限
    "content_age_days": 90,        # 只抓近3个月内容
    "chrome_debug_port": 9222,     # CDP复用登录态
    "proxy_pool_enabled": False,   # IP代理池(大规模采集时启用)
    "schedule": "0 2 * * *"        # 每日凌晨2点定时采集
}
```

### 2.4 性能指标

| 指标 | 目标值 | 测量方式 |
|---|---|---|
| 单平台采集速度 | ≥20条/分钟 | 任务日志统计 |
| 采集成功率 | >95% | 抓取成功数/总数 |
| 封号率 | <1%/月 | 账号状态监控 |
| 采集延迟(热点模式) | <30分钟 | 从热点触发到数据入库 |

---

## 3. 语义分析服务 (Semantic Analysis Service)

**绑定PRD**: §3 P0-02 语义去重、P0-03 三级标签分类

### 3.1 处理流水线

```
原始素材 ──→ 基础清洗 ──→ 向量化 ──→ 去重 ──→ 聚类 ──→ 标签分类 ──→ 选题库
              │            │         │        │         │
              ▼            ▼         ▼        ▼         ▼
         过滤广告/     tao-8k    余弦相似度  K-Means   规则+模型
         低质内容     768维       >0.7判定   自动分组   三级标签
```

### 3.2 核心数据模型

```sql
-- 处理后素材表(去重+分类后)
CREATE TABLE processed_materials (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    raw_material_id BIGINT NOT NULL,
    title           VARCHAR(500),
    content         LONGTEXT,
    content_hash    VARCHAR(64) COMMENT '内容SHA256指纹',
    embedding       JSON COMMENT '768维向量(JSON存储，生产迁移至Milvus)',
    tag_l1          VARCHAR(20) COMMENT '一级标签: A/B/C',
    tag_l2          VARCHAR(10) COMMENT '二级标签: A01~C07',
    tag_l3          VARCHAR(20) COMMENT '三级标签: XHS-tip等',
    is_duplicate    BOOLEAN DEFAULT FALSE,
    duplicate_of    BIGINT COMMENT '被判定为重复，指向保留的素材ID',
    similarity_score DECIMAL(4,3) COMMENT '与保留素材的相似度',
    quality_score   INT COMMENT '质量分(互动数据加权)',
    status          VARCHAR(20) DEFAULT 'pending' COMMENT 'pending/selected/used/discarded',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 选题库表
CREATE TABLE topic_library (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    topic_name      VARCHAR(200) NOT NULL,
    tag_l1          VARCHAR(20),
    tag_l2          VARCHAR(10),
    tag_l3          VARCHAR(20),
    source_material_ids JSON COMMENT '参考素材ID列表',
    pain_points     JSON COMMENT '家长高频痛点关键词',
    reference_structure TEXT COMMENT '爆款结构参考',
    content_gap     BOOLEAN DEFAULT FALSE COMMENT '是否为内容缺口选题',
    status          VARCHAR(20) DEFAULT 'pending' COMMENT 'pending/generating/published',
    platform_target VARCHAR(50) COMMENT '适配平台',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 3.3 向量检索 (RAG知识库)

```
┌──────────────────────────────────┐
│       RAG Knowledge Base          │
│  ┌────────────────────────────┐  │
│  │  深圳中考知识库              │  │
│  │  • 历年录取分数线 (向量)    │  │
│  │  • 公办高中梯队排名 (向量)  │  │
│  │  • 指标生分配规则 (向量)    │  │
│  │  • 中考政策原文 (向量)      │  │
│  │  • 志愿批次设置规则 (向量)  │  │
│  │  • 2026最新规则 (向量)      │  │
│  └──────────────┬─────────────┘  │
│                 ▼                 │
│  ┌────────────────────────────┐  │
│  │  Milvus 向量检索引擎        │  │
│  │  • 索引类型: IVF_FLAT      │  │
│  │  • 度量: COSINE            │  │
│  │  • Top-K: 5                │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
```

### 3.4 去重准确率指标

| 场景 | 目标准确率 | 测试方法 |
|---|---|---|
| 完全重复(同URL/同标题) | 100% | 自动化测试 |
| 高度相似(同角度改写) | >95% | 人工标注200对→对比系统输出 |
| 不同角度同主题 | 不误判 | 人工审核边界case |
| 跨平台同内容 | >90% | 跨平台素材对测试 |

---

## 4. AI内容生成引擎 (Content Generation Engine)

**绑定PRD**: §3 P0-04 AI文案批量生成、P0-05 RAG知识库增强

### 4.1 生成流水线

```
选题输入 → Prompt构造 → RAG检索 → LLM生成 → 合规检测 → 格式化输出
   │           │            │           │          │           │
   ▼           ▼            ▼           ▼          ▼           ▼
三级标签  平台模板+   Milvus召回  豆包/智谱  相似度<30%  标题+正文+
         知识库注入   Top-5文档   API调用   标识嵌入    标签+元数据
```

### 4.2 Prompt管理

```sql
CREATE TABLE prompt_templates (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    platform    VARCHAR(20) NOT NULL COMMENT 'xhs/douyin/ggzh/tt/bilibili',
    system_prompt TEXT NOT NULL COMMENT '系统提示词(含身份设定)',
    user_prompt_template TEXT NOT NULL COMMENT '用户提示词模板({topic}等占位)',
    output_schema JSON COMMENT '期望输出结构',
    version     INT DEFAULT 1,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 4.3 LLM API配置

```python
# config/llm.py
LLM_CONFIG = {
    "primary": {
        "provider": "doubao",          # 豆包(主力)
        "model": "doubao-pro-32k",
        "max_tokens": 4000,
        "temperature": 0.7,
        "rate_limit": 60,              # 每分钟请求上限
    },
    "fallback": {
        "provider": "zhipu",           # 智谱清言(备用)
        "model": "glm-4",
        "max_tokens": 4000,
        "temperature": 0.7,
    },
    "retry": {
        "max_retries": 3,
        "backoff_base": 2,             # 指数退避基数(秒)
        "timeout": 60,                 # 单次请求超时(秒)
    },
    "cache": {
        "enabled": True,
        "ttl": 86400,                  # 相同prompt 24h内缓存
    }
}
```

### 4.4 生成内容数据模型

```sql
CREATE TABLE generated_contents (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    topic_id        BIGINT NOT NULL,
    platform        VARCHAR(20) NOT NULL,
    title_options   JSON COMMENT '备选标题(3个)',
    content_body    LONGTEXT NOT NULL COMMENT '正文',
    tags            JSON COMMENT '平台标签',
    prompt_template_id BIGINT,
    rag_docs_used   JSON COMMENT 'RAG检索到的参考文档ID列表',
    similarity_check DECIMAL(4,3) COMMENT '与源素材最高相似度',
    compliance_label TEXT COMMENT '合规标识文本',
    metadata_json   JSON COMMENT '隐式标识元数据',
    status          VARCHAR(20) DEFAULT 'draft' COMMENT 'draft/reviewed/published',
    editor_id       BIGINT COMMENT '编辑人ID',
    edited_content  LONGTEXT COMMENT '人工润色后版本',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 4.5 合规标识注入

```python
# 按《人工智能生成合成内容标识办法》实施
def inject_compliance_label(content: str, platform: str, meta: dict) -> dict:
    """为AI生成内容注入显式标识和隐式标识"""
    return {
        # 显式标识 (第4条)
        "explicit_label": {
            "text": "⚠️ 本内容由AI辅助生成，数据来源为深圳教育局公开信息",
            "position": "end",  # 文末
            "style": "subtitle" if platform in ("douyin", "sph") else "text"
        },
        # 隐式标识 (第5条) — 写入文件元数据
        "implicit_metadata": {
            "ai_generated": True,
            "provider_code": "HSEE-CCP-001",
            "content_id": meta["content_id"],
            "generation_model": "doubao-pro-32k",
            "timestamp": meta["created_at"]
        }
    }
```

### 4.6 生成质量指标

| 指标 | 目标值 | 测量方式 |
|---|---|---|
| 单篇生成耗时 | <30秒 | API响应日志 |
| 批量生成吞吐 | >100篇/小时 | 队列消费速率 |
| 生成可用率(无需人工重写) | >70% | 编辑审核通过率 |
| RAG事实准确率 | >95% | 数据引用的逐条核验 |

---

## 5. 内容管理工作台 (Content Workbench)

**绑定PRD**: §3 P0-06 人工编辑工作台

### 5.1 API设计

```
POST   /api/v1/topics              # 创建选题
GET    /api/v1/topics              # 选题列表(支持标签/状态/平台筛选)
POST   /api/v1/topics/{id}/generate # 触发AI生成
GET    /api/v1/contents            # 内容列表
GET    /api/v1/contents/{id}       # 内容详情
PUT    /api/v1/contents/{id}       # 编辑内容(人工润色)
POST   /api/v1/contents/{id}/review # 提交审核
POST   /api/v1/contents/{id}/publish # 发布(触发分发+合规检测)
DELETE /api/v1/contents/{id}       # 删除内容

# 编辑工作台特有
GET    /api/v1/workbench/stats     # 工作台统计(今日产出/待审核/已发布)
GET    /api/v1/workbench/queue     # 待处理队列
PUT    /api/v1/contents/{id}/data  # 嵌入数据表格(分数线/学校对比)
POST   /api/v1/contents/{id}/case  # 插入真实案例
```

### 5.2 前端路由

```
/workbench              # 工作台首页(统计卡片)
/workbench/topics       # 选题管理
/workbench/topics/:id   # 选题详情→触发生成
/workbench/contents     # 内容列表(按状态筛选)
/workbench/editor/:id   # 编辑器(分屏: AI原稿|编辑区|预览)
/workbench/publish      # 发布管理(合规检测状态)
/dashboard              # 数据看板
```

---

## 6. 分发调度服务 (Distribution Service)

**绑定PRD**: §3 P1-02 多平台一键分发 (V1.1)

### 6.1 分发流水线

```
内容审核通过 → 合规终检 → 平台适配 → 排期入队 → API分发 → 结果回传
                  │           │          │          │          │
                  ▼           ▼          ▼          ▼          ▼
             相似度<30%  标题/标签/  各平台    蚁小二/    发布链接
             标识注入     封面适配   高峰时段  易媒API   状态记录
```

### 6.2 分发数据模型

```sql
CREATE TABLE publish_records (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    content_id      BIGINT NOT NULL,
    platform        VARCHAR(20) NOT NULL,
    publish_url     VARCHAR(500),
    publish_status  VARCHAR(20) DEFAULT 'pending' COMMENT 'pending/success/failed',
    scheduled_at    DATETIME COMMENT '计划发布时间',
    published_at    DATETIME COMMENT '实际发布时间',
    error_msg       TEXT,
    metrics_json    JSON COMMENT '发布后数据回传(播放/收藏/评论)',
    metrics_updated_at DATETIME,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 平台账号管理
CREATE TABLE platform_accounts (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    platform        VARCHAR(20) NOT NULL,
    account_name    VARCHAR(100),
    account_level   VARCHAR(20) COMMENT 'head/mid/small (头部/中部/小号)',
    cookie_token    TEXT COMMENT '加密存储的登录凭证',
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 6.3 分时段发布策略

```python
PLATFORM_SCHEDULE = {
    "xhs":    ["12:30", "20:00"],           # 小红书午间+晚间
    "douyin": ["19:00-21:00"],              # 抖音晚高峰
    "ggzh":   ["Tue 12:00", "Fri 12:00"],   # 公众号周二/五
    "tt":     ["08:00", "18:00"],            # 头条早晚
    "bilibili": ["12:00", "19:00"],          # B站午间+晚间
}
```

---

## 7. 数据反馈服务 (Feedback Service)

**绑定PRD**: §3 P1-03 数据反馈闭环 (V1.1)

### 7.1 反馈闭环

```
┌──────────────────────────────────────────────────────┐
│                   Feedback Loop                       │
│                                                       │
│  发布数据回传 ──→ 指标计算 ──→ 权重调整 ──→ 选题推荐  │
│       │              │             │            │      │
│       ▼              ▼             ▼            ▼      │
│  播放/收藏/     互动率/       高流量主题     下一周期   │
│  评论/分享      转化率        加权生产       选题输出   │
└──────────────────────────────────────────────────────┘
```

### 7.2 选题权重算法（简化版）

```python
def calculate_topic_weight(topic_id: int) -> float:
    """基于历史发布数据计算选题权重"""
    records = get_publish_records(topic_id, days=30)
    if not records:
        return 1.0  # 新品默认权重

    engagement = sum(
        r.likes * 1.0 +
        r.collects * 2.0 +       # 收藏权重加倍(实用性标志)
        r.comments * 3.0 +       # 评论权重最高(互动深度)
        r.shares * 8.0           # 分享权重最高(传播力)
        for r in records
    )
    avg_engagement = engagement / len(records)

    # 对数归一化到 [0.5, 2.0]
    return max(0.5, min(2.0, 1.0 + math.log10(avg_engagement + 1) / 3))
```

---

## 8. 容错与高可用设计

### 8.1 容错策略

| 故障场景 | 检测方式 | 恢复策略 | 影响范围 |
|---|---|---|---|
| MediaCrawler采集失败 | 任务状态监控+心跳 | 3次指数退避重试，超限后切换备用商用工具 | 单平台、单次采集 |
| LLM API超时/限流 | 请求超时+HTTP 429 | 指数退避重试(2s→4s→8s)，超限切换备用模型(智谱) | 单篇生成 |
| 数据库连接中断 | 连接池心跳检测 | 自动重连，连接池预热 | 全部服务(短暂) |
| Redis队列积压 | 队列长度监控 | 消费者自动扩容(最多3实例)，积压告警 | 采集/生成延迟 |
| 分发API失败 | HTTP状态码 | 3次重试，失败标记+人工介入 | 单平台、单次分发 |
| 磁盘空间不足 | 磁盘使用率监控 | 自动清理7天前日志+30天前临时文件 | 全系统 |

### 8.2 限流与降级

```python
# API限流配置
RATE_LIMIT = {
    "collection":  {"max_per_min": 5, "max_per_hour": 60},   # 采集接口
    "generation":  {"max_per_min": 10, "max_per_hour": 200}, # 生成接口
    "publish":     {"max_per_min": 3, "max_per_hour": 30},   # 分发接口
}

# 服务降级策略
DEGRADATION = {
    "level_1": {  # CPU>80%或内存>85%
        "actions": ["暂停非紧急采集任务", "生成队列限速50%"],
    },
    "level_2": {  # 数据库连接池耗尽
        "actions": ["只读模式", "暂停所有写入操作", "告警通知"],
    },
    "level_3": {  # 核心依赖不可用
        "actions": ["切换备用LLM", "切换备用采集工具", "暂停分发"],
    },
}
```

### 8.3 健康检查端点

```
GET /health              # 基础健康检查(200 OK)
GET /health/ready        # 就绪检查(DB+Redis+Milvus连通性)
GET /health/live         # 存活检查
GET /health/dependencies # 外部依赖检查(LLM API/采集引擎/分发API)
```

---

## 9. 安全设计

### 9.1 安全措施

| 层面 | 措施 | 说明 |
|---|---|---|
| 传输 | HTTPS | 所有API通信加密 |
| 认证 | JWT + 刷新Token | 管理后台登录，24h过期 |
| 授权 | RBAC | 管理员/编辑/只读三种角色 |
| 数据 | AES-256加密 | 平台账号cookie/密钥加密存储 |
| 审计 | 操作日志 | 所有编辑/发布/删除操作记录 |
| API | 限流+IP白名单 | 管理API限流，分发API可配白名单 |
| 依赖 | 定期CVE扫描 | `pip-audit` + GitHub Dependabot |

### 9.2 RBAC权限矩阵

| 操作 | 管理员 | 编辑 | 只读 |
|---|---|---|---|
| 查看选题/内容 | ✅ | ✅ | ✅ |
| 创建选题 | ✅ | ✅ | ❌ |
| 触发AI生成 | ✅ | ✅ | ❌ |
| 编辑内容 | ✅ | ✅ | ❌ |
| 删除内容 | ✅ | ❌ | ❌ |
| 发布内容 | ✅ | ✅(需审批) | ❌ |
| 配置采集任务 | ✅ | ❌ | ❌ |
| 管理平台账号 | ✅ | ❌ | ❌ |
| 查看数据看板 | ✅ | ✅ | ✅ |

---

## 10. 部署方案

### 10.1 Docker Compose 一键部署

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: ./backend
    ports: ["8080:8080"]
    environment:
      - DATABASE_URL=mysql://user:pass@mysql:3306/hsee_content
      - REDIS_URL=redis://redis:6379
      - MILVUS_URL=http://milvus:19530
    depends_on: [mysql, redis, milvus]

  worker_collector:
    build: ./backend
    command: celery -A tasks.collector worker -Q collector
    depends_on: [redis, mysql]

  worker_generator:
    build: ./backend
    command: celery -A tasks.generator worker -Q generator
    depends_on: [redis, mysql, milvus]

  webui:
    build: ./frontend
    ports: ["5173:5173"]
    depends_on: [api]

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: hsee_content
    volumes: [mysql_data:/var/lib/mysql]

  redis:
    image: redis:7-alpine
    volumes: [redis_data:/data]

  milvus:
    image: milvusdb/milvus:v2.3.0
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    depends_on: [etcd, minio]

  etcd:
    image: quay.io/coreos/etcd:v3.5.5

  minio:
    image: minio/minio:latest
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}

volumes:
  mysql_data:
  redis_data:
```

### 10.2 硬件要求

| 环境 | 规格 | 用途 |
|---|---|---|
| 最小开发环境 | 4核8G + 50G SSD | Docker Compose全栈 |
| 推荐生产环境 | 8核16G + 200G SSD | 含Milvus向量检索 |
| GPU加速(可选) | NVIDIA T4 16G | tao-8k推理加速(不必须) |

### 10.3 环境变量

```bash
# .env (不提交至Git)
MYSQL_ROOT_PASSWORD=xxx
MINIO_ROOT_PASSWORD=xxx
DOUBAO_API_KEY=xxx
ZHIPU_API_KEY=xxx
YIXIAOER_API_KEY=xxx      # 蚁小二分发API
XINBANG_API_KEY=xxx        # 新榜热点API
JWT_SECRET=xxx
ENCRYPTION_KEY=xxx         # 平台凭证加密密钥
```

---

## 11. 监控与运维

### 11.1 关键监控指标

| 类别 | 指标 | 告警阈值 |
|---|---|---|
| 采集 | 采集成功率、任务耗时 | 成功率<90%、耗时>2x均值 |
| 生成 | LLM API延迟、生成失败率 | P99延迟>60s、失败率>10% |
| 分发 | 分发成功率 | <95% |
| 系统 | CPU、内存、磁盘、DB连接数 | CPU>80%、磁盘>85% |
| 业务 | 日内容产出、合规检测拦截率 | 产出<目标值的50% |

### 11.2 日志规范

```json
{
  "timestamp": "2026-08-01T02:00:00.000Z",
  "level": "INFO",
  "service": "collection",
  "trace_id": "uuid",
  "event": "task_completed",
  "platform": "xhs",
  "keyword": "深圳中考志愿填报",
  "fetched_count": 85,
  "duration_ms": 12345
}
```

---

## 12. 迭代路线

| 版本 | 时间 | 交付内容 | 绑定PRD |
|---|---|---|---|
| MVP (v0.5) | 第1-2周 | 采集+去重+标签+手动生成验证 | P0-01, P0-02, P0-03 |
| v1.0 | 第3-4周 | AI批量生成+RAG+编辑工作台+合规标识 | P0-04~P0-07 |
| v1.1 | 第2个月 | 视频自动生成+多平台分发+数据反馈 | P1-01~P1-03 |
| v1.2 | 第3个月 | 热点响应+选题面板+合规检测自动化 | P1-04~P1-06 |
| v2.0 | 第4-6个月 | SaaS化多租户+A/B测试+评论分析 | P2-01~P2-04 |

---

> **追溯验证**: 每个技术模块(§2~§7)均标注了对应的PRD章节和需求编号。详见§1.3追溯矩阵。
