# AI-Skills: better-theme

## Language / 语言

| Language | File |
| :--- | :--- |
| English | **README-EN.md** (current) |
| 汉语（简体） | [README.md](../README.md) |
| 漢語（繁體） | [README-CN-HANT.md](README-CN-HANT.md) |
| 日本語 | [README-JP.md](README-JP.md) |
| español | [README-ES.md](README-ES.md) |

## Intro

> 为网页前端生成具有独特美学的设计方案，避免千篇一律的 SaaS 模板风格。
> An opinionated front-end design skill for AI agents.

A front-end design Skill for AI agents. It covers color, corner radius, copywriting, motion and
accessibility, and it exists to cure the "purple-to-blue gradient + huge rounded corners +
hero-plus-three-cards + empty marketing words" template disease.

## Structure

```text
better-theme/
├── SKILL.md                      # Entry point: design doctrine + workflow + strict mode
├── README.md                     # Simplified Chinese docs (the canonical one)
├── readme/                       # Docs in other languages
├── references/                   # On-demand reference docs (see references/README.md)
│   ├── README.md                 # Index: which file to read when
│   ├── agent-guide.md            # Optimization playbook: page type → diagnosis → fixes → checklist
│   ├── color-theme.md            # 7 scenario palettes + a color decision tree
│   ├── radius.md                 # macOS-style corner radius spec (tokens / concentric nesting / continuous curvature)
│   ├── copywriting.md            # UI copy reference (404 / empty states / sign-in / loading)
│   ├── interaction.md            # Motion and interaction spec (duration / easing / a11y / anti-patterns)
│   └── cases/
│       └── deepseek-glass.md     # Case study: glassmorphism + WebGL fluid + spring physics
├── asset/
│   └── icon/                     # 600+ offline SVG icons (collected from an icon library)
└── scripts/
    ├── check-refs.py             # Doc hygiene check (cross-refs / frontmatter / line endings / trailing whitespace)
    └── sync-global.sh            # Sync into the global ~/.dsh/skills/better-theme
```

**Loading rule**: `SKILL.md` is the entry point, `references/` is read on demand. Load only what the
current task actually needs — a pure color task never needs `interaction.md`.

## Install

To use it as a DSH Skill, drop the repo into your skills directory:

```bash
git clone https://github.com/JinSuperOfficial/better-theme.git ~/.dsh/skills/better-theme
```

You can also paste the contents of `SKILL.md` straight into a chat (for web-only AI that cannot read
local files). Browse the icons online:
[asset/icon](https://github.com/JinSuperOfficial/better-theme/tree/main/asset/icon/)

## Three hard limits

1. **The user wins**: brand colors, style and stack the user specifies override anything this repo suggests.
2. **Accessibility is not negotiable**: contrast, keyboard focus and `prefers-reduced-motion` are never skipped.
3. **No templates**: if the design still works after you swap the product name, it was not specific enough. Redo it.

## Anti-pattern cheatsheet

Warm cream background + serif headline + terracotta / near-black background + acid green or vermilion /
hairline borders + zero radius + dense multi-column / hero + three cards / everything mechanically
centered / one big radius for every component. Hit any of these and you redo the whole thing.

## Maintenance

After editing docs, run the check to make sure cross-references are intact, the frontmatter is valid
YAML, the language table is complete and line endings are consistent:

```bash
python3 scripts/check-refs.py
```

To push your changes into the global install, one command does it (`--dry-run` shows what would change):

```bash
./scripts/sync-global.sh
```

## Conventions

- Filenames are lowercase kebab-case, no version numbers, Chinese names translated to English.
- Case studies live in `references/cases/`.
- Cross-references use relative paths; update them when you rename a file.
- Line endings are always LF.

## Asset usage and copyright

The `asset/` directory in this repo provides icons, images and other visual reference material for
`better-theme`.

Some of those assets may come from third parties; copyright, trademark and related rights remain with
their original owners. The repo author claims no rights over any third-party asset that is not
explicitly part of this project.

For third-party assets, use is governed by the terms set by the original author, the publishing
platform or the applicable license. If an asset's license, source or authorization status is unclear,
do not use it in a public release, a commercial project, or any other situation that carries copyright
risk.

AI may access and read the contents of `asset/` in order to:

- understand the visual style of better-theme;
- find material suitable for web design;
- use it in a generated web page once the asset's license has been confirmed.

The mere presence of an asset in this repo does not mean it belongs to this project, that it can be
redistributed without restriction, or that it can be used commercially.

If a dispute arises over a third-party asset, the actual ownership, source and license information of
that asset governs. The repo author makes no rights claim over unauthorized third-party assets.

### Rules for AI use

Prefer assets that this project provides explicitly, whose source is clear and whose license permits
the intended use.

For assets with an unknown or unclear license:

1. they may be used as visual reference;
2. they must not be embedded into a final web page by default;
3. they should be replaced with clearly licensed assets;
4. when necessary, ask the user to confirm their right to use them.

Nothing here changes the original license or rights status of any third-party asset.

## License

This repo's own content (`SKILL.md`, `references/`, `scripts/`) may be freely used for design and
development; licensing for third-party assets under `asset/` is described above.
