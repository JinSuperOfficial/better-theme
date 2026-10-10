---
name: circle-angle
description: "圆角风格化窗口设计"
tags:
  - design
  - macos
  - radius
  - tailwind
  - css
  - ai-instruction
version: 1.0
---

# macOS 风格圆角规范（Web UI）

## 1. 核心目标

生成网页时，圆角应满足：

- 克制：不要所有元素都大圆角。
- 偏方：整体更接近 macOS 窗口、按钮、输入框，而不是 iOS 小组件。
- 小半径：绝大多数组件圆角不超过 `12px`。
- 连续曲率：优先模拟 Apple 的 continuous corner / squircle。
- 同心嵌套：内层圆角根据外层圆角和 padding 计算。
- 层级化：窗口、卡片、按钮、标签使用不同半径，不要统一一个值。

一句话标准：

> 默认 `rounded-md` / `rounded-lg`，窗口最多 `rounded-xl`，禁止 `rounded-2xl` / `rounded-3xl` 和全局 `rounded-full`。

---

## 2. 圆角层级 Token

### 2.1 基础半径

| 层级 | 半径 | Tailwind 建议 | 用途 |
|---|---:|---|---|
| 极小 | 4px | `rounded-xs` | 标签、徽章、小提示 |
| 小 | 6px | `rounded-sm` | 小按钮、输入框、分段控件 |
| 中 | 8px | `rounded-md` | 标准按钮、输入框、下拉框 |
| 大 | 10px | `rounded-lg` | 卡片、菜单、浮层、弹窗内容区 |
| 特大 | 12px | `rounded-xl` | 窗口、主面板、大型弹窗 |
| 胶囊 | 999px | `rounded-full` | 仅头像、开关、状态点 |

### 2.2 组件映射

| 组件 | 推荐圆角 | Tailwind |
|---|---:|---|
| 窗口 / 主面板 | 10–12px | `rounded-xl` |
| 弹窗 / Modal | 10–12px | `rounded-xl` |
| 卡片 / Card | 8–10px | `rounded-lg` |
| 下拉菜单 / Popover | 8–10px | `rounded-lg` |
| 按钮 / Button | 6–8px | `rounded-md` |
| 输入框 / Input | 6–8px | `rounded-md` |
| 选择器 / Select | 6–8px | `rounded-md` |
| 分段控件 | 6–8px | `rounded-md` |
| 标签 / Badge | 4–6px | `rounded-xs` / `rounded-sm` |
| 头像 / Avatar | 999px | `rounded-full` |
| 开关 / Switch | 999px | `rounded-full` |
| 状态点 | 999px | `rounded-full` |

---

## 3. 强制规则

### 3.1 小半径优先

- 普通按钮、输入框、选择器：`6–8px`。
- 卡片、菜单、浮层：`8–10px`。
- 窗口、弹窗、主面板：`10–12px`。
- 标签、徽章：`4–6px`。
- 只有头像、开关、状态点才允许 `999px` / `rounded-full`。

### 3.2 禁止项

禁止：

- 禁止卡片、按钮、输入框使用 `rounded-full`。
- 禁止默认使用 `rounded-2xl`、`rounded-3xl`。
- 禁止所有组件统一 `16px`、`20px`、`24px` 大圆角。
- 禁止气泡化 UI、胶囊化按钮、iOS 小组件式大圆角。
- 禁止嵌套时内外圆角相同。
- 禁止圆角超过元素高度的 `25%–30%`。
- 禁止为了圆角引入大型依赖。

### 3.3 高度比例

圆角不应超过元素高度的约 `25%`。

| 元素高度 | 推荐圆角 |
|---:|---:|
| 24px | 4–6px |
| 32px | 6–8px |
| 40px | 8px |
| 48px | 8–10px |
| 64px+ | 10–12px |

示例：

- 高度 32px 的按钮：用 `6–8px`，不要用 `16px`。
- 高度 40px 的输入框：用 `8px`，不要用 `20px`。
- 高度 48px 的卡片头：用 `10px` 左右。

### 3.4 同心嵌套

嵌套元素必须保持同心：

```text
inner-radius = max(0, outer-radius - padding)
```

如果内层没有独立背景、边框或阴影，可以不设置内层圆角。  
如果内层有独立背景，必须重新计算。

示例：

| 外层圆角 | padding | 内层圆角 |
|---:|---:|---:|
| 12px | 8px | 4px |
| 10px | 6px | 4px |
| 8px | 4px | 4px |
| 12px | 12px | 0px |
| 10px | 12px | 0px |

错误示例：

```css
/* 错误：外层 12px，内层也 12px */
.card { border-radius: 12px; padding: 8px; }
.card-inner { border-radius: 12px; }
```

正确示例：

```css
.card {
  border-radius: var(--radius-lg); /* 10px */
  padding: 8px;
}

.card-inner {
  border-radius: max(0px, calc(var(--radius-lg) - 8px)); /* 2px，可按视觉调至 4px */
}
```

---

## 4. CSS Token

```css
:root {
  --radius-none: 0;
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 10px;
  --radius-xl: 12px;
  --radius-pill: 999px;

  --radius-window: var(--radius-xl);
  --radius-modal: var(--radius-xl);
  --radius-card: var(--radius-lg);
  --radius-popover: var(--radius-lg);
  --radius-control: var(--radius-md);
  --radius-button: var(--radius-md);
  --radius-input: var(--radius-md);
  --radius-badge: var(--radius-xs);
  --radius-avatar: var(--radius-pill);
  --radius-switch: var(--radius-pill);
}
```

推荐组件样式：

```css
.mac-window,
.mac-modal {
  border-radius: var(--radius-window);
}

.mac-card,
.mac-popover,
.mac-menu {
  border-radius: var(--radius-card);
}

.mac-button,
.mac-input,
.mac-select,
.mac-segmented {
  border-radius: var(--radius-control);
}

.mac-badge,
.mac-tag {
  border-radius: var(--radius-badge);
}

.mac-avatar,
.mac-switch,
.mac-status-dot {
  border-radius: var(--radius-pill);
}
```

---

## 5. Tailwind 配置

建议直接覆盖 `theme.borderRadius`，避免 AI 使用默认大圆角。

```js
// tailwind.config.js
module.exports = {
  theme: {
    borderRadius: {
      none: '0',
      xs: '4px',
      sm: '6px',
      DEFAULT: '8px',
      md: '8px',
      lg: '10px',
      xl: '12px',
      '2xl': '12px',
      '3xl': '12px',
      full: '9999px',
    },
  },
};
```

使用约定：

```html
<!-- 窗口 / 弹窗 -->
<div class="rounded-xl">...</div>

<!-- 卡片 / 菜单 -->
<div class="rounded-lg">...</div>

<!-- 按钮 / 输入框 -->
<button class="rounded-md">...</button>
<input class="rounded-md" />

<!-- 标签 / 徽章 -->
<span class="rounded-xs">...</span>

<!-- 仅头像 / 开关 -->
<img class="rounded-full" />
<button class="rounded-full" role="switch">...</button>
```

禁止：

```html
<!-- 禁止：卡片大圆角 -->
<div class="rounded-3xl">...</div>

<!-- 禁止：按钮胶囊 -->
<button class="rounded-full">...</button>

<!-- 禁止：输入框大圆角 -->
<input class="rounded-2xl" />

<!-- 禁止：所有组件统一大圆角 -->
<div class="rounded-2xl">...</div>
```

---

## 6. 连续曲率 / Squircle

macOS 的圆角不是普通 `border-radius`，而是 continuous corner / squircle。  
Web 上优先使用渐进增强：

```css
.mac-squircle {
  border-radius: var(--radius-lg);
}

@supports (corner-shape: squircle) {
  .mac-squircle {
    corner-shape: squircle;
  }
}
```

说明：

- 如果浏览器支持 `corner-shape: squircle`，则启用连续曲率。
- 如果不支持，保留较小 `border-radius` 作为降级。
- 不要为了 squircle 引入大型 JS 依赖。
- 不要为了 squircle 牺牲可访问性和性能。
- 如果必须用 SVG，保持半径克制，不要做成大圆角胶囊。

---

## 7. AI 生成指令模板

### 7.1 项目级指令


```text
当生成本项目 UI 时，必须遵守 references/macos-radius.md。

圆角规则：
- 默认使用 rounded-md / rounded-lg。
- 窗口、主面板、弹窗最多 rounded-xl。
- 禁止 rounded-2xl、rounded-3xl。
- 禁止按钮、输入框、卡片使用 rounded-full。
- 按钮、输入框：6–8px。
- 卡片、菜单、浮层：8–10px。
- 窗口、弹窗：10–12px。
- 标签、徽章：4–6px。
- 头像、开关、状态点才允许 rounded-full。
- 圆角不得超过元素高度的 25%–30%。
- 嵌套元素保持同心：inner = max(0, outer - padding)。
- 优先使用 CSS 变量 --radius-*。
- 优先模拟 macOS 连续曲率，而不是 iOS 大圆角。
```

### 7.2 生成新 UI 时

```text
请按 macOS 设计语言生成网页。圆角克制、偏方、小半径、连续曲率、同心嵌套。
默认 rounded-md / rounded-lg，窗口最多 rounded-xl。
禁止 rounded-2xl、rounded-3xl，禁止按钮/输入框/卡片 rounded-full。
按钮/输入框 6–8px；卡片/弹窗 8–10px；窗口/主面板 10–12px；标签 4–6px；头像/开关 full。
不要气泡化、不要胶囊化、不要所有元素统一大圆角。
```

### 7.3 修正现有 UI 时

```text
检查所有 rounded-* 和 border-radius。

按以下规则修正：
- 大于 12px 的圆角改成对应层级：窗口/弹窗 10–12，卡片 8–10，按钮/输入框 6–8，标签 4–6。
- 删除 rounded-2xl、rounded-3xl。
- 按钮、输入框、卡片禁止 rounded-full。
- 头像、开关、状态点保留 rounded-full。
- 内层圆角按 inner = max(0, outer - padding) 重算。
- 圆角不得超过元素高度的 25%。
- 如果所有组件统一一个大圆角，拆成层级化 token。
```

---

## 8. 审查清单

生成或修改网页后，逐项检查：

- [ ] 是否出现 `rounded-2xl` / `rounded-3xl`？
- [ ] 是否所有按钮都用了 `rounded-full`？
- [ ] 输入框是否用了 `rounded-2xl` 或更大？
- [ ] 卡片是否超过 `10px`？
- [ ] 窗口 / 弹窗是否超过 `12px`？
- [ ] 标签 / 徽章是否超过 `6px`？
- [ ] 圆角是否超过元素高度 `25%–30%`？
- [ ] 嵌套元素是否内外同圆角？
- [ ] 是否所有组件统一一个大圆角？
- [ ] 是否只有头像、开关、状态点使用 `rounded-full`？
- [ ] 是否使用 `--radius-*` CSS 变量？
- [ ] 是否在支持时渐进增强 `corner-shape: squircle`？
- [ ] 视觉是否更像 macOS，而不是 iOS 小组件或气泡 UI？

---

## 9. 正例与反例

### 正例

```html
<div class="rounded-xl">窗口 / 弹窗</div>
<div class="rounded-lg">卡片 / 菜单</div>
<button class="rounded-md">按钮</button>
<input class="rounded-md" />
<span class="rounded-xs">标签</span>
<img class="rounded-full" />
<button class="rounded-full" role="switch">开关</button>
```

### 反例

```html
<div class="rounded-3xl">卡片过大</div>
<button class="rounded-full">按钮胶囊化</button>
<input class="rounded-2xl" />
<div class="rounded-2xl">所有元素统一大圆角</div>
<div class="rounded-xl p-2">
  <div class="rounded-xl">内外不同心</div>
</div>
```

---

## 10. 迁移与搜索

搜索可疑圆角：

```bash
rg "rounded-(2xl|3xl)" src
rg "rounded-full" src
rg "border-radius:\s*(1[6-9]|[2-9][0-9])px" src
```

替换建议：

- `rounded-3xl` → `rounded-xl` 或 `rounded-lg`
- `rounded-2xl` → `rounded-lg` 或 `rounded-xl`
- 按钮 `rounded-full` → `rounded-md`
- 输入框 `rounded-2xl` → `rounded-md`
- 卡片 `rounded-2xl` → `rounded-lg`
- 标签 `rounded-lg` → `rounded-xs` 或 `rounded-sm`
- 头像 / 开关 `rounded-full` 保留

注意：不要机械全局替换 `rounded-full`，因为头像、开关、状态点合法。

---

## 11. 验收标准

- 视觉：更像 macOS 窗口、按钮、输入框，而不是 iOS 小组件、气泡、胶囊。
- 代码：无新增 `rounded-2xl` / `rounded-3xl`。
- 组件：按钮、输入框、卡片没有 `rounded-full`。
- 比例：圆角不超过元素高度 `25%–30%`。
- 嵌套：内层圆角不大于外层圆角，且尽量同心。
- 维护：使用 `--radius-*` 或 Tailwind 配置统一管理。
- 渐进增强：支持时使用 `corner-shape: squircle`，不支持时保持小半径降级。

---

## 12. macOS 与 iOS 圆角差异

| 维度 | macOS | iOS |
|---|---|---|
| 圆角大小 | 克制、偏小 | 更大、更连续 |
| 按钮 | 6–8px 圆角矩形 | 常为胶囊 |
| 卡片 | 8–10px | 16–24px 常见 |
| 窗口 | 10–12px | 不适用 |
| 整体感觉 | 桌面、工具、精确 | 移动、气泡、触控 |
| 胶囊使用 | 仅头像、开关等 | 按钮、标签、搜索框常见 |

本规范只采用 macOS 方向：

> 小半径 + 连续曲率 + 同心嵌套 + 层级化。  
> 不是大半径 + 普通 border-radius + 全局胶囊化。

---

## 13. 最终提醒

给 AI 最有效的一句话是：

```text
默认 rounded-md / rounded-lg，窗口最多 rounded-xl，禁止 rounded-2xl / rounded-3xl 和全局 rounded-full；圆角不超过元素高度 25%，嵌套保持同心。
```

如果 AI 仍然生成过大圆角，追加：

```text
圆角再小 30%，去掉胶囊，改成连续曲率，参考 macOS 窗口和按钮，不是 iOS 小组件。
```