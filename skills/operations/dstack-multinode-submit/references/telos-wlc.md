# Telos/WLC 的已验证实例

记录日期：2026-09-05。以下是 scope 项目的历史证据，不是实时监控结果；每次执行前重读平台和共享队列状态。此文不存储凭据，也不要求其他项目沿用这些路径。

| 项目 | 实例值 |
|---|---|
| 平台 | https://dstack.telos-agent.com |
| project | ack-gpu-wulanchabu |
| 常驻 GPU run | wlc-xty-server，8 节点，每节点 8 GPU |
| 共享队列根 | /mnt/cluster/workspaces/xietianyu/pipeline/wlc-xty-server |
| 队列提交脚本 | /mnt/cluster/workspaces/xietianyu/artifacts/wlc-pipeline/submit-wlc-pipeline-job.sh |
| worker 脚本 | /mnt/cluster/workspaces/xietianyu/artifacts/wlc-pipeline/run-wlc-pipeline-worker.sh |
| 本地权重根 | /mnt/jfs/models/platform |
| 项目环境目录 | /mnt/cluster/workspaces/xietianyu/projects/scope |
| 输出根 | /mnt/cluster/workspaces/xietianyu/outputs/scope |
| CPU 辅助任务 | cpu-shared-gpu fleet，kubernetes，2 CPU / 8 GB / 0 GPU；当时可用 |

## 队列语义

当时 submit 脚本接收 `JOB_SCRIPT [JOB_NAME]`，复制该脚本为 staging 下的 `run.sh`，写 metadata，原子移动到 queue/job-id，然后写 READY 并返回 ID。它不传递提交进程的 export 环境。

worker 使用 `control/current-session` 指向当前 session，在 `sessions/SESSION/state/active` 发布作业；作业目录从 queue 移动到该 session 的 running，完成后移到 archive。每节点结果保存在 `sessions/SESSION/results/JOB`。

读取 active 文件存在竞态。本次已成功入队，但随后单次 `cat active` 失败，导致 CPU 辅助任务被标记 failed；独立读取证实 worker 正常领取了该作业。这不是重提训练的依据。

## scope 数据与角色

- GitHub：https://github.com/YF969/scope 。正式运行代码 commit：`7087abd8fc5f6addf4943fa55ff93e5b6579877c`。
- 训练集 `data/geneval/train_metadata.jsonl`：50,000 条，33,199 个唯一 prompt。
- 评测集 `geneval/prompts/evaluation_metadata.jsonl`：553 条；按去首尾空白/忽略大小写的 prompt 比对，重叠数为 0。
- 旧 `data/geneval/test_metadata.jsonl`：评测集每条重复四次，不要因用户路径名或 test/train 字样代替实际比对。
- 本例为 Qwen3-8B GRPO + Qwen-Image + GenEval：16 GPU 全参数训练、40 GPU 图像生成、8 GPU 评分。配比是本项目配置，不是新项目默认。
- `.venvs/train`、`.venvs/image`、`.venvs/geneval` 隔离依赖；GenEval 使用旧版 CUDA/PyTorch 和针对 H20 的注意力实现适配。
- 共享 NFS 为 `nolock,local_lock=all`，采用原子 mkdir 协调安装。历史残留锁须确认原 owner 已退出再处理。

## 已取得的证据及边界

正式 ID：`scope-train-20260905T082224Z-1333`。

固定版本目录：
`/mnt/cluster/workspaces/xietianyu/projects/scope-runs/7087abd8fc5f6addf4943fa55ff93e5b6579877c-upload`。

输出：
`/mnt/cluster/workspaces/xietianyu/outputs/scope/scope-train-20260905T082224Z-1333/`。

截至当时 08:27 UTC：远端 13 项测试、角色依赖摘要、模型路径、训练/评测数据检查通过；8 worker 已领取，40 图像 endpoint 健康、8 GenEval 服务加载完成；两个训练节点完成权重加载并进入 DeepSpeed BF16 优化器初始化。**当时未取得首步 loss/梯度/奖励统计，不能将这些记录当作有效训练或最终完成证明。**

更早的三卡 smoke 完成生成、评分和保存，但 `reward_std=0`、`grad_norm=0`、`clipped_ratio=1`，且输出上限 64 token；仅证明调用链和保存。正式训练仍需实际首步及多步验证。

证据入口：[仓库 debug 记录](https://github.com/YF969/scope/blob/5d13577/DEBUG_REPORT.md)。后续经验应在用户要求更新 skill 时补充，并保留测量日期与验证边界。
