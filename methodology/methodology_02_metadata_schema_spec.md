# 《個人AI賦能》主權大腦全庫大一統 JSON 規格書 (Sovereign Database Metadata Spec v2.1)

本規格書物理固化了主權研究大腦在整個 SQLite 資料庫（11張實體資料表）中，所有帶有 `meta_data` JSON 欄位的剛性資料契約 (Data Contract)。
本版本 (v2.1) 正式引進**「全域合規性檢核信封 (compliance_status)」**，用於動態記錄資料庫每筆詮釋資料的品質合規狀態、缺失欄位與審計軌跡，實體化「大腦自主品質治理」。

---

## 1. 帶有 meta_data 欄位之核心資料表盤點

在大腦十一表 Schema 中，以下核心資料表均掛載了 `meta_data` JSON 信封，用於隔離「剛性 SQL 外鍵與索引骨架」與「彈性肌肉詮釋資料」：

```
                              ┌──────────────────┐
                              │  projects.meta   │
                              └────────┬─────────┘
                                       │ (1對多)
                              ┌────────▼─────────┐
                              │   topics.meta    │
                              └────────┬─────────┘
                                       │ (1對多)
     ┌──────────────────┐     ┌────────▼─────────┐     ┌──────────────────┐
     │  exp_tasks.meta  ├────►│   papers.meta    │◄────┤  paper_urls.meta  │
     └──────────────────┘     └────────┬─────────┘     └──────────────────┘
                                       │ (1對多)
                              ┌────────┼─────────┐
                              │        │         │
                     ┌────────▼────────┐ ┌───────▼────────┐
                     │ empirical.meta  │ │ red_team.meta  │
                     └─────────────────┘ └────────────────┘
```

---

## 2. 全域必填：合規性檢核信封 (compliance_status)

為防止資料規格隨時間退化或與規格書脫節，**所有資料表** 的 `meta_data` JSON 根節點下，**[必須]** 包含一個固定的 `compliance_status` 物件。
此物件由大腦審計工具 `audit_brain_compliance.py` 自動定期掃描、檢核並動態打標更新：

```json
"compliance_status": {
  "is_compliant": "Boolean",          // true (完全合規) 或 false (未合規/欄位缺失)
  "checked_at": "Timestamp",           // 本次品質檢核的時間戳記 (ISO 8601 格式)
  "missing_fields": ["String"],        // 缺失的必填 key 完整路徑清單 (例如 ["paper_extraction.core_question"])
  "validation_message": "String"       // 合規性審計說明 (例如 "Missing Stage 2 Deep Extraction Details")
}
```

---

## 3. 各資料表 JSON 剛性結構合集

不論是 AI 探勘工具、紅軍自審審查器，或是人類學者，在寫入以下各資料表的 `meta_data` 時，必須 100% 遵守對應的剛性結構（嚴禁任何 key 的拼寫變形）：

### 📌 3.1 papers (背景文獻主表 - meta_data)
*   **用途**：記錄文獻的降維解構 DTO 與學術重力計量細節。
*   **JSON 剛性結構**：
```json
{
  "compliance_status": {              // 【全域合規信封】(自動審計打標)
    "is_compliant": false,
    "checked_at": "2026-05-26T18:42:00Z",
    "missing_fields": ["paper_extraction.core_question"],
    "validation_message": "Stage 2 details missing"
  },
  "stage": "String",                  // 'STAGE_1_PRELIMINARY' 或 'STAGE_2_DEEP'
  "preliminary_relevance": "String",  // Stage 1 初步價值猜想說明
  "academic_prestige": {              // 【學術重力與載體含金量計量】
    "citation_count": "Integer",      // 實時/高擬真被引用次數
    "venue_name": "String",           // 期刊/會議完整官方名稱
    "venue_tier": "String",           // 'Top_Journal' | 'Core_Venue' | 'Arxiv_Preprint' | 'Ordinary_Venue'
    "venue_bias_applied": "Real",     // 本地主題特異性偏置加分 (如 +3.0)
    "institution_name": "String",     // 第一作者所屬研究機構名稱
    "institution_tier": "String",     // 'Tier_1_Elite' | 'Tier_2_Core' | 'Tier_3_Ordinary'
    "institution_bias_applied": "Real",// 本地主題機構特異性偏置加分 (如 +1.5)
    "academic_gravity_score": "Real", // 計算出之學術重力最終分數 (Ga)
    "hydration_source": "String"      // 資料灌溉來源：'semantic_scholar_api' 或 'heuristic_fallback'
  },
  "paper_extraction": {               // 【標準論文降維萃取 DTO】(Stage 2 強制必填，若 stage = 'STAGE_1_PRELIMINARY' 則可先不填，但 is_compliant 將為 false)
    "core_question": "String",        // 論文試圖解決的具體痛點與背景問題
    "core_methodology": "String",     // 論文採用的具體方法、模型或物理/軟體架構
    "key_insights": ["String"],       // 2-3 個最具物理硬度與辯證價值的關鍵主張列表
    "unique_contribution": "String",  // 相比前人，這篇論文最核心、唯一的原創突破與 Novelty 判定
    "empirical_setup": "String",      // 實踐或實驗的物理情境、資料集、模擬工具與硬體配置
    "key_results": "String",          // 論文的定量成果與 Baseline 對比數值表現
    "limitations_outlook": "String",  // 論文自身承認的局限性、適用邊界與未來改善方向
    "key_references_to_suck": [       // 這篇論文中，對其具備基石/靈魂地位的參考文獻
      {
        "cite_key": "String",
        "reason": "String"
      }
    ],
    "sovereign_taste_verdict": {      // 【防掏空防線：主權學者批判性品位裁決】
      "critique": "String",           // 將他者文獻與我們本地實踐現地真值對比批判的 Verdict 防禦答辯
      "taste_score": "Real"           // 研究者給予該論文的學術品位主觀定錨評分 (0.0 至 10.0)
    }
  }
}
```

---

### 📌 3.2 empirical_evidences (肉身實踐與實體舉證表 - meta_data)
*   **用途**：記錄實作舉證時的系統環境、執行效率與物理摩擦力。
*   **JSON 剛性結構**：
```json
{
  "compliance_status": {              // 【全域合規信封】
    "is_compliant": true,
    "checked_at": "2026-05-26T18:42:00Z",
    "missing_fields": [],
    "validation_message": "All fields valid"
  },
  "host_name": "String",              // 實踐測試的主機名稱 (例如 'Habars_Mac Studio')
  "author_name": "String",            // 實作者/驗證者姓名 (例如 'wuulong')
  "execution_duration_sec": "Real",   // 實測執行或模擬耗時 (秒)
  "calibration_status": "String",     // 校準狀態：'CALIBRATED' (已校準) | 'UNCALIBRATED' (未校準)
  "environment_conditions": {         // 實作時的物理或網路環境
    "network_latency_ms": "Real",     // 實測網路延遲
    "allowed_friction_threshold": "Real" // 物理守恆所允許的誤差臨界值
  }
}
```

---

### 📌 3.3 red_team_logs (紅軍自審與品位裁決日誌表 - meta_data)
*   **用途**：記錄紅軍自審時所使用的 LLM 評審模型與消耗之 Token 資源。
*   **JSON 剛性結構**：
```json
{
  "compliance_status": {              // 【全域合規信封】
    "is_compliant": true,
    "checked_at": "2026-05-26T18:42:00Z",
    "missing_fields": [],
    "validation_message": "All fields valid"
  },
  "judge_model": "String",            // 扮演紅軍的 LLM 評審模型名稱 (如 'Gemini_1.5_Pro')
  "prompt_tokens": "Integer",         // 消耗的 Input Token 數
  "completion_tokens": "Integer",     // 消耗的 Output Token 數
  "temperature": "Real",              // 執行的 LLM 溫度參數
  "audit_signature": "String"         // AI 代理人或學術安全簽章
}
```

---

### 📌 3.4 exploration_tasks (探勘與採集任務日誌表 - meta_data)
*   **用途**：追溯外部資料進入資料庫的「數位基因與血統（Data Lineage）」。
*   **JSON 剛性結構**：
```json
{
  "compliance_status": {              // 【全域合規信封】
    "is_compliant": true,
    "checked_at": "2026-05-26T18:42:00Z",
    "missing_fields": [],
    "validation_message": "All fields valid"
  },
  "host_os": "String",                // 執行此任務的系統環境 (如 'macOS 15.4')
  "cli_flags": ["String"],            // 執行探勘時帶入的參數清單 (如 ["--ingest", "--limit=10"])
  "api_endpoint": "String",           // 使用的搜尋 API 端點
  "search_statistics": {              // 探勘統計
    "total_results_found": "Integer", // 線上符合查詢的總筆數
    "api_response_time_ms": "Integer" // API 回傳耗時
  }
}
```

---

### 📌 3.5 my_manuscripts (主權手稿表 - meta_data)
*   **用途**：記錄研究生自我創造論文手稿的版本控制與寫作平台關聯。
*   **JSON 剛性結構**：
```json
{
  "compliance_status": {              // 【全域合規信封】
    "is_compliant": true,
    "checked_at": "2026-05-26T18:42:00Z",
    "missing_fields": [],
    "validation_message": "All fields valid"
  },
  "overleaf_url": "String",           // 關聯的 Overleaf 線上協同寫作專案網址
  "git_commit_hash": "String",        // 當前寫作版本所對應的本地 Git commit hash
  "target_journal": "String",         // 預計發表的目標期刊或學術會議名稱
  "words_count": "Integer"            // 目前草稿的實體總字數
}
```

---

## 4. 資料品質約束與自動化審計 (Data Quality & Audit Rules)

*   **自動化審計與打標**：
    *   透過呼叫 `audit_brain_compliance.py` 自動掃描大腦，比對每筆 meta_data JSON 的 Key。
    *   若缺少必填 Key，腳本會將 `is_compliant` 標記為 `false`，並在 `missing_fields` 中記錄缺失的 Key 路徑，最後回寫回資料庫。
*   **一鍵 SQL 盲檢合規率**：
    *   導師可使用 SQLite 一鍵查詢大腦目前的資料品質合規率：
        ```sql
        SELECT 
          COUNT(*) as total,
          SUM(CASE WHEN json_extract(meta_data, '$.compliance_status.is_compliant') = 1 THEN 1 ELSE 0 END) as compliant_count,
          ROUND(AVG(CASE WHEN json_extract(meta_data, '$.compliance_status.is_compliant') = 1 THEN 1.0 ELSE 0.0 END) * 100, 2) as compliance_rate_pct
        FROM papers;
        ```
