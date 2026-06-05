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
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
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
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_db = os.path.join(base_dir, "data", "Research_Artifacts.db")
    default_contrib = os.path.join(base_dir, "data", "contributions")

    parser = argparse.ArgumentParser(description="哈爸主權聯邦共創 - 本地聯邦資料庫一鍵重構器")
    parser.add_argument("--db", default=default_db, help="重建資料庫之輸出路徑")
    parser.add_argument("--contrib-dir", default=default_contrib, help="JSON 貢獻包來源目錄")
    
    args = parser.parse_args()
    rebuild_database(args.db, args.contrib_dir)
