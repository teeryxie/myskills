# 提交接口与文件传输

以下协议在 Telos 的 dstack 实例于 2026-09-05 实际验证。其他部署先读其 `/openapi.json` 和当前 CLI/runner 实现。不要请求 server-injected 字段或绕过平台授权。

## 最短可用路径

有挂载共享卷的既有命令执行入口时直接使用；否则在授权范围内提交一个 CPU 辅助任务。该任务只部署、验证并入队；GPU 资源仍由已有 worker 持有。

在没有 SSH、没有网页操作且没有共享卷直连时，仅列出队列脚本的路径不能完成提交，必须证明一个能执行该脚本的入口实际可用。

## 本地打包

使用 Git 已跟踪文件且明确限定目录，输出目录放在仓库外：

```powershell
python "<skill>/scripts/bundle.py" --repo "F:/project" --out "F:/artifacts/run-upload" --include "src" --include "scripts" --include "configs" --include "data/train.jsonl"
```

`<skill>` 和项目路径是调用时要替换的参数。脚本拒绝脏工作区、越界路径、符号链接、明显凭据文件和重复输出。它不会审查文本内容是否含 token；调用者仍须审查文件选择和 diff。二进制文件不会做换行转换；常见文本文件规范化 CRLF，并在清单中记录实际打包内容的哈希。

输出：`upload.tar`、`manifest.json`。外层是普通 tar，内含一个 `payload.tar.gz`；内层包含源文件和 `SOURCE_MANIFEST.json`。默认保留 8 KiB multipart 余量，满足当时部署的 2 MiB 请求上限。上限不足时使用平台支持的大文件存储或缩小明确的代码/数据范围，不向命令塞入大段 base64。

## 上传协议

1. `POST /api/files/upload_archive`，multipart 字段名 `file`。
2. multipart 的 **filename 必须是整个外层普通 tar 的 SHA-256**。不是普通文件名，不是内层压缩包摘要。历史上服务端将 filename 直接登记为 hash，错误 filename 可能先上传成功、后被 agent 拒绝。
3. 检查返回的 `id` 和 `hash`，后者必须等于本地摘要。
4. `RunSpec.file_archives` 使用返回 ID，指定本任务临时文件位置：

```json
{"file_archives": [{"id": "UPLOAD_ID", "path": "/tmp/project-upload.tar.gz"}]}
```

runner 将外层 tar 的首级名字替换为目标名字。外层只有 `payload.tar.gz` 时，目标是 **文件** `/tmp/project-upload.tar.gz`，不是目录。不要将目标设为共享项目根目录：当时 runner 实现会移除已有目标后解包。

验证源文件后，使用类似 `tar -xzf /tmp/project-upload.tar.gz -C "$NEW_RELEASE"` 解开内层；`NEW_RELEASE` 必须是本次新建且归属明确的目录。随后核验 `SOURCE_MANIFEST.json` 中的 commit 和每个文件的哈希。

辅助上传脚本：

```powershell
# 凭据由当前安全环境提供，命令中不写字面 token。
python "<skill>/scripts/upload_archive.py" --server "https://dstack.example.com" --archive "F:/artifacts/run-upload/upload.tar" --receipt "F:/artifacts/run-upload/upload-receipt.json"
```

默认读取 `DSTACK_TOKEN`，可用 `--token-env` 指定已有环境变量名称。脚本只上传文件，无 runs/apply、停止、删除或集群创建接口。

## 计划与提交

读取当前 schema 后构造 `runs/get_plan`，目标 project 显式传入。检查返回 action、current_resource、实际 offer 的 GPU/CPU/后端/挂载和成本。辅助任务预期为 0 GPU、指定现有 fleet、独立唯一名称；不能仅看到有 offer 就断定请求正确。

当时的 apply 请求形状：

```json
{
  "plan": {"run_spec": "SCHEMA_VALIDATED_SPEC", "current_resource": null},
  "force": false,
  "replace_policy": "forbid"
}
```

示意中的 `run_spec` 应替换为 schema 验证的对象。拒绝把既有常驻任务作为替换目标；不擅自提高资源、移除时限或扩大权限来重试。

启动命令只包含短 bootstrap 或脚本路径；代码通过 file_archives 分发。执行环境先校验数据与环境，再调用当前项目真正的队列提交脚本。若该脚本只复制 `run.sh` 而不复制 shell 环境变量，必须把项目根目录、DATA_PATH、输出根目录等写入这份作业脚本，不能只在 CPU 提交进程里 export。

## 回执与重试边界

- 本地先持久化请求名；apply 无响应时查询同名任务，不自动重复 apply。
- 远端先写提交意图和固定 release 信息，再入队并立即保存正式 job ID。
- 只有确认失败发生在入队之前、队列/running/archive 中也没有本次作业，并且有针对性的修复时才再提交。
- 同一个原因在修复验证后仍重复失败两次，停止相同方案的重试，转向新的可核验路径或报告具体外部阻塞；不要不断创建临时任务。
- 已入队后的日志读取失败、辅助任务退出失败或 active 文件短暂缺失，只触发只读核查。没有权威证据时保留“不确定”，不能重提来掩盖状态不明。

## 实现依据

- 部署自身的 `/openapi.json` 是当前字段依据。
- 上游参考：[文件上传服务](https://github.com/dstackai/dstack/blob/master/src/dstack/_internal/server/services/files.py)、[runner 文件解包](https://github.com/dstackai/dstack/blob/master/runner/internal/runner/executor/files.go)。master 可能变化，排障时核实目标版本。
