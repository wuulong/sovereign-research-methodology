# 🧠 AI 時代的學術革命：主權科研大腦與自指自證實踐 (Sovereign Research Brain)

> **「當 AI 氾濫、學術語意泡沫化時，我們如何守護思考手感，物理證明『這篇論文是由這套系統物理長出來的』？」**

本專案是《個人 AI 賦能》專書第 15 章的開源實體示範 Repo。我們在此開源了「主權科研大腦（Sovereign Research Brain）」的完整方法論規格書、論文手稿、NotebookLM 整合封包以及自審/自證工具鏈。

本專案最核心的學術價值與哲學在於**「自指自證（Self-Referential Proof）」**：這篇論文本身，就是利用本 Repo 中的十一表 SQLite 資料庫與主權工具鏈，經過多輪紅軍自審、答辯與「現地真值對合」後，物理生成並編譯出來的。

---

## 🧬 為什麼需要這套大腦指標與架構？(The Architecture Why)

當前人機協作科研大多面臨「AI 幻覺無法校準」與「學生思維空洞化」的致命危機。本系統從物理層面設計了硬性的代數與資料庫約束，以捍衛思維主權：

### 1. 為什麼需要「手稿成熟與可信度指數 (MCI)」？
*   **痛點**：研究生在使用 AI 協作自審時，極易採取「投機自審」——只針對 1 篇無關緊要的文獻進行自審，便宣告 100% 通過。
*   **MCI 的救贖**：
    我們在 [scripts/verify_manuscript_maturity.py](scripts/README.md) 中設計了剛性算分指標：
    $$\text{MCI} = \text{文件完備分} \times 0.3 + \text{大腦定錨分} \times 0.7$$
    其中大腦定錨分被剛性設定為 **「60% 自審文獻覆蓋率 + 40% 自審通過率」**。如果小明只自審了 1 篇論文，覆蓋率會極低，進而觸發剛性扣分限制，MCI 指標會跳出 `CAUTION` 警告。**這物理逼迫學生必須老老實實完成全局文獻自審與 Socratic 答辯**。

### 2. 為什麼需要「元自證成熟度指數 (MPM)」與「物理摩擦」？
*   **痛點**：傳統學術評估流於「語意交鋒」，甚至使用 AI 評估 AI（如 RAGAS），容易產生自欺欺人的「自指幻覺共謀」。
*   **MPM 的救贖**：
    我們在 [scripts/verify_poc_completeness.py](scripts/README.md) 中打破了語意閉環，強行引入「非語意物理約束」——**「現地實測偏離度 (friction_percentage)」**。
    在 MPM 指數（40% 資料庫完整性 + 30% 工具鏈高可用 + 30% 手稿自指自證度）中，剛性要求手稿論點地圖中**必須包含資料庫實體 DTO JSON 的純文字指紋**。這向學術評審團物理證明了「這篇論文的論點與資料庫完全對合，是由這套系統物理長出來的」。

### 3. 為什麼需要「純文字 JSON 貢獻包 (DTO)」與「軟連結入庫」？
*   **痛點**：多名研究人員共同開發同一個研究大腦時，SQLite 二進位檔案在 push Git 時必然會發生無法自動 merge 的嚴重衝突；且版權 PDF 檔案因容量與隱私無法進入 Git 庫。
*   **DTO 與軟連結的救贖**：
    我們利用純文字的 [contributions/contrib_all.json](data/README.md) 信封包，實現了個人私有心流與聯邦大腦的解耦，完美抹平了 Git 二進位衝突。
    同時，我們在 `data/` 下建立了指向外部實體大檔案的相對軟連結（Symbolic Links），並**直接 add 提交軟連結入庫**。這使得任何人在 clone 本 repo 後，軟連結能自動無摩擦指向本地外部 PDF，兼顧了「大檔案隱私隔離」與「克隆即對齊」的高可用性。

---

## 📂 專案物理結構 (Directory Layout & Navigation)

點選以下目錄超連結，可直接查閱各分區的專屬詳細說明書（包含 Why 設計意圖）：

*   📁 **[methodology/](methodology/README.md) (主權科研方法論規格書分區)**
    - 存放系統需求規格書、元資料 schema 設計規範以及關係本體定義檔。構成大腦的「憲法與骨架」，防範 AI 隨意更改資料結構。
*   📁 **[manuscripts/](manuscripts/README.md) (手稿主檔與自證報告分區)**
    - 存放論文主手稿 [sovereign_research_05_manuscript.md](manuscripts/sovereign_research/sovereign_research_05_manuscript.md)、邏輯辯證地圖 APM 06、成熟度報告 MCI 09 以及元自證報告 MPM 10。將手稿產製物理級解構，消滅「未讀先引」。
*   📁 **[nblm_notes/](nblm_notes/README.md) (NotebookLM 4 大綜合封包與 15 大 Prompt)**
    - 存放高度整合、物理定錨的 Bundle 檔案。避開 Context 碎片化對 LLM 造成的語意盲區，提供 15 大大師級 Prompt。
*   📁 **[scripts/](scripts/README.md) (大腦運轉、自審與驗證核心腳本庫)**
    - 存放驅動大腦 SQLite 運轉與 MCI、MPM 指標計量的 Python 自治工具鏈。
*   📁 **[data/](data/README.md) (實體資料庫與 DTO 貢獻信封)**
    - 存放實體 SQLite 資料庫 `Research_Artifacts.db` 與純文字 DTO json 貢獻信封。

---

## 🚀 快速開始：一鍵重構與自指自審

### 1. 克隆專案並繼承軟連結
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

# 計算元自證成熟度 (MPM)
python scripts/verify_poc_completeness.py
```

---

## 🏛️ 主權學者領主宣言 (The Sovereign Scholar Manifesto)

> **「原創源自於肉身對實體世界偏離誤差的校正，而非對 LLM 語意幻想的無腦妥協。」**

在 AI 工具極大降低寫作門檻的今天，這套方法論強制我們在**「理論的邊界、資料的結構、肉身的實踐」**中，重新奪回思維主權。我們誠摯邀請您一起實踐行解合一的學術探索！
