# 🧠 AI 時代的學術革命：主權科研大腦與自指自證實踐 (Sovereign Research Brain)

> **「當 AI 氾濫、學術語意泡沫化時，我們如何守護思考手感，物理證明『這篇論文是由這套系統物理長出來的』？」**

本專案是《個人 AI 賦能》專書第 15 章的開源實體示範 Repo。我們在此開源了「主權科研大腦（Sovereign Research Brain）」的完整方法論規格書、論文手稿、NotebookLM 整合封包以及自審/自證工具鏈。

本專案最核心的哲學在於**「自指自證（Self-Referential Proof）」**：這篇論文本身，就是利用本 Repo 中的十一表 SQLite 資料庫與主權工具鏈，經過多輪紅軍自審、答辯與「現地真值對合」後，物理生成並編譯出來的。

---

## 🧬 核心解決痛點 (The Epistemic Defense)

在傳統人機協作研究中，研究生與學者常面臨以下六大痛點：
1. **認知空洞化**：無腦複製貼上 AI 生成的文字，失去思維主權。
2. **幽靈引文警告**：LLM 幻想出來的非真實文獻污染 Overleaf/LaTeX。
3. **未讀先引（根系浮空）**：引用了自己根本沒讀懂、沒消化過的公海文獻。
4. **師徒信任危機**：指導教授無法在短時間內驗證學生大腦的「消化血統」與論文的真實度。
5. **Git 二進位衝突**：多名研究人員共同協作 SQLite 資料庫時，二進位檔案造成嚴重的 merge 衝突。
6. **環境移植障礙**：絕對路徑寫死，導致研究大腦換了電腦就無法 rebuild。

本系統透過 **「十一表 SQLite 資料庫 + 純文字 JSON 貢獻包 (DTO) + 剛性自審指標 (MCI, MPM)」**，徹底解鎖上述痛點。

---

## 📂 專案物理結構 (Directory Layout)

```
sovereign-research-methodology/
├── README.md                          # 本引導文件
├── schema.sql                         # 十一表 SQLite 資料庫結構定義
├── rebuild_lab_brain.py               # 一鍵重構大腦與 DTO 匯入腳本
├── methodology/                       # 主權科研方法論規格說明書 (01-04)
├── manuscripts/                       # 手稿主檔與 11 大自證評估報告 (01-11)
│   ├── sovereign_research_05_manuscript.md   # 論文萬字主手稿
│   ├── sovereign_research_06_argument_map.md # 論點地圖 (APM)
│   └── sovereign_research_11_audit_report.md # 紅軍自審與答辯日誌
├── nblm_notes/                        # NotebookLM 4 大綜合封包與 15 大互動 Prompt
├── scripts/                           # 大腦運轉、爬蟲、自審與驗證核心腳本庫
│   ├── brain_cli.py                   # 大腦互動 CLI 介面
│   ├── audit_brain_compliance.py      # 物理盲檢與合規審計
│   ├── verify_argument_provenance.py  # 論點地圖驗證
│   ├── verify_manuscript_maturity.py  # 手稿成熟度與可信度指數 (MCI) 驗證
│   └── verify_poc_completeness.py     # 現地真值 (POC) 完整度驗證
└── data/
    ├── Research_Artifacts.db          # 實體 SQLite 資料庫（含完整自證與答辯日誌）
    ├── downloaded_papers              # [相對軟連結] 指向外部實體 PDF 目錄
    ├── pdfs                           # [相對軟連結] 指向外部預萃取 Markdown 目錄
    └── contributions/
        └── contrib_all.json           # 純文字 DTO 聯邦貢獻包
```

---

## 🚀 快速開始：一鍵重構與自指自審

### 1. 克隆專案並建立大檔案連結
```bash
git clone --recurse-submodules https://github.com/wuulong/sovereign-research-methodology.git
cd sovereign-research-methodology
```
*(注意：`data/downloaded_papers` 與 `data/pdfs` 已預設為相對軟連結，指向您的外部實體文獻目錄，避免版權 PDF 進入 Git 庫。)*

### 2. 一鍵重構主權大腦 (SQLite Rebuild)
利用純文字的 DTO 貢獻包，一鍵在本地無損還原二進位資料庫：
```bash
python rebuild_lab_brain.py
```
此步驟將會物理建立 `data/Research_Artifacts.db`，並將所有文獻 Ingestion 血統、論點定錨與答辯 Verdict PASS 歷史全數寫入。

### 3. 執行「哈教授的 30 秒 SQL 照妖鏡」
進入 SQLite，直接用物理 SQL 語意穿透審查大腦的消化狀況：
```bash
sqlite3 data/Research_Artifacts.db
```
*   **檢核一：Ingestion 消化血統審查**
    ```sql
    SELECT cite_key, read_status, citation_gravity FROM literature_records WHERE read_status = 'STAGE_2_PASS';
    ```
*   **檢核二：Verdict Lock 自審漏洞與答辯軌跡**
    ```sql
    SELECT log_id, topic_id, test_verdict, test_finding FROM red_team_logs ORDER BY created_at DESC LIMIT 5;
    ```

### 4. 驗證自證成熟度指標 (MCI & MPM)
執行以下自動化腳本，即可在終端機輸出本論文手稿的成熟度指數：
```bash
# 驗證論點與文獻定錨硬度
python scripts/verify_argument_provenance.py

# 計算手稿成熟與可信度指數 (MCI)
python scripts/verify_manuscript_maturity.py
```

---

## 🧠 NotebookLM 探索與發想大師指南

為了方便您在 [NotebookLM](https://notebooklm.google/) 中剖析這套方法論，我們已在 `nblm_notes/` 底下打包了 4 大綜合封包：
1. **01_SOVEREIGN_METHODOLOGY.md**：系統手冊與需求規格骨架。
2. **02_SOVEREIGN_MANUSCRIPT_TOC_MAP.md**：論文主稿大綱與論點地圖。
3. **03_SOVEREIGN_RESEARCH_GROUNDING.md**：文獻解構集與閱讀協議。
4. **04_SOVEREIGN_QUALITY_AUDIT.md**：成熟度評估、自審報告與自證實踐。

### 💬 頂級主題發想 Prompt
在您的 NotebookLM 建立一個名為 **「Sovereign Research Brain」** 的筆記本，拖曳上傳這 4 個封包檔案，並嘗試輸入以下 Prompt 與大腦共振：
*   > **六大痛點與關聯式資料庫的救贖**
    > 「請分析上傳檔案中的六大傳統學術/人機協作痛點。底層 SQLite 資料庫的十一張表（特別是 `empirical_evidences`、`paper_relations` 與 `red_team_logs`）在架構設計上是如何精準對應並解鎖這些痛點的？請提供一份清晰的技術映射分析。」
*   > **根系浮空懲罰與 BFS 演算法邏輯**
    > 「在 `academic-research-navigator` 技能的運作邏輯中，『根系浮空懲罰』的判定規則是什麼？它是如何利用底層 `paper_relations` 的 `GROUNDED_ON` 有向邊與廣度優先搜尋（BFS）二層探針演算法，來對未消化的經典文獻進行剛性扣分，從而徹底消滅『未讀先引』的學術投機？」

*(更多 Prompt 請詳閱 [nblm_notes/README.md](nblm_notes/README.md))*

---

## 🏛️ 主權學者領主宣言 (The Sovereign Scholar Manifesto)

> **「原創源自於肉身對實體世界偏離誤差的校正，而非對 LLM 語意幻想的無腦妥協。」**

在 AI 工具極大降低寫作門檻的今天，這套方法論強制我們在**「理論的邊界、資料的結構、肉身的實踐」**中，重新奪回思維主權。我們誠摯邀請您一起實踐行解合一的學術探索！
