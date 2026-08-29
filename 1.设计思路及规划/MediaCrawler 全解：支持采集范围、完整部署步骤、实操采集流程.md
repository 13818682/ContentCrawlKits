# MediaCrawler 全解：支持采集范围、完整部署步骤、实操采集流程

## 一、MediaCrawler 支持采集平台 \& 可抓取全部数据字段

### 1、覆盖主流平台

小红书 \(xhs\)、抖音 \(douyin\)、视频号 \(wechat\_video\)、B 站 \(bilibili\)、知乎 \(zhihu\)、微博 \(weibo\)、快手 \(kuaishou\)、百度贴吧 \(tieba\)。

### 2、三大采集模式

1）关键词搜索采集；2）指定创作者主页全量抓取；3）单作品精准抓取 \+ 评论抓取。

### 3、可拿到的结构化数据（对你深圳中考文案素材采集完全够用）

#### （1）图文 / 作品基础信息

1. 作品 ID、作品链接、发布时间、发布定位

2. 标题、正文完整文案、话题标签、封面图链接

3. 作者 ID、昵称、头像、简介、粉丝量

4. 互动指标：点赞数、收藏数、评论数、转发 / 分享量（核心筛选爆款）

#### （2）短视频专属数据

- 视频音频地址、**自动识别提取视频内嵌字幕文案**（抖音 / 视频号口播脚本核心来源）

- 视频时长、分辨率、背景音乐信息

#### （3）评论数据（二级深挖家长真实需求）

一级评论、二级楼中楼评论、评论者昵称、评论内容、评论点赞数、评论发布时间；
可用来汇总深圳家长高频疑问，反向生成答疑类选题。

#### （4）导出存储格式

JSON、JSONL、CSV、Excel、SQLite、MySQL，可直接导入数据库、飞书表格、AI 分析工具。

### 4、不支持内容

付费可见内容、私密作品、用户私信、后台隐私数据、付费专栏内容；仅能抓取**公开展示内容**。

---

## 二、MediaCrawler 完整部署教程

### 环境硬性要求

1. 操作系统：Windows10\+/macOS/Linux（Ubuntu/CentOS）

2. Python：3\.11 及以上版本

3. Node\.js：v16\+（如需启用 Web 可视化后台必须安装）

4. 内存建议 ≥8G，运行更稳定；系统预装谷歌 Chrome 正式版

### 方式一：推荐部署（uv 包管理器，依赖零冲突，首选）

#### 步骤 1：拉取项目源码

打开终端（Windows 用 PowerShell、CMD，Mac/Linux 终端）

```bash
# 克隆代码仓库
git clone https://github.com/NanmiCoder/MediaCrawler.git
# 进入项目文件夹
cd MediaCrawler
```

#### 步骤 2：安装 uv 高速依赖管理工具

```bash
# Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell（管理员）
irm https://astral.sh/uv/install.ps1 | iex
```

安装完成后关闭终端重新打开，让环境变量生效。

#### 步骤 3：一键安装项目全部 Python 依赖

```bash
uv sync
```

#### 步骤 4：安装 Playwright 自动化浏览器驱动

依托真实 Chrome 环境模拟真人访问，绕过大部分前端加密校验

```bash
uv run playwright install chrome
```

### 方式二：原生 pip 虚拟环境部署（Windows 新手备选）

```bash
git clone https://github.com/NanmiCoder/MediaCrawler.git
cd MediaCrawler

# 创建虚拟环境
python -m venv venv

# Windows 激活环境
venv\Scripts\activate
# Mac/Linux激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
# 安装浏览器驱动
playwright install chrome
```

### 可选：部署可视化 WebUI 后台（不用敲命令，网页可视化操作）

1. 进入前端目录

```bash
cd webui
# 安装前端依赖
npm install
# 启动前端页面
npm run dev
```

2. 新开终端启动后端接口

```bash
uv run uvicorn api.main:app --host 0.0.0.0 --port 8080
```

3. 访问地址
前端：[http://127\.0\.0\.1:5173](http://127.0.0.1:5173)
后端接口地址：[http://127\.0\.0\.1:8080](http://127.0.0.1:8080)

### 关键前置优化：Chrome 远程调试（大幅降低封号、风控拦截）

1. 关闭所有 Chrome 窗口，新开终端启动带调试端口的 Chrome

```bash
# Windows示例
chrome.exe --remote-debugging-port=9222
# Mac
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

2. 在弹出的浏览器里手动登录小红书、抖音、B 站等账号；
爬虫会复用该浏览器登录状态，无需项目内重复扫码登录，风控最低。

---

## 三、三种主流采集实操方式（命令行 \+ 配置文件）

配置文件统一路径：`config/base_config.py`，所有关键词、抓取间隔、存储方式在此修改。

### 通用启动命令格式

```bash
uv run main.py --platform=平台代号 --lt=qrcode --type=采集类型
```

- `--platform`：xhs/douyin/bilibili/zhihu/wechat\_video

- `--lt qrcode`：扫码登录；搭配上面 9222 调试浏览器可免扫码

- `--type`：search 关键词抓取 /creator 博主主页抓取 /detail 单作品抓取

### 场景 1：关键词采集（适配你的需求：抓取深圳中考相关文案）

1. 打开 `config/base_config.py`，修改关键词数组

```python
KEYWORDS = [
    "深圳中考志愿填报",
    "深圳指标生政策",
    "深圳中考一分一段表",
    "深圳公办高中录取分数线",
    "深圳中考冲稳保志愿搭配"
]
```

同时配置抓取间隔 `SLEEP_TIME = 12`（单位秒，每抓取一条等待 12s，防封禁）
2\. 执行采集小红书关键词数据

```bash
uv run main.py --platform=xhs --lt=qrcode --type=search
```

运行后会唤起浏览器扫码，登录后自动根据关键词循环抓取全部公开笔记。

### 场景 2：抓取指定升学博主全部作品

1. 修改配置文件内创作者 ID 列表 `CRAWLER_CREATOR_ID_LIST`，填入目标博主主页 ID

2. 启动命令

```bash
uv run main.py --platform=xhs --lt=qrcode --type=creator
```

自动遍历该账号全部历史图文、视频、互动数据。

### 场景 3：单条爆款作品抓取 \+ 全量评论

填入目标作品链接 / ID，抓取正文、字幕、全部评论：

```bash
uv run main.py --platform=douyin --lt=qrcode --type=detail
```

### 数据存储设置

在`base_config.py`修改`DATA_SAVE_TYPE`：

1. `csv`：本地 csv 表格，直接打开查看、导入飞书多维表格；

2. `mysql`：存入 MySQL 数据库，适合你自建素材库长期存储；

3. `sqlite`：轻量化本地数据库。

---

## 四、WebUI 可视化傻瓜式采集（非技术人员推荐）

1. 前后端服务全部启动完成后打开 [http://127\.0\.0\.1:5173](http://127.0.0.1:5173)

2. 左侧选择目标平台：小红书 / 抖音等

3. 选择采集模式：关键词搜索 / 博主采集 / 单作品采集

4. 页面输入关键词 / 博主 ID，设置抓取延时、是否抓取评论

5. 一键扫码登录，点击「启动采集」

6. 实时查看抓取日志，任务结束后页面一键导出 Excel/CSV 素材文件。

---

## 五、适配你深圳中考项目的最佳采集配置 \& 风控要点

1. 抓取间隔固定 ≥10s，禁止极速并发抓取；

2. 优先复用本地已登录 Chrome（9222 调试模式），封号概率最低；

3. 分时段定时采集，每日凌晨低峰期自动跑采集任务；

4. 仅抓取近 3 个月发布内容，减少无效历史数据；

5. 采集数据仅用作选题分析、文案结构参考，禁止直接搬运原文商用；

6. 搭配 IP 代理池（可选）：大批量长期抓取时配置代理，防止本机 IP 被平台限制。

---

## 六、常见报错快速解决

1. 登录失败：确认 Chrome 9222 调试端口正常，浏览器提前手动登录账号；

2. 依赖报错：全程只用 uv 安装，不要混用 pip；

3. 抓取为空：关键词过于冷门、账号风控限制，换账号、拉长等待时间；

4. 无法启动 WebUI：确认 Node\.js 版本≥16，前端依赖 npm install 执行成功。

> （注：部分内容可能由 AI 生成）
