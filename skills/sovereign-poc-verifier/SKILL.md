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
