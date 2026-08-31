# myskills

个人 Codex skills 集合，用于在多台机器之间统一管理、安装和更新常用工作流。

本仓库按领域组织 skill，但安装时以每个 `SKILL.md` frontmatter 中的 `name` 作为最终名称。安装脚本会递归发现 `skills/` 下的全部 skill，因此以后新增目录后不需要维护硬编码清单。

## 目录

| 分类 | Skill | 用途 | 来源 |
| --- | --- | --- | --- |
| Research | `ccfa-paper-figures` | CCF-A/顶会论文数据图、架构图与 camera-ready 审查 | 自维护 |
| Research | `drawio-diagram-builder` | 创建、复刻和迭代优化可编辑的 draw.io 科研与技术图 | [Will-hxw/drawio-diagram-builder-skill](https://github.com/Will-hxw/drawio-diagram-builder-skill) |
| Research | `scientific-figure-generator` | AI/CS 论文科研示意图生成 | [Deepshare-Official/CCF-Figure](https://github.com/Deepshare-Official/CCF-Figure) |
| Research | `rebuttal-writer` | 基于论文、审稿意见和证据撰写学术 rebuttal | 自维护 |
| Research | `rebuttal-critic` | 严格审查 rebuttal 的覆盖、证据、语气和 AC 说服力 | 自维护 |
| Research | `latex-paper-en` | 英文学术论文 LaTeX 审查、改写、编译与引用检查 | 自维护 |
| Research | `latex-thesis-zh` | 中文硕博论文 LaTeX 写作、审查、编译与去 AI 化 | 自维护 |
| Research | `notion-paper-read` | 下载论文、生成中文精读笔记并写入 Notion | 自维护，公开版已移除个人路径 |
| Documents | `docx-polish-pipeline` | Markdown/草稿到 DOCX/PDF 的精修管线 | 自维护 |
| Browser | `ego-browser` | ego-lite 浏览器自动化 | [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) |
| Browser | `playwright` | Playwright 浏览器测试与抓取 | Microsoft/OpenAI 分发版本 |
| Operations | `remote-codex-update` | 无外网 Linux 远端的 Codex 离线更新 | 自维护，公开版已脱敏 |
| Integrations | `collaborating-with-gemini-cli` | 通过 JSON bridge 调用 Gemini CLI 进行复核、调试和方案比较 | [ZhenHuangLab/collaborating-with-gemini-cli](https://github.com/ZhenHuangLab/collaborating-with-gemini-cli) |
| Integrations | `lark-ops-control` | 飞书官方 CLI 安装、身份、OAuth 授权和资源权限诊断 | 自维护；依赖 [larksuite/cli](https://github.com/larksuite/cli) |
| Integrations | `lark-progress-sync` | 跨私聊、群聊、会议和文档提炼进度，经确认后发送 | 自维护；依赖官方 `lark-*` Skills |
| Integrations | `lark-weekly-report-submit` | 定位周次、填写个人周报、登记小组链接并回读验证 | 自维护；依赖官方 `lark-*` Skills |
| Presentations | `gpt-image2-ppt` | 使用 gpt-image-2、风格库或用户模板生成高分辨率 PPT | [JuneYaooo/gpt-image2-ppt-skills](https://github.com/JuneYaooo/gpt-image2-ppt-skills) |
| Frontend | `frontend-ui-standards` | 跨框架前端规范与组件复用 | 自维护 |
| Frontend | `create-adaptable-composable` | 创建支持值、ref 和 getter 的 Vue composable | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| Frontend | `vue-best-practices` | Vue 3、Composition API、TypeScript 和 SSR 主规范 | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| Frontend | `vue-debug-guides` | Vue 3 运行时、响应式、异步和 hydration 排错 | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| Frontend | `vue-jsx-best-practices` | Vue JSX/TSX 语法和配置规范 | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| Frontend | `vue-options-api-best-practices` | Vue 3 Options API 和 TypeScript 规范 | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| Frontend | `vue-pinia-best-practices` | Pinia store、状态管理和响应式模式 | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| Frontend | `vue-router-best-practices` | Vue Router 4 和导航守卫规范 | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| Frontend | `vue-testing-best-practices` | Vitest、Vue Test Utils 和 Playwright 测试模式 | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| Frontend | `ui-craft` | UI 设计与实现的主工作流 | [educlopez/ui-craft](https://github.com/educlopez/ui-craft) |
| Frontend | `ui-craft-dense-dashboard` | 高密度后台和数据工具 | [educlopez/ui-craft](https://github.com/educlopez/ui-craft) |
| Frontend | `audit` | 可访问性、性能与响应式审计 | [educlopez/ui-craft](https://github.com/educlopez/ui-craft) |
| Frontend | `critique` | 视觉层级和设计清晰度评审 | [educlopez/ui-craft](https://github.com/educlopez/ui-craft) |
| Frontend | `colorize` | 重点色与配色收敛 | [educlopez/ui-craft](https://github.com/educlopez/ui-craft) |
| Frontend | `typeset` | 字体、字号、行高和微排版 | [educlopez/ui-craft](https://github.com/educlopez/ui-craft) |
| Frontend | `tokens` | 三层设计 Token 体系 | [educlopez/ui-craft](https://github.com/educlopez/ui-craft) |
| Frontend | `polish` | UI 最终细节精修 | [educlopez/ui-craft](https://github.com/educlopez/ui-craft) |
| Frontend | `finalize` | 发布前质量门禁 | [educlopez/ui-craft](https://github.com/educlopez/ui-craft) |
| Frontend | `ui-ux-pro-max` | UI/UX 样式、配色、字体和图表数据库 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |

`ui-craft` 系列保持在同一分类目录中，因为子 skill 会读取 `ui-craft/references/`。安装 `audit`、`tokens`、`finalize` 等子 skill 时，应同时安装 `ui-craft`。

`collaborating-with-gemini-cli` 需要已安装并完成认证的 Gemini CLI。`gpt-image2-ppt` 需要 Python 3.8+、其目录中 `requirements.txt` 列出的依赖，以及通过进程环境或框架密钥管理注入的 OpenAI API 凭据；仓库不存储 `.env` 或真实密钥。

三个飞书自维护 Skills 需要飞书官方 `lark-cli` 及其随版本内置的官方 `lark-*` Skills。本仓库验证版本为 `1.0.92`：

```bash
npx @larksuite/cli@1.0.92 install
```

官方 Skills 不在本仓库重复镜像，以避免和 CLI 自动安装的同名 Skills 冲突。应用密钥、用户/机器人访问令牌、open_id、chat_id、文档 token 和授权链接都只保存在本机或运行时，不进入仓库。安装、授权、能力图和权限边界见 [`lark-ops-control`](skills/integrations/lark-ops-control/SKILL.md)。

## 新机器安装

### 方式一：克隆后创建链接（推荐）

这种方式以 Git 仓库作为唯一内容源。已有 skill 会随 `git pull` 立即更新；仓库加入新 skill 后，重新运行安装脚本即可补充新链接。

Windows PowerShell：

```powershell
git clone https://github.com/teeryxie/myskills.git
Set-Location "myskills"
powershell -ExecutionPolicy Bypass -File "./scripts/install.ps1"
```

Linux/macOS：

```bash
git clone https://github.com/teeryxie/myskills.git
cd myskills
chmod +x ./scripts/install.sh
./scripts/install.sh
```

默认目标是 OpenAI 当前文档使用的用户级目录：

```text
~/.agents/skills
```

如果某个 Codex 安装仍使用 `~/.codex/skills`，可以显式指定：

```powershell
powershell -ExecutionPolicy Bypass -File "./scripts/install.ps1" -Destination "$HOME/.codex/skills"
```

```bash
CODEX_SKILLS_DIR="$HOME/.codex/skills" ./scripts/install.sh
```

Windows 默认创建目录联接，Linux/macOS 默认创建符号链接。脚本不会删除或覆盖已有的普通目录；遇到名称冲突时会跳过并报告。

若不能使用链接，可以复制安装：

```powershell
powershell -ExecutionPolicy Bypass -File "./scripts/install.ps1" -Copy
```

```bash
./scripts/install.sh --copy
```

复制模式适合一次性安装，但后续 `git pull` 不会自动更新已复制的目录。

### 方式二：让 Codex 使用 skill-installer

在新机器的 Codex 中直接说明仓库和目标路径，例如：

```text
使用 $skill-installer 从 teeryxie/myskills 的 main 分支安装：
skills/operations/remote-codex-update
```

也可以在一次请求中提供多个路径。`skill-installer` 会把每个路径的末级目录作为安装目录；如果目标目录已经存在，它会安全终止而不是覆盖。

安装整个 `ui-craft` 套件时至少同时提供：

```text
skills/frontend/ui-craft
skills/frontend/ui-craft-dense-dashboard
skills/frontend/audit
skills/frontend/colorize
skills/frontend/critique
skills/frontend/finalize
skills/frontend/polish
skills/frontend/tokens
skills/frontend/typeset
```

## 更新与新增 skill

更新现有 skill：

```bash
git pull --ff-only
```

链接安装无需其他操作。若本次更新新增了 skill，再运行一次对应平台的安装脚本。

新增 skill 时：

1. 在合适的 `skills/<category>/<skill-name>/` 下加入完整 skill 目录。
2. 确保存在 `SKILL.md`，且 frontmatter 至少包含 `name` 和 `description`。
3. 不要提交密钥、令牌、Cookie、飞书应用 ID、open_id、chat_id、文档 token、授权链接、私有主机名、内网 IP 或个人绝对路径。
4. 运行结构校验和敏感信息扫描。
5. 更新本 README 的分类表和 `THIRD_PARTY_NOTICES.md`（若来自第三方）。
6. 提交并推送；其他机器执行 `git pull --ff-only`，再运行安装脚本发现新 skill。

Codex 通常会自动发现新安装的 skill；若未出现，重启 Codex。可以在 Codex CLI/IDE 中通过 `/skills` 或输入 `$` 检查和调用。

## 校验状态

发布前执行以下检查：

- 36 个 `SKILL.md` 均存在且能被递归发现；
- 公开内容不包含私钥、Token、密码或真实 API Key；
- `remote-codex-update` 的公开版本不包含个人主机名、用户名、内网地址或个人目录；
- 安装脚本在隔离目标目录中测试，不覆盖现有用户 skills；
- 第三方许可证和来源记录在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

使用当前 `skill-creator` 严格校验器时，33 个 skill 完全通过。以下 3 个保留了上游扩展 frontmatter，因此会收到“额外字段”提示，但仍能被当前 Codex 发现：

- `scientific-figure-generator`：`version`、`platforms`、`author`、`source`；
- `ui-craft`：`argument-hint`；
- `ui-craft-dense-dashboard`：`argument-hint`。

这些字段来自上游分发格式，本仓库没有为通过单一校验器而静默删除上游元数据。

## 许可证与来源

本仓库不声明统一的仓库级许可证。每个第三方 skill 保留其上游许可证和归属；自维护 skill 在未单独声明许可证时保留所有权利。详情见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 参考

- [OpenAI Docs: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Agent Skills specification](https://agentskills.io/specification)
