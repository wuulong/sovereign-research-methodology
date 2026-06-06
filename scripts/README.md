# 🛠️ 大腦核心腳本庫說明書 (Scripts & Toolchain Guide)

本目錄存放了驅動「主權科研大腦」十一表 SQLite 資料庫運轉、文獻探勘、紅軍自審、MCI 與 MPM 指標計量的核心工具鏈。本手冊旨在引導人類研究者自行手動執行這些腳本，將理論完美落實為日常寫作與驗證心流。

---

## 🧬 設計哲學：環境自治與物理自證

1. **環境自治 (Self-Containment)**：所有腳本均已進行路徑自治化重構，全面以 Repo 根目錄相對計算。研究者將本 Repo clone 至本機後，即可直接執行，解決「換電腦即崩潰」的移植痛點。
2. **物理約束替代語意幻覺**：不使用 AI 虛無地「自己評估自己」，而是透過剛性盲檢 SQLite 外鍵、腳本可用率、以及手稿 Checksum 自指，以**非語意的「物理摩擦與代數約束」**死守學術硬度。

---

## 💻 1. 前置環境與依賴準備 (Environment Setup)

在手動執行腳本前，請確保您的本機環境已安裝以下 Python 相依套件：

```bash
# 安裝學術文獻解析與 BibTeX 完璧裝配之必要套件
pip install bibtexparser requests pyyaml
```

*   **Zotero 連線準備**：若需同步 Zotero 本地資料，請確保本機已安裝 Zotero，並在資料庫的 `directory_roots` 中設定了您的 Zotero 實體儲存路徑。
*   **資料庫初始化**：若本地無資料庫，請先執行根目錄下的一鍵重建：
    ```bash
    python rebuild_lab_brain.py
    ```

---

## 📂 2. 核心腳本與執行參數矩陣 (Tool Matrix)

為防止執行失敗，研究者必須注意部分腳本在手動執行時需傳入**「手稿代碼（MS_CODE）」**或**「文獻 ID（paper_id）」**：

| 腳本路徑與名稱 | 實體執行指令與參數範例 | 執行目的與 DB 讀寫表 |
| :--- | :--- | :--- |
| `rebuild_lab_brain.py`<br>(置於 Repo 根目錄) | `python rebuild_lab_brain.py` | **一鍵冷啟動大腦**：讀取 `contribution.json` DTO，秒級重建全庫十一張表。 |
| `scripts/brain_cli.py` | `python scripts/brain_cli.py` | **啟動互動式大腦 CLI**：提供人類互動終端，免去手動輸入 SQL 之苦。 |
| `scripts/verify_manuscript_maturity.py`| `python scripts/verify_manuscript_maturity.py [MS_CODE]` <br> *範例：`python scripts/verify_manuscript_maturity.py sovereign_research`* | **計算手稿 MCI 指標**：掃描特定手稿 Claims 與紅軍日誌，計算覆蓋率與自審 PASS 率，產出成熟度看板。 |
| `scripts/verify_poc_completeness.py` | `python scripts/verify_poc_completeness.py [MS_CODE]` <br> *範例：`python scripts/verify_poc_completeness.py sovereign_research`* | **計算手稿 MPM 指標**：盲檢 SQLite 外鍵與腳本可用率，產出 PoC 自證與釋出成熟度報告 `[MS_CODE]_poc_proof_report.md`。 |
| `scripts/setup_research_db.py` | `python scripts/setup_research_db.py` | **初始化專案骨架**：寫入永恆專案與循序主題，防範 rebuild 時級聯清空。 |
| `scripts/sync_zotero_to_staging.py` | `python scripts/sync_zotero_to_staging.py` | **同步 Zotero 本地文獻**：直連本地 Zotero SQLite，同步 PDF 至 staging 區。 |
| `scripts/paper_scout.py` | `python scripts/paper_scout.py --query "[關鍵字]"` <br> *範例：`python scripts/paper_scout.py --query "Duffing bifurcation"`* | **公海文獻探採**：使用 Semantic Scholar API 搜尋文獻，並灌溉重力 Ga 分數。 |
| `scripts/literature_deconstruct_and_save.py`| `python scripts/literature_deconstruct_and_save.py [paper_id]` <br> *範例：`python scripts/literature_deconstruct_and_save.py Wang2026ARWET`* | **手動 Stage 2 消化**：將 Zotero 載入的單篇文獻進行 10 大因子解構，狀態升級為 `STAGE_2_DEEP`。 |
| `scripts/anchor_manuscript_citations.py` | `python scripts/anchor_manuscript_citations.py [MS_CODE]` <br> *範例：`python scripts/anchor_manuscript_citations.py sovereign_research`* | **引文完璧裝配**：對合手稿引文，自動生成 100% 無損之 `[MS_CODE]_references.bib`。 |
| `scripts/extract_evolution_history.py` | `python scripts/extract_evolution_history.py` | **提煉自證演化史**：讀取紅軍答辯日誌與 Git submodule log，自動提煉並回寫手稿。 |

---

## 🔄 3. 人類研究者日常工作流 SOP (Human-in-the-loop Workflow)

當您獨自開工寫論文時，請遵循以下 5 大階段的工作流手動執行腳本，這能確保您的研究大腦與論文進度永遠對合：

### 🎯 階段一：專案宣告與大腦冷啟動
1. 在 SQLite 資料庫中配置您的專案關鍵字契約：
   ```bash
   python rebuild_lab_brain.py
   ```
2. 啟動大腦 CLI 確認專案骨架與當前 sequence_order 主題：
   ```bash
   python scripts/brain_cli.py
   # 進入後輸入: topics
   ```

### 🔍 階段二：文獻引渡、重力篩選與主題靠泊
1. **同步 Zotero 本地 PDF 暫存**：
   ```bash
   python scripts/sync_zotero_to_staging.py
   ```
2. **在公海探採特定領域的高引用文獻**：
   ```bash
   python scripts/paper_scout.py --query "acoustic wireless power"
   ```
3. **執行學術重力 Ga 計算，排序 Pending 精讀清單**：
   ```bash
   python scripts/hydrate_citations_and_gravity.py
   ```

### 📖 階段三：Stage 2 穿透精讀與降維消化 (最核心)
1. **啟動互動式大腦 CLI**，選擇特定文獻進行降維解構：
   ```bash
   python scripts/brain_cli.py
   # 執行指令: python scripts/literature_deconstruct_and_save.py [paper_id]
   ```
   *（系統會引導您提取 10 大核心因子與寫入您的學者批判 Taste Verdict，隨後將該文獻狀態升級為 `STAGE_2_DEEP`）*

### 🛡️ 階段四：手稿寫作、紅軍對抗與答辯防禦 (MCI 防線)
1. 當您在手稿中寫入 Claims 並引用文獻後，**執行 MCI 品質評估**：
   ```bash
   python scripts/verify_manuscript_maturity.py sovereign_research
   ```
2. **啟動紅軍 Socratic 格網拷問**，主動抓取手稿漏洞並寫入日誌：
   ```bash
   # 紅軍會模擬口試委員提問，並將您的 Claim Verdict 標記為 VULNERABLE，此時 Verdict Lock 啟用，阻斷編譯
   python scripts/verify_manuscript_maturity.py sovereign_research --grill
   ```
3. **肉身現地修復手稿，並手動提交答辯**：
   ```bash
   # 針對被質疑的紅軍日誌 ID 填寫答辯內容與實踐證據 (evidence_id)
   python scripts/verify_manuscript_maturity.py sovereign_research --defense [LOG_ID] "[您的物理答辯內容]"
   ```
4. **解鎖 Verdict Lock**：當指導教授或系統判定答辯通過，執行：
   ```bash
   python scripts/verify_manuscript_maturity.py sovereign_research --pass [LOG_ID]
   # 阻斷鎖解除，重推電閘
   ```

### ⚡ 階段五：完璧裝配、指紋自指與 Rebuild 導出 (MPM 防線)
1. **手稿一鍵合龍與白箱 BibTeX 完美組裝**：
   ```bash
   python scripts/anchor_manuscript_citations.py sovereign_research
   # 這會在手稿目錄生成 100% 合致、無幽靈引文的 references.bib 檔案
   ```
2. **計算 MPM 自證度，生成 PoC 自證與成熟度報告**：
   ```bash
   python scripts/verify_poc_completeness.py sovereign_research
   ```
3. **大腦物理指紋 (Checksum) 回寫**：
   ```bash
   # Verifier 會重新 rebuild 並將 contribution.json Checksum 雜湊值自動填入您手稿的最後章節，完成理論與資料庫的物理自指合龍
   python scripts/verify_poc_completeness.py sovereign_research --checksum
   ```
4. **導出純文字 DTO 貢獻包以提交 Git**：
   ```bash
   python scripts/export_contributions.py
   # 生成 contribution.json，此時即可將 contribution.json 與手稿安全 commit 提交 Git，絕無二進位衝突！
   ```

---

## ⌨️ 3. 大腦 CLI 工具快速指南 (brain_cli.py CLI Quickstart)

為了讓您在沒有 Agent 協助的情況下也能流暢查詢資料庫，可直接呼叫大腦 CLI 工具。這是一隻基於 `argparse` 的命令列參數查詢腳本（非互動式控制台，詳細參數指南請參閱 [scripts/brain_cli_manual.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/scripts/brain_cli_manual.md)）：

```bash
# 啟動大腦 CLI，使用各功能參數進行單次快速查詢
python scripts/brain_cli.py [功能參數]
```

### 📌 常用功能參數選項
*   `python scripts/brain_cli.py -l`：列出資料庫所有 Tables、當前 Row 統計與欄位摘要。
*   `python scripts/brain_cli.py -t`：列出所有研究專案及其下的子主題與 sequence_order 主題演進看板。
*   `python scripts/brain_cli.py --roots`：抽象路徑體檢，實體測試本地 Zotero 或 NAS 儲存路徑是否在線。
*   `python scripts/brain_cli.py -c [paper_id] -v`：一鍵繪製 ASCII 引用樹，並展開通讀樹中已消化 Stage 2 文獻的 10 大因子。
*   `python scripts/brain_cli.py -g [ms_id]`：將指定手稿的所有相關 DB 內容與自審日誌一鍵匯出為全景 Markdown 報告。
*   `python scripts/brain_cli.py -s "[SQL_string]"`：直接在終端輸入實體 SQL 照妖鏡語句進行硬核查詢。
