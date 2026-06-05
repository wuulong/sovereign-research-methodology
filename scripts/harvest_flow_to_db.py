#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 師徒自審 Feedback 考古自動落庫工具 (harvest_flow_to_db.py)

目的：
會後自動讀取哈爸自己扮演「哈教授」所進行的紅軍自審日誌 (.md)，
解析 [Audit::Aspect] 與 [Attack::ProfessorHaba] 標籤，
自動將哈教授的學術質疑落庫為 SQLite 的 `red_team_logs`，並強制 Verdict 預設為 'VULNERABLE'。
"""

import os
import sys
import re
import sqlite3
import argparse
import json
from datetime import datetime

def harvest_meeting_feedback(db_path, meeting_path):
    if not os.path.exists(meeting_path):
        print(f"[-] 錯誤：找不到會議記錄檔案：{meeting_path}")
        return
        
    print(f"[*] 正在解析思考日誌：{meeting_path}")
    with open(meeting_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 使用正則表達式尋找 [Audit::Aspect] 區塊
    # 格式：
    # [Audit::Aspect] 標題 (關聯ID)
    # [Attack::ProfessorHaba] 質疑內容...
    pattern = r"\[Audit::Aspect\]\s*(.*?)\s*\((.*?)\)\s*\n\s*\[Attack::ProfessorHaba\]\s*(.*)"
    matches = re.findall(pattern, content)
    
    if not matches:
        print("[!] 提示：未在日誌中發現符合 [Audit::Aspect] 與 [Attack::ProfessorHaba] 結構的 Feedback。")
        return
        
    print(f"[+] 偵測到 {len(matches)} 筆哈教授自審 Feedback。正在進行主權落庫...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    inserted_count = 0
    for aspect, ref_id, attack in matches:
        aspect = aspect.strip()
        ref_id = ref_id.strip()
        attack = attack.strip()
        
        # 判定 ref_id 是 paper_id 還是 manuscript_id
        paper_id = "zotero_multimodal_hydrology" # 預設安全 fallback
        manuscript_id = None
        
        # 檢查資料庫中是否存在該 paper_id
        cursor.execute("SELECT paper_id FROM papers WHERE paper_id = ?;", (ref_id,))
        if cursor.fetchone():
            paper_id = ref_id
        else:
            # 檢查是否為手稿 ID
            cursor.execute("SELECT manuscript_id FROM my_manuscripts WHERE manuscript_id = ?;", (ref_id,))
            if cursor.fetchone():
                manuscript_id = ref_id
                # 取得該手稿關聯主題下的隨機文獻作為 paper_id (滿足外鍵限制)
                cursor.execute("SELECT paper_id FROM papers LIMIT 1;")
                row = cursor.fetchone()
                if row:
                    paper_id = row[0]
                    
        # 建立唯一的 log_id
        log_id = f"log_auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{inserted_count + 1}"
        
        # 寫入 red_team_logs
        try:
            cursor.execute("""
            INSERT INTO red_team_logs (log_id, paper_id, manuscript_id, aspect_analyzed, reviewer_attack, student_defense, verdict, test_time, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                log_id,
                paper_id,
                manuscript_id,
                aspect,
                f"[哈教授] {attack}",
                "", # 學生防禦預設為空，等待哈爸親自填寫
                "VULNERABLE", # 預設強制為脆弱點 (鎖定合併！)
                datetime.now().isoformat(),
                json.dumps({"source_file": os.path.basename(meeting_path), "automatic_harvest": True}, ensure_ascii=False)
            ))
            inserted_count += 1
            print(f"  [+] 成功落庫自審脆弱點：{aspect} -> 預設 'VULNERABLE'")
        except Exception as e:
            print(f"  [-] 寫入脆弱點時出錯 (可能有外鍵約束問題): {e}")
            
    conn.commit()
    conn.close()
    print(f"\n🎉 考古落庫完畢！累計寫入 {inserted_count} 筆 'VULNERABLE' 脆弱點到 SQLite。")
    print("[*] 哈爸必須在本地針對此脆弱點進行模擬與防禦更新，將 Verdict 改為 'PASS' 始可解除物理合併鎖！\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="哈爸主權研究大腦 - 師徒自審 Feedback 考古自動落庫工具")
    parser.add_argument("--meeting", required=True, help="思考日誌 / 週會記錄 Markdown 檔案路徑")
    
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    harvest_meeting_feedback(db_path, args.meeting)
