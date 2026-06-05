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
