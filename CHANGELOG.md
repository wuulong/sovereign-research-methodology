# 📝 變更日誌 (Changelog)

本檔案物理記錄了「主權科研大腦（Sovereign Research Brain）」開源儲存庫的版本演進歷史與變更明細。本專案遵循語意化版本（Semantic Versioning）規範進行版本管理。

---

## [v0.2.1] - 2026-06-06
### 🚀 釋出與重構
*   **四大核心主權技能完整釋出**：將 Navigator、Builder、Auditor、Verifier 四大核心 Skill 複製到子模組的 `skills/` 目錄下，建立導航說明，正式完整釋出。
*   **方法論規格大合流**：將原本分散的 `02_metadata_schema_spec.md` (元資料規格) 與 `03_relation_ontology.md` (關係本體規格)，完整併入 `methodology_02_system_architecture_navigator.md` (原 04 改名為 02)，使大憲章規格精簡收攏為 01 (需求) 與 02 (系統規格與運作手冊) 兩大基石，並清理舊有 02, 03, 04 檔案。
*   **NotebookLM 封包重建**：建置並執行 `rebuild_notebooklm_pack.py` 腳本，自動將合流後的最新 `methodology` 重構拼裝至封包檔 [methodology_notebooklm.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/nblm_notes/methodology_notebooklm.md)。

### 🛠️ 品質治理與本土化
*   **全域台灣用語本土化**：擴展並執行 `taiwanize_submodule_skills.py` 腳本，對子模組中全部 24 個 `.md` 檔案與四大 Skill 檔案執行轉換，將「數據、優化、閉環、代碼」等中國用語 100% 替換為「資料、最佳化、完整鏈結、程式碼」等台灣慣用語。
*   **Git Log 每日摘要化**：在 `extract_evolution_history.py` 實作每日合併摘要邏輯，將密集 Commit 合併為精簡的每日事件表格。

---

## [v0.2] - 2026-06-06
### 🚀 獨立開源發表
*   **子模組 Repo 初始化**：將主權大腦方法論、手稿、自審與驗證腳本從主專案獨立至全新的開源子儲存庫 `sovereign-research-methodology`，並在外層 `bmad-pa` 專案中註冊為 Git Submodule 以維持去中心化大腦。
*   **無摩擦軟連結入庫**：將實體大體積 PDF 移出 Git 追蹤，於 `data/` 下建立相對軟連結並提交，達成克隆即對齊的高可用性。
*   **專書連結重定向**：將《個人 AI 賦能》專書第 15 章的所有超連結改為開源 GitHub 線上 Blob 網址，推動理論與物理實踐的雙向自指。

---

## [v0.1.1] - 2026-05-26
### 🛡️ 自審對抗與加權指標
*   **十一表大腦 Schema 升級**：SQLite 升級為十一表剛性骨架，引進 `empirical_evidences`（實踐與實體舉證表）取代模擬表。
*   **品質看板算分指標落地**：正式開發並實裝 MCI（手稿成熟度指數，首發 86.39%）與 MPM（元自證成熟度指數，首發 80.00%）剛性算分器。
*   **Verdict Lock 合併阻斷防線**：在 `red_team_logs` 中引入 `'VULNERABLE'` 紅軍自審漏洞合併鎖，強制阻斷合流，逼迫研究生進行剛性答辯。

---

## [v0.1] - 2026-05-14
### 🏛️ 大腦原型建置
*   **單一資料表大腦原型**：首次於 SQLite 實作大腦資料庫化，採用單一資料表設計與基礎知識分層。
*   **資料定錨與編碼規範**：導入 ID-Prefix 標準編碼與多源資料聚合規範，確保多資料源的版本追蹤與資料定錨。
