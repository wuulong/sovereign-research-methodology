#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 全庫大一統資料品質合規性審計與打標工具 (audit_brain_compliance.py)

目的：
1. 實作 metadata_schema_spec.md v2.1 規範。
2. 自動掃描 papers、empirical_evidences、red_team_logs、exploration_tasks、my_manuscripts 的 meta_data。
3. 依據剛性契約進行 Key 完整性檢驗，動態打標更新 compliance_status 信封回寫資料庫。
4. 提供一鍵盲檢資料合規品質之實體化工具。
"""

import os
import sys
import json
import sqlite3
from datetime import datetime

# 剛性必填 Key 規範對照表
REQUIRED_KEYS_REGISTRY = {
    "papers": {
        "basic": [
            "stage", 
            "preliminary_relevance", 
            "academic_prestige",
            "academic_prestige.citation_count",
            "academic_prestige.venue_name",
            "academic_prestige.venue_tier",
            "academic_prestige.academic_gravity_score"
        ],
        "stage_2": [
            "paper_extraction",
            "paper_extraction.core_question",
            "paper_extraction.core_methodology",
            "paper_extraction.key_insights",
            "paper_extraction.unique_contribution",
            "paper_extraction.empirical_setup",
            "paper_extraction.key_results",
            "paper_extraction.limitations_outlook",
            "paper_extraction.key_references_to_suck",
            "paper_extraction.sovereign_taste_verdict",
            "paper_extraction.sovereign_taste_verdict.critique",
            "paper_extraction.sovereign_taste_verdict.taste_score"
        ]
    },
    "empirical_evidences": [
        "host_name", "author_name", "execution_duration_sec", "calibration_status", "environment_conditions"
    ],
    "red_team_logs": [
        "judge_model", "prompt_tokens", "completion_tokens", "temperature", "audit_signature"
    ],
    "exploration_tasks": [
        "host_os", "cli_flags", "api_endpoint", "search_statistics"
    ],
    "my_manuscripts": [
        "overleaf_url", "git_commit_hash", "target_journal", "words_count"
    ]
}

def get_nested_value(d, key_path):
    """
    透過點點路徑（如 'academic_prestige.citation_count'）取得 nested dict 中的值
    """
    parts = key_path.split('.')
    current = d
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current

def audit_json(meta_dict, table_name):
    """
    針對特定資料表，比對 JSON 內容並返回 (is_compliant, missing_fields, msg)
    """
    if not isinstance(meta_dict, dict):
        return False, ["ROOT_IS_NOT_JSON_OBJECT"], "Metadata root must be a valid JSON object"
        
    missing = []
    
    if table_name == "papers":
        # 1. 檢查基本欄位
        for key in REQUIRED_KEYS_REGISTRY["papers"]["basic"]:
            val = get_nested_value(meta_dict, key)
            if val is None:
                missing.append(key)
                
        # 2. 檢查 Stage 2 深度欄位 (如果 stage 標記為 STAGE_2_DEEP)
        stage = meta_dict.get("stage", "STAGE_1_PRELIMINARY")
        if stage == "STAGE_2_DEEP":
            for key in REQUIRED_KEYS_REGISTRY["papers"]["stage_2"]:
                val = get_nested_value(meta_dict, key)
                if val is None:
                    missing.append(key)
        else:
            # 即使 stage 為 Stage 1，但如果缺少 stage 2 欄位，我們在 overall_compliance 上也記為 incomplete
            # 但給予合理的 validation message
            for key in REQUIRED_KEYS_REGISTRY["papers"]["stage_2"]:
                val = get_nested_value(meta_dict, key)
                if val is None:
                    missing.append(key)
                    
        is_compliant = (len(missing) == 0)
        msg = "All fields valid" if is_compliant else f"Missing {len(missing)} fields (Stage: {stage})"
        return is_compliant, missing, msg
        
    else:
        # 其他表格的比對
        required_list = REQUIRED_KEYS_REGISTRY.get(table_name, [])
        for key in required_list:
            val = get_nested_value(meta_dict, key)
            if val is None:
                missing.append(key)
                
        is_compliant = (len(missing) == 0)
        msg = "All fields valid" if is_compliant else f"Missing {len(missing)} fields"
        return is_compliant, missing, msg

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    if not os.path.exists(db_path):
        print(f"[!] 大腦資料庫不存在: {db_path}")
        sys.exit(1)
        
    print(f"🕵️‍♂️ 啟動《個人AI賦能大腦》全庫大一統資料品質合規審計...")
    print(f"[*] 連線資料庫中: {db_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tables_to_audit = [
        ("papers", "paper_id", "SELECT paper_id, title, meta_data FROM papers;"),
        ("empirical_evidences", "evidence_id", "SELECT evidence_id, practice_scenario, meta_data FROM empirical_evidences;"),
        ("red_team_logs", "log_id", "SELECT log_id, aspect_analyzed, meta_data FROM red_team_logs;"),
        ("exploration_tasks", "task_id", "SELECT task_id, query, meta_data FROM exploration_tasks;"),
        ("my_manuscripts", "manuscript_id", "SELECT manuscript_id, title, meta_data FROM my_manuscripts;")
    ]
    
    now_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    global_stats = {}
    
    for table_name, pk_col, query in tables_to_audit:
        print(f"📌 正在掃描資料表: {table_name}...")
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as e:
            print(f"  [!] 無法讀取資料表 {table_name}: {e} (跳過)")
            continue
            
        total = len(rows)
        compliant_count = 0
        
        for row in rows:
            pk_val, label, meta_str = row
            
            # 解析 meta_data JSON
            meta = {}
            if meta_str:
                try:
                    meta = json.loads(meta_str)
                except:
                    # JSON 語法損毀，建立一個空的 dict
                    meta = {}
            else:
                meta = {}
                
            # 執行合規比對
            is_compliant, missing, msg = audit_json(meta, table_name)
            
            # 建立/更新 compliance_status
            meta["compliance_status"] = {
                "is_compliant": is_compliant,
                "checked_at": now_str,
                "missing_fields": missing,
                "validation_message": msg
            }
            
            if is_compliant:
                compliant_count += 1
                
            # 回寫寫入資料庫
            try:
                cursor.execute(f"""
                    UPDATE {table_name} 
                    SET meta_data = ? 
                    WHERE {pk_col} = ?;
                """, (json.dumps(meta, ensure_ascii=False), pk_val))
            except Exception as e:
                print(f"    [!] 更新 {pk_val} 失敗: {e}")
                
        # 統計
        rate = (compliant_count / total * 100) if total > 0 else 100.0
        global_stats[table_name] = {
            "total": total,
            "compliant": compliant_count,
            "rate": rate
        }
        print(f"  ➔ 統計: 總筆數 {total} | 合規數 {compliant_count} | 🎯 資料品質合規率: {rate:.2f}%\n")
        
    try:
        conn.commit()
        print("=" * 80)
        print("🎉 物理品質審計完畢！大腦合規性標記 compliance_status 已全庫打標就位！")
        print("📊 大腦各分區品質合規看板：")
        for tbl, stats in global_stats.items():
            print(f"  - {tbl:22s}: 合規率 {stats['rate']:6.2f}% ({stats['compliant']}/{stats['total']})")
        print("=" * 80)
    except Exception as e:
        conn.rollback()
        print(f"[!] 提交品質審計失敗: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
