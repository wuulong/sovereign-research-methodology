# 📐 主權科研方法論規格說明書清單 (Methodology Specifications List)

本目錄存放了主權科研大腦（Sovereign Research Brain）的系統需求規格書、元資料 schema 設計規範、關係本體定義檔以及核心 Skills 指南。

為了提升系統工程架構的模組化與高內聚性，本規格目錄採用「**每區預算 10 碼，區間跳跃式分區**」進行二位數編號。

---

## 📂 10 大分區與 18 大方法論規格檔矩陣 (The 18 Specs Matrix)

### 📌 第 0 分區：系統需求與架構導覽 (Portal)
- **`01` [requirements](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_01_requirements.md)**
  - *Why it exists*: 明確宣示主權大腦的設計目標，界定「思維主權邊界」與「防範認知空洞化」的頂層需求。
- **`02` [architecture_navigator](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_02_system_architecture_navigator.md)**
  - *Why it exists*: **【總入口導覽頁】** 系統四星運作拓撲總圖、10 大分區編號規範與跳轉矩陣。

### 🧱 第 1 分區：底層資料庫與中繼資料規格 (Database Specs)
- **`11` [database_schema_spec](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_11_database_schema_spec.md)**
  - *Why it exists*: 定義 SQLite 十一表 Schema 設計與 `meta_data` JSON 的剛性欄位約束。
- **`12` [relation_ontology_spec](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_12_relation_ontology_spec.md)**
  - *Why it exists*: 定義 `paper_relations` 的 8 大關係本體（`GROUNDED_ON`, `REFUTES` 等）與關係 DTO 格式。

### 🧱 第 2 分區：文獻引渡與 Stage 2 消化加工 (Ingestion)
- **`21` [three_tier_federated_brain](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_21_three_tier_federated_brain.md)**
  - *Why it exists*: 定義三層聯邦大腦（Layer 0 緩衝、Layer 1 靠泊、Layer 2 深消化）的架構與隔離邊界。
- **`22` [academic_gravity_and_digesting](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_22_academic_gravity_and_digesting.md)**
  - *Why it exists*: 規範學術重力場公式 $G_a$、精讀優先級與 Stage 2 十大學術因子降維解構工序。

### 🧱 第 3 分區：理論演化與學者品位裁決 (Topology & Taste)
- **`31` [theory_grounding_and_bfs_topology](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_31_theory_grounding_and_bfs_topology.md)**
  - *Why it exists*: 規範理論地墊檢測與 BFS 二層有向演化拓撲演算法之判定規則。
- **`32` [sovereign_taste_and_critique](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_32_sovereign_taste_and_critique.md)**
  - *Why it exists*: 定義學者品位裁決（Taste Verdict）信封欄位與防止 AI 代寫掏空思考之剛性 Grounding。

### 🧱 第 4 分區：安全對抗與合併阻斷防禦 (Security & Lock)
- **`41` [verdict_lock_and_socratic_grill](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_41_verdict_lock_and_socratic_grill.md)**
  - *Why it exists*: 定義紅軍 Socratic grill 拷問、`red_team_logs` 與合併阻斷鎖（Verdict Lock）剛性阻斷編譯發表。

### 🧱 第 5 分區：現地對合與實踐校準 (Calibration)
- **`51` [physical_friction_and_empirical_evidence](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_51_physical_friction_and_empirical_evidence.md)**
  - *Why it exists*: 規範 `empirical_evidences` 本地實踐對合、物理誤差摩擦計量公式與學者聯覺裁決。

### 🧱 第 6 分區：多人協作與去中心化合流 (Collaboration)
- **`61` [decentralized_dto_and_rebuild](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_61_decentralized_dto_and_rebuild.md)**
  - *Why it exists*: 規範純文字 DTO 還原與冷啟動一鍵重建流程，免除 Git 二進位衝突。
- `62` `multi_agent_collaboration_protocol.md` (規劃中) ➔ 多人與多 Agent 協同合流協定。
- `63` `ci_cd_automated_audit_pipeline.md` (規劃中) ➔ 自動化 CI 審計流水線。

### 🧱 第 7 分區：雙看板指標與自審測試 (Metrics & Benchmark)
- **`71` [mci_maturity_metric](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_71_mci_maturity_metric.md)**
  - *Why it exists*: 定義手稿成熟與可信度看板 MCI 剛性演算法、幽靈引文與紅軍防投機公式。
- **`72` [mpm_poc_proof_metric](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_72_mpm_poc_proof_metric.md)**
  - *Why it exists*: 定義元自證看板 MPM 剛性加權演算法（SQLite完整性、工具可用性、自指 Checksum）。
- `73` `evaluation_and_benchmark_spec.md` (規劃中) ➔ 大腦解構與自審品質基準測試規範。
- **`74` [manuscript_lifecycle_case_study](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_74_manuscript_lifecycle_case_study.md)**
  - *Why it exists*: 以真實手稿 `sovereign_research` 寫作生命週期為例之實戰心流案例。

### ⚡ 第 8 分區：星級 Skills 協同規範 (Agentic Skills)
- **`81` [academic_research_navigator_skill](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_81_academic_research_navigator_skill.md)**
  - *Why it exists*: Navigator 技能指南（包含重力場 Ingestion 流水線圖與根系 BFS 檢索圖）。
- **`82` [academic_advisor_auditor_skill](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_82_academic_advisor_auditor_skill.md)**
  - *Why it exists*: Auditor 技能指南（包含 Verdict Lock 斷電與答辯解鎖狀態機圖）。
- **`83` [academic_paper_builder_skill](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_83_academic_paper_builder_skill.md)**
  - *Why it exists*: Builder 技能指南與 11 大 SRCC 心流命令剛性規格（含心流 SOP 圖，重命名自 `03`）。
- **`84` [sovereign_poc_verifier_skill](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_84_sovereign_poc_verifier_skill.md)**
  - *Why it exists*: Verifier 技能指南（含 MPM 三維自證校驗架構圖）。

### ⚡ 第 9 分區：系統維護、提示詞與工具手冊 (System Operations)
- **`91` [brain_cli_manual](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/methodology/methodology_91_brain_cli_manual.md)**
  - *Why it exists*: `brain_cli.py` 命令列工具使用手冊、看板查詢與 verbose 十大因子展開實戰（重命名自 `04`）。
- `92` `prompt_system_design.md` (規劃中) ➔ Agent 提示詞系統架構與 Socratic 拷問範本規格。

---

## 🪐 線上 GitHub 連結
本方法論的所有系統需求與 DDL 設計均已開源。您可以直接在 GitHub 上點閱 [Sovereign Research Methodology Specifications](https://github.com/wuulong/sovereign-research-methodology/tree/main/methodology)，繼承這套代表學術主權的最硬核系統美學設計。
