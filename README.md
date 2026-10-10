# AI-Skills: better-theme

## Language / 语言

| Language | File |
| :--- | :--- |
| English | [README-EN.md](readme/README-EN.md) |
| 汉语（简体） | **README.md**（当前） |
| 漢語（繁體） | [README-CN-HANT.md](readme/README-CN-HANT.md) |
| 日本語 | [README-JP.md](readme/README-JP.md) |
| español | [README-ES.md](readme/README-ES.md) |

## 导语

> 为网页前端生成具有独特美学的设计方案，避免千篇一律的 SaaS 模板风格。
> An opinionated front-end design skill for AI agents.

一个给 AI Agent 用的前端设计 Skill：管配色、圆角、文案、动效、可访问性，
专门治"蓝紫渐变 + 大圆角 + Hero 三卡片 + 空洞文案"这一套生成式模板病。

## 结构

```text
better-theme/
├── SKILL.md                      # 入口：设计总纲 + 执行流程 + 严格模式
├── README.md                     # 简体中文说明（本文件）
├── readme/                       # 其它语言说明
├── references/                   # 按需加载的参考文档（见 references/README.md）
│   ├── README.md                 # 索引：什么时候读哪一份
│   ├── agent-guide.md            # 优化操作手册：判型 → 诊断 → 修正 → 检查清单
│   ├── color-theme.md            # 7 组场景配色 + 选色决策树
│   ├── radius.md                 # macOS 风格圆角规范（token / 同心嵌套 / 连续曲率）
│   ├── copywriting.md            # UI 文案参考（404 / 空状态 / 登录 / 加载）
│   ├── interaction.md            # 动效与交互规范（时长 / 缓动 / a11y / 反模式）
│   └── cases/
│       └── deepseek-glass.md     # 案例：玻璃拟态 + WebGL 流体 + Spring 动画
├── asset/
│   └── icon/                     # 600+ 离线 SVG 图标（阿里图标库整理）
└── scripts/
    ├── check-refs.py             # 文档卫生检查（交叉引用 / frontmatter / 换行符 / 行尾空白）
    └── sync-global.sh            # 同步到全局 ~/.dsh/skills/better-theme
```

**加载原则**：`SKILL.md` 是入口，`references/` 按需读。只加载当前任务真正需要的文件——纯配色任务不用读 `interaction.md`。

## 安装

作为 DSH Skill 使用，把仓库放进 skills 目录即可：

```bash
git clone https://github.com/JinSuperOfficial/better-theme.git ~/.dsh/skills/better-theme
```

也可以直接把 `SKILL.md` 的内容粘进对话使用（网页版 AI 无法读取本地文件时）。
图标素材在线浏览：[asset/icon](https://github.com/JinSuperOfficial/better-theme/tree/main/asset/icon/)

## 三条底线

1. **用户要求优先**：用户指定的品牌色、风格、技术栈，压过本仓库的任何建议。
2. **可访问性不让步**：对比度、键盘焦点、`prefers-reduced-motion` 三项不可跳过。
3. **不做模板**：把产品名换掉方案还成立，就说明不够具体，重做。

## 反模式速查

暖奶油背景 + 衬线标题 + 陶土橙 / 近黑背景 + 酸性绿 · 朱红 / 细线边框 + 零圆角 + 密集多栏 /
Hero + 三卡片 / 全页机械居中 / 所有组件统一一个大圆角 —— 命中任一，直接重做。

## 维护

改完文档跑一遍检查，确保交叉引用没断、frontmatter 是合法 YAML、语言表齐全、换行符统一：

```bash
python3 scripts/check-refs.py
```

改了内容要更新全局安装时，一条命令同步（`--dry-run` 可先看会改什么）：

```bash
./scripts/sync-global.sh
```

## 约定

- 文件名全小写、kebab-case，不写版本号，中文名改英文。
- 案例文档放 `references/cases/`。
- 文档间交叉引用用相对路径，重命名同步更新。
- 换行符一律 LF。

## Asset 使用与版权说明

本仓库中的 `asset/` 目录用于为 `better-theme` 提供网页设计所需的图标、图片及其他视觉参考资源。

部分资源可能来自第三方，其版权、商标权及其他相关权利仍归原权利人所有。仓库作者不主张拥有任何未明确属于本项目的第三方资源的权利。

对于第三方资源，其使用应以对应资源原作者、发布平台或许可证所规定的授权条件为准。若某项资源的许可证、来源或授权状态不明确，请勿将其直接用于公开发布、商业项目或其他可能产生版权风险的场景。

AI 可以访问和读取 `asset/` 内容，用于：

- 了解 better-theme 的视觉风格；
- 查找适合网页设计的素材；
- 在确认资源具有相应使用许可时，将其用于生成的网页。

AI 不应因为资源存在于本仓库，就默认认为该资源属于本项目、可以无限制转载，或可以用于任何商业用途。

如发生第三方资源相关的版权、商标或其他权利争议，应以该资源的实际权利归属、来源及许可证信息为准。仓库作者不对未经授权的第三方资源作权利声明。

### AI 使用原则

优先使用本项目明确提供、来源清晰且许可允许使用的资源。

对于许可证未知或授权状态不明确的资源：

1. 可以用于视觉参考；
2. 不应默认直接嵌入最终网页；
3. 应优先替换为具有明确授权的资源；
4. 必要时要求用户确认其使用权。

本说明不改变任何第三方资源原有的许可证或权利状态。

## License

本仓库自身内容（`SKILL.md`、`references/`、`scripts/`）可自由用于设计与开发；`asset/` 下第三方资源的授权见上文。
