# 📁 實體資料庫與 DTO 貢獻信封 (Data Directory)

本目錄存放了主權大腦的二進位 SQLite 資料庫、軟連結、以及純文字的 DTO 知識合流信封。

---

## 📂 檔案與目錄說明 (Why it exists)

### 1. `Research_Artifacts.db`
*   **Why it exists**: 本地 serverless 的十一表 SQLite 實體資料庫。它儲存了本專案的所有 Ingestion 文獻、Manning's n 實測物理誤差、會後 Feedback 以及 Verdict PASS 自審答辯軌跡。
*   **物理證據作用**：它是這篇論文產製過程最剛性、無法捏造的「現地真值（Ground Truth）物理鐵證」。

### 2. `contributions/`
*   **Why it exists**: 存放純文字 JSON 格式的知識合流信封（如 `contrib_all.json`、`contrib_top_sovereign_methodology.json`）。
*   **多人協作解鎖**：為了解決 SQLite 在 Git 上 Push 時造成的二進位衝突，實驗室成員僅導出純文字的 JSON 貢獻包。在 rebuild 時，由重建腳本自動讀取本目錄下的 JSON 檔，在 0.5 秒內還原出完整的資料庫。

### 3. `downloaded_papers` & `pdfs` (Relative Symlinks)
*   **Why it exists**: 符號連結（Symbolic Links），指向 Repo 外部的實體 PDF 與預萃取 Markdown 資料夾。
*   **隱私與效能平衡**：確保版權/大體積 PDF 檔案不進入 GitHub 倉庫，同時確保代碼可無摩擦地在本地尋路讀取。
