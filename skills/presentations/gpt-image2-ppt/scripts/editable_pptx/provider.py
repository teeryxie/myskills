"""OpenAI-compatible image generation and edit provider."""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Any


class OpenAIImageProvider:
    """Small adapter around the OpenAI Python SDK Images resource."""

    def __init__(self, client: Any, model: str = "gpt-image-2", quality: str = "high") -> None:
        self.client = client
        self.model = model
        self.quality = quality

    @classmethod
    def from_env(cls) -> "OpenAIImageProvider":
        base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not base_url:
            raise ValueError("缺少 OPENAI_BASE_URL")
        if not api_key:
            raise ValueError("缺少 OPENAI_API_KEY")

        from openai import OpenAI

        client = OpenAI(base_url=base_url, api_key=api_key)
        return cls(
            client,
            os.environ.get("GPT_IMAGE_MODEL_NAME", "gpt-image-2"),
            os.environ.get("GPT_IMAGE_QUALITY", "high"),
        )

    @staticmethod
    def _decode_first_image(response: Any) -> bytes:
        data = getattr(response, "data", None) or []
        if not data:
            raise RuntimeError("图片接口没有返回图片数据")
        encoded = getattr(data[0], "b64_json", None)
        if not encoded:
            raise RuntimeError("图片接口未返回 b64_json")
        try:
            return base64.b64decode(encoded, validate=True)
        except (ValueError, TypeError) as exc:
            raise RuntimeError("图片接口返回了无效的 b64_json") from exc

    def generate(self, prompt: str, output_path: Path | str, size: str = "1024x1024") -> Path:
        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=size,
            quality=self.quality,
        )
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self._decode_first_image(response))
        return path

    def edit(
        self,
        image_path: Path | str,
        mask_path: Path | str,
        prompt: str,
        output_path: Path | str,
        size: str = "1024x1024",
    ) -> Path:
        with open(image_path, "rb") as image_file, open(mask_path, "rb") as mask_file:
            response = self.client.images.edit(
                model=self.model,
                image=image_file,
                mask=mask_file,
                prompt=prompt,
                size=size,
                quality=self.quality,
            )
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self._decode_first_image(response))
        return path
