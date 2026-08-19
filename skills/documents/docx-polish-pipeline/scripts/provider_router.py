#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import mimetypes
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


class ProviderError(RuntimeError):
    pass


@dataclass
class ReviewResponse:
    status: str
    backend: str
    model: str
    text: str


def _load_skill_env() -> None:
    env_file = os.environ.get("DOC_POLISH_ENV_FILE")
    env_path = Path(env_file).expanduser() if env_file else Path.home() / ".codex" / "skill-env" / "docx-polish-pipeline.env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and value and key not in os.environ:
            os.environ[key] = value


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ProviderError(f"Missing required environment variable: {name}")
    return value


def _openai_compatible_api_key() -> str:
    api_key = os.environ.get("DOC_POLISH_API_KEY", "").strip() or os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ProviderError("Missing DOC_POLISH_API_KEY or OPENAI_API_KEY for openai-compatible review.")
    return api_key


_load_skill_env()


def _post_json(url: str, payload: dict, headers: dict[str, str] | None = None) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ProviderError(f"HTTP {exc.code} from {url}: {body}") from exc
    except urllib.error.URLError as exc:
        raise ProviderError(f"Failed to reach {url}: {exc}") from exc


def _data_uri_for_path(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/png"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{payload}"


def _review_text_openai_compatible(system_prompt: str, user_prompt: str) -> ReviewResponse:
    base_url = _required_env("DOC_POLISH_BASE_URL").rstrip("/")
    api_key = _openai_compatible_api_key()
    model = os.environ.get("DOC_POLISH_TEXT_MODEL", "gpt-5.4")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    data = _post_json(
        f"{base_url}/chat/completions",
        payload,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    text = data["choices"][0]["message"]["content"]
    return ReviewResponse(status="ok", backend="openai-compatible", model=model, text=text)


def _review_vision_openai_compatible(system_prompt: str, user_prompt: str, image_paths: list[Path]) -> ReviewResponse:
    base_url = _required_env("DOC_POLISH_BASE_URL").rstrip("/")
    api_key = _openai_compatible_api_key()
    model = os.environ.get("DOC_POLISH_VISION_MODEL", os.environ.get("DOC_POLISH_TEXT_MODEL", "gpt-5.4"))
    content = [{"type": "text", "text": user_prompt}]
    for path in image_paths:
        content.append({"type": "image_url", "image_url": {"url": _data_uri_for_path(path)}})
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
    }
    data = _post_json(
        f"{base_url}/chat/completions",
        payload,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    text = data["choices"][0]["message"]["content"]
    return ReviewResponse(status="ok", backend="openai-compatible", model=model, text=text)


def _review_text_internal_http(system_prompt: str, user_prompt: str) -> ReviewResponse:
    base_url = os.environ["DOC_POLISH_INTERNAL_BASE_URL"].rstrip("/")
    token = os.environ.get("DOC_POLISH_INTERNAL_TOKEN", "")
    payload = {"system_prompt": system_prompt, "user_prompt": user_prompt}
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    data = _post_json(f"{base_url}/review/text", payload, headers=headers)
    text = data.get("output_text") or data.get("text") or data.get("result") or json.dumps(data, ensure_ascii=False)
    return ReviewResponse(status="ok", backend="internal-http", model=data.get("model", "internal-http"), text=text)


def _review_vision_internal_http(system_prompt: str, user_prompt: str, image_paths: list[Path]) -> ReviewResponse:
    base_url = os.environ["DOC_POLISH_INTERNAL_BASE_URL"].rstrip("/")
    token = os.environ.get("DOC_POLISH_INTERNAL_TOKEN", "")
    payload = {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "images": [
            {
                "filename": path.name,
                "mime_type": mimetypes.guess_type(path.name)[0] or "image/png",
                "base64": base64.b64encode(path.read_bytes()).decode("ascii"),
            }
            for path in image_paths
        ],
    }
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    data = _post_json(f"{base_url}/review/vision", payload, headers=headers)
    text = data.get("output_text") or data.get("text") or data.get("result") or json.dumps(data, ensure_ascii=False)
    return ReviewResponse(status="ok", backend="internal-http", model=data.get("model", "internal-http"), text=text)


def review_text(system_prompt: str, user_prompt: str) -> ReviewResponse:
    backend = os.environ.get("DOC_POLISH_REVIEW_BACKEND", "none").strip().lower()
    if backend in {"", "none"}:
        return ReviewResponse(status="skipped", backend="none", model="none", text="External text review skipped.")
    if backend == "openai-compatible":
        return _review_text_openai_compatible(system_prompt, user_prompt)
    if backend == "internal-http":
        return _review_text_internal_http(system_prompt, user_prompt)
    raise ProviderError(f"Unsupported DOC_POLISH_REVIEW_BACKEND: {backend}")


def review_vision(system_prompt: str, user_prompt: str, image_paths: list[Path]) -> ReviewResponse:
    backend = os.environ.get("DOC_POLISH_REVIEW_BACKEND", "none").strip().lower()
    if backend in {"", "none"}:
        return ReviewResponse(status="skipped", backend="none", model="none", text="External vision review skipped.")
    if backend == "openai-compatible":
        return _review_vision_openai_compatible(system_prompt, user_prompt, image_paths)
    if backend == "internal-http":
        return _review_vision_internal_http(system_prompt, user_prompt, image_paths)
    raise ProviderError(f"Unsupported DOC_POLISH_REVIEW_BACKEND: {backend}")
