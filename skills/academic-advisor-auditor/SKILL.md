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
