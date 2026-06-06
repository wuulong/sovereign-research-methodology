# 📐 方法論與手稿物理分離架構重構決策日誌 (01_methodology_manuscript_separation_plan)

> [!NOTE]
> **本建構日誌物理定錨於 2026-05-30 的進度會談。**  
> 記錄了主權大腦方法論發展史上第一次重大的「典範與實體分離」架構重構。旨在透過物理目錄區隔，確立方法論本體與寫作手稿的清晰邊界，建立「一對多（One Methodology, Multi-Papers）」的可擴展科研工序。

---

## 📊 1. 重構背景與決策經緯

在主權大腦方法論建構的初期，由於典範定義與第一篇論文寫作（介紹方法論本身的論文手稿 `sovereign_research`）是互相共演與驗證的過程，我們扁平地將所有檔案都堆疊在 `manuscripts/sovereign_research/` 底下。

然而，隨著科研心流與大腦架構越來越清晰，這種扁平的混雜結構帶來了職責模糊的問題：
1.  **大憲章與實例混淆**：大腦的系統規格（需求書、資料庫 Schema 規格、關係本體規格）是整套科研典範的「憲法地基」，不應被判定為某一篇單一論文的私有寫作資產。
2.  **無法平行寫作**：當君王想使用這套方法論平行撰寫其他應用領域的手稿（如山區水文觀測等）時，無法輕易調用這套憲法規格，會造成嚴重的程式碼與文件心智摩擦。

為了徹底解決這個架構瓶頸，君王 (wuulong) 物理拍板了「**方法論規格大憲章（Methodology）**」與「**具體手稿實體（Manuscripts）**」物理分離的最高架構決策。

---

## 🏗️ 2. 物理重構軌跡與目錄對位

重構物理移除了 `manuscripts/sovereign_research/` 中的典範檔案，並將其重新命名歸口移入新創立的 `methodology/` 目錄，雙軌各自獨立：

### 📐 Methodology 支柱：大憲章本體規格 (`methodology/`)
本目錄專門整理大腦方法論的架構、規則與改良，包含三大地基定錨規格（地基定錨生命週期階段一）：
- `methodology_01_requirements.md` ➔ 系統工程規格需求書。
- `methodology_02_system_architecture_navigator.md` ➔ 總入口導覽與 10 大分區地圖。
- `methodology_11_database_schema_spec.md` ➔ 十一表大腦 Schema 剛性規範。
- `methodology_12_relation_ontology_spec.md` ➔ 文獻有向演化關係本體規格。
- **`build_log/`** ➔ **方法論專屬建構日誌**（本檔案即為 `01` 號第一案），用以物理存檔方法論本身的改良決策軌跡。

### 📂 Manuscripts 支柱：具體寫作手稿 (`manuscripts/`)
本目錄專注存放具體寫作論文，各論文配有獨立子目錄（例如 `manuscripts/sovereign_research/`），手稿檔案採用數字工序契約，從 `04` 順序開始編起（工序階段二至階段五）：
- `sovereign_research_04_toc.md` 至 `sovereign_research_14_audit_report.md`。
- **`build_log/`** ➔ **手稿專屬建構日誌**（第一案為 `01_mci_improvement_plan.md`，用以物理存檔如何拉高該篇論文的 MCI 指數之行動對策）。

---

## 🧪 3. 工具鏈無痛相容與驗證結論

我們物理執行了兩大審計與驗證工具（MCI 審計與 MPM 驗證），以檢核本次重構是否影響工具鏈。

- **結論**：100% 成功無錯跑通！
- **相容原理**：
  1.  `verify_manuscript_maturity.py` (MCI) 在設計上原本就僅掃描與寫作密切相關的 8 大聯邦手稿檔案（從 `04_toc.md` 至 `11_reading_protocol.md`），本就不包含 `01`、`02`、`03`。故規格書移出，工具完全無痛相容。
  2.  `verify_poc_completeness.py` (MPM) 聚焦於手稿本體與資料庫的自指合龍，檔案路徑的升級適配已在上一輪重構中完美落地，本次移動無任何負面衝擊。
