# 使用方式

仅在需要给出客户端设置、调用代码或实际发送聊天请求时读取本文件。

## OpenAI 兼容参数

```text
Base URL: http://127.0.0.1:8080/v1
API Key: local
Model: 从 GET /v1/models 动态读取
Temperature: 0.7
Max tokens: 1024 或 2048
Context: 8192
Stream: 开启
Concurrency: 1
```

服务默认不校验 API Key，因此客户端可填写任意非空字符串，例如 `local`。如果启动环境设置了 `QWEN38_API_KEY`，则使用该值，不要回显或记录密钥。

## PowerShell 聊天

```powershell
$baseUrl = "http://127.0.0.1:8080/v1"
$model = (Invoke-RestMethod "$baseUrl/models" -TimeoutSec 30).data[0].id
$body = @{
    model = $model
    messages = @(
        @{ role = "user"; content = "你好，请用中文回答。" }
    )
    temperature = 0.7
    max_tokens = 1024
    stream = $false
} | ConvertTo-Json -Depth 8

$response = Invoke-RestMethod `
    -Method Post `
    -Uri "$baseUrl/chat/completions" `
    -ContentType "application/json" `
    -Body $body `
    -TimeoutSec 180

$response.choices[0].message.content
```

## Python OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="local",
)
model = client.models.list().data[0].id

stream = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "请用中文回答。"}],
    temperature=0.7,
    max_tokens=1024,
    stream=True,
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
```

## 图形客户端

Cherry Studio、Chatbox 和 Open WebUI 都选择“OpenAI 兼容”提供商，填入上述 Base URL 和 API Key。优先让客户端自动拉取模型列表；若必须手填，使用 `/v1/models` 返回的完整模型 ID：

```text
/home/<user>/.local/share/qwen38-27b-mlx/model/4-bit
```

该服务只监听 `127.0.0.1`。其他电脑、手机或 WSL 外的远程主机不能直接访问；不要为了方便自行改成 `0.0.0.0`，暴露服务前必须让用户明确授权并设计认证与防火墙规则。
