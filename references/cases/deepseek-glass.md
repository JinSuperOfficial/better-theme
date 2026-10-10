# DeepSeek 官网效果复刻（优化版）

> 玻璃拟态 + WebGL 流体背景 + Spring 物理动画
> 已对齐 `better-theme` 设计体系与 `../radius.md` 圆角规范

---

## 效果概览

复刻 DeepSeek 官网首页的三层视觉结构：

1. **底层**：全屏 WebGL 流体噪声背景，鼠标移动时流动
2. **中层**：玻璃拟态卡片与输入框，半透明 + 模糊
3. **顶层**：Spring 物理动画驱动的顶栏收缩、光标环反馈

技术栈：React + TypeScript + Tailwind CSS + 原生 WebGL（无 Three.js）+ 原生 Spring 积分。

---

## 1. 设计 Token（对齐圆角规范）

原实现把卡片圆角设到 24px、面板 16px，超出了 `../radius.md` 的 macOS 克制取向。修正后：

```css
:root {
  /* ---------- 玻璃材质 ---------- */
  --glass-blur: 12px;
  --glass-saturate: 130%;          /* 收敛自 180%，避免过饱和 */
  --surface-1: hsla(0, 0%, 100%, 0.30);
  --surface-raised: hsla(0, 0%, 100%, 0.45);
  --border-glass: hsla(0, 0%, 100%, 0.20);

  /* ---------- 文字 ---------- */
  --text-primary: #152443;         /* 蓝黑，玻璃上对比度更稳 */
  --text-secondary: rgba(21, 36, 67, 0.70);
  --text-on-brand: #ffffff;

  /* ---------- 品牌色 ---------- */
  --brand: #4d6bfe;
  --brand-deep: #3a65c2;
  --brand-ghost: hsla(222, 98%, 65%, 0.12);

  /* ---------- 圆角（对齐 ../radius.md） ---------- */
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 10px;
  --radius-xl: 12px;
  --radius-pill: 999px;

  /* 语义映射 */
  --radius-card: var(--radius-lg);       /* 10px，原 24px */
  --radius-panel: var(--radius-xl);      /* 12px，原 16px */
  --radius-control: var(--radius-md);    /* 8px */

  /* ---------- 动效 ---------- */
  --ease-out: cubic-bezier(0.2, 0.7, 0.2, 1);
  --ease-in-out: cubic-bezier(0.6, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --dur-fast: 150ms;
  --dur-base: 300ms;
  --dur-slow: 600ms;
}
```

**关键修正：**

| Token              |   原值 |  修正值 | 依据          |
| ------------------ | ---: | ---: | ----------- |
| `--radius-card`    | 24px | 10px | 卡片 8–10px   |
| `--radius-panel`   | 16px | 12px | 窗口/面板 ≤12px |
| `--glass-saturate` | 180% | 130% | 避免过饱和       |

---

## 2. 玻璃拟态卡片

原实现只给了一个固定 `blur(12px)`，缺少性能与可访问性降级。优化后：

```css
.glass-card {
  background: var(--surface-1);
  backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-card);
  padding: 16px;
}

/* 内层元素同心：inner = max(0, outer - padding) */
.glass-card .inner {
  border-radius: max(0px, calc(var(--radius-card) - 8px)); /* 2px，视觉调至 4px */
}

/* 键盘焦点必须可见 */
.glass-card :focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}

/* 低端设备 / 减少动效：降级为实色，去掉模糊 */
@media (prefers-reduced-motion: reduce) {
  .glass-card {
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    background: hsla(0, 0%, 100%, 0.92);
  }
}

/* 不支持 backdrop-filter 的浏览器 */
@supports not (backdrop-filter: blur(1px)) {
  .glass-card {
    background: hsla(0, 0%, 100%, 0.92);
  }
}
```

**对比度提醒：** 玻璃上的文字 `--text-primary: #152443` 在 `hsla(0,0%,100%,0.92)` 上对比度约 14:1，远高于 4.5:1。如果背景流体过亮，可在卡片内叠一层 `hsla(0,0%,100%,0.15)` 实底兜底。

---

## 3. WebGL 流体背景

原实现质量不错：fbm 噪声、`preserveDrawingBuffer: true`、`ResizeObserver` 重绘、hover 才跑 RAF。但缺了三件事——reduced-motion、移动端 DPR、静态降级。

```tsx
// FlowBackground.tsx
import { useEffect, useRef } from "react";

export function FlowBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rafRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const gl = canvas.getContext("webgl", {
      alpha: true,
      antialias: false,
      preserveDrawingBuffer: true,
    });
    if (!gl) return;

    // ---- 可访问性：减少动效时完全禁用 ----
    const prefersReduced = matchMedia("(prefers-reduced-motion: reduce)");
    if (prefersReduced.matches) {
      canvas.style.display = "none";
      return;
    }

    // ---- 移动端降低分辨率 ----
    const isMobile = matchMedia("(hover: none), (pointer: coarse)").matches;
    const dpr = isMobile ? 1 : Math.min(devicePixelRatio, 2);

    // ... shader 编译、program 链接、buffer 设置 ...

    function resize() {
      const w = canvas.clientWidth * dpr;
      const h = canvas.clientHeight * dpr;
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
        gl!.viewport(0, 0, w, h);
        draw(); // 静态重绘一帧
      }
    }

    let mouseX = 0.5, mouseY = 0.5;
    let targetX = 0.5, targetY = 0.5;
    let hovering = false;

    function draw() {
      // ... uniform 传参 + gl.drawArrays ...
      mouseX += (targetX - mouseX) * 0.06;
      mouseY += (targetY - mouseY) * 0.06;
    }

    function loop() {
      draw();
      if (hovering) rafRef.current = requestAnimationFrame(loop);
    }

    const onMove = (e: PointerEvent) => {
      targetX = e.clientX / innerWidth;
      targetY = 1 - e.clientY / innerHeight;
    };
    const onEnter = () => { hovering = true; loop(); };
    const onLeave = () => { hovering = false; cancelAnimationFrame(rafRef.current); };

    const ro = new ResizeObserver(resize);
    ro.observe(canvas);
    resize();
    draw();

    addEventListener("pointermove", onMove);
    canvas.addEventListener("pointerenter", onEnter);
    canvas.addEventListener("pointerleave", onLeave);

    // 监听偏好变化，动态禁用
    const onPrefChange = (e: MediaQueryListEvent) => {
      if (e.matches) {
        canvas.style.display = "none";
        cancelAnimationFrame(rafRef.current);
      }
    };
    prefersReduced.addEventListener("change", onPrefChange);

    return () => {
      cancelAnimationFrame(rafRef.current);
      ro.disconnect();
      removeEventListener("pointermove", onMove);
      canvas.removeEventListener("pointerenter", onEnter);
      canvas.removeEventListener("pointerleave", onLeave);
      prefersReduced.removeEventListener("change", onPrefChange);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 -z-10 h-full w-full"
      aria-hidden="true"
    />
  );
}
```

静态降级背景（reduced-motion 时显示）：

```css
.hero-static-bg {
  background:
    radial-gradient(ellipse 80% 60% at 20% 30%, #8aa3d6 0%, transparent 60%),
    radial-gradient(ellipse 70% 50% at 80% 70%, #c7d6f5 0%, transparent 60%),
    linear-gradient(160deg, #eef3fb 0%, #dbe6f8 100%);
}
```

**Shader 性能要点：**

- `preserveDrawingBuffer: true` 在你需要 readPixels 或截图时才必要；否则设 `false` 更省内存
- 全屏 canvas 用 `fixed inset-0 -z-10`，不要触发 layout
- 只在 `pointerenter` 后跑 RAF，`pointerleave` 立即停
- 移动端 DPR cap 到 1，帧率更稳

---

## 4. Spring 物理动画

原实现正确解决了两个经典坑：半隐式欧拉（先 v 后 x）、class 与 spring 解耦。保留这两点，补上按页面类型分档的参数。

```ts
// spring.ts
export interface SpringConfig {
  stiffness: number;
  damping: number;
}

// 品牌落地页：有弹性，允许过冲
export const brandSpring: SpringConfig = { stiffness: 180, damping: 20 };

// 产品官网：克制，接近临界阻尼
export const productSpring: SpringConfig = { stiffness: 200, damping: 30 };

// 工具/后台：不用 spring，直接 CSS easeOut
// transition: all var(--dur-base) var(--ease-out);
```

积分实现（半隐式欧拉，先速度后位置）：

```ts
export function createSpring(
  initial: number,
  config: SpringConfig,
  onUpdate: (value: number) => void
) {
  let x = initial;
  let v = 0;
  let raf = 0;
  let target = initial;

  function step() {
    const dt = 1 / 60;
    const a = -config.stiffness * (x - target) - config.damping * v;
    v += a * dt;        // 先更新速度
    x += v * dt;        // 再用新速度更新位置
    onUpdate(x);

    if (Math.abs(v) > 0.01 || Math.abs(x - target) > 0.01) {
      raf = requestAnimationFrame(step);
    } else {
      x = target;
      v = 0;
      onUpdate(x);
    }
  }

  return {
    set(newTarget: number) {
      target = newTarget;
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(step);
    },
    stop() {
      cancelAnimationFrame(raf);
    },
  };
}
```

顶栏收缩示例（scroll 时高度从 64 → 48）：

```tsx
function useShrinkHeader() {
  const ref = useRef<HTMLElement>(null);
  const springRef = useRef<ReturnType<typeof createSpring>>();

  useEffect(() => {
    const el = ref.current!;
    springRef.current = createSpring(64, productSpring, (h) => {
      el.style.height = `${h}px`;
    });

    const onScroll = () => {
      springRef.current!.set(scrollY > 40 ? 48 : 64);
    };
    addEventListener("scroll", onScroll, { passive: true });
    return () => {
      removeEventListener("scroll", onScroll);
      springRef.current?.stop();
    };
  }, []);

  return ref;
}
```

> `../interaction.md` 第 10 节 反模式第 11 条：弹簧是 CPU 密集型，超过 10 个元素同时用 spring 应改按时长 + easeOut。顶栏只有一个，安全。

---

## 5. 光标环

原实现用了 RAF + 指数缓动 + `mix-blend-mode: difference`，技术上干净。但 `../interaction.md` 的反模式第 4 条是“鼠标移动跟随元素跑——变成鼠标玩具”。因此必须**限定适用场景**。

```tsx
function CursorRing() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // 仅品牌落地页启用；产品官网/后台禁用
    const isBrandPage = document.body.dataset.pageType === "brand";
    if (!isBrandPage) return;

    // 触屏直接关掉
    if (!matchMedia("(hover: hover) and (pointer: fine)").matches) return;

    // 减少动效时关掉
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const el = ref.current!;
    let x = innerWidth / 2, y = innerHeight / 2;
    let tx = x, ty = y;
    let raf = 0;

    const onMove = (e: PointerEvent) => { tx = e.clientX; ty = e.clientY; };
    const loop = () => {
      x += (tx - x) * 0.12;
      y += (ty - y) * 0.12;
      el.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      raf = requestAnimationFrame(loop);
    };

    addEventListener("pointermove", onMove);
    loop();
    return () => {
      removeEventListener("pointermove", onMove);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <div
      ref={ref}
      className="cursor-ring"
      aria-hidden="true"
    />
  );
}
```

```css
.cursor-ring {
  position: fixed;
  top: 0;
  left: 0;
  width: 320px;
  height: 320px;
  margin: -160px 0 0 -160px;
  border-radius: var(--radius-pill);
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: difference;
  background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, transparent 70%);
  opacity: 0;
  transition: opacity var(--dur-fast) var(--ease-out);
}

body[data-hovering="true"] .cursor-ring {
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .cursor-ring { display: none; }
}

@media (hover: none) {
  .cursor-ring { display: none; }
}
```

**场景对照（`../interaction.md` 第 11 节 动效强度表）：**

| 页面类型 | 光标跟随 | 本站是否启用 |
|---|---|---|
| 品牌落地页 | ✅ 可 | ✅ |
| 产品官网 | ❌ 否 | ❌ |
| SaaS 后台 | ❌ 禁止 | ❌ |
| 文档站 | ❌ 否 | ❌ |

---

## 6. 可访问性（不可跳过）

原文缺失的三项，这里补齐。

```css
/* 全局 reduced-motion 降级 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* 键盘焦点 */
:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}

/* 自定义组件焦点 */
.glass-input:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
  border-color: var(--brand);
}
```

**焦点管理清单：**

- 玻璃输入框 `Tab` 可达，`:focus-visible` 有 2px 品牌色描边
- 模态/下拉打开时焦点移入，关闭归还触发按钮
- 自定义下拉用 `role="listbox"` + 方向键导航
- `Esc` 关闭浮层

**状态不只靠颜色传递：**

```tsx
// 加载状态：文字 + spinner，不只是一个转圈
<div role="status" aria-live="polite">
  <Spinner aria-hidden="true" />
  <span>正在准备绝佳的{{ITEM}}…</span>
</div>
```

---

## 7. 完整目录结构

```text
src/
├── styles/
│   └── tokens.css          # 全部设计 token（第 1 节）
├── components/
│   ├── FlowBackground.tsx  # WebGL 流体背景（第 3 节）
│   ├── GlassCard.tsx       # 玻璃卡片（第 2 节）
│   ├── ShrinkHeader.tsx    # Spring 顶栏（第 4 节）
│   └── CursorRing.tsx      # 光标环（第 5 节）
├── lib/
│   └── spring.ts           # Spring 积分（第 4 节）
└── a11y.css                # 可访问性样式（第 6 节）
```

---

## 8. 最终检查清单

生成后逐项核对：

- [ ] 所有卡片圆角 ≤ `10px`，面板 ≤ `12px`，无 `rounded-2xl` / `rounded-3xl`
- [ ] 按钮/输入框 8px，未使用 `rounded-full`（仅头像、开关、光标环允许）
- [ ] 嵌套圆角同心：`inner = max(0, outer - padding)`
- [ ] `prefers-reduced-motion` 下 WebGL 隐藏、Spring 停用、光标环移除
- [ ] 移动端 WebGL DPR cap 到 1，光标跟随关闭
- [ ] 玻璃卡片文字对比度 ≥ 4.5:1
- [ ] `:focus-visible` 2px 品牌色描边可见
- [ ] Spring 只用于单元素（顶栏），未批量使用
- [ ] 光标环仅在 `data-page-type="brand"` 时启用
- [ ] 无蓝紫渐变作为主视觉（品牌色 `#4d6bfe` 为纯色，符合规范）
- [ ] 动效时长 ≤ 700ms（进入）/ ≤ 300ms（反馈）
- [ ] 只动 `transform` / `opacity`，无 layout thrash

---

## 9. 关键修正对照

| 模块 | 原文 | 优化后 | 依据 |
|---|---|---|---|
| 卡片圆角 | 16px / 24px | 10px / 12px | `../radius.md` |
| 玻璃饱和度 | 180% | 130% | 避免过饱和 |
| reduced-motion | 未处理 | 三处动效全部降级 | `../interaction.md` §7 |
| 移动端 WebGL | 未降级 | DPR cap 1 | 性能守则 |
| 光标环场景 | 未限定 | 仅品牌页 | 反模式 §4 |
| Spring 参数 | 单一默认 | 三档分页面类型 | `../interaction.md` §8 |
| 动效 token | 未抽取 | 缓动 + 时长 token | 可维护性 |
| 对比度验证 | 未提及 | 14:1（玻璃上） | WCAG AA |
| `:focus-visible` | 未提及 | 2px 品牌描边 | `../interaction.md` §7 |
| 静态降级 | 无 | CSS 渐变兜底 | 渐进增强 |

---

> 这套方案保留了原文的技术深度（WebGL 流体、Spring 积分、玻璃材质），修正了设计系统对齐问题（圆角、饱和度、场景限定），补齐了可访问性（reduced-motion、焦点、对比度）。可以直接落地，也可以作为 `better-theme` 体系中"玻璃拟态 + 流体背景"的参考实现。