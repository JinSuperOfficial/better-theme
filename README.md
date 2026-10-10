# better-theme

> 为网页前端生成具有独特美学的设计方案，避免千篇一律的 SaaS 模板风格。
> An opinionated front-end design skill for AI agents.

一个给 AI Agent 用的前端设计 Skill：管配色、圆角、文案、动效、可访问性，
专门治"蓝紫渐变 + 大圆角 + Hero 三卡片 + 空洞文案"这一套生成式模板病。

## 结构

```text
better-theme/
├── SKILL.md                      # 入口：设计总纲 + 执行流程 + 严格模式
├── README.md                     # 本文件
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
    └── check-refs.py             # 文档卫生检查（交叉引用 / 换行符 / 行尾空白）
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

改完文档跑一遍检查，确保交叉引用没有断、换行符统一：

```bash
python3 scripts/check-refs.py
```

## 约定

- 文件名全小写、kebab-case，不写版本号，中文名改英文。
- 案例文档放 `references/cases/`。
- 文档间交叉引用用相对路径，重命名同步更新。
- 换行符一律 LF。

## License

见仓库；`asset/icon` 图标来源于公开图标库，商用请自行核对原始授权。
