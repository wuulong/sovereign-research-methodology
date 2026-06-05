# NotebookLM Asset Pack - events/my_research/sovereign-research-methodology/skills
- **Source Folder**: `events/my_research/sovereign-research-methodology/skills`
- **Generated At**: 2026-06-06 07:15:31

---

================================================================================
📂 FILE PATH: skills/README.md
================================================================================

# 📁 四大主權核心 Skill 庫 (Sovereign Skills)

本目錄存放了驅動「主權科研大腦（Sovereign Research Brain）」的**「四大核心主權 Skill」**規格與設計說明。

這些 Skill 是整個方法論運行的控制本體，強制約制了 AI 的手腳，守護人類學術研究的原創性：

## 🧬 四大主權 Skill 列表

1. **[academic-research-navigator](academic-research-navigator/SKILL.md) (學術研究導航員)**
   * **目標**：解決公海文獻的快速探勘與消化瓶頸，徹底消除「未讀先引（根系浮空）」的學術投機。
   * **機制**：直連文獻庫進行 Ingestion 靠泊，以文獻引用邊建立拓撲圖，並執行 BFS 計算文獻學術重力 $G_a$，若缺乏 STAGE_2_DEEP 深入文獻則發動剛性扣分懲罰。

2. **[academic-paper-builder](academic-paper-builder/SKILL.md) (學術手稿建構師)**
   * **目標**：將論文寫作由單純的「文字盲目編排」提升為大腦資料庫節點的「物理定錨與拼裝」。
   * **機制**：在 `my_manuscripts` 表中註冊手稿實體，實施論點地圖 (APM) 引用硬度白箱化管理，並在編譯合龍時一鍵物理匯出無幽靈引文的合規 `references.bib`。

3. **[academic-advisor-auditor](academic-advisor-auditor/SKILL.md) (學術自審審計師)**
   * **目標**：防堵人機協作中人類思維被 AI 語意泡沫掏空、以及師徒間進度誠信崩塌的危機。
   * **機制**：建立紅軍自審脆弱點防線，導師/自審腦 Feedback 自動寫入 `red_team_logs`。若狀態為 `'VULNERABLE'` 則發動 **「合併阻斷鎖 (Verdict Lock)」** 阻斷代碼與資料合流，答辯通過改為 `'PASS'` 後始能解鎖。

4. **[sovereign-poc-verifier](sovereign-poc-verifier/SKILL.md) (主權 PoC 驗證器)**
   * **目標**：打破 AI 自評估的語意幻覺閉環，以本地工具鏈的執行狀況與資料庫物理一致性進行剛性自證。
   * **機制**：盲檢底層 SQLite 資料庫的參照完整性與「主題三位一體對合率」，計算 MPM (元自證成熟度) 指標並物理產出 SMPRR 驗證報告。


================================================================================
📂 FILE PATH: skills/academic-advisor-auditor/SKILL.md
================================================================================

---
name: academic-advisor-auditor
description: 專注於學術自審、論點溯源盲檢與品質治理的全域防線技能。透過實體 SQLite 十一表資料庫的資料對合完整性，執行「30 秒 SQL 照妖鏡盲檢」、評估論點引經據典硬度、自動輸出學術盲檢報告，並透過 Verdict Lock（合併鎖）與 Socratic 自審對抗阻斷 AI 語意掏空。
---

# Academic Advisor Auditor Skill (哈教授學術自審與品質盲檢審計技能)

此技能專用於實體化「第二支柱：本地實測與紅軍自審（肉身實踐）」，為導師與研究生提供了一套白箱盲檢論文論論據硬度、文獻消化深度以及物理實測完整性的「防掏空物理防線」。

---

## 1. 核心哲學與資料契約 (Auditing Philosophy)

AI 時代的學術革命，核心在於將論文產出解構為**「論文手稿」**與**「論點證明地圖 (Argument Provenance Map)」**雙軌文件。
任何出現在這兩份文件中的學術引用（`@cite_key`），在本地主權大腦（SQLite 資料庫）中皆必須具備 100% 完整的實體資料，且最終都必須經歷 **Stage 2 深度解構與合規洗滌 (is_compliant = True)**。這意味著：**所有用以證明核心主張的科學證據，大部分均已高精沉澱在資料庫 `papers.meta_data` 的十大學術因子 DTO 中**。本技能專用於自動掃描對合此剛性不變量 (Invariant)。

---

## 2. 核心操作指令與工作流 (CLI Commands)

### 📌 工作流 A：哈教授 30 秒 SQL 照妖鏡盲檢 (30-Sec SQL Blind Audit)
當學生回報進度時，導師（或 AI 導師分身）直接直呼 SQLite 盲檢指令，檢查資料庫的完整性與真實物理誤差：

```bash
# 1. 盲檢文獻 Ingestion 血統與合規打標率
sqlite3 /Users/wuulong/github/bmad-pa/events/my_research/data/Research_Artifacts.db \
"SELECT paper_id, cite_key, json_extract(meta_data, '$.compliance_status.is_compliant') FROM papers ORDER BY year DESC LIMIT 10;"

# 2. 盲檢本地實測誤差是否存在且符合現地真值 (friction_percentage)
sqlite3 /Users/wuulong/github/bmad-pa/events/my_research/data/Research_Artifacts.db \
"SELECT evidence_id, practice_scenario, friction_percentage FROM empirical_evidences;"

# 3. 盲檢自審答辯軌跡與 Verdict 裁決狀態
sqlite3 /Users/wuulong/github/bmad-pa/events/my_research/data/Research_Artifacts.db \
"SELECT aspect_analyzed, verdict, json_extract(meta_data, '$.verdict_details.approved_by') FROM red_team_logs;"
```

---

### 📌 工作流 B：一鍵論點溯源與學術硬度 blind-audit (Argument Grounding Audit)
當手稿修改完成，欲評估論據硬度並進行自審時，Agent **[必須]** 直接直呼盲檢工具 `verify_argument_provenance.py`：

```bash
python3 /Users/wuulong/github/bmad-pa/events/my_research/scripts/verify_argument_provenance.py
```

*   **自動化掃描**：工具會自動解析 `sovereign_research_paper.md` 與 `argument_provenance_map.md` 的核心主張與 cite_keys。
*   **剛性對合**：連線 SQLite 資料庫，比對其註冊狀態與 Stage 2 合規標記。
*   **產出報告**：自動在論文目錄下輸出 [manuscripts/argument_audit_report.md](file:///Users/wuulong/github/bmad-pa/events/my_research/manuscripts/argument_audit_report.md)，列出「Claims Grounding Matrix」對照矩陣，開出「缺失診斷書（Missing DTO Signature）」，作為解鎖 Git 合併的前置門檻。

---

### 📌 工作流 C：紅軍自審答辯與 Verdict Lock 解鎖控制 (Adversarial & Verdict Lock)
在進行程式碼與文字合併前，實施 Socratic 師徒對審：

1.  **註冊脆弱點 (VULNERABLE)**：導師發現公式或邊界缺陷，在 DB 中物理註冊為 `VULNERABLE`，阻斷合併。
2.  **寫入肉身實踐答辯 (student_defense)**：研究生進行本地模擬或現地觀測，將 `evidence_id` 與實測誤差物理綁定，並更新至 `red_team_logs`。
3.  **導師行使裁決 (Verdict PASS)**：導師確認實測誤差合理且答辯堅實，將 verdict 改為 `'PASS'`，正式解鎖物理合併鎖。

---

### 📌 工作流 D：全庫合規信封動態品質治理 (Compliance Audit)
定期執行品質體檢，掃描 core tables 的 meta_data JSON 完整性：

```bash
python3 /Users/wuulong/github/bmad-pa/events/my_research/scripts/audit_brain_compliance.py
```

---

### 📌 工作流 E：!paper_ 快速指令家族 (Quick Interactive Commands)
為了消除人機協作過程中的操作摩擦，並固化軟體定義科研工序 (SRCC)，當使用者在對話中輸入以 `!paper_` 為前綴的快速指令時，Agent 必須優先、即時響應並物理執行對應的學術動作：

1. **`!paper_grill`**：
   - **觸發意圖**：主動發動「紅軍哈教授」的學術拷問質疑機制！
   - **實體動作**：Agent 會扮演嚴厲、犀利的哈教授，針對當前手稿中 MCI 體檢或論點地圖中防線最脆弱的 Claims，提出 2-3 個極具學術品位的「靈魂逼問」，逼迫研究生進行肉身物理實踐答辯，等待 Verdict 裁決。
2. **`!paper_red [質疑與吐槽內容]`**：
   - **觸發意圖**：將人類「君王」對 AI、對文獻、或對當前手稿設計的**真實質疑與脆弱點指摘**，直接物理寫入大腦資料庫 `red_team_logs` 的紅軍自審日誌中！
   - **實體動作**：Agent 物理提取對話脈絡，以 `log_` 為前綴在 `red_team_logs` 中物理註冊一筆 `verdict = 'VULNERABLE'` 的質審日誌。
   - **剛性規範限制**：
     * **語言契約**：`aspect_analyzed` 欄位（分析/自審脆弱點）**必須強制使用繁體中文（台灣語境，禁止使用中國用語）**撰寫，以利君王在本地以 CLI 查閱時的心智直覺對齊。
     * **意圖對合引導**：當人類進行吐槽或輸入質疑時，其目標對象可能是：(i) 正在寫的論文手稿/方法論本身（如 `paper_haba_sovereign_2026`）；(ii) 正在精讀的某篇特定引用文獻（如 `arxiv_AgenticScience_2025_14111`）；(iii) 整個工具鏈/工程底層設計。**若存在綁定意圖的模糊性，Agent [必須] 主動向君王提供選項進行確認**，切忌粗暴、無腦地綁定到無關的引用文獻上。
     * **主動捕捉與提示註冊**：在日常對話中，若君王對 AI 的生成、論點設計或工序提出了犀利的吐槽、修正與質疑，**Agent 必須具備學術敏感度，主動將其捕捉**，並禮貌詢問君王是否需要物理註冊為 `red_team_logs` 中一筆 `VULNERABLE` 的紅軍日誌，消除 AI 與人腦在對審過程中的記憶磨損，全面厚化紅軍紀錄。
3. **`!paper_audit`**：
   - **觸發意圖**：一鍵呼叫 `verify_manuscript_maturity.py`，重新對當前手稿進行全景成熟度與可信度對合體檢。
   - **實體動作**：自動產出並覆寫 `[MS_CODE]_maturity_report.md`，即時在對話中為您展示最新的 MCI 綜合指數與哈教授下一步改善指南。
4. **`!paper_guide`**：
   - **觸發意圖**：文獻閱讀引航與學術重力排序！
   - **實體動作**：Agent 會自動解析當前手稿關聯的 citations，連線 SQLite 大腦計量其學術重力評分 $G_a$（引文數、期刊與機構分），依權重排序，並結合當前 Stage 2 狀態，即時為您生成「建議當前最該開始研讀的 3 篇核心文獻清單與戰術定位指南」，徹底解決文獻消化順序混亂 of 痛點。

---


## 3. 手稿全景成熟度與可信度自審審計協定 (SMMCAP v1.0)

為了更全面地度量手稿的學術可信度，我們引進了 **Sovereign Manuscript Maturity & Credibility Audit Protocol (SMMCAP v1.0)**，將「八大聯邦手稿資產」與「SQLite 大腦地基」融會形成單一且客觀的 **Maturity & Credibility Index (MCI，成熟與可信度指數)**。

### 📌 聯邦手稿齊全度契約 (Federated Assets completeness)
手稿專案必須具備以下「八大聯邦手稿資產」作為行解合一的黃金地墊：
1. **主稿 (Manuscript)** : `[MS_CODE]_manuscript.md` (主論述與結論)
2. **大綱 (ToC)** : `[MS_CODE]_toc.md` (寫作意圖與兩層骨架)
3. **論點地圖 (Argument Map)** : `[MS_CODE]_argument_map.md` (主張與文獻對合 APM)
4. **原創防禦地圖 (Originality Defense)** : `[MS_CODE]_originality_defense.md` (與 SOTA 對比之 Novelty)
5. **文獻解構集 (Deconstruction)** : `[MS_CODE]_deconstruction.md` (Stage 1/2 閱讀猜想)
6. **引文文獻清單 (References List)** : `[MS_CODE]_references_list.md` (引用來源及初步評估)
7. **閱讀協議 (Reading Protocol)** : `[MS_CODE]_reading_protocol.md` (通讀與自審答辯機制)
8. **標準 References.bib** : `[MS_CODE]_references.bib` (SQLite 撈出的 BibTeX 全集)

### 📊 MCI 評分指標與剛性加權算法
MCI 滿分為 100%，由兩大板塊剛性加權組成：
$$\text{MCI} = (\text{聯邦文件齊全度與進度分} \times 0.5) + (\text{大腦資料庫 Grounding 綜合分} \times 0.5)$$

1.  **聯邦文件成熟度分 (50%)**：
    - 掃描上述 8 大檔案是否存在。檔案不存在計 `0%`；檔案存在但含有 `TODO`/`Draft` 或未完工者，根據內容長度與 TODO 數量給予 `20% ~ 95%` 不等的進度評估。100% 必須完全無 TODO 且通過格式審查。
2.  **大腦 Grounding 綜合分 (50%)**：
    - **已註冊 cite_key 存在率 (20%)**：手稿與 Claim Map 中出現的 `@cite_key` 是否皆在 SQLite 中註冊。
    - **Stage 2 消化率 (30%)**：已就位並完成 `STAGE_2_DEEP` 深度解構與合規洗滌的文獻比例。
    - **重要文獻遞迴閱讀率 (20%)**：在 `paper_relations` 的 `GROUNDED_ON` 有向拓撲關係中，核心文獻的下層 (2 層深度內) 被引文獻在 DB 中已被 digest/Ingestion 的比例。
    - **紅軍自審 PASS 率 (20%)**：`red_team_logs` 的對抗紀錄數，且 verdict 為 `'PASS'` 的解鎖比例。
    - **Claims Grounding 完整率 (10%)**：Argument Map 中，所有核心主張都有對應的 proved 引用文獻支援（無 "無引用" 漏洞）。

---

## 4. 智力防線：如何防止學生「認知掏空」？
在執行本技能時，Agent 必須維持高度的**「指導者品位（Taste Guidance）」**：
1.  **不給答案，只提質問**：當學生答辯脆弱點時，Agent 僅指出「邏輯漂移」或「物理守恆違反」，要求學生自己修改 Manning 阻力係數或電路阻抗參數。
2.  **無實踐資料，拒絕 Verdict PASS**：任何僅有「空洞黑話」的語意答辯一律駁回；唯有包含「實測誤差百分比 (friction_percentage)」且低於閾值（如 5% 或 15%）的肉身實體證據，始能解鎖 Verdict Lock。
3.  **依據 MCI 引導寫作**：在寫作初期，MCI 分數較低時，主要評價指出遺漏；隨著寫作深入，動態計算 MCI，指引學生捕獲高重力 Pending 論文、補充實測舉證與發動紅軍對抗，直至可信度達到 90% 以上始得准予編譯！
4.  **記錄考古筆記**：對抗答辯與 Verdict 過程，使用 `aiqa-scribe` 存入週報，做為誠信審查憑證。


================================================================================
📂 FILE PATH: skills/academic-paper-builder/SKILL.md
================================================================================

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



================================================================================
📂 FILE PATH: skills/academic-research-navigator/SKILL.md
================================================================================

---
name: academic-research-navigator
description: 專注於新一代學術研究「硬核兵器庫」，支援線上文獻檢索、SQLite 結構化資料落庫、LaTeX 公式處理與紅軍自審評估。
---

# Academic Research Navigator Skill (學術研究導航員技能)

此技能專用於實體化「第一支柱：硬核研究兵器庫 (The Physical Stack)」，提供 Agentic AI 一套標準化、無摩擦的文獻自動化探勘、高擴展性結構化落庫與紅軍對抗自審指南。

---

## 1. 核心工具鏈與資源分佈 (Resource Stack)

*   **資料庫路徑**：`/Users/wuulong/github/bmad-pa/data/research/Research_Artifacts.db`
*   **文獻探勘腳本**：`/Users/wuulong/github/bmad-pa/scripts/research/paper_scout.py`
*   **論文結構化萃取腳本**：`/Users/wuulong/github/bmad-pa/scripts/research/parse_paper_to_db.py`
*   **資料庫初始化腳本**：`/Users/wuulong/github/bmad-pa/scripts/research/setup_research_db.py`
*   **直連直呼規格書**：`/Users/wuulong/github/bmad-pa/scripts/research/paper_scout_cli_spec.md`

---

## 2. 核心操作指令與工作流 (CLI Commands)

### 📌 工作流 A：文獻探索與自動落庫 (Paper Scout & Ingestion)
當使用者要求搜尋特定物理主題或元件參數時，Agent **不應盲目猜測**，應直接透過命令行直呼 `paper_scout.py`：

```bash
python3 /Users/wuulong/github/bmad-pa/scripts/research/paper_scout.py --query "<關鍵字>" --limit <數量> --save-db
```

*   **沙盒降級處理**：若執行時遭遇網路連線阻礙（Timeout 或 429），腳本會自動退避至【離線模擬模式 (Offline Mock Mode)】生成高度自洽的 AR-WET 測試資料並完成落庫，Agent 應直接以此資料進行後續推理與 Grounding。
*   **成果彙報**：在對話中直接為使用者渲染出高品質的 Markdown 對照表，並提醒文獻已寫入 `Research_Artifacts.db`。

### 📌 工作流 B：非結構化 LaTeX 論文之紅軍自審與 Stage 2 深度解構 (Adversarial & Stage 2 Deep)
當使用者提供 Marker CLI 轉出之 Markdown 論文，或指定特定文獻進行深度學術因子解構時，Agent 應遵循「認知先導、兩階段對齊」原則：

1. **第一階段：文獻先導閱讀卡 (Staging Card)**
   - 在正式執行 Stage 2 深度因子析取前，必須先從資料庫與 Markdown 檔案中提取基本資訊（標題 title、作者 authors、年份 year、發表期刊 venue_name、基本摘要 abstract），並在對話中為使用者渲染出精美的「主權文獻先導閱讀卡」。
   - 摘要應優先取自資料庫 `papers.meta_data.abstract`。若為空，則自動透過 `extract_abstract_from_md` 從比鄰 Markdown 預萃取並暫存。
   
2. **第二階段：因子深度洗滌與落庫**
   - 獲得使用者確認後，再執行深度 Stage 2 學術因子分析，並執行以下命令或寫入腳本進行高精合規落庫：
     ```bash
     python3 /Users/wuulong/github/bmad-pa/events/my_research/scripts/audit_brain_compliance.py
     ```

*   **萃取維度**：
    1.  `core_method`：一句話的核心高維語義摘要。
    2.  `key_parameters` (JSON)：動態物理/電路特性參數。
    3.  `critique_score` (JSON)：紅軍對抗漏洞與評分（Reviewer 2 視角）。
    4.  `meta_data` (JSON)：數位基因封套（含 timestamp、abstract 與 10 大學術因子）。

### 📌 工作流 C：學術真值庫唯讀分析 (Grounding & Analytics)
Agent 可以使用 SQL SELECT 指令直接對本地已落庫的文獻進行橫向比對，為使用者解答「哪一種方法能獲得最佳物理特性」：

```bash
sqlite3 /Users/wuulong/github/bmad-pa/data/research/Research_Artifacts.db "<唯讀 SELECT 語句>"
```

*   **安全限制**：**嚴禁**執行 `UPDATE`、`DELETE`、`DROP` 等寫入指令，僅允許執行 `SELECT` 唯讀查詢。
*   **JSON 函數查詢範例**：
    ```sql
    -- 橫向比對品質因子大於 10000 的論文標題與漏洞
    SELECT title, json_extract(critique_score, '$.vulnerabilities') FROM papers WHERE json_extract(key_parameters, '$.Q') > 10000;
    ```

### 📌 工作流 D：雙軌標籤與階層拓撲樹狀渲染 (Taxonomy & Hierarchy Tree) [NEW]
當進行文獻 Ingestion 或 citations 實體化傳播時，Agent 應主導對合雙軌標籤機制，將平面關鍵字與帶有 `/` 的多重階層路徑寫入 `paper_tags` 表：

1. **自動打標與前綴防禦**：
   - 呼叫 `hydrate_paper_assets.py` 或 `extract_citations_to_records.py` 時，系統會自動匹配關鍵字，打上如 `AI應用/個人賦能/主權治理` 之階層標籤。
   - 系統會自動比對永恆骨架表 `taxonomy_framework`，前置前綴未註冊者將強制退避修正，防禦語意漂移。
   
2. **一鍵子領域樹狀渲染**：
   - 使用者或 Agent 可直接直呼渲染器，生成高彩度子領域樹狀拓撲，以掌握全局：
     ```bash
     python3 /Users/wuulong/github/bmad-pa/events/my_research/scripts/render_taxonomy_tree.py
     ```

---

## 3. 智力防線：如何防止學生「認知掏空」？
在執行本技能時，Agent 必須維持高度的**「指導者品位（Taste Guidance）」**：
1.  **不直接給出最終答案**：當學生詢問「這段推導怎麼寫」時，應引導學生查詢資料庫中的 `critique_score`，讓學生自己評估替代方案的缺點。
2.  **促成「品位裁決」面試準備**：每次落庫後，Agent 應主動向學生提問：「這篇論文的 key_parameters 在高功率下有 Duffing 分歧缺陷，如果我是指導教授，本週開會我會挑剔你這一點，你打算怎麼修正你的實驗設計？」
3.  **留下考古紀錄**：協助學生將高難度來回推導的對話，使用 `aiqa-scribe` 技能存入 notes/ai-qa/ 週報中，作為教授「關卡一（考古日誌）」的審查憑證。



================================================================================
📂 FILE PATH: skills/sovereign-poc-verifier/SKILL.md
================================================================================

---
name: sovereign-poc-verifier
description: 專注於方法論本體 100% 「自指自證（Self-Referential Proof）」的實體物理檢驗與釋出治理技能。負責盲檢底層 SQLite 資料庫有效性、量化工具鏈無摩擦摩擦率、審計手稿第 15 章自指對合度，並一鍵物理產出 SMPRR 自證報告與 MPM 元指標。
---

# Sovereign PoC Verifier Skill (主權自證驗證器技能)

此技能專用於實體化**「第四支柱：方法論元自證與物理自指完整鏈結」**。  
它超越了單純的手稿寫作與引文消化，專門用以量化與物理證明「這套方法論不僅是邏輯自洽的理論，更是一套在君王本機電腦上 100% 跑通、無摩擦運行，且能將其大腦 SQLite 實體資料物理匯出回寫手稿，達成行解合一的終極自證科學典範」。

---

## 1. 核心自證三大工序與物理指標 (Sovereign Verification Triad)

本技能剛性檢驗並量化以下三大部分，以徹底防範 AI 語意掏空與學術泡沫：

### 🛠️ 工序一：底層 SQLite 物理有效性檢驗 (DB Integrity Assertions)
*   **物理動作**：直接連線大腦資料庫 `Research_Artifacts.db`，發起系列 SQL 斷言檢測。
*   **檢核指標**：
    *   **外鍵與約束合規率**： papers、red_team_logs、empirical_evidences 等表之外鍵完整性與 `manuscript_id` 大一統對齊率。
    *   **資料分布無空洞率**： papers.meta_data 欄位 JSON 信封之合規解析率。
    *   **三位一體對合率 (Methodology Grounding Rate)**： 主題 Topics 中同時擁有「文獻沉澱」＋「本地實體 Evidence 舉證」＋「手稿 Manuscript 產出」的實質率。

### 🛠️ 工序二：工具鏈無摩擦高可用性計量 (Toolchain Usability & Friction)
*   **物理動作**：量化分析整個 SRCC 命令鏈與支援腳本的可用性與執行摩擦力。
*   **檢核指標**：
    *   **SRCC 命令可用率**： `brain_cli.py`、`hydrate_paper_assets.py` 等關鍵腳本是否確實存在、可無錯編譯執行。
    *   **雙防線 API 避退強韌度**： 當遭遇 429 限流時，比鄰 Markdown References 正則析取與學術重力 heuristic 專家估算補償機制的備載就位率。

### 🛠️ 工序三：手稿第 15 章自指自證完整鏈結度 (Self-Referential Proof Closed-Loop)
*   **物理動作**：檢驗「紙質手稿本體」是否與「大腦 SQLite 資料」完成了物理上的自我指涉（Self-Referentiality）雙向螺旋合龍。
*   **檢核指標**：
    *   **大腦 DTO 物理匯出率**： 檢查手稿第 15 章或 `sovereign_research_argument_map.md` 中，是否確實物理匯入並包含了 `Research_Artifacts.db` 的純文字 DTO JSON 資料。這向評審團證明「這篇論文的骨架與資料正是用這套系統 100% 物理長出來的」，達成終極自指。

---

## 2. 核心操作指令與工作流 (CLI Commands)

### 📌 元自證一鍵物理審計指令
當君王下達 `!paper_poc_verify` 指令時，Agent 必須呼叫專屬腳本 `verify_poc_completeness.py`：

```bash
python3 /Users/wuulong/github/bmad-pa/events/my_research/scripts/verify_poc_completeness.py [MS_CODE]
```

*   **物理產出**：自動覆寫產出最新的 **`[MS_CODE]_poc_proof_report.md`（主權方法論 PoC 自證與釋出成熟度報告，Sovereign Methodology PoC & Release Report, SMPRR）**。
*   **量化元指標**：產出 **`MPM` (Meta-Proof Maturity, 元自證成熟度指數)**，目標值須大於 **`90.00% (🟢 Elite Proof)`** 始准予論文最終合龍與開源釋出。

---

## 3. 智力防線與自證品位 (Taste & Proof Integrity)

在執行本技能時，Agent 必須死守「行解合一」的最高指導品位：
1.  **資料即證據**：MPM 指數的計算必須建立在對 SQLite 的實體 SELECT count 上，嚴禁任何無實體資料庫支援的「假性自證」與黑箱黑話。
2.  **理論不懸空**：若檢測到手稿核心主張中存在「無文獻引用（0 引用）」的理論懸置點，MPM 必須執行剛性下修懲罰，物理逼迫君王或 AI 補充引渡文獻定錨。
3.  **無縫合龍**：引導君王定期執行 DTO 匯出，將大腦的物理指紋螺旋回寫至手稿中，以達成學術釋出的完美工程完整鏈結。

