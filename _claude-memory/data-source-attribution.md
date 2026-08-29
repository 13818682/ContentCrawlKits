---
name: data-source-attribution
description: "内容文案\"数据来源\"标注统一用官方来源（深圳市教育局正式发布文件），不写内部数据库表/视图名"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e6318ad8-253f-4d0f-b55e-446a5bd20cd2
  modified: 2026-08-15T04:35:53.179Z
---

深圳地区市场文案里，"数据来源"统一写官方来源，如"数据来源：深圳市教育局正式发布文件"，不要写内部数据库表名/视图名（sz_v_school_scores_timeline、sz_v_quota_summary_readable、v_school_enrollment_detail 等）。

**Why:** HSEE 数据库数据是从官方教育局网站采集清洗得到的；读者不需要、也不该看到内部表名。官方来源标注建立信任（PRD Layer 1 数据可信），内部表名反而泄露实现细节、降低可信度。

**How to apply:** 对外文案的"数据来源"footnote 统一写官方来源（"数据来源：深圳市教育局正式发布文件"）；frontmatter `data_source` 属内部元数据，保留内部口径（HSEE 表/视图名，供溯源），不改。品牌名 HSEE 可保留（CTA 引导如"在HSEE查"）。相关 [[compliance-requirements]]。
