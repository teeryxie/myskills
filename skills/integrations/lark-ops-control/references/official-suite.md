# 官方 Skill 能力图

本仓库不镜像飞书官方 `lark-*` Skill 源文件。它们由 `@larksuite/cli` 内置，并与 CLI 版本同步；重复安装会造成同名 Skill 冲突。使用 `lark-cli skills list` 获取当前机器的真实清单。

在 `lark-cli 1.0.92` 上验证到 28 个官方 Skills：

| 领域 | Skills |
| --- | --- |
| 认证与扩展 | `lark-shared`, `lark-openapi-explorer`, `lark-skill-maker`, `lark-event` |
| 消息与人员 | `lark-im`, `lark-contact` |
| 文档与空间 | `lark-doc`, `lark-drive`, `lark-markdown`, `lark-wiki`, `lark-whiteboard` |
| 结构化数据 | `lark-base`, `lark-sheets` |
| 演示与应用 | `lark-slides`, `lark-apps` |
| 协同工作 | `lark-calendar`, `lark-task`, `lark-okr`, `lark-approval`, `lark-attendance` |
| 邮件 | `lark-mail` |
| 会议 | `lark-meeting`, `lark-minutes`, `lark-note`, `lark-vc`, `lark-vc-agent` |
| 官方组合流程 | `lark-workflow-meeting-summary`, `lark-workflow-standup-report` |

其中 `lark-minutes`、`lark-note`、`lark-vc` 和 `lark-vc-agent` 是兼容入口，实际会议任务统一路由到 `lark-meeting`。

本仓库额外维护：

- `lark-ops-control`：安装、身份、授权和权限诊断。
- `lark-progress-sync`：跨聊天/会议提炼进度，经确认后发送。
- `lark-weekly-report-submit`：定位周次、填写个人周报、登记链接并回读验证。

官方 CLI 更新后先比较 `lark-cli skills list`、关键 Skill 说明和权限需求，再决定是否更新本仓库的能力图；不要把旧快照称为最新官方能力。
