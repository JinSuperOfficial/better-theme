# AI-Skills: better-theme

## Language / 语言

| Language | File |
| :--- | :--- |
| English | [README-EN.md](README-EN.md) |
| 汉语（简体） | [README.md](../README.md) |
| 漢語（繁體） | **README-CN-HANT.md**（當前） |
| 日本語 | [README-JP.md](README-JP.md) |
| español | [README-ES.md](README-ES.md) |

## 導語

> 為網頁前端生成具有獨特美學的設計方案，避免千篇一律的 SaaS 模板風格。
> An opinionated front-end design skill for AI agents.

一個給 AI Agent 用的前端設計 Skill：管配色、圓角、文案、動效、無障礙，
專門治「藍紫漸層 + 大圓角 + Hero 三卡片 + 空洞文案」這一套生成式模板病。

## 結構

```text
better-theme/
├── SKILL.md                      # 入口：設計總綱 + 執行流程 + 嚴格模式
├── README.md                     # 簡體中文說明（本文件）
├── readme/                       # 其它語言說明
├── references/                   # 按需載入的參考文件（見 references/README.md）
│   ├── README.md                 # 索引：什麼時候讀哪一份
│   ├── agent-guide.md            # 優化操作手冊：判型 → 診斷 → 修正 → 檢查清單
│   ├── color-theme.md            # 7 組場景配色 + 選色決策樹
│   ├── radius.md                 # macOS 風格圓角規範（token / 同心嵌套 / 連續曲率）
│   ├── copywriting.md            # UI 文案參考（404 / 空狀態 / 登入 / 載入）
│   ├── interaction.md            # 動效與互動規範（時長 / 緩動 / a11y / 反模式）
│   └── cases/
│       └── deepseek-glass.md     # 案例：玻璃擬態 + WebGL 流體 + Spring 動畫
├── asset/
│   └── icon/                     # 600+ 離線 SVG 圖示（阿里圖示庫整理）
└── scripts/
    ├── check-refs.py             # 文件衛生檢查（交叉引用 / frontmatter / 換行符 / 行尾空白）
    └── sync-global.sh            # 同步到全域 ~/.dsh/skills/better-theme
```

**載入原則**：`SKILL.md` 是入口，`references/` 按需讀。只載入當前任務真正需要的檔案——純配色任務不用讀 `interaction.md`。

## 安裝

作為 DSH Skill 使用，把倉庫放進 skills 目錄即可：

```bash
git clone https://github.com/JinSuperOfficial/better-theme.git ~/.dsh/skills/better-theme
```

也可以直接把 `SKILL.md` 的內容貼進對話使用（網頁版 AI 無法讀取本機檔案時）。
圖示素材線上瀏覽：[asset/icon](https://github.com/JinSuperOfficial/better-theme/tree/main/asset/icon/)

## 三條底線

1. **使用者要求優先**：使用者指定的品牌色、風格、技術棧，壓過本倉庫的任何建議。
2. **無障礙不讓步**：對比度、鍵盤焦點、`prefers-reduced-motion` 三項不可跳過。
3. **不做模板**：把產品名換掉方案還成立，就說明不夠具體，重做。

## 反模式速查

暖奶油背景 + 襯線標題 + 陶土橙 / 近黑背景 + 酸性綠 · 朱紅 / 細線邊框 + 零圓角 + 密集多欄 /
Hero + 三卡片 / 全頁機械居中 / 所有元件統一一個大圓角 —— 命中任一，直接重做。

## 維護

改完文件跑一遍檢查，確保交叉引用沒斷、frontmatter 是合法 YAML、語言表齊全、換行符統一：

```bash
python3 scripts/check-refs.py
```

改了內容要更新全域安裝時，一條指令同步（`--dry-run` 可先看會改什麼）：

```bash
./scripts/sync-global.sh
```

## 約定

- 檔案名稱全小寫、kebab-case，不寫版本號，中文名改英文。
- 案例文件放 `references/cases/`。
- 文件間交叉引用用相對路徑，重新命名時同步更新。
- 換行符一律 LF。

## Asset 使用與版權說明

本倉庫中的 `asset/` 目錄用於為 `better-theme` 提供網頁設計所需的圖示、圖片及其他視覺參考資源。

部分資源可能來自第三方，其著作權、商標權及其他相關權利仍歸原權利人所有。倉庫作者不主張擁有任何未明確屬於本專案的第三方資源的權利。

對於第三方資源，其使用應以對應資源原作者、發布平台或授權條款所規定的授權條件為準。若某項資源的授權條款、來源或授權狀態不明確，請勿將其直接用於公開發布、商業專案或其他可能產生著作權風險的情境。

AI 可以存取和讀取 `asset/` 內容，用於：

- 了解 better-theme 的視覺風格；
- 查找適合網頁設計的素材；
- 在確認資源具有相應使用授權時，將其用於生成的網頁。

AI 不應因為資源存在於本倉庫，就預設認為該資源屬於本專案、可以無限制轉載，或可以用於任何商業用途。

如發生第三方資源相關的著作權、商標或其他權利爭議，應以該資源的實際權利歸屬、來源及授權條款資訊為準。倉庫作者不對未經授權的第三方資源作權利聲明。

### AI 使用原則

優先使用本專案明確提供、來源清晰且授權允許使用的資源。

對於授權條款未知或授權狀態不明確的資源：

1. 可以用於視覺參考；
2. 不應預設直接嵌入最終網頁；
3. 應優先替換為具有明確授權的資源；
4. 必要時要求使用者確認其使用權。

本說明不改變任何第三方資源原有的授權條款或權利狀態。

## License

本倉庫自身內容（`SKILL.md`、`references/`、`scripts/`）可自由用於設計與開發；`asset/` 下第三方資源的授權見上文。
