---
name: notion-paper-read
description: Download an academic paper by title, archive it locally, produce beginner-friendly Chinese reading notes, and write structured notes with subpages to a Notion paper database. Use when the user wants a complete paper-reading workflow saved locally and in Notion.
---

# Notion Paper Read

## Overview
执行“论文题目 → 下载 → 本地归档 → 精读笔记 → 写入 Notion 数据库”的固定流程，产出可读性强的中文笔记与子页面。

## Workflow (Sequential)

### Step 1: 定位论文与下载 PDF
- 使用当前环境可用的网页搜索工具搜索论文题目，优先找到 arXiv 或官方出版页的 PDF。
- 解析 PDF 链接并下载。
- 输出根目录按以下优先级确定：用户明确指定的目录、环境变量 `PAPER_NOTES_DIR`、`~/paper-notes`。
- 目录规范：`<output-root>/YYYY-MM-DD_<Paper-Title>`，不得假设某台机器的个人绝对路径。
- 必要文件：`paper.pdf`。

### Step 2: 提取文本与草稿输出
- 首选 `pdftotext` 提取全文到 `paper_extracted.txt`。
- 生成 `draft.md`，内容包含：
  - 摘要翻译与超短总结
  - 研究问题与设定
  - 核心贡献
  - 方法细节（含超参与缺失细节）
  - 实验可信度
  - 消融与机制解释
  - 局限与失效模式
  - 最终产物（1-2页式总结 + 3条质疑）
  - 论文故事线/科学问题
  - 意义与写作优点
  - 动机、基准与结果、意味着什么
- `draft.md` 默认要求“可直接阅读的成文版”，不是提纲：
  - 总字数建议 ≥ 2200 中文字（不含标题）。
  - `最终产物：1-2页式总结` 建议 ≥ 700 中文字。
  - 每个一级章节至少 2-4 条有效信息（数字、设置、结论或局限）。
- 若用户要求，增加“图示化解释/流程示意”（ASCII 图）。
- **注意**：用户未要求时，不写“迁移到你的研究”。

### Step 2.5: 质量自检（写入 Notion 前必须执行）
- 对照论文正文核对关键数字（数据规模、主结果、超参、消融差值）。
- 检查是否出现“只有结论、缺机制解释”的空泛段落；若有必须补充“为什么”。
- 检查是否出现“全是项目符号、没有可连续阅读段落”；若有必须补充长段总结。
- 通过后才执行 Step 3 写入 Notion。

### Step 3: 写入 Notion 数据库
- `notion-search` 或已知 URL 定位数据库“论文笔记”。如需限定搜索模式，使用 `content_search_mode: "workspace_search"` 或 `"ai_search"`（不要用 `"workspace"`）。
- `notion-fetch` 读取 schema，确认字段名：`Name`, `Tags`(date), `名字`, `备注`, `重要性`。
- 在数据源下 `notion-create-pages` 新建条目：
  - `Name` 与 `名字` = 论文标题
  - `Tags` = 今日日期（YYYY-MM-DD）
  - `备注` = 关键词摘要
  - `重要性` = 单选值（如 B）。注意：MCP 参数请直接传字符串 `"B"`（不要传数组），避免类型校验失败。
- 在条目下新建子页面：
  - 子页面1：`精读与复现负责人视角`（写入完整笔记）
  - 子页面2：`写作方法参考（可复用）`（若写作质量可借鉴）

## Quality Bar
- 语言：简体中文，面向不熟悉读者，解释充分但不冗长。
- 结构：由浅入深，先讲动机/故事，再讲方法/结果。
- 事实：所有数字与超参来自论文正文。
- 风格：优先“高信息密度 + 可读长段”，避免只有提纲式短句。
- 完整性：必须覆盖“方法细节、实验可信度、消融机制、局限、3条质疑”。

## Output Template（强制模板）
- `# 摘要翻译`
- `# 超短总结（一句话）`
- `# 研究问题与设定`
- `# 核心贡献`
- `# 方法细节（含关键超参与实现要点）`
- `# 实验可信度与结果要点`
- `# 消融与机制解释`
- `# 局限与失效模式`
- `# 最终产物：1-2页式总结（精炼长文）`
- `# 3条质疑`
- `# 论文故事线 / 科学问题`
- `# 意义与写作优点`
- `# 动机、基准与结果、意味着什么`

## Notion 写入要求（强制）
- 子页面 `精读与复现负责人视角` 必须写入完整模板内容，不得只写压缩版提纲。
- 若本轮已有旧内容，优先 `replace_content` 全量替换为新版本，避免增量追加导致风格混杂。
- 子页面 `写作方法参考（可复用）` 至少包含 4 条“可迁移写作套路”，每条含“做法 + 作用”。

## Notes
- 不执行 Git 提交、分支等操作，除非用户明确要求。
- 路径始终使用双引号，优先 `/` 分隔符。
