---
name: model-config
description: "会话模型配置为 deepseek-v4-flash[1m],上下文窗口 100 万 token"
metadata: 
  node_type: memory
  type: user
  originSessionId: cd9cf1de-3a71-44db-95b4-7846eedf372c
  modified: 2026-08-22T01:52:08.284Z
---

用户使用 Claude Code 时的模型配置为 **deepseek-v4-flash[1m]**,上下文窗口为 **100 万 token**。

**Why:** 上下文容量极大,单次会话可一次性处理超长内容(完整 PRD、多文件代码库、大段原始调研资料),无需频繁裁剪上下文。

**How to apply:** 在处理大文件或长文档时,可放心整读而不必刻意分段;仅在超过百万 token 量级的极端情况下才需考虑上下文管理。此配置为长期默认,无需每轮重复确认。
