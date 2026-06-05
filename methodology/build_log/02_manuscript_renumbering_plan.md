# 📐 手稿 Manuscripts 寫作工序重新排序（從 01 起算）重構決策日誌 (02_manuscript_renumbering_plan)

> [!NOTE]
> **本建構日誌物理定錨於 2026-05-30 的進度會談。**  
> 記錄了主權大腦方法論發展史上第二次重大的「工序解耦與心流純化」重構。旨在透過將手稿寫作檔案統一從 `01` 開始編起，徹底解耦具體論文與方法論規格的數字依賴，實現極致自洽的手稿生命週期。

---

## 📊 1. 重構背景與決策經緯

在我們完成「方法論本體（Methodology）」與「具體手稿（Manuscripts）」物理分離後，`manuscripts/sovereign_research/` 底下的 11 個寫作與審計檔案依舊從 `04_toc.md` 開始編起。

這帶來了新的認知與工序懸置：
- 對於一個寫作具體論文（Instance）的人，他的子目錄下沒有 `01`、`02`、`03`（因為已經搬移到 `methodology/`），直接以 `04` 開頭，顯得結構不自洽，心智摩擦極大。
- 為了讓每一篇論文的寫作心流，都是一個獨立、自洽、完美的生命週期（從 `01_toc.md` 順暢推進至 `10_poc_proof_report.md` 看板），君王 (wuulong) 物理拍板了「**將手稿寫作工序重新排序為從 01 起算**」的最高決策！

---

## 🏗️ 2. 物理重命名與工序重新排序

重命名使用 `git mv` 保留完整歷史紀錄，手稿 11 個檔案與工序重新對位：

### 🪵 階段二：手稿骨架與文獻探勘 Staging (01 - 02)
*   **`sovereign_research_01_toc.md`** (原 `04_toc.md`) ➔ 有向大綱 ToC。
*   **`sovereign_research_02_references_list.md`** (原 `05_references_list.md`) ➔ 引文文獻清單。

### 🪵 階段三：穿透解構與實體主稿寫作 (03 - 05)
*   **`sovereign_research_03_deconstruction.md`** (原 `06_deconstruction.md`) ➔ 文獻深度解構集。
*   **`sovereign_research_04_references.bib`** (原 `07_references.bib`) ➔ 引文 BibTeX 標準庫。
*   **`sovereign_research_05_manuscript.md`** (原 `08_manuscript.md`) ➔ 論文手稿主體。

### 🪵 階段四：論點對合、原創防禦與自審答辯 (06 - 08)
*   **`sovereign_research_06_argument_map.md`** (原 `09_argument_map.md`) ➔ 論點地圖 APM。
*   **`sovereign_research_07_originality_defense.md`** (原 `10_originality_defense.md`) ➔ 原創防禦地圖 ODB。
*   **`sovereign_research_08_reading_protocol.md`** (原 `11_reading_protocol.md`) ➔ 閱讀協議與對抗答辯 RP。

### 🪵 階段五：品質審計與元自證釋出 (09 - 11)
*   **`sovereign_research_09_maturity_report.md`** (原 `12_maturity_report.md`) ➔ MCI Mature 看板審計報告。
*   **`sovereign_research_10_poc_proof_report.md`** (原 `13_poc_proof_report.md`) ➔ MPM Proof 看板自證報告。
*   **`sovereign_research_11_audit_report.md`** (原 `14_audit_report.md`) ➔ 自審盲檢報告歷史存檔。

---

## 🧪 3. 工具鏈對位升級與驗收

我們同時升級了自動化工具鏈的檔名對應，並跑通審計測試：
1.  **`verify_manuscript_maturity.py`** ➔ 將 `federated_files` 舊的 `04-11` 編號更新為全新 `01-08` 映射，成功覆寫產出最新的 `09_maturity_report.md`。
2.  **`verify_poc_completeness.py`** ➔ 讀取的 `argument_map` 改為 `06`，`manuscript` 改為 `05`，報告成功覆寫產出最新 `10_poc_proof_report.md`。
3.  **MCI與MPM雙看板審計完美通過**，這物理證明了寫作工序從 `01` 開始編起是 100% 正確且極具系統完備性的！
