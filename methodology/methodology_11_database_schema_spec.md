# 🧱 methodology_11: SQLite 十一表 Schema 設計與自動合規性審計 (Database Schema & Compliance Specification)

本規格書物理固化了主權大腦的資料庫 Schema 設計哲學，以及各資料表 `meta_data` JSON 欄位的剛性資料契約 (Data Contract)，並定義了自動品質治理之檢核機制。

---

## 🏛️ 1. 十一表設計哲學與痛點解鎖方案

底層 SQLite 資料庫 (`Research_Artifacts.db`) 的欄位與關係設計，是針對傳統學術研究痛點與人機協作失控危機所量身打造的「防禦性架構」：

| 核心痛點 (Pain Point) | 底層資料庫架構解決方案 (Database Architecture Solution) | 具體解鎖機制 (How it solves the problem) |
| :--- | :--- | :--- |
| **1. 認知掏空與 AI 虛無**<br>（AI 代寫、散裝黑話堆砌，研究者喪失思考手感） | **`empirical_evidences` 表**<br>聯動 **`my_manuscripts`表** | **Claims 與 DTO 雙向物理自指合龍**：<br>強制手稿中每一個學術主張 (Claim)，都必須在 `empirical_evidences` 中有對應的「現地實踐真值資料（`evidence_payload` JSON信封）」或已消化文獻，以實體資料強制 Grounding。 |
| **2. 理論地基浮空與引用斷代**<br>（僅看最新結論，對經典奠基理論一無所知，缺乏理論厚度） | **`paper_relations` 表**<br>聯動 **有向 BFS 2-Level 拓撲** | **演化圖譜二層廣度優先檢索**：<br>`paper_relations` 的 `GROUNDED_ON` 關係將平面引用升格為有向演化網絡。利用遞迴 SQL 檢索與 BFS 二層探針，若底層經典文獻未消化或未載入，發動「根系未開發懲罰」，剛性扣減 MCI 評分。 |
| **3. 幽靈引文與未讀先引**<br>（快餐式引用，將未讀文獻直接丟進 References 濫竽充數） | **`papers.meta_data` JSON信封**<br>聯動 **`manuscript_citations`** | **Stage 2 降維解構合規洗滌**：<br>文獻必須先完成 Stage 2 深度解構（降維提取 10 大學術因子，置於 `meta_data`），大腦才認可其為 `'STAGE_2_DEEP'`。`manuscript_citations` 自動核對手稿引用，未過關者觸發「幽靈引文警告」。 |
| **4. 自我認知偏差與投機防巧**<br>（自我審查流於形式，或對一兩篇文獻自審 PASS 虛報進度） | **`red_team_logs` 表**<br>聯動 **合併鎖 (Verdict Lock) 與加權計分** | **Socratic 對抗與 Verdict Lock 剛性阻斷**：<br>紅軍攻擊寫入 `red_team_logs`，狀態為 `VULNERABLE` 時會觸發合併鎖，物理阻斷論文編譯。在 MCI 算法中，紅軍得分採用「自審覆蓋率 60% + PASS率 40%」綜合模型，覆蓋率不足會受到強力制約。 |
| **5. 跨電腦移植性差與路徑衝突**<br>（不同成員電腦環境絕對路徑不同，導致資料庫外鍵斷線與無法執行） | **`directory_roots` 表**<br>聯動 **`paper_urls` 表** | **抽象 Root Key 與相對路徑解耦設計**：<br>`directory_roots` 隔離各電腦的實體絕對路徑，提供 `root_key`。`paper_urls` 僅儲存 `root_key` 與相對路徑。移機時僅需修改一處絕對路徑即可全庫復活，實現永續傳承。 |
| **6. 多人協作與 Git 資料庫衝突**<br>（SQLite 二進位檔案在多人提交 Git 時必然發生無法 merge 的衝突） | **純文字 DTO 封裝**<br>（如 `contribution.json`） | **二進位解耦與跳躍式知識遺傳**：<br>不直接在 Git 提交二進位 `.db` 檔，而是由匯出指令導出為純文字 DTO JSON。協作者拉取後一鍵 rebuild 重建本地資料庫，完美避開 Git 二進位衝突。 |

---

## 📊 2. SQLite 十一表實體關係圖 (ER Diagram)

以下為主權大腦資料庫 `Research_Artifacts.db` 的完整實體關係圖，呈現核心專案主題、文獻探勘、實踐舉證、紅軍對抗與手稿編譯之間的強耦合關聯：

```mermaid
erDiagram
    PROJECTS ||--o{ TOPICS : "contains"
    TOPICS ||--o{ PAPERS : "organizes"
    TOPICS ||--o{ MY_MANUSCRIPTS : "drives"
    TOPICS ||--o{ TOPIC_GRAVITY_OVERRIDES : "overrides"
    EXPLORATION_TASKS ||--o{ PAPERS : "collects"
    DIRECTORY_ROOTS ||--o{ PAPER_URLS : "mounts"
    
    PAPERS ||--o{ PAPER_RELATIONS : "references as source"
    PAPERS ||--o{ PAPER_RELATIONS : "referenced as target"
    PAPERS ||--o{ PAPER_URLS : "resolves to"
    PAPERS ||--o{ PAPER_TAGS : "tagged with"
    PAPERS ||--o{ EMPIRICAL_EVIDENCES : "proves"
    PAPERS ||--o{ RED_TEAM_LOGS : "attacks"
    
    MY_MANUSCRIPTS ||--o{ RED_TEAM_LOGS : "critiques"
    MY_MANUSCRIPTS ||--o{ MY_MANUSCRIPTS : "inherits from"
    MY_MANUSCRIPTS ||--o{ MANUSCRIPT_CITATIONS : "cites"
    PAPERS ||--o{ MANUSCRIPT_CITATIONS : "cited by"

    PROJECTS {
        string project_id PK
        string project_name
        string description
        string search_spec "JSON"
        string architecture_spec "JSON"
        timestamp created_time
        string meta_data "JSON"
    }
    TOPICS {
        string topic_id PK
        string project_id FK
        string topic_name
        int sequence_order
        string focus_spec "JSON"
        string status
        string meta_data "JSON"
    }
    EXPLORATION_TASKS {
        string task_id PK
        string query
        timestamp run_time
        string status
        int papers_found
        string agent_version
        string error_log
        string meta_data "JSON"
    }
    DIRECTORY_ROOTS {
        string root_key PK
        string owner_name
        string absolute_path
        string meta_data "JSON"
    }
    PAPERS {
        string paper_id PK
        string task_id FK
        string topic_id FK
        string title
        string authors
        int year
        string core_method
        string cite_key "Unique"
        string bibtex
        string meta_data "JSON"
    }
    PAPER_RELATIONS {
        string relation_id PK
        string source_paper_id FK
        string target_paper_id FK
        string relation_type "IMPROVES | REFUTES | GROUNDED_ON"
        string description
    }
    PAPER_URLS {
        string url_id PK
        string paper_id FK
        string root_key FK
        string url_link
        string url_type
        string download_status
        int file_size_bytes
        string meta_data "JSON"
    }
    PAPER_TAGS {
        string paper_id PK
        string tag_name PK
        string meta_data "JSON"
    }
    TOPIC_GRAVITY_OVERRIDES {
        string topic_id PK
        string entity_name PK
        string entity_type PK
        real bias_score
        string description
    }
    EMPIRICAL_EVIDENCES {
        string evidence_id PK
        string paper_id FK
        string practice_scenario "JSON"
        string evidence_payload "JSON"
        real friction_percentage
        string artifact_visual_path
        timestamp evidence_time
        string meta_data "JSON"
    }
    RED_TEAM_LOGS {
        string log_id PK
        string paper_id FK
        string manuscript_id FK
        string aspect_analyzed
        string reviewer_attack
        string student_defense
        string verdict "PASS | VULNERABLE | CRITICAL_BUG"
        timestamp test_time
        string meta_data "JSON"
    }
    MY_MANUSCRIPTS {
        string manuscript_id PK
        string topic_id FK
        string title
        string cite_key "Unique"
        string manuscript_type "Conference | Journal | Thesis"
        string evolution_stage "Planning | Writing | Under_Review | Published"
        string previous_manuscript_id FK
        string meta_data "JSON"
    }
    MANUSCRIPT_CITATIONS {
        string manuscript_id PK
        string paper_id PK
        string citation_context
        string meta_data "JSON"
    }
}

---

## 🧪 3. 全庫大一統 JSON 規格書 (Metadata Schema Spec v2.1)

此設計引進了**「全域合規性檢核信封 (compliance_status)」**，用於動態記錄資料庫每筆詮釋資料的品質合規狀態、缺失欄位與審計軌跡，實體化「大腦自主品質治理」。

### 3.1 全域必填：合規性檢核信封 (compliance_status)
為防止資料規格隨時間退化，**所有資料表** 的 `meta_data` JSON 根節點下，**[必須]** 包含一個固定的 `compliance_status` 物件，由大腦審計工具 `audit_brain_compliance.py` 自動定期掃描更新：

```json
"compliance_status": {
  "is_compliant": "Boolean",          // true (完全合規) 或 false (未合規/欄位缺失)
  "checked_at": "Timestamp",           // 本次品質檢核的時間戳記 (ISO 8601 格式)
  "missing_fields": ["String"],        // 缺失的必填 key 完整路徑清單
  "validation_message": "String"       // 合規性審計說明
}
```

---

## 🧱 4. 各資料表 JSON 剛性結構合集

### 📌 papers (背景文獻主表 - meta_data)
```json
{
  "compliance_status": {
    "is_compliant": false,
    "checked_at": "2026-05-26T18:42:00Z",
    "missing_fields": ["paper_extraction.core_question"],
    "validation_message": "Stage 2 details missing"
  },
  "stage": "String",                  // 'STAGE_1_PRELIMINARY' 或 'STAGE_2_DEEP'
  "preliminary_relevance": "String",  // Stage 1 初步價值猜想說明
  "academic_prestige": {              // 【學術重力與載體含金量】
    "citation_count": "Integer",      // 被引用次數
    "venue_name": "String",           // 期刊/會議完整官方名稱
    "venue_tier": "String",           // 'Top_Journal' | 'Core_Venue' | 'Arxiv_Preprint' | 'Ordinary_Venue'
    "venue_bias_applied": "Real",     // 本地主題特異性偏置加分
    "institution_name": "String",     // 第一作者所屬研究機構名稱
    "institution_tier": "String",     // 'Tier_1_Elite' | 'Tier_2_Core' | 'Tier_3_Ordinary'
    "institution_bias_applied": "Real",// 本地主題機構偏置加分
    "academic_gravity_score": "Real", // 計算出之學術重力最終分數 (Ga)
    "hydration_source": "String"      // 資料灌溉來源
  },
  "paper_extraction": {               // 【標準論文降維萃取 DTO】
    "core_question": "String",        // 論文試圖解決的具體痛點與背景問題
    "core_methodology": "String",     // 論文採用的具體方法、模型或架構
    "key_insights": ["String"],       // 2-3 個最具物理硬度與辯證價值的關鍵主張列表
    "unique_contribution": "String",  // 核心突破與 Novelty 判定
    "empirical_setup": "String",      // 實踐或實驗的物理情境、資料集與硬體配置
    "key_results": "String",          // 論文的定量成果與 Baseline 對比數值
    "limitations_outlook": "String",  // 適用邊界與未來改善方向
    "key_references_to_suck": [       // 對其具備基石地位的參考文獻
      {
        "cite_key": "String",
        "reason": "String"
      }
    ],
    "sovereign_taste_verdict": {      // 【學者批判性品位裁決】
      "critique": "String",           // 與本地實踐現地真值對比批判的 Verdict
      "taste_score": "Real"           // 研究者主觀定錨評分 (0.0 至 10.0)
    }
  }
}
```

### 📌 empirical_evidences (現地實踐與實體舉證表 - meta_data)
```json
{
  "compliance_status": {
    "is_compliant": true,
    "checked_at": "2026-05-26T18:42:00Z",
    "missing_fields": [],
    "validation_message": "All fields valid"
  },
  "host_name": "String",              // 實踐測試的主機名稱
  "author_name": "String",            // 實作者/驗證者姓名
  "execution_duration_sec": "Real",   // 實測執行或模擬耗時 (秒)
  "calibration_status": "String",     // 校準狀態：'CALIBRATED' | 'UNCALIBRATED'
  "environment_conditions": {         // 實作環境參數
    "network_latency_ms": "Real",
    "allowed_friction_threshold": "Real"
  }
}
```

### 📌 red_team_logs (紅軍自審與品位裁決日誌表 - meta_data)
```json
{
  "compliance_status": {
    "is_compliant": true,
    "checked_at": "2026-05-26T18:42:00Z",
    "missing_fields": [],
    "validation_message": "All fields valid"
  },
  "judge_model": "String",            // 評審模型
  "prompt_tokens": "Integer",
  "completion_tokens": "Integer",
  "temperature": "Real",
  "audit_signature": "String"
}
```

### 📌 my_manuscripts (主權手稿表 - meta_data)
```json
{
  "compliance_status": {
    "is_compliant": true,
    "checked_at": "2026-05-26T18:42:00Z",
    "missing_fields": [],
    "validation_message": "All fields valid"
  },
  "overleaf_url": "String",           // Overleaf 專案網址
  "git_commit_hash": "String",        // 對應之本地 git commit hash
  "target_journal": "String",         // 目標發表載體
  "words_count": "Integer"            // 草稿實體字數
}
```

---

## 📈 5. 資料品質約束與自動化審計

*   **自動化審計打標**：透過呼叫 `scripts/audit_brain_compliance.py` 自動掃描大腦，比對每筆 `meta_data` JSON 的 Key。若缺少必填 Key，將 `is_compliant` 標記為 `false` / `true`，並在 `missing_fields` 中記錄缺失的 Key 路徑。
*   **一鍵 SQL 盲檢合規率**：
    ```sql
    SELECT 
      COUNT(*) as total,
      SUM(CASE WHEN json_extract(meta_data, '$.compliance_status.is_compliant') = 1 THEN 1 ELSE 0 END) as compliant_count,
      ROUND(AVG(CASE WHEN json_extract(meta_data, '$.compliance_status.is_compliant') = 1 THEN 1.0 ELSE 0.0 END) * 100, 2) as compliance_rate_pct
    FROM papers;
    ```
