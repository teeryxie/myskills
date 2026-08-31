# 权限模型与审计清单

## 四层权限模型

| 层 | 是什么 | 不包含什么 | 当前作用 |
| --- | --- | --- | --- |
| 应用后台权限 | 飞书开发者后台为应用启用的开放平台权限范围 | 不代表某个用户已经授权，也不代表资源共享给调用者 | 决定应用最多能申请哪些能力 |
| 用户 OAuth 授权 | 用户在浏览器批准应用代表自己使用的权限子集 | 不包含机器人身份，也不自动授予资源所有权 | `--as user` 命令使用 |
| 执行身份 | `user` 是授权用户本人；`bot` 是应用机器人 | 两者的可见资源、群成员关系和管理员能力不互通 | 每条命令显式选择调用者 |
| 资源级权限 | 文档共享、知识空间角色、群成员关系、会议可见性等 | 即使开放平台 scope 已授予，也可能缺少这一层 | 决定目标资源是否真的可读写 |

“最大授权”只扩大前两层的能力集合，不绕过资源级权限、群管理员规则、所有者限制或写操作确认。

## 关键权限组合

下面是这套流程在 2026-08-31 验证过的关键权限名称，不是要求所有环境无条件全开。

| 工作流 | 关键权限 |
| --- | --- |
| 搜索联系人和消歧 | `contact:user:search`, `contact:user.basic_profile:readonly` |
| 读取私聊/群聊 | `im:chat:read`, `im:message:readonly`, `im:message.p2p_msg:get_as_user`, `im:message.group_msg:get_as_user`, `search:message` |
| 以用户身份发送 | `im:message.send_as_user`, `im:message` |
| 消息图片和文件 | `im:resource` |
| 读取/创建/编辑文档 | `docx:document:readonly`, `docx:document:create`, `docx:document:write_only`, `docs:document.content:read` |
| 文档权限诊断 | `docs:permission.member:retrieve`, `docs:permission.setting:read` |
| 知识库节点 | `wiki:node:read`, `wiki:node:retrieve`, `wiki:node:create`; 移动或复制时另需对应 scope |
| 妙记与会议产物 | `minutes:minutes.basic:read`, `minutes:minutes.artifacts:read`, `minutes:minutes.search:read`, `vc:note:read` |
| 文档搜索 | `search:docs:read` |
| 长期用户登录 | `offline_access`，只允许 CLI 安全存储，不进入仓库 |

当前应用审计时用户令牌包含 174 个权限项，上表关键权限均已验证为 granted。这个数字和授权结果会变化；新机器或重新授权后必须实时执行 `auth status` 与 `auth check`，不能复用历史结论。

## 写操作门禁

| 操作 | 写前必须确认 | 写后验证 |
| --- | --- | --- |
| 私聊/群消息发送 | 收件人、完整正文、发送身份 | `ok=true`，保存并返回 `message_id` |
| 云文档编辑 | 目标文档、影响范围、正文意图 | 重新 fetch，确认修订号、正文和资源引用 |
| 周报提交 | 周次、小组、报告人、主责/跨组关系 | 个人文档和登记表链接都回读成功 |
| 知识库节点创建/移动 | 父节点、空间、标题、移动影响 | 重新列出父节点并核对 node token |
| 审批、删除、所有者转移 | 精确对象与不可逆影响 | 按命令返回和目标资源状态复核 |

初始用户请求已经同时明确收件人、正文和身份时可视为确认；否则在真正发送前展示草稿并等待确认。不要把“帮我看看”“帮我整理”解释为允许外部发送。

## 常见误判

- `wiki:node:create` 已授予，但在具体小组节点下仍返回 `131006` 或文档接口 `3380004`：这是资源级权限不足，不是 scope 缺失。请求空间管理员授权或让用户预建子页面；不要反复重试，也不要改建到个人目录冒充完成。
- `--as bot` 返回空列表：机器人可能不是群成员或没有资源可见性；空成功不证明用户侧没有数据。
- `running`、`ready` 或 token valid：只证明身份可用，不证明某个文档、群聊或会议可访问。
- 能读取不代表能写入：读取、创建、编辑、删除和权限管理通常是不同 scope，也可能有不同资源角色限制。
