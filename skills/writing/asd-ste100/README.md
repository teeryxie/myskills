# ASD-STE100 中文使用指南

这个技能用于把冗长、有歧义的英文技术文本改写得更清楚，适合工具说明、错误消息、系统提示、代理间指令和状态报告。

ASD-STE100 是一套简化技术英语写作规范。STE 是 Simplified Technical English，意为“简化技术英语”。本技能借用其结构规则，没有收录官方批准词典，也不保证官方合规。

## 在 Codex 中使用

已安装到 `~/.codex/skills/asd-ste100`，下一轮对话可使用。可明确指定 `$asd-ste100`，也可用中文提出相关请求：

- “用 $asd-ste100 简化这段英文工具说明，保留全部条件。”
- “消除这条英文错误消息的歧义，不要把‘可能失败’改成‘已经失败’。”
- “按 STE100 改写这段指令，给我前后对照，并用中文解释原因。”
- “用参考 STE 模式修改这个 README，保留技术术语。”

默认结果是可直接使用的英文正文。要求解释时，规则名称、表头和原因用中文；英文原句和改写句仍保持英文。中文润色或翻译可另行明确请求。

## 两种模式

- **严格模式（Strict）**：操作步骤、工具说明、错误消息等。应用句子结构限制，并尽量统一词义和词性；官方批准用词仍须查词典。
- **参考 STE 模式（STE-flavored）**：README、代码合并请求说明、更新记录及解释性文章。保持短句和清楚结构，词汇限制作为建议。

改写必须保留事实、数字、条件、范围和不确定性。不能编造原因、频率或验证结果，也不能为了缩短句子省略安全条件。创意和营销文案通常不适用。

## 英文检测脚本

脚本保持上游原样，只需要 Python 标准库。例如：

```bash
uv run --no-project ~/.codex/skills/asd-ste100/scripts/ste-lint.py your-english-text.md
uv run --no-project ~/.codex/skills/asd-ste100/scripts/ste-lint.py --json your-english-text.md
uv run --no-project ~/.codex/skills/asd-ste100/scripts/ste-lint.py --selftest
```

`--baseline N` 容许 N 个硬性问题；`--disable rule1,rule2` 停用指定规则。硬性问题超过容许数量时退出码为 1，建议项不导致失败。脚本输出保持英文，Codex 可用中文解释。

检测采用模式匹配，只覆盖部分英文写作问题。它不验证语义是否保持一致，不验证官方批准词典，也不适用于检查中文句长或语法。

列表检查支持行首 0–3 个空格后的 `-`、`*`、`+`、`1.` 和 `1)`，标记后须有 ASCII 空格。它检查缩进续行末尾的悬空连词，不完整解析引用内列表、无缩进续行或嵌套列表语义。独立行前有至少 4 个空格时，不视为列表标记；已有列表项中的内容缩进可视为续行。以三个反引号或波浪号开头的去空白行会切换代码块状态。

[列表边界示例](examples/linter-edge-cases.md) 刻意包含错误；检测时预期报告两处问题，不能当作合规正文。

## 保留的英文资料

- [技能完整说明](SKILL.md)：已中文化，并增加中文反馈约定。
- [规则参考](references/writing-rules.md)：保留英文规则类别和原始来源。
- [改写示例](examples/before-after.md)：保留英文正反例，便于核对英文语法和原意。
- [官方申请页面](https://www.asd-ste100.org/STE_downloads.html)：精确合规要求应使用官方标准。免费获取不意味着可以自由再发布。

## 来源与本地修改

来源：[danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)，`master` 分支，上游版本 `0.4.0`。2026-10-04 安装并完成本地中文适配。

修改仅涉及入口说明和本使用指南。入口的 `version` 移到 Codex 支持的 `metadata.version` 中，值保持不变。LICENSE、英文参考、示例和检测脚本保持上游内容。原始安装文件备份在 `~/.codex/skill-backups/asd-ste100-20261004/upstream`。

以后更新上游时需要重新合并中文修改，避免直接覆盖。许可证为 MIT，见 [LICENSE](LICENSE)。
