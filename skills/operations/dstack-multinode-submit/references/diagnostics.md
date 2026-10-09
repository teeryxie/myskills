# 排障与验证

先用 `runs/get` 读 run 状态及每个 job 的最新 submission，必要时查 `runs/diagnostics`。记录 `termination_reason`、`termination_reason_message`、`exit_status`；单看总状态会丢失失败阶段。

`logs/poll` 使用该 run 的实际 job_submission_id。保留 next_token 并分页/增量读取，避免每轮从头拉全量日志。日志工具本身成功退出不代表远端任务成功。

| 证据 | 能得出的结论 | 下一步 |
|---|---|---|
| provisioning，无日志 | 尚未观察到用户脚本执行 | 查 job 错误、镜像进度、处理时间；有界等待，不盲目重提 |
| creating_container_error + reconciliation deadline | agent/容器创建阶段失败 | 比较成功与失败的镜像、挂载、资源、命令大小；无详细证据不要归因 VPN 或资源不足 |
| registered digest mismatch | 归档登记摘要与 agent 校验不一致 | 确认 multipart filename 是外层原始字节 SHA-256，回读 hash；不要改用不校验下载 |
| archive/tar invalid tar header | runner 收到的归档格式不匹配 | 普通 tar 作为外层，内层可压缩；不要直接给 gzip 流 |
| 上传返回超过大小限制 | 请求在上传入口被拒绝 | 读取实际限制，为 multipart 留余量；压缩内层或用受支持存储 |
| container_exited_with_error，无 traceback | shell 前置检查或命令失败 | 每个关键阶段输出标记，ERR trap 打印失败行；检查目标文件/目录语义 |
| 输出 SCOPE_FORMAL_QUEUED 后辅助任务 failed | 正式作业可能已入队 | 查询 queue、running、archive、结果目录；不要再次提交 |
| queue 消失、active 指向本 job | worker 已领取 | 查看各节点 started/log、role 健康及模型加载 |
| running、健康检查成功 | 进程或服务在线 | 做真实计算/请求与产物验证，不宣称训练完成 |

## 分阶段证据

1. **资源可用**：目标常驻 run 当前状态、节点数、每节点 GPU 可见性。API Running 不证明队列空闲。
2. **已入队**：正式 job ID、READY 或已领取/归档记录、源脚本摘要。
3. **已领取**：当前 session active 为该 job，各预期节点有 started 与日志。旧 session 的记录不是当前运行证据。
4. **角色就绪**：图像/评分/推理 endpoint 健康，所需模型实际加载，节点间访问通过。统计完整实例数，不能用一个服务代表全部。
5. **初始化完成**：训练 rank 加载模型、分布式进程组和优化器就绪。警告和真实异常分开判断。
6. **计算有效**：首步 loss/梯度、组内奖励方差、截断和产物，或真实推理请求/流式响应。继续检查多步是否稳定；单个零梯度可能由样本决定。
7. **完成**：各 rank 退出码、overall 状态、checkpoint/输出完整性、仅自身进程退出。常驻 worker 继续处理后续任务。

日志包含 traceback、持续无进展或服务退出时，按所属角色定位。不要为修复子作业错误调用 dstack stop/delete 常驻 run。需要取消作业时，先核实当前队列控制协议与既有授权，只影响确切 job ID。

## 多机多卡的额外检查

- NCCL/Gloo 网卡、rendezvous 地址端口、节点 rank/总数与 GPU 实际分配一致；不把本例网络变量移植为所有平台默认。
- 共享目录每个角色都可读写所需路径；模型只读，输出按 job/rank 隔离。
- 各 rank 对齐相同步数和分布式同步点，服务启动/失败不会让其他节点无限等待。
- 环境安装锁有明确 owner 和截止时间；共享环境升级不影响在跑任务。
- 推理确认张量/流水线并行拓扑、模型 shard 数、真实端到端输出、并发容量与服务占用队列的结束方式。
- LoRA smoke 与全参数分布式训练的显存、梯度图和优化器不同；不能据前者宣布后者已验证。

## 无管理员时

先区分自己的上传/脚本协议错误和平台不可用。已有成功 CPU task 是可参考证据，不证明现在平台一定正常。修复可复现的客户端问题后，用最小已授权任务核实；不要创建 GPU 集群、重启 VPN 或扩大权限作为泛化排障手段。所有现有执行路径均无权限或平台持续失败时，给出精确接口与错误，诚实说明当前外部阻塞。
