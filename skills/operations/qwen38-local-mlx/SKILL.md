---
name: qwen38-local-mlx
description: 管理、诊断并使用本机 Windows/WSL2 上的 Qwen3.8-27B 4-bit MLX CUDA 模型服务。适用于用户询问该模型的启动、停止、重启、状态、日志、聊天、OpenAI 兼容 API、客户端接入、显存占用或 vLLM/SGLang 取舍；不用于管理其他本地模型服务。
---

# Qwen3.8 本地 MLX

管理已经部署在本机 RTX 4090 上的 Qwen3.8-27B 服务。用实际命令和 API 结果判断状态，不把进程存在或模型文件存在等同于推理可用。

## 固定环境

- Windows 主机通过 `wsl.exe -d Ubuntu-24.04` 调用 WSL2。
- 管理脚本：`/home/<user>/.local/bin/qwen38-mlx`
- 模型：`/home/<user>/.local/share/qwen38-27b-mlx/model/4-bit`
- Python 环境：`/home/<user>/.venvs/qwen38-27b-mlx`
- API：`http://127.0.0.1:8080/v1`，只监听本机回环地址。
- 日志：`/home/<user>/.local/state/qwen38-27b-mlx/server.log`
- 当前服务限制：8K KV 上下文、单并发、单次最多生成 2048 tokens。

不要修改 Clash、VPN、Docker、注册表、WSL 全局配置或开机自启。不要为了释放显存擅自关闭用户的浏览器、桌面应用或其他 GPU 进程。

## 操作方式

先运行状态命令，除非用户已经明确要求启动或停止：

```powershell
wsl.exe -d Ubuntu-24.04 -- bash -lc "/home/<user>/.local/bin/qwen38-mlx status"
```

按用户意图调用管理脚本：

```powershell
# 启动，重复执行是幂等的
wsl.exe -d Ubuntu-24.04 -- bash -lc "/home/<user>/.local/bin/qwen38-mlx start"

# 停止，只终止 PID 文件记录的模型服务
wsl.exe -d Ubuntu-24.04 -- bash -lc "/home/<user>/.local/bin/qwen38-mlx stop"

# 重启
wsl.exe -d Ubuntu-24.04 -- bash -lc "/home/<user>/.local/bin/qwen38-mlx restart"
```

不要使用宽泛的 `pkill`、`killall` 或 Windows `taskkill`。如果正常停止在 30 秒内没有完成，报告精确 PID 和日志，不自动强制终止。

启动完成后至少检查 `/v1/models`。当用户要求确认“能用”、排障或部署验收时，再发送一个短小、限时的 `/v1/chat/completions` 请求验证真实生成。停止后需要验收时，确认 Windows 端口 8080 已不再监听。

## 聊天与咨询

服务运行时通过 OpenAI 兼容 API 提问。不要同时执行 `qwen38-mlx generate`，因为它会再次加载约 18.6 GB 的模型并造成 24 GB 显存不足。

只有服务已经停止、且用户明确想使用一次性命令行生成时，才使用：

```powershell
wsl.exe -d Ubuntu-24.04 -- bash -lc "/home/<user>/.local/bin/qwen38-mlx generate '提示词'"
```

需要提供 PowerShell、Python OpenAI SDK、Cherry Studio、Chatbox 或 Open WebUI 的配置和示例时，读取 [references/usage.md](references/usage.md)。模型 ID 始终从 `/v1/models` 动态获取；不要假设客户端接受简称。

## 状态判断

- `运行中` 且 `/v1/models` 返回 HTTP 200：API 入口已就绪。
- 进程存在但 API 未就绪：模型可能仍在加载；读取最近日志并等待，不要重复启动。
- PID 文件存在但进程不存在：管理脚本会在下一次 `start` 或 `stop` 时清理陈旧状态。
- 空闲显存低于 18,000 MiB：提示可能启动失败并列出实际占用；未经用户要求不结束其他进程。
- 正常运行时通常占用约 20-23 GiB Windows GPU 显存，MLX 报告峰值约 18.6 GB。

查看诊断日志时优先使用有界输出，避免让任务无限跟随：

```powershell
wsl.exe -d Ubuntu-24.04 -- bash -lc "tail -n 120 /home/<user>/.local/state/qwen38-27b-mlx/server.log"
```

仅当用户明确要求持续看日志时使用管理脚本的 `logs` 子命令。

## 已知兼容性

`mlx-vlm 0.6.15` 的 Qwen3.5/Qwen3.8 fused greedy 路径原本会在 CUDA 上误调 Metal kernel。本机环境已在 `fused_greedy_decode()` 入口加入非 Metal 回退。原文件备份：

`/home/<user>/.venvs/qwen38-27b-mlx/lib/python3.12/site-packages/mlx_vlm/models/qwen3_5/language.py.pre-cuda-fallback`

升级或重装 `mlx-vlm` 后若出现 `[metal_kernel] No Metal back-end`，先比较补丁是否被覆盖，不要重新下载模型或改动 CUDA 驱动。

当前 MLX affine 权重不能直接由 vLLM 或 SGLang 加载。单张 RTX 4090 上，FP8 27B 通常超出 24 GB，NVFP4 主要面向 Blackwell；除非用户愿意更换模型格式和部署目标，否则维持已实测约 29-31 token/s 的 MLX CUDA 方案。GGUF 替代方案应使用 llama.cpp。
