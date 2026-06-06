-- ==============================================================================
-- 🌊 主權大腦 SQLite 常用 SQL 查詢範本 Cheatsheet (brain_queries.sql)
-- 
-- 目的：
-- 提供君王 (wuulong) 一系列在手動分析、學術盲檢或紅軍對抗時，最常使用的 SQL 語句。
-- 這些查詢可以直接複製，並搭配大腦 CLI 的 -s 參數執行：
-- 
-- 執行範例：
--   python3 events/my_research/sovereign-research-methodology/scripts/brain_cli.py -s "[貼上 SQL 語句]"
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 📊 類別 A：資料品質與合規性審計 (Compliance & Ingestion Auditing)
-- ------------------------------------------------------------------------------

-- 1. 查詢所有背景論文的 Ingestion 階段、合規狀態與發表年份
SELECT 
    cite_key, 
    year, 
    json_extract(meta_data, '$.stage') AS ingestion_stage,
    json_extract(meta_data, '$.compliance_status.is_compliant') AS is_compliant,
    json_extract(meta_data, '$.compliance_status.validation_message') AS validation_msg
FROM papers 
ORDER BY year DESC;

-- 2. 統計大腦資料庫目前的 Stage 2 深度消化率與總體合規比例
SELECT 
    COUNT(*) AS total_papers,
    SUM(CASE WHEN json_extract(meta_data, '$.stage') = 'STAGE_2_DEEP' THEN 1 ELSE 0 END) AS stage2_count,
    ROUND(AVG(CASE WHEN json_extract(meta_data, '$.stage') = 'STAGE_2_DEEP' THEN 1.0 ELSE 0.0 END) * 100, 2) AS stage2_percentage,
    SUM(CASE WHEN json_extract(meta_data, '$.compliance_status.is_compliant') = 1 THEN 1 ELSE 0 END) AS compliant_count
FROM papers;

-- 3. 找出所有尚未完成 Stage 2 合規（缺失十大學術因子）的文獻與其缺漏欄位
SELECT 
    cite_key, 
    json_extract(meta_data, '$.stage') AS stage,
    json_extract(meta_data, '$.compliance_status.missing_fields') AS missing_fields
FROM papers 
WHERE json_extract(meta_data, '$.compliance_status.is_compliant') = 0 
   OR json_extract(meta_data, '$.compliance_status.is_compliant') IS NULL;


-- ------------------------------------------------------------------------------
-- 🧠 類別 B：十大學術因子 DTO 深度檢索 (Ten Academic Factors Extraction)
-- ------------------------------------------------------------------------------

-- 4. 提取特定論文 (以 CAG2024RAG 為例) 的核心研究問題與獨特貢獻
SELECT 
    cite_key,
    json_extract(meta_data, '$.paper_extraction.core_question') AS core_question,
    json_extract(meta_data, '$.paper_extraction.unique_contribution') AS unique_contribution,
    json_extract(meta_data, '$.paper_extraction.sovereign_taste_verdict.taste_score') AS taste_score
FROM papers 
WHERE cite_key = 'CAG2024RAG';

-- 5. 通讀所有已消化 Stage 2 論文的主權評判 (Sovereign Taste Verdict) 與判詞
SELECT 
    cite_key, 
    json_extract(meta_data, '$.paper_extraction.sovereign_taste_verdict.taste_score') AS taste_score,
    json_extract(meta_data, '$.paper_extraction.sovereign_taste_verdict.critique') AS critique
FROM papers 
WHERE json_extract(meta_data, '$.stage') = 'STAGE_2_DEEP';


-- ------------------------------------------------------------------------------
-- 🛠️ 類別 C：現地實踐與誤差指標監控 (Empirical Evidences & Friction)
-- ------------------------------------------------------------------------------

-- 6. 盤點物理誤差 (friction_percentage) 超標 (大於 10.0%) 的現地實踐紀錄
SELECT 
    e.evidence_id, 
    p.cite_key, 
    e.friction_percentage, 
    e.practice_scenario,
    e.evidence_time
FROM empirical_evidences e
LEFT JOIN papers p ON e.paper_id = p.paper_id
WHERE e.friction_percentage > 10.0 
ORDER BY e.friction_percentage DESC;


-- ------------------------------------------------------------------------------
-- 🥊 類別 D：紅軍對抗與自審答辯進度 (Red Team Logs & Defense)
-- ------------------------------------------------------------------------------

-- 7. 查詢尚未通過 (verdict != 'PASS') 的紅軍自審脆弱點與拷問明細
--    (可用來定位尚未獲得 Verdict Lock 解鎖的代碼或文字區段)
SELECT 
    log_id, 
    paper_id, 
    manuscript_id, 
    aspect_analyzed, 
    reviewer_attack, 
    verdict,
    test_time
FROM red_team_logs 
WHERE verdict != 'PASS' OR verdict IS NULL;


-- ------------------------------------------------------------------------------
-- 🧬 類別 E：手稿演化鏈與引用對合 (Manuscript Evolution & Citations)
-- ------------------------------------------------------------------------------

-- 8. 查詢特定手稿 (以 ms_journal_haba_2026 為例) 所引用的所有背景文獻及其 BibTeX
SELECT 
    p.cite_key, 
    p.title, 
    mc.citation_context,
    p.bibtex
FROM manuscript_citations mc
LEFT JOIN papers p ON mc.paper_id = p.paper_id
WHERE mc.manuscript_id = 'ms_journal_haba_2026';

-- 9. 追溯所有正在撰寫中 (Writing) 或已發表 (Published) 的手稿與前導手稿的演化繼承鏈
SELECT 
    m1.manuscript_id AS active_manuscript, 
    m1.title AS manuscript_title,
    m1.evolution_stage, 
    m2.manuscript_id AS previous_manuscript,
    m2.title AS previous_title
FROM my_manuscripts m1
LEFT JOIN my_manuscripts m2 ON m1.previous_manuscript_id = m2.manuscript_id;
