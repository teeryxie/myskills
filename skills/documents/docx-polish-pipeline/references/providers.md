# Providers

## Principle

Keep document generation independent from review backends. The pipeline must still generate `docx/pdf` artifacts even when no external review backend is available.

## Supported Backends

### `none`

Use when:

- no external key is available
- network access is unavailable
- the user only needs document generation

Behavior:

- skip text and vision review
- still emit all file artifacts

### `openai-compatible`

Use when the environment can call an OpenAI-compatible API gateway or provider.

Environment variables:

- `DOC_POLISH_REVIEW_BACKEND=openai-compatible`
- `DOC_POLISH_API_KEY`
- `DOC_POLISH_BASE_URL`
- `DOC_POLISH_TEXT_MODEL`
- `DOC_POLISH_VISION_MODEL`

Security note:

- the skill does not store the key in files
- the endpoint still receives the prompt, images, and bearer token
- trust the endpoint before using sensitive content

### `internal-http`

Use when a shared internal review service should hide provider-specific credentials from end users.

Environment variables:

- `DOC_POLISH_REVIEW_BACKEND=internal-http`
- `DOC_POLISH_INTERNAL_BASE_URL`
- `DOC_POLISH_INTERNAL_TOKEN` (optional)

Expected endpoints:

- `POST /review/text`
- `POST /review/vision`

## Recommended Boundary

For personal use, `openai-compatible` is enough.

For team reuse, prefer `internal-http` so the skill remains reusable without distributing third-party keys.
