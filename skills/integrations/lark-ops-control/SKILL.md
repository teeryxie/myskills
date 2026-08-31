---
name: lark-ops-control
description: 安装、审计和排查飞书官方 lark-cli 及其 Agent Skills，处理应用配置、用户与机器人身份、OAuth 授权、业务权限和资源级权限。当用户要配置飞书机器人、检查能力/权限、迁移环境或诊断“已授权但仍无权访问”时使用；普通文档、消息或会议操作应交给对应 lark-* Skill。
metadata:
  requires:
    bins: ["lark-cli"]
    skills: ["lark-shared"]
---

# 飞书 CLI 运维总控

管理飞书官方 `lark-cli` 的安装、认证、身份和权限边界。`lark-cli` 是飞书开放平台官方命令行工具，内置与 CLI 版本同步的 `lark-*` Agent Skills；本 Skill 只负责控制面，不复制或改写官方业务 Skill。

## 先路由

- 安装、升级、配置、登录、授权、身份、权限诊断：留在本 Skill，并读取 [安装与验证](references/setup-and-validation.md) 和 [权限模型](references/permissions.md)。
- 想知道当前官方 Skill 覆盖什么：读取 [官方 Skill 能力图](references/official-suite.md)。
- 具体业务操作：转给匹配的官方 Skill，例如消息走 `lark-im`、文档走 `lark-doc`、会议与妙记走 `lark-meeting`、知识库节点走 `lark-wiki`。
- 周报提交走 `lark-weekly-report-submit`；跨来源进度整理与发送走 `lark-progress-sync`。

## 核心规则

1. **先定义身份。** `user` 表示使用用户访问令牌，以授权用户本人身份读取和操作其可见资源；`bot` 表示使用租户访问令牌，以应用机器人身份操作，只能访问机器人被允许看到的资源。不要依赖 `auto` 猜身份，业务命令显式传 `--as user` 或 `--as bot`。
2. **四层权限分别检查。** 应用后台权限、用户 OAuth 授权、执行身份和具体资源权限缺一不可。OAuth 是用户批准应用代表自己使用哪些开放平台能力的授权，不等于某篇文档、某个知识库节点或某个群聊的访问权。
3. **不暴露凭证。** 不读取或输出应用密钥、访问令牌、刷新令牌、Cookie、设备码或密钥链内容；公开仓库中也不保存应用 ID、用户 open_id、群 ID、文档 token 或授权链接。
4. **不静默扩大权限。** 只申请完成当前任务所需的业务域。用户要求“最大授权”时仍保留写操作确认、资源权限检查和高风险门禁，不关闭默认风险控制。
5. **授权链接配二维码。** 命令返回验证或控制台 URL 时，原样交付链接，并用 `lark-cli auth qrcode` 生成二维码；不要重写查询参数。
6. **以结构化结果判断成功。** JSON 输出检查 `ok == true` 或进程退出码；不要以不存在的顶层 `code == 0` 判断。
7. **高风险写操作单独确认。** 遇到退出码 10 或 `confirmation_required` 时，展示动作、风险和目标，取得明确同意后才追加命令提示的确认参数。

## 诊断顺序

1. `command -v lark-cli` 与 `lark-cli --version`：确认二进制和版本。
2. `lark-cli skills list`：确认官方 Skills 与 CLI 同步可用。
3. `lark-cli auth status --verify --json`：确认用户和机器人身份是否 ready；只在本地查看，向用户汇报时去除所有标识和时间敏感令牌信息。
4. `lark-cli auth check --scope "<space-separated scopes>" --json`：确认当前用户令牌是否包含任务关键权限。
5. 对目标资源执行最小只读查询：验证文档、知识库节点、群聊或会议是否真的可见。
6. 只有前五步通过后才做写操作；写后按业务 Skill 要求回读。

应用权限已授予但资源写入仍返回 `permission_denied` 时，不要重复请求相同参数。先区分资源共享权限、知识空间角色、群成员关系、所有者/管理员限制和身份选错；缺资源权限时请求资源所有者授权，或让用户在目标位置预建空白资源。不要改到其他目录冒充成功。
