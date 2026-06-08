#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 資料庫結構遷移腳本 v1.3 (migration_v1.3.py)
用途：安全更新 SQLite 資料庫，為 papers 表新增 read_depth_level，
      為 red_team_logs 新增 raw_student_defense 與 defense_refinement_delta。
"""

import os
import sqlite3

def run_migration():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    if not os.path.exists(db_path):
        print(f"[!] 找不到大腦資料庫: {db_path}，無法進行遷移。")
        return
        
    print(f"🚀 啟動大腦資料庫結構遷移 v1.3 (資料庫: {db_path})...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;") # 遷移時暫時關閉外鍵
    
    # 1. 檢查並更新 papers 表
    cursor.execute("PRAGMA table_info(papers);")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "read_depth_level" not in columns:
        print("  [+] papers 表缺少 'read_depth_level'，正在新增該欄位...")
        cursor.execute("ALTER TABLE papers ADD COLUMN read_depth_level TEXT DEFAULT 'UNREAD';")
        # 同步初始化已被 Ingest 且為 STAGE_2_DEEP 的論文為 DTO_SUMMARY 或更高
        # 以防舊的已消化文獻全部回退成 0.0 權重
        cursor.execute("""
            UPDATE papers 
            SET read_depth_level = 'DTO_SUMMARY' 
            WHERE json_extract(meta_data, '$.stage') = 'STAGE_2_DEEP';
        """)
        print("  [+] 已將所有 Stage 2 消化文獻初始化為 'DTO_SUMMARY' 狀態。")
    else:
        print("  [=] papers 表的 'read_depth_level' 欄位已存在。")
        
    # 2. 檢查並更新 red_team_logs 表
    cursor.execute("PRAGMA table_info(red_team_logs);")
    rt_columns = [col[1] for col in cursor.fetchall()]
    
    if "raw_student_defense" not in rt_columns:
        print("  [+] red_team_logs 表缺少 'raw_student_defense'，正在新增該欄位...")
        cursor.execute("ALTER TABLE red_team_logs ADD COLUMN raw_student_defense TEXT;")
        # 將現有已通過答辯的日誌，將原始答辯備份為當前 student_defense
        cursor.execute("UPDATE red_team_logs SET raw_student_defense = student_defense WHERE student_defense IS NOT NULL AND student_defense != '';")
    else:
        print("  [=] red_team_logs 表的 'raw_student_defense' 欄位已存在。")
        
    if "defense_refinement_delta" not in rt_columns:
        print("  [+] red_team_logs 表缺少 'defense_refinement_delta'，正在新增該欄位...")
        cursor.execute("ALTER TABLE red_team_logs ADD COLUMN defense_refinement_delta TEXT;")
    else:
        print("  [=] red_team_logs 表的 'defense_refinement_delta' 欄位已存在。")
        
    # 3. 提交變更
    try:
        conn.commit()
        print("\n🎉 資料庫結構遷移 v1.3 成功！所有新欄位已完成部署與初始化。")
    except Exception as e:
        conn.rollback()
        print(f"[!] 遷移失敗，已復原變更: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
