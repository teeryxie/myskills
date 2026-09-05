# Third-party notices

This repository is a categorized synchronization collection. It does not apply one blanket license to every skill.

## ui-craft suite

The following skills originate from [educlopez/ui-craft](https://github.com/educlopez/ui-craft):

- `adapt`
- `animate`
- `audit`
- `bolder`
- `brief`
- `clarify`
- `colorize`
- `craft`
- `critique`
- `delight`
- `distill`
- `extract`
- `finalize`
- `harden`
- `heuristic`
- `polish`
- `quieter`
- `redesign`
- `remember`
- `sddesign`
- `shape`
- `start`
- `tokens`
- `typeset`
- `ui-craft`
- `ui-craft-dense-dashboard`
- `ui-craft-editorial`
- `ui-craft-minimal`
- `unhappy`

Pinned from commit `ceecc8e1fb0c2befda73da996435900d6dd0c1ac`. Upstream license: MIT. A copy is stored at `third_party/licenses/educlopez-ui-craft-MIT.txt`. Codex mirrors are used; sub-skill reference paths are adapted to the sibling `ui-craft/references/` directory without duplicating shared documents.

## ego-browser

Source: [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite).

Upstream license: MIT. A copy is stored at `third_party/licenses/citrolabs-ego-lite-MIT.txt`.

## ui-ux-pro-max

Source: [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), pinned from commit `f3ac195224eac1eb0dfe1a3059c2a6add78ffbe3`. Invocation examples use the installed skill directory rather than Claude-only environment variables; data and search logic remain upstream-derived.

Upstream license: MIT. A copy is stored at `third_party/licenses/nextlevelbuilder-ui-ux-pro-max-skill-MIT.txt`.

## scientific-figure-generator

Source: [Deepshare-Official/CCF-Figure](https://github.com/Deepshare-Official/CCF-Figure).

The skill directory contains its upstream MIT `LICENSE` file. Preserve it when redistributing the skill.

## drawio-diagram-builder

Source: [Will-hxw/drawio-diagram-builder-skill](https://github.com/Will-hxw/drawio-diagram-builder-skill), pinned from commit `a922507ccd51815f4e8764846d640a65b5fb6f7e` (version `0.4.1`).

Upstream license: MIT. A copy is stored at `third_party/licenses/Will-hxw-drawio-diagram-builder-skill-MIT.txt`. The bundled Tabler icons retain their own MIT license in the skill directory.

## playwright

The skill directory contains its upstream Apache License 2.0 `LICENSE.txt` and Microsoft `NOTICE.txt`. Preserve both files when redistributing the skill.

## collaborating-with-gemini-cli

Source: [ZhenHuangLab/collaborating-with-gemini-cli](https://github.com/ZhenHuangLab/collaborating-with-gemini-cli), pinned from commit `5cc88cbe23c3663ca0af73d1578f3315c1d0a4d0`.

Upstream license: MIT. A copy is stored at `third_party/licenses/ZhenHuangLab-collaborating-with-gemini-cli-MIT.txt`, and the skill directory also retains its upstream `LICENSE`.

## gpt-image2-ppt

Source: [JuneYaooo/gpt-image2-ppt-skills](https://github.com/JuneYaooo/gpt-image2-ppt-skills), pinned from commit `2d57ef8127b83e8232a1be4e9515f0b3cc9fc91e`.

Upstream license: Apache License 2.0. A copy is stored at `third_party/licenses/JuneYaooo-gpt-image2-ppt-skills-Apache-2.0.txt`, and the skill directory also retains its upstream `LICENSE`. This collection includes the skill runtime, styles, recipes, and directly referenced documentation, but excludes upstream repository metadata, development instructions, installer, top-level README, and environment-file example. The installation section and file tree in `SKILL.md` are adapted to this collection's shared installer and curated directory layout; generation behavior remains upstream-derived.

## lark-cli

The locally maintained `lark-ops-control`, `lark-progress-sync`, and `lark-weekly-report-submit` skills depend on the official [larksuite/cli](https://github.com/larksuite/cli). The CLI and its official embedded `lark-*` skills are not vendored in this repository; install them separately from the official npm package. The integration was verified with `@larksuite/cli` version `1.0.92`.

Upstream license: MIT. A copy is stored at `third_party/licenses/larksuite-cli-MIT.txt`.

## Vue skills

The following skills originate from [vuejs-ai/skills](https://github.com/vuejs-ai/skills), pinned from commit `c9d355ff23f654309dd02006be671859df0a134c`:

- `create-adaptable-composable`
- `vue-best-practices`
- `vue-debug-guides`
- `vue-jsx-best-practices`
- `vue-options-api-best-practices`
- `vue-pinia-best-practices`
- `vue-router-best-practices`
- `vue-testing-best-practices`

Upstream license: MIT. A copy is stored at `third_party/licenses/vuejs-ai-skills-MIT.txt`. Frontmatter-only compatibility edits move upstream `author`, `version`, and `compatibility` values into the supported `metadata` field and replace angle-bracket placeholders that the current validator rejects; workflow content remains upstream-derived.

## Locally maintained skills

The following skills are maintained in this collection and do not currently declare a separate open-source license:

- `ccfa-paper-figures`
- `docx-polish-pipeline`
- `frontend-ui-standards`
- `latex-paper-en`
- `latex-thesis-zh`
- `lark-ops-control`
- `lark-progress-sync`
- `lark-weekly-report-submit`
- `notion-paper-read`
- `rebuttal-critic`
- `rebuttal-writer`
- `remote-codex-update`

Unless a skill directory says otherwise, no additional license grant is implied.
