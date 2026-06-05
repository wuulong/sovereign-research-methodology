# 🛠️ 大腦核心腳本庫說明書 (Scripts & Toolchain Guide)

本目錄存放了驅動「主權科研大腦」十一表 SQLite 資料庫運轉、文獻探勘、紅軍自審、MCI 與 MPM 指標計量的核心工具鏈。

---

## 🧬 為什麼我們需要這些腳本？(The Design Philosophy)

如果說 SQLite 資料庫是我們大腦的「數位記憶皮質」，那麼本目錄下的 Python 腳本就是引導資訊進出、自審防禦與物理剪枝的「數位神經元」。

### 1. 消除「無法遺傳的環境孤島」：環境自治 (Self-Containment)
在早期的科研工具中，腳本常常寫死特定電腦的絕對路徑（例如：`/Users/username/Downloads/...`），這導致整個研究大腦具備極致的脆弱性——一旦換了電腦，或是學弟妹克隆倉庫，整個系統就會崩潰。
本目錄下的腳本經過了**「自治化重構」**，全面以 Repo 根目錄進行相對路徑計算。這保障了任何人在任何 macOS/Linux 裝置上 clone 本 repo 後，即可一鍵 `rebuild` 資料庫，實現無摩擦的「知識遺傳」。

### 2. 打破「以 AI 評估 AI」的語意完整鏈結
當前的科研 Agent（如 RAGAS 框架）通常使用 AI 來評估 AI 產出的品質，這本質上是自欺欺人的「語意幻覺共謀」。
本工具鏈（如 `verify_poc_completeness.py` 與 `verify_manuscript_maturity.py`）透過剛性盲檢 SQLite 外鍵約束、物理計量腳本存在率，以及審計手稿論點中是否包含資料庫匯出的實體 DTO 指紋，以**非語意的「物理摩擦與代數約束」**，強制對 AI 語意進行謬誤剪枝，完成自指自證。

---

## 📂 核心腳本清單與存在目的 (Tool Matrix)

| 腳本名稱 | 運作目的 (Why it exists) | 驅動的資料庫實體表 (DB Tables) |
| :--- | :--- | :--- |
| `rebuild_lab_brain.py` (置於根目錄) | **Why**: 繞過 SQLite 二進位檔案在 Git 上的合併衝突，藉由讀取純文字的 DTO JSON 貢獻包，在本地秒級重建整合大腦。 | 全庫十一張表 (自 `schema.sql` 重建) |
| `scripts/brain_cli.py` | **Why**: 提供無摩擦的大腦互動 CLI 介面，免去繁瑣的 SQL 查詢輸入。 | `papers`, `topics`, `empirical_evidences` |
| `scripts/setup_research_db.py` | **Why**: 在初始化時物理固化實驗室專案（projects）與主題（topics）的「永恆骨架」，防止 rebuild 時將 staging 公海文獻一併級聯清空 (Cascade Crash)。 | `projects`, `topics` |
| `scripts/verify_manuscript_maturity.py` | **Why**: 計算「手稿成熟與可信度指數 (MCI)」，以 60% 覆蓋率與 40% PASS 率的剛性加權，制約研究生的投機自審行為。 | `my_manuscripts`, `red_team_logs`, `papers` |
| `scripts/verify_poc_completeness.py` | **Why**: 計算「元自證成熟度指數 (MPM)」，盲檢 SQLite 完整性與「三位一體對合率」，並物理寫入自證報告。 | 全庫十一張表 (含 `empirical_evidences`) |
| `scripts/audit_brain_compliance.py` | **Why**: 物理盲檢全庫 Ingestion 品質，對合規資料進行 compliance_status 剛性打標，作為防範 AI 污染的物理關卡。 | `papers`, `empirical_evidences`, `red_team_logs` |
| `scripts/sync_zotero_to_staging.py` | **Why**: 繞過脆弱的線上 API 與 429 Rate Limit，直連 Zotero SQLite，自動解析 8 碼隨機金鑰，一鍵同步 PDF 至 staging。 | `papers`, `paper_urls` |
| `scripts/scout_zotero_global_landscape.py`| **Why**: 站在四大理論支柱高度，在 staging 公海大腦中模糊檢索匹配文獻，以 SQL UPDATE 一鍵引渡重定向靠泊。 | `papers`, `topics` |
| `scripts/anchor_manuscript_citations.py` | **Why**: 將主題下文獻與手稿進行物理繫結，並撈取 BibTeX 匯出為完璧 references.bib，確保引文與 SQLite 完全一致。 | `manuscript_citations`, `papers` |
| `scripts/extract_evolution_history.py` | **Why**: 讀取本地資料庫的 `red_team_logs` 自審答辯軌跡與 Git Submodule Commit logs，去識別化自動提煉大腦螺旋建構歷程，寫回第二章手稿。 | `red_team_logs` |

---

## 🧪 驗證指令
在根目錄下，您可以使用以下指令，親眼見證工具鏈的自治化執行：
```bash
# 1. 重建大腦
python rebuild_lab_brain.py

# 2. 驗證成熟度 MCI
python scripts/verify_manuscript_maturity.py

# 3. 驗證自證率 MPM
python scripts/verify_poc_completeness.py
```
