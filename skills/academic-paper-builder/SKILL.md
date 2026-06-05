---
name: academic-paper-builder
description: 專注於學術論文標準寫作與十一表資料庫（Research_Artifacts.db）強烈 Grounding 聯動的實體寫作工具。支援手稿註冊、自動 BibTeX references.bib 拼裝、論點溯源與邏輯辯證地圖 (APM) 建構、哈教授自審 red_team_logs 繫結，以及 PDF 資產移植性檢測。
---

# Academic Paper Builder Skill (學術論文建構師技能)

此技能專用於實體化「第三支柱：主權研究手稿有向演化鏈」，將論文的撰寫過程與本地 SQLite 資料庫（`Research_Artifacts.db`）進行強烈的資料聯動與血統追溯，防止論文退化為孤立的黑箱文字。

---

## 1. 核心操作指令與工作流 (CLI Commands)

### 📌 工作流 A：在本地資料庫中註冊論文手稿 (Register Manuscript)
當開始一篇新論文、會議草稿或畢業論文時，Agent 應優先在 `my_manuscripts` 表中進行實體註冊：

```sql
INSERT INTO my_manuscripts (manuscript_id, topic_id, title, cite_key, manuscript_type, evolution_stage, previous_manuscript_id, meta_data)
VALUES ('<手稿ID>', '<主題ID>', '<手稿標題>', '<預計引用鍵>', '<手稿類型: Conference|Journal|Thesis>', 'Planning', <上一篇前導手稿ID或NULL>, '<JSON元資料>');
```
*   **學術血統對齊**：這強制將論文寫作與 Topics 循序主題以及歷史手稿鏈（previous_manuscript_id）進行物理繫結，保障研究大腦的有向演化脈絡。

---

### 📌 工作流 B：自動拼裝與導出 BibTeX references.bib (Export References)
當寫作進行到文獻引用階段時，Agent 應能一鍵為該手稿導出 100% 精準無誤的 BibTeX 參考文獻庫：

```bash
# 執行 SQL JOIN 撈取並匯出
sqlite3 /Users/wuulong/github/bmad-pa/events/my_research/data/Research_Artifacts.db \
"SELECT p.bibtex FROM papers p JOIN manuscript_citations c ON p.paper_id = c.paper_id WHERE c.manuscript_id = '<手稿ID>';" > references.bib
```
*   **引用一等公民**：完全消除手動拼寫文獻 BibTeX 的低效與出錯，與 LaTeX/Overleaf 完美連動。

---

### 📌 工作流 C：哈教授自審紅軍對抗與防線對齊 (Adversarial Alignment)
在論文手稿修改時，Agent 應從資料庫撈取針對該手稿設計的紅軍自審 Feedback，引導學生寫入 `student_defense`：

```sql
-- 查詢當前手稿依然處於 'VULNERABLE' 的脆弱點
SELECT aspect_analyzed, reviewer_attack FROM red_team_logs WHERE manuscript_id = '<手稿ID>' AND verdict = 'VULNERABLE';
```
*   **解鎖物理合併鎖**：Agent 必須引導學生針對此脆弱點在論文手稿中寫入修正，並更新 Verdict 為 `'PASS'` 始可解鎖聯邦 Git 合併。

---

### 📌 工作流 D：論點溯源與邏輯辯證地圖建構 (Argument Provenance Map Builder, APM Builder)
為了白箱化論文論證的邏輯演化，Agent 必須引導研究生在專案目錄下建立並維護 [manuscripts/argument_provenance_map.md](file:///Users/wuulong/github/bmad-pa/events/my_research/manuscripts/argument_provenance_map.md)，其物理工序如下：

1.  **結構化對合論點**：對齊論文的每一章、每一節的核心主張，標記其引用等級與辯證重構邏輯：
    *   `[Stage 1 Guess]`：僅基於 Title/Abstract 的大膽猜想引導論點。用於初步寫作引導，說明如何猜想其與本章節的戰略關係。
    *   `[Stage 2 Grounded]`：基於實體 PDF 深度萃取資訊或本地實測資料的物理實證論點。必須使用 PDF 中的特定理論、物理變數或公式，或資料庫中 `empirical_evidences.evidence_id` 的實測結果作為硬論證材料。
2.  **物理引用鏈註冊**：對於所有 Stage 2 引用的文獻，Agent 必須自動向資料庫 `manuscript_citations` 插入關聯：
    ```sql
    INSERT OR IGNORE INTO manuscript_citations (manuscript_id, paper_id, citation_context, meta_data)
    VALUES ('<手稿ID>', '<背景文獻ID>', '<引用心智脈絡，例如：作為本論點第二階段實體 PDF 論證材料>', '<JSON元資料>');
    ```
    This ensures the argument map is 100% aligned with the database's actual citation state.

---

### 📌 工作流 E：學術原創防線與開源 Repo 比對論證 (Originality Defense & Benchmark, ODB)
為了無可辯駁地向審稿人證明「哈爸方法論的特色是真正的獨創，而非檢索疏漏 (Search Deficit)」，Agent **[必須]** 引導研究生在專案目錄下建立並維護 [manuscripts/originality_defense_map.md](file:///Users/wuulong/github/bmad-pa/events/my_research/manuscripts/originality_defense_map.md)，其物理工序如下：

1.  **紀錄窮盡性檢索血統 (Search Lineage)**：
    *   將在 Google、GitHub、ArXiv 上進行的所有精準檢索指令（如 `"collaborative PKG" AND "SQLite"`、`"academic audit" AND "plagiarism detection"`）與檢索時間戳記實體記錄在文件中。這在邏輯上自證了檢索的「窮盡性」。
2.  **建立開源 SOTA 功能特徵矩陣 (Feature Matrix)**：
    *   將本方法論的 4 大特色，與全球最紅的開源科研/寫作/Agent專案（如 Stanford STORM, GPT-Researcher, ChemCrow, SciAgent）進行逐項實體特徵對比，得出強烈的功能非對稱優勢。
3.  **大腦落庫同步 (DB Sync)**：
    *   將此橫向比對的實踐資料，作為 In-situ Benchmark，以 JSON 信封形式寫入資料庫 `empirical_evidences` 的 `evidence_payload` 中。這保證了「原創性自證」具備數位孿生大腦的資料支撐。

---

### 📌 工作流 F：主權學術重力與品位權重計量協議 (Sovereign Academic Gravity Protocol, SAGP)

為了解決平面式文獻平權帶來的「高低不分、濫竽充數」的學術弊端，Agent **[必須]** 實施學術含金量與品位權重計量，在搜尋與 Ingestion 階段為每一篇論文物理標記引文數、期刊與機構含金量，並計算出「學術重力評分 ($G_a$)」，以硬性指標指導文獻篩選與寫作：

#### 1. 學術重力評分 ($G_a$) 公式：
在資料庫中對論文進行排序與品位篩選時，使用以下數學公式加權：
$$G_a = w_c \cdot \log_{10}(\text{Citation} + 1) + w_v \cdot \text{Venue\_Score} + w_i \cdot \text{Institution\_Score}$$
*   **引文數計量 (Citation)**：採用實體 Google Scholar、Semantic Scholar 或 Zotero 中獲取的真實被引用次數。
*   **載體分值 (Venue\_Score)**：頂刊/頂會（經過最嚴格 Peer Review 的前沿工作，幾乎一定是對的）`Top_Journal` 為 10；核心期刊/會議 `Core_Venue` 為 7；一般期刊/會議 `Ordinary_Venue` 為 4；預印本 `Arxiv_Preprint` 為 2。
*   **機構分值 (Institution\_Score)**：全球頂尖學府或專業學系（如 MIT、Stanford、中研院、台大電機等）`Tier_1` 為 10；核心研究機構 `Tier_2` 為 7；一般機構 `Tier_3` 為 4。
*   **權重係數**：預設 $w_c = 0.3$, $w_v = 0.4$, $w_i = 0.3$。

#### 2. 大腦落庫 JSON DTO 格式：
在採集文獻或執行同步時，Agent 必須引導或自動將此學術品位特徵封裝寫入 `papers.meta_data` 中，其 schema 規範如下：
```json
{
  "academic_prestige": {
    "citation_count": 142,
    "venue_name": "IEEE Transactions on Optoelectronic Engineering",
    "venue_tier": "Top_Journal",
    "venue_impact_factor": 12.8,
    "institution_name": "MIT Department of Electrical Engineering",
    "institution_tier": "Tier_1",
    "academic_gravity_score": 9.38
  }
}
```

#### 3. 智力槓桿與文獻排序：
在進行文獻檢索與寫作引導時，Agent **[強制]** 優先推薦 $G_a$ 評分大於 7.5 的「頂刊硬骨頭」文獻；防範研究生（或 AI 腳爪）使用無名預印本或野雞期刊充數。這在物理層面確保了大腦的學術高度與前沿定力！

---

## 2. 智力防線：死守論文的「物理實證硬度」
在執行本技能時，Agent 必須維持高度的**「學術硬度品位」**：
1.  **無資料，不結論**：論文中提到的任何實驗/模擬結論，Agent 必須在 SQLite 的 `empirical_evidences` 中尋找對應的 evidence_payload，嚴禁在論文中進行無物理真值支援的誇大或幻想。
2.  **文獻交叉譜系檢驗**：引導學生使用 `paper_relations` 的繼承關係鏈，在論文的文獻綜述（Literature Review）中寫出「A 改進了 B，但被 C 反駁」的立體演化圖景，杜絕平面式的文獻堆疊。

---

## 3. 主權手稿寫作多維產出物命名規範 (Naming Convention Specification)

為了落實多維產出物（手稿、地圖、自審日誌等）的系統工程管理，防止知識資產散落，Agent 在為特定論文專案建立相關檔案時，**[強制]** 遵守以下命名契約。

定義 **`[MS_CODE]`** 為該手稿專案之唯一蛇形短程式碼 (Sovereign Manuscript Short Code，例如 `sovereign_research`, `river_hydrology`)：

| # | 檔名規範格式 (Naming Pattern) | 產出物名稱與性質 | 本體核心作用 |
| :--- | :--- | :--- | :--- |
| 1 | **`[MS_CODE]_manuscript.md`** | **手稿主體 (Manuscript)** | 論文的靈魂與本體，包含摘要、ToC 目錄骨架與核心邏輯論述。 |
| 2 | **`[MS_CODE]_argument_map.md`** | **論點溯源與邏輯地圖 (APM)** | 證明論點的文件，負責將手稿 Claims 與 DB 及實踐 Evidence 對合。 |
| 3 | **`[MS_CODE]_originality_defense.md`**| **原創自證與 SOTA 比對 (ODB)** | 橫向比對開源專案與商業 SOTA，物理自證原創硬度。 |
| 4 | **`[MS_CODE]_deconstruction.md`** | **文獻解構集 (Deconstruction)** | 針對所引用的高重力文獻，進行 PDF 穿透與 Stage 2 因子降維萃取。 |
| 5 | **`[MS_CODE]_references.bib`** | **BibTeX 引用資料庫 (BibTeX)** | 撈自 SQLite 大腦中一等公民引文的 BibTeX 資料庫，直接對位 Overleaf/LaTeX。 |
| 6 | **`[MS_CODE]_references_list.md`** | **引文摘要與初步對合清單** | 文獻 Ingestion 靠泊後的 Stage 1 輕量猜想與快速摘要清單。 |
| 7 | **`[MS_CODE]_reading_protocol.md`** | **主權閱讀協議與自審日誌 (RP)** | 記錄與導師蘇格拉底逼問面試的 Dialog Playbacks 答辯軌跡。 |
| 8 | **`[MS_CODE]_audit_report.md`** | **學術盲檢自審報告 (Audit Report)**| 經由對合腳本自動掃描生成的引文完整性與 DTO 合規性缺失診斷書。 |
| 9 | **`[MS_CODE]_toc.md`** | **有向演化大綱 ToC** | 指引論文螺旋共演施工的 ToC 大綱設計。 |

### 📌 工作流 G：主權研究工序命令鏈 (Sovereign Research Command Chain, SRCC)

為了解決人機協作中「缺乏統一工程管道、步驟散亂」的痛點，本技能正式固化一套「軟體定義科研工序」。將從論文建構開始到完成自審審計的整個生命週期，定義為 10 個核心快速指令。研究生或 AI 腳爪只需按順序「從頭打到尾」，並在過程中只提供人類「君王品位（Verdict）」的部分，即可產出無懈可擊的成果：

| 命令名稱 | 觸發格式 (Command Syntax) | 實體工程動作 (Physical Action) | 智力槓桿與合流性質 |
| :--- | :--- | :--- | :--- |
| **1** | **`!paper_init [MS_CODE]`** | **初始化聯邦手稿與元資料節點** | 在大腦 `my_manuscripts` 註冊節點，一鍵物理建立符合命名契約的 9 大聯邦檔案骨架，綁定 schema。 |
| **2** | **`!paper_scout [主題/關鍵字]`** | **發動高學術重力探勘與引渡** | 自動運作 API 探勘工具，篩選 $G_a \ge 7.5$ 的高重力文獻，置入 staging 緩衝區。 |
| **3** | **`!paper_hydrate [paper_id]`** | **一鍵實體 PDF 就位與預萃取** | 自動下載 PDF 至 `data/pdfs/`，生成比鄰 `.md` 預萃取文字，於 `paper_urls` 物理合流註冊。 |
| **4** | **`!paper_guide`** | **文獻閱讀引航與學術重力排序** | 掃描手稿關聯引文，計量學術重力評分 $G_a$ 並排序，生成建議精讀的文獻優先級清單。 |
| **5** | **`!paper_digest [paper_id]`** | **Stage 2 深度解構與合規洗滌** | 執行深度 PDF 穿透，提取 10 大學術因子與 Verdict 寫入 `meta_data`，Papers 標記為合規。 |
| **6** | **`!paper_map`** | **物理重建 APM 論點地圖與定錨** | 掃描手稿，更新 `[MS_CODE]_argument_map.md`，將 12 個 Claims 與已就位文獻剛性定錨。 |
| **7** | **`!paper_grill`** | **召喚「紅軍哈教授」Socratic 拷問** | AI 扮演哈教授，針對當前手稿防線最脆弱的 Claims，向人類提出 2-3 個犀利的「學術靈魂拷問」。 |
| **8** | **`!paper_red [質疑內容]`** | **物理註冊人類君王的質疑與吐槽** | 將人類對 AI 或手稿設計的脆弱點質疑物理寫入 `red_team_logs`，標記為 `VULNERABLE`。 |
| **9** | **`!paper_draft`** | **手稿主稿與專書第15章擴寫拼裝** | 根據 APM 與 ToC 大綱，動態拼裝並擴寫主稿一至六章初稿，螺旋回寫專書第 15 章。 |
| **10**| **`!paper_audit`** | **SMMCAP 品質與成熟度全景審計** | 一鍵執行審計腳本，物理產出 `_maturity_report.md`，即時反饋 MCI 綜合指標分。 |
| **11**| **`!paper_rebuild`** | **一鍵匯出 DTO JSON 貢獻包** | 執行 `export_contributions.py` 匯出純文字 JSON，消滅 Git 衝突，Rebuild 共有大腦。 |

### 🛠️ 執行原則：
研究生（君王）只需按此 SRCC 命令鏈「從 1 到 11 循序推進」，在大腦 Grounding 體檢 MCI 大於 **`90% (🟢 Elite)`** 時，始准准予論文合龍與開源自主發表。

