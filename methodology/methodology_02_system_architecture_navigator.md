# 📐 methodology_02: 主權大腦系統架構與 10 大分區導覽 (System Architecture & Operations Portal)

本手冊是主權科研大腦的運行大憲章入口。系統性整合了圍繞著實體 SQLite 十一表資料庫所構成的四大主權核心 Skill 運作網絡，並提供全景 10 大分區規格書的跳轉地圖。

---

## 🏛️ 1. 主權大腦四星協同運作模型 (Sovereign Skills & DB Orchestration)

整個主權科研典範並非依靠單一 AI 代理人的心流碰撞，而是由 **四大專屬學術研究 Skill** 圍繞著實體 **SQLite 資料庫 (`Research_Artifacts.db`)** 所構成的精密防禦縱深：

```mermaid
flowchart TD
    %% 定義 Skill 節點
    subgraph Skills["⚡ 四大主權核心 Skill"]
        NAV["1️⃣ academic-research-navigator<br>(學術研究導航員 - 81)"]
        AUD["2️⃣ academic-advisor-auditor<br>(學術品質自審審計 - 82)"]
        BLD["3️⃣ academic-paper-builder<br>(學術論文建構師 - 83)"]
        VRF["4️⃣ sovereign-poc-verifier<br>(主權自證驗證器 - 84)"]
    end

    %% 定義 SQLite 資料表節點
    subgraph DB["🔬 底層實體大腦 (SQLite DB Tables)"]
        T_Task[(exploration_tasks<br>探採任務)]
        T_Proj[(projects & topics<br>專案與循序主題)]
        T_Paper[(papers<br>背景文獻主表)]
        T_Rel[(paper_relations<br>文獻演化關係)]
        T_Url[(paper_urls & roots<br>多重資源相對路徑)]
        T_Evid[(empirical_evidences<br>實踐與實體舉證)]
        T_Red[(red_team_logs<br>紅軍自審對抗)]
        T_MS[(my_manuscripts & cites<br>手稿演化與引用脈絡)]
    end

    %% 定義 聯邦檔案與腳本
    subgraph Artifacts["📂 聯邦手稿與腳本資產"]
        MS_Doc["sovereign_research_05_manuscript.md<br>(手稿主體)"]
        APM_Doc["sovereign_research_06_argument_map.md<br>(論點地圖)"]
        MCI_Doc["sovereign_research_09_maturity_report.md<br>(MCI 品質看板)"]
        MPM_Doc["sovereign_research_10_poc_proof_report.md<br>(MPM 自證看板)"]
        BIB_File["sovereign_research_04_references.bib<br>(標準 BibTeX 引文庫)"]
    end

    %% 關聯線：Navigator
    NAV -->|1. 寫入任務與主題| T_Task
    NAV -->|2. 靠泊引渡與消化| T_Paper
    NAV -->|3. 計算有向演化與相對路徑| T_Rel

    %% 關聯線：Advisor-Auditor
    AUD -->|1. 提取攻防日誌| T_Red
    AUD -->|2. 剛性 Verdict Lock| T_Red
    T_Red -->|3. 計算 MCI 指標| MCI_Doc
    MCI_Doc -->|4. 觸發合併阻斷| MS_Doc

    %% 關聯線：Paper-Builder
    BLD -->|1. 追蹤寫作基因與 Claim 對合| T_MS
    T_Paper -->|2. 自動拼裝 BibTeX| BIB_File
    APM_Doc -->|3. 抽取 Claims 脈絡| T_MS
    T_MS -->|4. 動態擴寫編譯| MS_Doc

    %% 關聯線：PoC-Verifier
    VRF -->|1. 檢驗外鍵與實體完整性| T_Evid
    VRF -->|2. 檢測工具鏈無摩擦率| DB
    VRF -->|3. 覆寫產出自證報告| MPM_Doc

    %% 樣式設定
    style NAV fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    style AUD fill:#fbe9e7,stroke:#d84315,stroke-width:2px;
    style BLD fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    style VRF fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px;
    style DB fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
```

---

## 📐 2. 10 大分區系統化編號規範 (Segmentation Specs)

為確保方法論規格書的易讀性與擴充對稱性，本目錄下的所有檔案均採用「**每區預算 10 碼，區間跳跃式分區**」進行編號。每一分區的 `X0` 碼作為該分區總導覽/保留使用，而規格書則從 `X1` 開始編號：

```
- 第 0 區 [00-09]：系統需求與架構導覽 (Requirements & Portal)
- 第 1 區 [10-19]：底層資料庫與中繼資料規格 (Database Schema & Metadata)
- 第 2 區 [20-29]：文獻引渡與 Stage 2 消化加工 (Ingestion & Digesting)
- 第 3 區 [30-39]：理論演化與學者品位裁決 (Topology & Taste)
- 第 4 區 [40-49]：安全對抗與合併阻斷防禦 (Security & Verdict Lock)
- 第 5 區 [50-59]：現地對合與實踐校準 (Empirical Evidences & Calibration)
- 第 6 區 [60-69]：多人協作與去中心化合流 (Collaboration & Git merge)
- 第 7 區 [70-79]：雙看板指標與自審測試 (Metrics & Benchmark)
- 第 8 區 [80-89]：星級 Skills 協同規範 (Agentic Skills Specification)
- 第 9 區 [90-99]：系統維護、提示詞與工具手冊 (System Operations & Prompts)
```

> [!TIP]
> **未來新增檔案指引**  
> 若未來要加入與「版本釋出」、「多 Agent 協同協定」等相關的規格，請將其放入 **第 6 區**，命名為 `methodology_64_xxx.md`，以此類推。這能保持編號在二位數（01 - 99）內的絕對自洽。

---

## 📂 3. 10 大分區規格書跳轉地圖 (The Specification Matrix)

### 第 0 區：系統需求與架構導覽
*   **`01`**：[methodology_01_requirements.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_01_requirements.md) ➔ 宣示思維主權與防衛認知掏空的頂層規格需求。
*   **`02`**：[methodology_02_system_architecture_navigator.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_02_system_architecture_navigator.md) ➔ **【本入口頁面】** 系統總覽與 10 大分區地圖。

### 第 1 區：底層資料庫與中繼資料規格
*   **`11`**：[methodology_11_database_schema_spec.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_11_database_schema_spec.md) ➔ 十一表 DDL 設計、`meta_data` JSON 規格與合規性自動化審計。
*   **`12`**：[methodology_12_relation_ontology_spec.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_12_relation_ontology_spec.md) ➔ 文獻有向演化之 8 大關係本體與關係 DTO 規格。

### 第 2 區：文獻引渡與 Stage 2 消化加工
*   **`21`**：[methodology_21_three_tier_federated_brain.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_21_three_tier_federated_brain.md) ➔ 三層聯邦大腦（Layer 0 緩衝 ➔ Layer 1 靠泊 ➔ Layer 2 深消化）。
*   **`22`**：[methodology_22_academic_gravity_and_digesting.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_22_academic_gravity_and_digesting.md) ➔ 學術重力場公式 $G_a$、精讀優先級與 Stage 2 十大因子降維解構工序。

### 第 3 區：理論演化與學者品位裁決
*   **`31`**：[methodology_31_theory_grounding_and_bfs_topology.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_31_theory_grounding_and_bfs_topology.md) ➔ 理論地墊檢測與 BFS 二層有向演化拓撲演算法。
*   **`32`**：[methodology_32_sovereign_taste_and_critique.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_32_sovereign_taste_and_critique.md) ➔ 主權學者品位裁決（Taste Verdict）與 Claims 剛性 Grounding 防掏空機制。

### 第 4 區：安全對抗與合併阻斷防禦
*   **`41`**：[methodology_41_verdict_lock_and_socratic_grill.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_41_verdict_lock_and_socratic_grill.md) ➔ 紅軍 Socratic 靈魂拷問與合併阻斷鎖（Verdict Lock）剛性斷電防衛。

### 第 5 區：現地對合與實踐校準
*   **`51`**：[methodology_51_physical_friction_and_empirical_evidence.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_51_physical_friction_and_empirical_evidence.md) ➔ 本地實作證據、物理誤差摩擦計量公式與學者聯覺裁決。

### 第 6 區：多人協作與去中心化合流
*   **`61`**：[methodology_61_decentralized_dto_and_rebuild.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_61_decentralized_dto_and_rebuild.md) ➔ 去中心化大腦與純文字 DTO 還原重建流程，解決 Git 二進位衝突。
*   **`62`**：`multi_agent_collaboration_protocol.md` *(規劃中)* ➔ 多人與多代理人協同合流協定。
*   **`63`**：`ci_cd_automated_audit_pipeline.md` *(規劃中)* ➔ 自動化 CI/CD 審計與 PR 阻斷流水線。

### 第 7 區：雙看板指標與自審測試
*   **`71`**：[methodology_71_mci_maturity_metric.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_71_mci_maturity_metric.md) ➔ MCI (手稿成熟度) 剛性加權演算法、幽靈引文與紅軍防投機公式。
*   **`72`**：[methodology_72_mpm_poc_proof_metric.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_72_mpm_poc_proof_metric.md) ➔ MPM (元自證成熟度) 剛性加權演算法、SQLite 檢測與手稿自指校驗。
*   **`73`**：`evaluation_and_benchmark_spec.md` *(規劃中)* ➔ 大腦解構與自審品質基準測試規範。
*   **`74`**：[methodology_74_manuscript_lifecycle_case_study.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_74_manuscript_lifecycle_case_study.md) ➔ `sovereign_research` 手稿誕生之真實實戰生命週期案例。

### 第 8 區：星級 Skills 協同規範
*   **`81`**：[methodology_81_academic_research_navigator_skill.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_81_academic_research_navigator_skill.md) ➔ Navigator (導航員) 技能規格（含 Ingestion 與根系檢索圖）。
*   **`82`**：[methodology_82_academic_advisor_auditor_skill.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_82_academic_advisor_auditor_skill.md) ➔ Auditor (自審審計) 技能規格（含 Verdict Lock 狀態機圖）。
*   **`83`**：[methodology_83_academic_paper_builder_skill.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_83_academic_paper_builder_skill.md) ➔ Builder (建構師) 技能與 11 大 SRCC 命令運作規範（含心流 SOP 圖）。
*   **`84`**：[methodology_84_sovereign_poc_verifier_skill.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_84_sovereign_poc_verifier_skill.md) ➔ Verifier (自證驗證) 技能規格（含 MPM 三維校驗圖）。

### 第 9 區：系統維護、提示詞與工具手冊
*   **`91`**：[methodology_91_brain_cli_manual.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_91_brain_cli_manual.md) ➔ `brain_cli.py` 命令列工具使用手冊與看板範例。
*   **`92`**：`prompt_system_design.md` *(規劃中)* ➔ Agent 提示詞系統架構與 Socratic 拷問範本規格。
