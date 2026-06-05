# NotebookLM Asset Pack - Root files of events/my_research/sovereign-research-methodology
- **Source Folder**: `events/my_research/sovereign-research-methodology`
- **Generated At**: 2026-06-06 07:37:50

---

================================================================================
📂 FILE PATH: README.md
================================================================================

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
    我們在 [scripts/verify_poc_completeness.py](scripts/README.md) 中打破了語意完整鏈結，強行引入「非語意物理約束」——**「現地實測偏離度 (friction_percentage)」**。
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
*   📁 **[skills/](skills/README.md) (四大主權核心 Skill 規格分區)**
    - 存放 Navigator、Builder、Auditor、Verifier 四大主權 Skill 的規格檔，是方法論對 AI 進行物理約束的控制本體。
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


================================================================================
📂 FILE PATH: rebuild_lab_brain.py
================================================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 本地聯邦資料庫一鍵重構器 (rebuild_lab_brain.py)

目的：
學弟妹或指導教授拉取最新的 Git 代碼倉庫後，一鍵執行此腳本，系統會：
1. 自動呼叫 `setup_research_db.py`，重建十一表結構並預載哈爸的專案與 Topics 骨架。
2. 自動掃描 `contributions/` 目錄下的所有純文字 JSON 貢獻包。
3. 將所有學長姐貢獻的背景文獻與關係鏈安全寫入，重構出 100% 整合的聯邦大腦！
"""

import os
import sys
import sqlite3
import json
import argparse

def rebuild_database(db_path, contrib_dir):
    print(f"[*] 啟動一鍵重構主權聯邦資料庫：{db_path}")
    
    # 1. 呼叫 setup_research_db.py 進行全新初始化
    scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
    sys.path.append(scripts_dir)
    try:
        import setup_research_db
        setup_research_db.setup_db()
        print("  [+] 資料庫結構、環境路由與三大專案 Topics 永恆骨架建立成功！")
    except Exception as e:
        print(f"  [-] 資料庫初始化失敗：{e}")
        return

    # 2. 掃描 contributions 目錄並寫入合流數據
    if not os.path.exists(contrib_dir):
        print(f"[!] 警告：找不到貢獻包目錄：{contrib_dir} (將保留空的專案與主題骨架)")
        return

    print(f"[*] 正在連線資料庫進行合流：{db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;") # 暫時關閉外鍵以Bulk寫入

    print(f"[*] 正在掃描共創貢獻目錄：{contrib_dir}")
    json_files = [f for f in os.listdir(contrib_dir) if f.endswith(".json")]

    if not json_files:
        print("  [o] 提示： contributions 目錄中尚無任何 JSON 貢獻包。")
    
    papers_count = 0
    relations_count = 0

    for json_file in json_files:
        json_path = os.path.join(contrib_dir, json_file)
        print(f"  - 載入貢獻包：{json_file}")
        
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"    [-] JSON 解析失敗：{e} (跳過)")
                continue

            # A. 寫入 papers
            papers_data = data.get("papers", [])
            for p in papers_data:
                cursor.execute("""
                INSERT OR IGNORE INTO papers (
                    paper_id, task_id, topic_id, title, authors, year, core_method, cite_key, bibtex, meta_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    p.get("paper_id"), p.get("task_id"), p.get("topic_id"),
                    p.get("title"), p.get("authors"), p.get("year"),
                    p.get("core_method"), p.get("cite_key"), p.get("bibtex"),
                    json.dumps(p.get("meta_data")) if p.get("meta_data") else None
                ))
                if cursor.rowcount > 0:
                    papers_count += 1

            # B. 寫入 paper_relations
            relations_data = data.get("paper_relations", [])
            for r in relations_data:
                cursor.execute("""
                INSERT OR IGNORE INTO paper_relations (
                    relation_id, source_paper_id, target_paper_id, relation_type, description
                ) VALUES (?, ?, ?, ?, ?)
                """, (
                    r.get("relation_id"), r.get("source_paper_id"),
                    r.get("target_paper_id"), r.get("relation_type"),
                    r.get("description")
                ))
                if cursor.rowcount > 0:
                    relations_count += 1

    conn.commit()
    conn.close()

    print(f"\n[+] 重構與合流完成！")
    print(f"  - 累計成功寫入背景文獻 (papers)：{papers_count} 筆。")
    print(f"  - 累計成功寫入演化關係 (relations)：{relations_count} 筆。")
    print(f"[*] 實驗室「聯邦共有大腦」已成功在本地重建！您可立即開啟 SQL 照妖鏡進行查詢。\n")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_db = os.path.join(base_dir, "data", "Research_Artifacts.db")
    default_contrib = os.path.join(base_dir, "data", "contributions")

    parser = argparse.ArgumentParser(description="哈爸主權聯邦共創 - 本地聯邦資料庫一鍵重構器")
    parser.add_argument("--db", default=default_db, help="重建資料庫之輸出路徑")
    parser.add_argument("--contrib-dir", default=default_contrib, help="JSON 貢獻包來源目錄")
    
    args = parser.parse_args()
    rebuild_database(args.db, args.contrib_dir)


================================================================================
📂 FILE PATH: schema.sql
================================================================================

-- ==============================================================================
-- 《個人AI賦能》v1.2.2 學術研究兵器庫 - 實體資料庫結構定義檔 (schema.sql)
-- 
-- 戰略設計：三層聯邦主權星系架構 (3-Tier Sovereign Knowledge Schema)
-- 本 Schema 將「他者背景文獻（他山之石）」、「本地實測與紅軍自審（肉身實踐）」與
-- 「主權研究手稿有向演化鏈（自我創造）」徹底融會對齊，是新一代 Agentic AI 方法論的數位孿生體。
-- 
-- 升級亮點：引進「抽象根目錄映射系統 (Abstract Directory Roots System)」，
-- 徹底隔離個人本地 Mac 與研究室共用 NAS 的絕對實體路徑，保證 100% 跨裝置移植與協同分享！
-- ==============================================================================

PRAGMA foreign_keys = ON; -- 強制啟用 SQLite 外鍵約束，確保參照完整性

-- ==============================================================================
-- 【第一層：探勘與血統任務層 (Ingestion & Lineage)】
-- 目的：追溯所有外部數據進入資料庫的「數位基因與血統」，保障學術數據之來源可信任性。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：exploration_tasks (探勘與採集任務日誌表)
-- 目的：記錄每一次執行 `paper_scout.py` 的探針軌跡。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exploration_tasks (
    task_id TEXT PRIMARY KEY,
    query TEXT NOT NULL,                  -- 本次探勘的原始關鍵字查詢
    run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 任務啟動時間戳記
    status TEXT NOT NULL,                 -- 任務狀態：'ONLINE' (線上直連) 或 'OFFLINE_FALLBACK' (離線模擬避退)
    papers_found INTEGER,                 -- 本次探勘成功捕獲並入庫的文獻數量
    agent_version TEXT,                   -- 執行此任務的 Agent 核心版本 (Lineage 追溯)
    error_log TEXT,                       -- 若有報錯，記錄詳細 Error Stack 以供 Agent 自行熱修復
    meta_data TEXT                        -- JSON 信封：{"host_os": "macOS", "cli_flags": ["--save-db"]}
);


-- ==============================================================================
-- 【第二層：主權專案與有向演化路線圖層 (Sovereign Project & Topic Roadmap)】
-- 目的：宣告研究生的領土主權，將大領域劃分為具備「時間向量與邏輯相依性」的有向演化路徑。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：projects (研究專案/領域主表)
-- 目的：定義博士生或研究團隊的核心研究疆域，作為全局架構的最高定錨點。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,           -- 專案名稱 (例如 'AR-WET 生醫植入式無線傳能系統')
    description TEXT,                     -- 專案宏觀願景與學術意圖描述
    
    -- 📡 【探勘契約 JSON】：記錄本專案與 Agent 之間持續搜尋論文的自動化查詢契約
    -- 欄位用途：Agent 讀取此欄位即可自主發動 Ingestion，不需學生重複下 Prompt。
    -- 格式範例：{"keywords": ["AR-WET", "acoustic-resonant"], "exclude": ["electromagnetic"], "min_year": 2018}
    search_spec TEXT NOT NULL, 
    
    -- 🏗️ 【物理架構脈絡 JSON】：定義本專案的基礎物理常數、目標規格與系統硬性限制
    -- 欄位用途：做為本地實測數據比對的 Baseline，判斷是否達成「專案目標規格」。
    -- 格式範例：{"target_freq_MHz": 25.0, "max_depth_mm": 10.0, "allowed_temp_rise_C": 2.0}
    architecture_spec TEXT, 
    
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    meta_data TEXT                        -- JSON 信封：預留向前相容的詮釋資料空間
);

-- ------------------------------------------------------------------------------
-- 資料表：topics (循序研究主題表)
-- 目的：將大專案劃分為「循序推進」的子主題，作為演進的「邏輯脊椎」。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS topics (
    topic_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    topic_name TEXT NOT NULL,             -- 主題名稱 (例如 '非線性 Duffing 分歧之匹配電路補償')
    
    -- 🔢 【邏輯演進順序】：標記此主題在專案中的邏輯相依次序 (如 1, 2, 3)
    -- 欄位用途：
    --   1. 自動上下文繼承：當 seq = 2 啟動時，Agent 自動載入所有 seq < 2 的研究真值作為 Baseline。
    --   2. 定位施工現場：系統能精確辨識目前處於哪一個 active 戰場，防止認知過載。
    sequence_order INTEGER NOT NULL, 
    
    -- 🎯 【聚焦研判 JSON】：記錄本主題特有的焦點物理變數、核心公式與自動打標標籤
    -- 欄位用途：指引紅軍對抗 Agent 針對特定公式（如 Duffing）發動精確的自審攻擊。
    -- 格式範例：{"focus_variables": ["Q_factor", "bifurcation_threshold"], "equations": ["Duffing_equation"]}
    focus_spec TEXT NOT NULL, 
    
    status TEXT NOT NULL,                 -- 當前狀態：'PLANNED' (規劃中) | 'ACTIVE' (施工中) | 'COMPLETED' (已完成)
    meta_data TEXT,                       -- JSON 信封：擴展詮釋資料
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);


-- ==============================================================================
-- 【第三層：環境定錨與抽象路徑層 (Environment Roots & Mapping)】
-- 目的：將物理實體路徑抽象化，徹底隔離「個人本地環境」與「研究室共享環境」的移植衝突。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：directory_roots (目錄實體映射配置表)
-- 目的：定義在當前執行環境下，各個抽象根目錄鍵 (Root Key) 對應的實際絕對路徑。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS directory_roots (
    root_key TEXT PRIMARY KEY,            -- 抽象根目錄鍵 (例如 'zotero_storage' | 'lab_nas' | 'workspace_root')
    owner_type TEXT NOT NULL,             -- 擁有者類型：'STUDENT_LOCAL' (研究生個人) | 'LAB_SHARED' (研究室公用)
    owner_name TEXT NOT NULL,             -- 擁有者名稱 (例如 研究生姓名 'wuulong' 或實驗室代號 'vres_lab')
    absolute_path TEXT NOT NULL,          -- 實體運作環境下的絕對路徑 (例如 '/Users/wuulong/Zotero/storage/')
    meta_data TEXT                        -- JSON 信封：{"mount_protocol": "smb", "os_compatibility": "macOS"}
);


-- ==============================================================================
-- 【第四層：結構化文獻定錨層 (Structured Literature Grounding)】
-- 目的：存放嚴謹的第三方背景文獻，並建立強大的「多維標籤系統」與「LaTeX 引用直達車」。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：papers (背景文獻主表)
-- 目的：存儲高質量的外部文獻，作為知識定錨的基石。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS papers (
    paper_id TEXT PRIMARY KEY,
    task_id TEXT,                         -- 關聯至探勘任務，追溯此數據的採集血統
    topic_id TEXT,                        -- 關聯至特定的子主題，理清文獻的邏輯定位
    title TEXT NOT NULL,                  -- 論文標題
    authors TEXT,                         -- 作者清單 (文字格式，適合檢索)
    year INTEGER,                         -- 發表年份
    core_method TEXT,                     -- 核心方法摘要 (如：高維度語義摘要)
    
    -- ✍️ 【學術引用一等公民欄位】：與 LaTeX / Overleaf 100% 對齊的引用機制
    -- 欄位用途：寫論文時，Agent 可秒級導出所有已引用的 BibTeX，拼裝成完美的 references.bib。
    cite_key TEXT UNIQUE NOT NULL,        -- LaTeX 引用鍵 (例如 'Wang2026ARWET')
    bibtex TEXT NOT NULL,                 -- 原始完整的 BibTeX 條目字串
    
    meta_data TEXT,                       -- JSON 信封：存放動態物理參數 {"Q": 12000, "freq_MHz": 28.5}
    FOREIGN KEY (task_id) REFERENCES exploration_tasks(task_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);

-- ------------------------------------------------------------------------------
-- 資料表：paper_relations (背景文獻交叉關係演化表 - v1.2.2)
-- 目的：追溯文獻之間的繼承與批判關係，支援 SQL 自動生成學術演化譜系圖。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paper_relations (
    relation_id TEXT PRIMARY KEY,
    source_paper_id TEXT NOT NULL,       -- 起點文獻 (新文獻)
    target_paper_id TEXT NOT NULL,       -- 目標文獻 (被繼承或被批判之舊文獻)
    relation_type TEXT NOT NULL,         -- 關係類型：'IMPROVES' (改進) | 'REFUTES' (反駁) | 'GROUNDED_ON' (基於)
    description TEXT,                    -- 關係心智描述
    FOREIGN KEY (source_paper_id) REFERENCES papers(paper_id),
    FOREIGN KEY (target_paper_id) REFERENCES papers(paper_id)
);

-- ------------------------------------------------------------------------------
-- 資料表：paper_urls (文獻多重資源關聯表 - B方案實體抽象版)
-- 目的：支援單篇文獻掛載多重資源（官方網頁、ArXiv、本地 PDF 等）。
-- 
-- 💡 【核心演化】：此表格不直接存放實體路徑，而是存放「相對路徑（url_link）」並外鍵關聯
-- 至「目錄實體映射表（directory_roots）」，一舉解決資料庫跨電腦移植時路徑斷線的噩夢！
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paper_urls (
    url_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    
    -- 🔑 【抽象根目錄外鍵】：強烈參照至 directory_roots 表格，實現路徑的抽象化定錨
    root_key TEXT NOT NULL,               
    
    -- 📂 【相對路徑】：相對於該 root_key 所指向之實體絕對路徑的相對位址 (例如 'ABCDE123/paper.pdf')
    url_link TEXT NOT NULL,               
    
    url_type TEXT NOT NULL,               -- 資源類型：'publisher' (官方) | 'arxiv_pdf' (預印) | 'local_pdf' (本地) | 'code_repo'
    download_status TEXT,                 -- 下載狀態：'PENDING' | 'DOWNLOADED' | 'FAILED'
    file_size_bytes INTEGER,              -- 本地實體檔案大小，用於檢驗文件完整性
    meta_data TEXT,                       -- JSON 信封：{"download_retry_count": 0, "http_status": 200}
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id),
    FOREIGN KEY (root_key) REFERENCES directory_roots(root_key)
);

-- ------------------------------------------------------------------------------
-- 資料表：paper_tags (文獻多維關聯式標籤表)
-- 目的：克服分類單一性的缺陷，為文獻打上多維度標籤，實現超高效的交叉檢索。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paper_tags (
    paper_id TEXT NOT NULL,
    tag_name TEXT NOT NULL,               -- 標籤名稱 (例如 'piezoelectric', 'non-linear', 'biomedical')
    meta_data TEXT,                       -- JSON 信封
    PRIMARY KEY (paper_id, tag_name),
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);
CREATE INDEX IF NOT EXISTS idx_tags_name ON paper_tags(tag_name); -- 加速標籤查詢

-- ------------------------------------------------------------------------------
-- 資料表：taxonomy_framework (大一統階層分類架構表 - v2.3 新增)
-- 目的：定義哈爸審定之大一統主/次分類骨架，剛性防禦 AI 自動標記時的語意漂移。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS taxonomy_framework (
    path TEXT PRIMARY KEY,               -- 階層前綴路徑 (例如 'AI應用/個人賦能')
    description TEXT,                    -- 分類意圖說明
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- ------------------------------------------------------------------------------
-- 資料表：topic_gravity_overrides (主題學術重力偏置表 - v1.2.3)
-- 目的：支援「主題敏感型學術重力計量 (Topic-Sensitive Academic Gravity)」，
--       針對不同主題，動態調整特定期刊/會議或機構的學術重力偏置值。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS topic_gravity_overrides (
    topic_id TEXT NOT NULL,
    entity_name TEXT NOT NULL,           -- 期刊/會議或機構的名稱 (不分大小寫比對)
    entity_type TEXT NOT NULL,           -- 'VENUE' (學術載體) 或 'INSTITUTION' (研究機構)
    bias_score REAL NOT NULL,            -- 偏置得分 (例如 +3.0 表示在此主題極權威，-2.5 表示無關)
    description TEXT,                    -- 為什麼要做此偏置的學術考量說明
    PRIMARY KEY (topic_id, entity_name, entity_type),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);


-- ==============================================================================
-- 【第五層：實體執行與紅軍對抗層 (Execution, Synthesis & Red Teaming)】
-- 目的：將文獻理論與「學生的肉身實踐（模擬/量測）」以及「心智對抗過程」徹底對齊。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：empirical_evidences (肉身實踐與實體舉證表)
-- 目的：記錄研究生針對論文理論所做出的實作、系統測試或實體舉證，作為「現地真值（Ground Truth）」比對與手感定錨。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS empirical_evidences (
    evidence_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    
    -- 🛠️ 【實踐與舉證配置 JSON】：記錄本次實踐的背景情境與條件設定
    -- 格式範例：{"study_basin": "Zengwen River Midstream", "elevation_reference": "DEM_20M"}
    practice_scenario TEXT NOT NULL, 
    
    -- 📊 【實體舉證數據 JSON】：記錄實作取得的證據、誤差或 Payload
    -- 格式範例：{"measured_flow_rate_cms": 1.2, "estimated_flow_rate_cms": 1.05}
    evidence_payload TEXT, 
    friction_percentage REAL,             -- 【主權比對指標】：實踐中的物理誤差、數值偏離度或網路摩擦力百分比 (如 12.5%)
    artifact_visual_path TEXT,            -- 【主權多模態】實體舉證圖表/實測波形圖/代碼路徑之相對路徑
    evidence_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    meta_data TEXT,                       -- JSON 信封：{"host": "Habars_Mac Studio"}
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);


-- ------------------------------------------------------------------------------
-- 資料表：red_team_logs (紅軍自審與品位裁決日誌表)
-- 目的：記錄學生與紅軍 Agent 對抗自審的螺旋演化軌跡，做為「品位裁決」的實體證據。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS red_team_logs (
    log_id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    manuscript_id TEXT,                   -- 關聯至手稿，直接對研究生自己的論文設計發動對抗 (v1.2.2)
    aspect_analyzed TEXT,                 -- 本次對抗的分析維度 (例如 'Duffing Non-linear Bifurcation')
    reviewer_attack TEXT,                 -- 紅軍 Agent (扮演嚴厲審稿人) 提出的尖銳物理質疑
    student_defense TEXT,                 -- 學生做出「品位裁決」後的防禦策略、修正公式與推導
    verdict TEXT NOT NULL,                -- 裁決判定：'PASS' (通過) | 'VULNERABLE' (脆弱) | 'CRITICAL_BUG' (嚴重錯誤)
    test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    meta_data TEXT,                       -- JSON 信封：{"judge_model": "Gemini_3.0_Pro", "tokens_used": 1540}
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id),
    FOREIGN KEY (manuscript_id) REFERENCES my_manuscripts(manuscript_id)
);


-- ==============================================================================
-- 【第六層：主權手稿有向演化層 (Sovereign Manuscript Evolution Chain)】
-- 目的：記錄研究生「自我創造」的成果演化。自己的論文不再是孤島，而是承載了前人基因的演化鏈。
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 資料表：my_manuscripts (主權手稿表)
-- 目的：記錄自己正在撰寫、修改或已發表的系列論文（繼承演化鏈）。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS my_manuscripts (
    manuscript_id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    title TEXT NOT NULL,                  -- 手稿標題
    cite_key TEXT UNIQUE,                 -- 本篇手稿預計的 Citation Key (如 'Wang2026_Ch1_Draft')
    manuscript_type TEXT NOT NULL,         -- 手稿類型：'Conference' | 'Journal' | 'Thesis' (論文)
    evolution_stage TEXT NOT NULL,        -- 演化階段：'Planning' | 'Writing' | 'Under_Review' | 'Published'
    
    -- 🧬 【手稿演化外鍵】：指向上一篇前導研究手稿，建立「心智基因繼承鏈」
    -- 欄位用途：讓 Agent 與指導教授清晰理清整套畢業論文的研究脈絡傳承。
    previous_manuscript_id TEXT, 
    
    meta_data TEXT,                       -- JSON 信封：存放寫作專案網址 {"overleaf_url": "https://overleaf.com/123456"}
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
    FOREIGN KEY (previous_manuscript_id) REFERENCES my_manuscripts(manuscript_id)
);

-- ------------------------------------------------------------------------------
-- 資料表：manuscript_citations (主權手稿引用關聯表)
-- 目的：精確理清我的論文與他人背景文獻之間的「引用脈絡」。
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS manuscript_citations (
    manuscript_id TEXT NOT NULL,          -- 我的手稿 ID
    paper_id TEXT NOT NULL,               -- 被引用的背景論文 ID
    
    -- 🧠 【引用心智脈絡】：記錄「我為什麼要在我的這篇草稿中引用這篇背景文獻」
    -- 欄位用途：寫論文時，Agent 可依據此欄位自動產出極具說服力的文獻綜述（Literature Review）。
    -- 格式範例：'作為品質因子 Q 值實測 Baseline 的對比依據'
    citation_context TEXT, 
    
    meta_data TEXT,                       -- JSON 信封
    PRIMARY KEY (manuscript_id, paper_id),
    FOREIGN KEY (manuscript_id) REFERENCES my_manuscripts(manuscript_id),
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);

