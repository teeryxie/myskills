# 安装与验证

## 来源与版本

- 官方包：`@larksuite/cli`
- 官方仓库：<https://github.com/larksuite/cli>
- 许可证：MIT
- 本仓库验证快照：`lark-cli 1.0.92`，2026-08-31

官方 Skills 编译进 CLI，并随 CLI 版本更新。不要把本仓库中的快照说明当成最新版本声明；执行时以 `lark-cli --version` 和 `lark-cli skills list` 为准。

## 安装

需要 Node.js 16 或更高版本。可复现安装使用已验证版本：

```bash
npx @larksuite/cli@1.0.92 install
```

主动升级时使用官方最新版，但升级后必须重新执行本页验证：

```bash
npx @larksuite/cli@latest install
```

## 首次配置

```bash
lark-cli config init --new
lark-cli auth login --recommend
lark-cli auth status --verify --json
```

应用密钥只通过交互式配置或标准输入进入本机安全存储，不写入 shell 历史、Skill、仓库文件或日志。登录命令输出验证 URL 时，同时生成二维码交给用户完成浏览器授权。

`--recommend` 只申请官方推荐权限。需要特定业务域时使用 `--domain` 或精确 `--scope`，不要为了省事自动申请全部权限。

## 验证清单

```bash
lark-cli --version
lark-cli skills list
lark-cli auth status --verify --json
lark-cli auth check --scope "contact:user:search im:chat:read im:message:readonly im:message.send_as_user docx:document:readonly docx:document:write_only wiki:node:read minutes:minutes.basic:read" --json
```

验证结果必须同时满足：

- CLI 能运行，版本明确。
- 官方 Skills 可列出。
- 需要的身份为 `ready` 且服务端验证通过。
- 任务所需权限全部位于 `granted`，`missing` 为空。
- 对实际目标资源的最小只读查询成功。

## 迁移新机器

1. 安装固定或已审核的新版本 `lark-cli`。
2. 从 `myskills` 安装本仓库自维护 Skills。
3. 重新配置应用并由用户完成 OAuth 授权；不要复制访问令牌或密钥链文件。
4. 运行验证清单。
5. 用无副作用的联系人查询、文档读取和消息草稿 dry-run 做冒烟验证。

认证状态与资源权限具有时效性。迁移记录只保存版本、权限名称和验证结果，不保存应用 ID、open_id、chat_id、文档 token、授权 URL 或令牌到期时间。
