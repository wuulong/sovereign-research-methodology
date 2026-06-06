# 🧱 methodology_74: 手稿誕生之真實實戰生命週期案例研討 (Manuscript Lifecycle & Operations Case Study)

本案例研討記錄了第一篇方法論論文手稿（`sovereign_research`）從最初的痛點考古、文獻引渡，到紅軍拷問、Verdict Lock 阻斷以及最終剛性答辯與發表的完整真實生命週期，旨在為初學者提供具體的實作指引。

---

## 📅 階段一：痛點探索、數位考古與 Staging 靠泊 (2026/05/10 - 05/11)

*   **實務現場**：研究團隊為了破解「研究生做研究混亂、導師難以稽核、大腦知識資產難以傳承」等三大戰壕痛點，在博班交流會前向大腦拋出「問題起點考古提問 (Q1.6)」。
*   **大腦時序流轉**：
    1.  **任務註冊**：大腦協作代理人（Antigravity）調用 `academic-research-navigator`，將此探索軌跡與考古對比矩陣寫入 `exploration_tasks`。
    2.  **文獻探勘**：導師下達 `!paper_scout` 指令，Navigator 探針隨即在 Zotero 與公海文獻庫中定位出 Snell2024 (思維主權與防衛) 與 Denkin2024 (可執行技能固化) 等頂級文獻。
    3.  **Layer 0 ➔ Layer 1 引渡**：運行 `sync_zotero_to_staging.py`。這些 PDF 被 Marker CLI 完美解析為 LaTeX Markdown，靠泊寫入 `paper_urls`，同時在 `papers` 表中註冊為待消化的 **`PENDING`** 狀態。

---

## 📅 階段二：降維解構、三位一體成熟與實體對合 (2026/05/20 - 05/25)

*   **實務現場**：導師受邀給研究生演講，將方法論初步概念寫入專書第 14 章。大腦資料庫由單一 papers 表急劇演進為十一表鋼鐵 Schema。
*   **大腦時序流轉**：
    1.  **Stage 2 深度解構**：導師下達 `!paper_digest` 指令，Navigator 接棒引導 AI 深度穿透 Snell2024 的理論骨架，高精降維提取 **10 大核心學術因子**（包含核心理論衝突、實證邊界與失效率）寫入 `papers.meta_data` JSON 欄位中，文獻狀態升級為頂級的 **`STAGE_2_DEEP`**。
    2.  **實作證據對合**：導師在開發此套工具鏈時遭遇的實體摩擦力（例如：Zotero 同步時部分 metadata 欄位需要人工手動 UPDATE 校正），被 `academic-paper-builder` 作為「現地實踐真值資料」，剛性註冊至 `empirical_evidences`，自動計算出偏離誤差。

---

## 📅 階段三：論點地圖合龍、紅軍突擊與 Verdict Lock 鎖定 (2026/05/26 - 06/03)

*   **實務現場**：方法論完全成熟，黃金 9 天發表衝刺發動！導師與評審約定於 06/05 進行硬核審查。研究生必須在會面前用這套大腦本身，把這篇方法論手稿物理編譯出來。
*   **大腦時序流轉**：
    1.  **一鍵骨架初始化**：下達 `!paper_init sovereign_research`，`academic-paper-builder` 秒級在 `my_manuscripts` 註冊本篇手稿，物理生成 8 大聯邦檔案骨架。
    2.  **APM 雙向合龍**：研究主稿撰寫完後，建構論點地圖（`06_argument_map.md`），下達 `!paper_map`。Builder 強制將手稿中的 12 個核心主張與資料庫 `papers` 表的 `STAGE_2_DEEP` 欄位以及 `empirical_evidences` 進行外鍵強烈 JOIN，寫入 `manuscript_citations`。
    3.  **紅軍靈魂拷問襲擊**：為了防止研究生自我感覺良好，下達 `!paper_grill` 指令。
    4.  **Verdict Lock 剛性阻斷**：紅軍 Skill `academic-advisor-auditor` 瞬間被物理喚醒，扮演最刻薄的哈教授發起猛烈攻勢：「*你宣稱這套科研典範能 100% 物理自指自證，那麼本手稿中是否確實包含了 Research_Artifacts.db 本身實體資料指紋的 DTO 記錄？若無，則自指純屬空談！*」
    5.  Auditor 將此質疑寫入 `red_team_logs`，狀態判定為 **`VULNERABLE`**。**Verdict Lock (合併鎖) 瞬間啟動，剛性阻斷手稿合龍與編譯輸出！**

---

## 📅 階段四：剛性答辯解鎖、一鍵拼裝與實體釋出 (2026/06/03 - 06/05)

*   **實務現場**：大限臨近，手稿必須在 Verdict PASS 的綠色狀態下才能通過審計，提交給資深學術前輩。
*   **大腦時序流轉**：
    1.  **剛性物理答辯**：研究生拒絕任何口頭投機。他運行 `!paper_rebuild`，將本地 SQLite 資料庫的全部結構與 Row 狀態一鍵導出為純文字 DTO `contribution.json` 並生成資料指紋。研究生將此資料指紋物理寫入論文手稿內，並於 `student_defense` 寫下剛性物理答辯軌跡。
    2.  **合併鎖解鎖**：Auditor 重新掃描手稿與 DTO，確認自指合龍度已達 100%，手動將 Verdict 更新為 **`PASS`**， Verdict Lock 隨即物理打開，解鎖編譯限制。
    3.  **MCI/MPM 雙看板盲檢**：`sovereign-poc-verifier` 啟動，PRAGMA 掃描資料庫實體完整度無摩擦，檢測本機 8 大 Python 腳本 100% 可用。MPM 自證度錄得 `92.50% (🟢 Elite)`，手稿 MCI 錄得 `91.80% (🟢 Elite)`。
    4.  **一鍵 BibTeX 拼裝與發表**：Paper-Builder 掃描手稿中所有的 `@cite_key`，從資料庫中自動抓取 BibTeX 條目，一鍵拼裝產出完美的 `references.bib`，並自動編譯回寫主稿，順利通過大佬會面審查。隨即直接自主發表上網，成為個人 AI 賦能專書的第 15 章！
