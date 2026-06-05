#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌊 主權大腦實體探勘命令列工具 (brain_cli.py)

目的：
提供君王 (wuulong) 一個 100% 精準、零 Token 消耗、毫秒級響應的本地大腦 SQLite 數據庫手動查驗工具。
支援文獻、紅軍日誌、現地實踐數據的快速檢索，並吃多種參數。

用法範例：
  1. 列出大腦所有 Table 狀態:   python3 brain_cli.py -l
  2. 查驗特定文獻註冊與 Meta:  python3 brain_cli.py -p arxiv_AgenticScience_2025_14111
  3. 查驗當前紅軍自審日誌:     python3 brain_cli.py -r
  4. 執行自訂 SQL 照妖鏡:      python3 brain_cli.py -s "SELECT paper_id, title FROM papers LIMIT 3;"
"""

import os
import sys
import json
import sqlite3
import argparse

# 剛性預設路徑定義
DEFAULT_DB_PATH = "/Users/wuulong/github/bmad-pa/events/my_research/data/Research_Artifacts.db"

class BrainCLI:
    def __init__(self, db_path):
        self.db_path = db_path
        if not os.path.exists(db_path):
            print(f"❌ 錯誤：找不到主權大腦 SQLite 資料庫：{db_path}")
            sys.exit(1)
            
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 允許使用字典方式存取欄位
        return conn

    def format_table(self, rows, headers):
        """極具質感的純文字 ASCII 表格格式化器"""
        if not rows:
            return "Empty set"
        
        # 轉化為字串矩陣
        data = [[str(item) if item is not None else "NULL" for item in row] for row in rows]
        
        # 計算每欄最大寬度
        col_widths = [len(h) for h in headers]
        for row in data:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(val))
                
        # 繪製邊框與內容
        sep = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
        header_line = "| " + " | ".join([h.ljust(col_widths[i]) for i, h in enumerate(headers)]) + " |"
        
        lines = [sep, header_line, sep.replace("-", "=")]
        for row in data:
            row_line = "| " + " | ".join([val.ljust(col_widths[i]) for i, val in enumerate(row)]) + " |"
            lines.append(row_line)
        lines.append(sep)
        return "\n".join(lines)

    def list_brain_tables(self, as_json=False):
        """列出資料庫所有 Tables 及其 Row Count"""
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row['name'] for row in cursor.fetchall()]
        
        results = []
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as cnt FROM {table};")
            count = cursor.fetchone()['cnt']
            
            # 取得欄位清單
            cursor.execute(f"PRAGMA table_info({table});")
            cols = ", ".join([col['name'] for col in cursor.fetchall()])
            
            results.append({
                "Table Name": table,
                "Row Count": count,
                "Columns": cols[:60] + "..." if len(cols) > 60 else cols
            })
            
        conn.close()
        
        if as_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            headers = ["Table Name", "Row Count", "Columns"]
            rows = [[r["Table Name"], r["Row Count"], r["Columns"]] for r in results]
            print("\n🧠 --- 主權十一表大腦全景看板 ---")
            print(self.format_table(rows, headers))

    def query_paper(self, cite_key, as_json=False):
        """精準查詢文獻的註冊與 Stage 2 合規狀態"""
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT paper_id, topic_id, title, cite_key, meta_data 
            FROM papers 
            WHERE LOWER(cite_key) = LOWER(?) OR LOWER(paper_id) = LOWER(?);
        """, (cite_key, cite_key))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            print(f"❌ 查無此文獻：在 papers 表中找不到 cite_key 或 paper_id 為 '{cite_key}' 的資料。")
            return
            
        meta_str = row['meta_data']
        is_compliant = "❌ 待消化 (Stage 1)"
        stage = "STAGE_1_PRELIMINARY"
        missing = []
        
        if meta_str:
            try:
                meta = json.loads(meta_str)
                stage = meta.get("stage", "STAGE_1_PRELIMINARY")
                compliance = meta.get("compliance_status", {})
                if compliance.get("is_compliant", False):
                    is_compliant = "🟢 深度合規 (Stage 2)"
                missing = compliance.get("missing_fields", [])
            except:
                is_compliant = "⚠️ Meta JSON 解析失敗"
                
        result = {
            "Paper ID": row['paper_id'],
            "Cite Key": row['cite_key'],
            "Topic ID": row['topic_id'],
            "Title": row['title'][:50] + "..." if len(row['title']) > 50 else row['title'],
            "Ingestion Stage": stage,
            "Maturity Verdict": is_compliant,
            "Missing Fields": str(missing) if missing else "None"
        }
        
        if as_json:
            result["full_meta_data"] = json.loads(meta_str) if meta_str else None
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n📑 --- 文獻實體檢索報告: {cite_key} ---")
            for k, v in result.items():
                print(f"  ▪️ {k.ljust(18)}: {v}")
            if meta_str and stage == "STAGE_2_DEEP":
                try:
                    meta = json.loads(meta_str)
                    verdict = meta["paper_extraction"]["sovereign_taste_verdict"]
                    print(f"\n  ⚖️  主權品位評判 (Verdict) [Score: {verdict.get('taste_score', 'N/A')}]:")
                    print(f"     \"{verdict.get('critique', '無判詞')}\"")
                except:
                    pass

    def query_redteam(self, ms_id="ms_sovereign_research_2026", as_json=False):
        """查詢紅軍對抗與自審答辯日誌"""
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT log_id, paper_id, aspect_analyzed, reviewer_attack, student_defense, verdict, test_time 
            FROM red_team_logs 
            WHERE manuscript_id = ? OR paper_id = ?;
        """, (ms_id, ms_id))
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for r in rows:
            results.append({
                "Log ID": r['log_id'],
                "Target Paper": r['paper_id'] if r['paper_id'] else "Manuscript",
                "Aspect Analyzed": r['aspect_analyzed'],
                "Verdict": "🟢 PASS" if r['verdict'] == 'PASS' else "🔴 VULNERABLE",
                "Checked At": r['test_time'],
                "Reviewer Attack": r['reviewer_attack'],
                "Student Defense": r['student_defense']
            })
            
        if as_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            # 1. 輸出摘要表格 (Aspect 截斷到 40 字以防表格爆開)
            headers = ["Log ID", "Target Paper", "Aspect Analyzed (Summary)", "Verdict", "Checked At"]
            row_data = []
            for r in results:
                aspect_summary = r["Aspect Analyzed"][:37] + "..." if len(r["Aspect Analyzed"]) > 37 else r["Aspect Analyzed"]
                row_data.append([r["Log ID"], r["Target Paper"], aspect_summary, r["Verdict"], r["Checked At"]])
                
            print(f"\n🥊 --- 紅軍自審與答辯防線日誌 (Manuscript: {ms_id}) ---")
            print(self.format_table(row_data, headers))
            
            # 2. 輸出 100% 完整日誌明細
            print("\n📋 ==========================================================================")
            print("📝  紅軍自審日誌 100% 完整明細帳本 (FULL LOG DETAILS)")
            print("==========================================================================")
            
            for idx, r in enumerate(results, 1):
                print(f"\n[{idx}] 🥊 日誌 ID: {r['Log ID']}")
                print(f"    🎯 挑戰目標 (Target) : {r['Target Paper']}")
                print(f"    🔎 分析面向 (Aspect) : {r['Aspect Analyzed']}")
                print(f"    ⚖️  裁決狀態 (Verdict): {r['Verdict']}  (時間: {r['Checked At']})")
                print("    " + "-" * 70)
                
                # 處理多行文字的縮排展示
                attack_indented = "\n      ".join(r['Reviewer Attack'].strip().split("\n"))
                defense_indented = "\n      ".join(r['Student Defense'].strip().split("\n"))
                
                print(f"    ⚡️ 紅軍拷問質疑 (Reviewer Attack):\n      {attack_indented}")
                print(f"    🛡️  君王防衛答辯 (Student Defense):\n      {defense_indented}")
                print("    " + "=" * 70)

    def execute_custom_sql(self, sql_str, as_json=False):
        """執行君王自訂的 SQL 照妖鏡查詢"""
        conn = self._connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql_str)
            rows = cursor.fetchall()
            
            if not rows:
                print("Empty set (Query returned 0 rows).")
                conn.close()
                return
                
            headers = rows[0].keys()
            results = [dict(row) for row in rows]
            conn.close()
            
            if as_json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                row_data = [[r[h] for h in headers] for r in results]
                print(f"\n🔮 --- 實體 SQL 照妖鏡執行結果 ---")
                print(self.format_table(row_data, headers))
                print(f"(* 累計檢索到 {len(results)} 筆 rows *)")
        except Exception as e:
            conn.close()
            print(f"❌ SQL 執行失敗，語法錯誤：{e}")

def main():
    parser = argparse.ArgumentParser(description="🌊 主權大腦實體探勘命令列工具 (wuulong's Brain CLI)")
    parser.add_argument("-d", "--db", default=DEFAULT_DB_PATH, help="指定 SQLite 資料庫檔案路徑")
    parser.add_argument("-l", "--list", action="store_true", help="列出大腦資料庫中所有 Tables 與 Row 統計")
    parser.add_argument("-p", "--paper", help="查詢特定文獻的註冊與 Stage 2 合規明細")
    parser.add_argument("-r", "--red", nargs="?", const="ms_sovereign_research_2026", help="查詢紅軍自審日誌 (可帶入手稿 ID，預設為 ms_sovereign_research_2026)")
    parser.add_argument("-s", "--sql", help="直接輸入自訂 SQL 語句進行硬核查詢")
    parser.add_argument("--json", action="store_true", help="切換為結構化 JSON 輸出格式")
    
    args = parser.parse_args()
    
    cli = BrainCLI(args.db)
    
    # 參數路由
    if args.list:
        cli.list_brain_tables(args.json)
    elif args.paper:
        cli.query_paper(args.paper, args.json)
    elif args.red:
        cli.query_redteam(args.red, args.json)
    elif args.sql:
        cli.execute_custom_sql(args.sql, args.json)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
