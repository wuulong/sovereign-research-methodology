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
DEFAULT_DB_PATH = "/Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/data/Research_Artifacts.db"

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
        
        if not cite_key:
            # 沒帶引數，列出所有文獻的 ID、Cite Key 與 Title
            cursor.execute("""
                SELECT paper_id, cite_key, title, meta_data, read_depth_level 
                FROM papers 
                ORDER BY cite_key;
            """)
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for r in rows:
                meta_str = r['meta_data']
                stage = "STAGE_1_PRELIMINARY"
                if meta_str:
                    try:
                        meta = json.loads(meta_str)
                        stage = meta.get("stage", "STAGE_1_PRELIMINARY")
                    except:
                        pass
                status_str = "🟢 Stage 2" if stage == "STAGE_2_DEEP" else "🟡 Stage 1"
                
                results.append({
                    "Paper ID": r['paper_id'],
                    "Cite Key": r['cite_key'],
                    "Title": r['title'][:50] + "..." if len(r['title']) > 50 else r['title'],
                    "Stage": status_str,
                    "Read Depth": r['read_depth_level'] if r['read_depth_level'] else "UNREAD"
                })
                
            if as_json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                headers = ["Paper ID", "Cite Key", "Title", "Stage", "Read Depth"]
                row_data = [[r["Paper ID"], r["Cite Key"], r["Title"], r["Stage"], r["Read Depth"]] for r in results]
                print("\n📑 --- 大腦背景文獻全景清單 ---")
                print(self.format_table(row_data, headers))
                print(f"(* 累計檢索到 {len(results)} 筆文獻 *)")
            return
            
        cursor.execute("""
            SELECT paper_id, topic_id, title, cite_key, meta_data, read_depth_level 
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
            "Real Read Depth": row['read_depth_level'] if row['read_depth_level'] else "UNREAD",
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
                    ext = meta["paper_extraction"]
                    
                    print("\n  📖  十大學術因子 DTO (Ten Academic Factors DTO):")
                    print(f"    1. 🎯 核心問題 (Core Question):\n       \"{ext.get('core_question', 'N/A')}\"")
                    print(f"    2. 🧪 核心方法 (Core Methodology):\n       \"{ext.get('core_methodology', 'N/A')}\"")
                    
                    insights = ext.get('key_insights', [])
                    print(f"    3. 💡 關鍵洞見 (Key Insights):")
                    if isinstance(insights, list):
                        for ins in insights:
                            print(f"       • {ins}")
                    else:
                        print(f"       • {insights}")
                        
                    print(f"    4. 🏆 獨特貢獻 (Unique Contribution):\n       \"{ext.get('unique_contribution', 'N/A')}\"")
                    print(f"    5. 🔬 實證條件 (Empirical Setup):\n       \"{ext.get('empirical_setup', 'N/A')}\"")
                    print(f"    6. 📊 關鍵結果 (Key Results):\n       \"{ext.get('key_results', 'N/A')}\"")
                    print(f"    7. 🛑 限制與展望 (Limitations & Outlook):\n       \"{ext.get('limitations_outlook', 'N/A')}\"")
                    
                    refs = ext.get('key_references_to_suck', [])
                    ref_list = []
                    if isinstance(refs, list):
                        for r in refs:
                            if isinstance(r, dict):
                                ck = r.get("cite_key", "Unknown_Key")
                                reas = r.get("reason", "")
                                if reas:
                                    ref_list.append(f"@{ck} ({reas})")
                                else:
                                    ref_list.append(f"@{ck}")
                            else:
                                ref_list.append(str(r))
                    else:
                        ref_list = [str(refs)]
                    ref_str = ", ".join(ref_list)
                    print(f"    8. 🔗 核心參考文獻 (References to Ingest):\n       [{ref_str}]")
                    
                    verdict = ext.get("sovereign_taste_verdict", {})
                    print(f"    9. ⚖️  主權品位評判 (Verdict) [Score: {verdict.get('taste_score', 'N/A')}]:\n       \"{verdict.get('critique', '無判詞')}\"")
                except Exception as e:
                    print(f"  [-] 無法讀取十大學術因子: {e}")

    def query_redteam(self, ms_id="ms_sovereign_research_2026", as_json=False):
        """查詢紅軍對抗與自審答辯日誌"""
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT log_id, paper_id, aspect_analyzed, reviewer_attack, student_defense, verdict, test_time, raw_student_defense, defense_refinement_delta 
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
                "Student Defense": r['student_defense'],
                "Raw Defense": r['raw_student_defense'],
                "Refinement Delta": r['defense_refinement_delta']
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
                attack_indented = "\n      ".join(r['Reviewer Attack'].strip().split("\n")) if r['Reviewer Attack'] else ""
                defense_indented = "\n      ".join(r['Student Defense'].strip().split("\n")) if r['Student Defense'] else ""
                
                print(f"    ⚡️ 紅軍拷問質疑 (Reviewer Attack):\n      {attack_indented}")
                
                if r.get('Raw Defense'):
                    raw_indented = "\n      ".join(r['Raw Defense'].strip().split("\n"))
                    print(f"    🛡️  研究者原始答辯 (Raw User Defense):\n      {raw_indented}")
                    print(f"    🛡️  AI 潤飾學術答辯 (AI Polished Defense):\n      {defense_indented}")
                else:
                    print(f"    🛡️  君王防衛答辯 (Student Defense):\n      {defense_indented}")
                    
                if r.get('Refinement Delta'):
                    delta_indented = "\n      ".join(r['Refinement Delta'].strip().split("\n"))
                    print(f"    ⚖️  AI 潤飾語意偏差 (Semantic Friction Delta):\n      {delta_indented}")
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

    def update_read_depth(self, args_list, as_json=False):
        """批次手動更新文獻的真實閱讀層次"""
        if not args_list:
            print("❌ 錯誤：請提供 cite_key:level 參數或 JSON 檔案路徑。")
            return
            
        LEVEL_MAP = {
            "0": "UNREAD",
            "1": "DTO_SUMMARY",
            "2": "SKIMMED",
            "3": "BODY_ON_DEEP",
            "unread": "UNREAD",
            "dto_summary": "DTO_SUMMARY",
            "skimmed": "SKIMMED",
            "body_on_deep": "BODY_ON_DEEP"
        }
        
        updates = {}
        
        # 判斷是否為 JSON 檔案
        if len(args_list) == 1 and args_list[0].endswith(".json"):
            json_path = args_list[0]
            # 如果不是絕對路徑，則尋找相對於專案目錄的路徑
            if not os.path.isabs(json_path):
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                json_path = os.path.join(base_dir, json_path)
                
            if not os.path.exists(json_path):
                print(f"❌ 錯誤：找不到指定的 JSON 批次檔案：'{args_list[0]}'")
                return
                
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    print("❌ 錯誤：JSON 檔案格式應為 {\"cite_key\": \"level\"} 的 Key-Value 對應。")
                    return
                updates = data
            except Exception as e:
                print(f"❌ 錯誤：讀取 JSON 檔案失敗: {e}")
                return
        else:
            # 命令行鍵值對解析
            for item in args_list:
                if ":" not in item:
                    print(f"❌ 錯誤：參數格式不正確：'{item}'。應為 'cite_key:level' 形式。")
                    return
                parts = item.split(":", 1)
                updates[parts[0].strip()] = parts[1].strip()
                
        if not updates:
            print("[-] 沒有需要更新的文獻資料。")
            return
            
        # 檢驗與映射所有 levels
        validated_updates = []
        for key, raw_level in updates.items():
            level_key = str(raw_level).strip().lower()
            if level_key not in LEVEL_MAP:
                print(f"❌ 錯誤：不正當的閱讀層次：'{raw_level}'（對應文獻：'{key}'）。\n可接受層次：0=UNREAD, 1=DTO_SUMMARY, 2=SKIMMED, 3=BODY_ON_DEEP")
                return
            validated_updates.append((key, LEVEL_MAP[level_key]))
            
        # 執行資料庫更新 (包在 Transaction 中)
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        success_count = 0
        update_summary = []
        
        try:
            for key, level in validated_updates:
                # 剛性檢索 papers 是否存在該 key
                cursor.execute("SELECT paper_id, cite_key, title FROM papers WHERE LOWER(cite_key) = LOWER(?) OR LOWER(paper_id) = LOWER(?);", (key, key))
                row = cursor.fetchone()
                if not row:
                    raise Exception(f"大腦資料庫中查無文獻：'{key}'，無法執行更新。")
                    
                target_key = row['cite_key']
                title_brief = row['title'][:30] + "..." if len(row['title']) > 30 else row['title']
                
                cursor.execute("""
                    UPDATE papers 
                    SET read_depth_level = ? 
                    WHERE LOWER(cite_key) = LOWER(?) OR LOWER(paper_id) = LOWER(?);
                """, (level, key, key))
                
                success_count += 1
                update_summary.append([target_key, title_brief, level])
                
            conn.commit()
            
            if as_json:
                json_out = [{"cite_key": item[0], "title": item[1], "new_read_depth": item[2]} for item in update_summary]
                print(json.dumps(json_out, ensure_ascii=False, indent=2))
            else:
                print(f"\n🎉 成功批次手動更新 {success_count} 筆文獻之真實閱讀層次！")
                headers = ["Cite Key", "Title", "New Read Depth"]
                print(self.format_table(update_summary, headers))
                
        except Exception as e:
            conn.rollback()
            print(f"\n❌ 批次更新失敗，已復原所有變更。原因：{e}")
        finally:
            conn.close()

    def query_projects_and_topics(self, project_id=None, as_json=False):
        """查詢專案與循序主題看板"""
        conn = self._connect()
        cursor = conn.cursor()
        
        if project_id:
            cursor.execute("""
                SELECT p.project_id, p.project_name, t.topic_id, t.topic_name, t.sequence_order, t.status, t.focus_spec
                FROM projects p
                LEFT JOIN topics t ON p.project_id = t.project_id
                WHERE p.project_id = ? OR t.topic_id = ?
                ORDER BY p.project_id, t.sequence_order;
            """, (project_id, project_id))
        else:
            cursor.execute("""
                SELECT p.project_id, p.project_name, t.topic_id, t.topic_name, t.sequence_order, t.status, t.focus_spec
                FROM projects p
                LEFT JOIN topics t ON p.project_id = t.project_id
                ORDER BY p.project_id, t.sequence_order;
            """)
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for r in rows:
            focus_str = r['focus_spec']
            focus_summary = ""
            if focus_str:
                try:
                    focus = json.loads(focus_str)
                    focus_summary = ", ".join(focus.get("focus_variables", []))
                except:
                    focus_summary = focus_str[:30]
            
            results.append({
                "Project ID": r['project_id'],
                "Project Name": r['project_name'],
                "Topic ID": r['topic_id'] if r['topic_id'] else "None",
                "Topic Name": r['topic_name'] if r['topic_name'] else "None",
                "Seq": r['sequence_order'] if r['sequence_order'] is not None else "N/A",
                "Status": r['status'] if r['status'] else "N/A",
                "Focus variables": focus_summary
            })
            
        if as_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            headers = ["Project ID", "Project Name", "Topic ID", "Topic Name", "Seq", "Status", "Focus variables"]
            row_data = [[r["Project ID"], r["Project Name"], r["Topic ID"], r["Topic Name"], r["Seq"], r["Status"], r["Focus variables"]] for r in results]
            print("\n🗺️ --- 主權專案與循序主題演進看板 ---")
            print(self.format_table(row_data, headers))

    def query_empirical_evidences(self, paper_id=None, as_json=False):
        """查詢現地實踐與誤差指標"""
        conn = self._connect()
        cursor = conn.cursor()
        
        if paper_id:
            cursor.execute("""
                SELECT e.evidence_id, e.paper_id, p.cite_key, e.practice_scenario, e.friction_percentage, e.evidence_time
                FROM empirical_evidences e
                LEFT JOIN papers p ON e.paper_id = p.paper_id
                WHERE e.paper_id = ? OR p.cite_key = ? OR e.evidence_id = ?;
            """, (paper_id, paper_id, paper_id))
        else:
            cursor.execute("""
                SELECT e.evidence_id, e.paper_id, p.cite_key, e.practice_scenario, e.friction_percentage, e.evidence_time
                FROM empirical_evidences e
                LEFT JOIN papers p ON e.paper_id = p.paper_id;
            """)
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for r in rows:
            fric = r['friction_percentage']
            fric_str = f"{fric:.2f}%" if fric is not None else "N/A"
            if fric is not None and fric > 10.0:
                fric_str += " ⚠️"
                
            results.append({
                "Evidence ID": r['evidence_id'],
                "Cite Key": r['cite_key'] if r['cite_key'] else r['paper_id'],
                "Scenario": r['practice_scenario'][:40] + "..." if len(r['practice_scenario']) > 40 else r['practice_scenario'],
                "Friction": fric_str,
                "Checked At": r['evidence_time']
            })
            
        if as_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            headers = ["Evidence ID", "Cite Key", "Scenario", "Friction", "Checked At"]
            row_data = [[r["Evidence ID"], r["Cite Key"], r["Scenario"], r["Friction"], r["Checked At"]] for r in results]
            print("\n🛠️ --- 現地實踐與物理誤差檢視看板 ---")
            print(self.format_table(row_data, headers))

    def query_manuscripts(self, manuscript_id=None, as_json=False):
        """查詢主權手稿演化鏈與引用上下文"""
        conn = self._connect()
        cursor = conn.cursor()
        
        if manuscript_id:
            # 查詢單一手稿及其引用關係
            cursor.execute("""
                SELECT manuscript_id, topic_id, title, cite_key, manuscript_type, evolution_stage, previous_manuscript_id, meta_data
                FROM my_manuscripts
                WHERE manuscript_id = ? OR cite_key = ?;
            """, (manuscript_id, manuscript_id))
            ms = cursor.fetchone()
            
            if not ms:
                conn.close()
                print(f"❌ 查無此手稿：'{manuscript_id}'")
                return
                
            # 查詢引用關聯
            cursor.execute("""
                SELECT mc.paper_id, p.cite_key, p.title, mc.citation_context
                FROM manuscript_citations mc
                LEFT JOIN papers p ON mc.paper_id = p.paper_id
                WHERE mc.manuscript_id = ?;
            """, (ms['manuscript_id'],))
            citations = cursor.fetchall()
            conn.close()
            
            results = {
                "Manuscript ID": ms['manuscript_id'],
                "Title": ms['title'],
                "Cite Key": ms['cite_key'] if ms['cite_key'] else "None",
                "Type": ms['manuscript_type'],
                "Stage": ms['evolution_stage'],
                "Previous ID": ms['previous_manuscript_id'] if ms['previous_manuscript_id'] else "None",
                "Citations": [{"Paper ID": c['paper_id'], "Cite Key": c['cite_key'] if c['cite_key'] else "None", "Title": c['title'], "Context": c['citation_context']} for c in citations]
            }
            
            if as_json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                print(f"\n🧬 --- 主權手稿詳細資訊: {ms['manuscript_id']} ---")
                print(f"  ▪️ Title             : {results['Title']}")
                print(f"  ▪️ Cite Key         : {results['Cite Key']}")
                print(f"  ▪️ Type             : {results['Type']}")
                print(f"  ▪️ Stage            : {results['Stage']}")
                print(f"  ▪️ Previous ID      : {results['Previous ID']}")
                
                print("\n  📚 引用的文獻與心智脈絡 (Citations & Context):")
                if not citations:
                    print("     (無引用記錄)")
                else:
                    cit_rows = [
                        [
                            c['cite_key'] if c['cite_key'] else c['paper_id'], 
                            c['title'][:40] + "..." if c['title'] and len(c['title']) > 40 else (c['title'] if c['title'] else "None"),
                            c['citation_context'] if c['citation_context'] else "None"
                        ] 
                        for c in citations
                    ]
                    print(self.format_table(cit_rows, ["Cite Key", "Title", "Citation Context"]))
        else:
            # 查詢所有手稿
            cursor.execute("""
                SELECT manuscript_id, topic_id, title, cite_key, manuscript_type, evolution_stage, previous_manuscript_id
                FROM my_manuscripts;
            """)
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for r in rows:
                results.append({
                    "Manuscript ID": r['manuscript_id'],
                    "Title": r['title'][:40] + "..." if len(r['title']) > 40 else r['title'],
                    "Type": r['manuscript_type'],
                    "Stage": r['evolution_stage'],
                    "Previous ID": r['previous_manuscript_id'] if r['previous_manuscript_id'] else "None"
                })
                
            if as_json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                headers = ["Manuscript ID", "Title", "Type", "Stage", "Previous ID"]
                row_data = [[r["Manuscript ID"], r["Title"], r["Type"], r["Stage"], r["Previous ID"]] for r in results]
                print("\n🧬 --- 主權手稿有向演化看板 ---")
                print(self.format_table(row_data, headers))

    def check_directory_roots(self, as_json=False):
        """檢查抽象目錄定錨與本機實體路徑連線狀態"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT root_key, owner_type, owner_name, absolute_path FROM directory_roots;")
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for r in rows:
            path = r['absolute_path']
            exists = os.path.exists(path)
            status_str = "🟢 OK" if exists else "🔴 斷線/不存在"
            
            results.append({
                "Root Key": r['root_key'],
                "Owner Type": r['owner_type'],
                "Owner Name": r['owner_name'],
                "Absolute Path": path,
                "Status": status_str
            })
            
        if as_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            headers = ["Root Key", "Owner Type", "Owner Name", "Absolute Path", "Status"]
            row_data = [[r["Root Key"], r["Owner Type"], r["Owner Name"], r["Absolute Path"], r["Status"]] for r in results]
            print("\n📂 --- 抽象目錄根節點移植移植性體檢看板 ---")
            print(self.format_table(row_data, headers))

    def query_citation_tree(self, paper_id_or_key, depth=2, verbose=False, as_json=False):
        """查詢論文之引用參考文獻樹狀合規看板，並可通讀十大因子"""
        conn = self._connect()
        cursor = conn.cursor()
        
        # 1. 檢查根論文是否存在
        cursor.execute("""
            SELECT paper_id, cite_key, title, meta_data 
            FROM papers 
            WHERE LOWER(paper_id) = LOWER(?) OR LOWER(cite_key) = LOWER(?);
        """, (paper_id_or_key, paper_id_or_key))
        root_row = cursor.fetchone()
        
        if not root_row:
            conn.close()
            print(f"❌ 錯誤：在 papers 表中找不到 '{paper_id_or_key}' 的資料。")
            return
            
        root_id = root_row['paper_id']
        root_key = root_row['cite_key']
        root_title = root_row['title']
        
        # 2. 定義輔助遞迴函數，建構樹狀與收集所有存在於 DB 且為 Stage 2 的 papers
        tree_structure = {}
        stage2_papers_collected = {} # cite_key -> paper_data
        
        def build_tree(current_id, current_key, current_title, current_depth):
            if current_depth > depth:
                return {"status": "MAX_DEPTH", "title": current_title}
                
            # 查詢該節點
            cursor.execute("SELECT paper_id, cite_key, title, meta_data FROM papers WHERE paper_id = ? OR cite_key = ?;", (current_id, current_key))
            row = cursor.fetchone()
            
            node_info = {
                "id": current_id,
                "cite_key": current_key,
                "title": current_title,
                "in_db": False,
                "stage": "N/A",
                "children": []
            }
            
            if row:
                node_info["in_db"] = True
                meta_str = row['meta_data']
                meta = {}
                if meta_str:
                    try:
                        meta = json.loads(meta_str)
                    except:
                        pass
                stage = meta.get("stage", "STAGE_1_PRELIMINARY")
                node_info["stage"] = stage
                node_info["cite_key"] = row['cite_key']
                node_info["id"] = row['paper_id']
                node_info["title"] = row['title']
                
                # 若為 Stage 2，收集其資訊以便後續通讀
                if stage == "STAGE_2_DEEP" and "paper_extraction" in meta:
                    stage2_papers_collected[row['cite_key']] = {
                        "cite_key": row['cite_key'],
                        "title": row['title'],
                        "extraction": meta["paper_extraction"]
                    }
                
                # 取得其子引用
                # 管道 A: key_references_to_suck
                references = []
                if "paper_extraction" in meta and "key_references_to_suck" in meta["paper_extraction"]:
                    refs = meta["paper_extraction"]["key_references_to_suck"]
                    if isinstance(refs, list):
                        for r in refs:
                            if isinstance(r, dict):
                                clean_ref = r.get("cite_key", "").replace("@", "").strip()
                            else:
                                clean_ref = str(r).replace("@", "").strip()
                            if clean_ref:
                                references.append((None, clean_ref, clean_ref))
                # 管道 B: paper_relations
                cursor.execute("""
                    SELECT pr.target_paper_id, p.cite_key, p.title
                    FROM paper_relations pr
                    LEFT JOIN papers p ON pr.target_paper_id = p.paper_id
                    WHERE pr.source_paper_id = ?;
                """, (row['paper_id'],))
                for pr_row in cursor.fetchall():
                    target_id = pr_row['target_paper_id']
                    target_key = pr_row['cite_key'] if pr_row['cite_key'] else target_id
                    target_title = pr_row['title'] if pr_row['title'] else target_id
                    references.append((target_id, target_key, target_title))
                
                # 除重
                seen = set()
                unique_refs = []
                for tid, tkey, ttitle in references:
                    if tkey.lower() not in seen:
                        seen.add(tkey.lower())
                        unique_refs.append((tid, tkey, ttitle))
                
                # 遞迴子節點
                for tid, tkey, ttitle in unique_refs:
                    if tkey.lower() != current_key.lower():
                        child_node = build_tree(tid, tkey, ttitle, current_depth + 1)
                        node_info["children"].append(child_node)
            else:
                node_info["in_db"] = False
                node_info["stage"] = "N/A"
                
            return node_info
            
        tree_data = build_tree(root_id, root_key, root_title, 0)
        conn.close()
        
        if as_json:
            output = {
                "tree": tree_data,
                "stage2_details": stage2_papers_collected
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return
            
        # 3. 輸出樹狀 ASCII
        print(f"\n🌳 --- 引用文獻樹狀合規看板 (Cite Tree) ---")
        
        def print_ascii_tree(node, prefix="", is_last=True):
            if node["in_db"]:
                if node["stage"] == "STAGE_2_DEEP":
                    status = "🟢 Stage 2 (已合規)"
                else:
                    status = "🟡 Stage 1 (未洗滌)"
            else:
                status = "❌ 未在大腦資料庫中註冊"
                
            marker = "└── " if is_last else "├── "
            print(f"{prefix}{marker}{node['cite_key']} ({node['title'][:30]}...) [{status}]")
            
            new_prefix = prefix + ("    " if is_last else "│   ")
            child_count = len(node.get("children", []))
            for i, child in enumerate(node.get("children", [])):
                print_ascii_tree(child, new_prefix, i == child_count - 1)
                
        root_status = "🟢 Stage 2 (已合規)" if tree_data["stage"] == "STAGE_2_DEEP" else "🟡 Stage 1 (未洗滌)"
        print(f"{tree_data['cite_key']} ({tree_data['title'][:40]}...) [{root_status}]")
        child_count = len(tree_data.get("children", []))
        for i, child in enumerate(tree_data.get("children", [])):
            print_ascii_tree(child, "", i == child_count - 1)
            
        # 4. 若有 verbose，印出十大學術因子 DTO 通讀
        if verbose:
            print("\n" + "=" * 80)
            print("📖  十大學術因子 DTO 深度通讀看板 (Ten Academic Factors DTO)")
            print("=" * 80)
            
            if not stage2_papers_collected:
                print("⚠️  在此引用樹中，未找到任何已消化完成 (Stage 2) 的參考文獻。")
            else:
                for idx, (ckey, pdata) in enumerate(stage2_papers_collected.items(), 1):
                    ext = pdata["extraction"]
                    verdict = ext.get("sovereign_taste_verdict", {})
                    
                    print(f"\n[{idx}] 📄 文獻引用鍵: @{ckey}")
                    print(f"    標題: {pdata['title']}")
                    print("    " + "-" * 70)
                    print(f"    1. 🎯 核心問題 (Core Question):\n       \"{ext.get('core_question', 'N/A')}\"")
                    print(f"    2. 🧪 核心方法 (Core Methodology):\n       \"{ext.get('core_methodology', 'N/A')}\"")
                    
                    insights = ext.get("key_insights", [])
                    print(f"    3. 💡 關鍵洞見 (Key Insights):")
                    if isinstance(insights, list):
                        for ins in insights:
                            print(f"       • {ins}")
                    else:
                        print(f"       • {insights}")
                        
                    print(f"    4. 🏆 獨特貢獻 (Unique Contribution):\n       \"{ext.get('unique_contribution', 'N/A')}\"")
                    print(f"    5. 🔬 實證條件 (Empirical Setup):\n       \"{ext.get('empirical_setup', 'N/A')}\"")
                    print(f"    6. 📊 關鍵結果 (Key Results):\n       \"{ext.get('key_results', 'N/A')}\"")
                    print(f"    7. 🛑 限制與展望 (Limitations & Outlook):\n       \"{ext.get('limitations_outlook', 'N/A')}\"")
                    
                    refs = ext.get("key_references_to_suck", [])
                    ref_list = []
                    if isinstance(refs, list):
                        for r in refs:
                            if isinstance(r, dict):
                                ck = r.get("cite_key", "Unknown_Key")
                                reas = r.get("reason", "")
                                if reas:
                                    ref_list.append(f"@{ck} ({reas})")
                                else:
                                    ref_list.append(f"@{ck}")
                            else:
                                ref_list.append(str(r))
                    else:
                        ref_list = [str(refs)]
                    ref_str = ", ".join(ref_list)
                    print(f"    8. 🔗 核心參考文獻 (References to Ingest):\n       [{ref_str}]")
                    
                    print(f"    9. ⚖️  主權品位評判 (Verdict) [Score: {verdict.get('taste_score', 'N/A')}]:\n       \"{verdict.get('critique', '無判詞')}\"")
                    print("    " + "=" * 80)

    def generate_report(self, manuscript_id, as_json=False):
        """將與指定手稿相關的所有資料庫內容匯出為 Markdown 報告或 JSON 結構"""
        conn = self._connect()
        cursor = conn.cursor()
        
        # 1. 查詢手稿基本資訊
        cursor.execute("""
            SELECT manuscript_id, topic_id, title, cite_key, manuscript_type, evolution_stage, previous_manuscript_id, meta_data
            FROM my_manuscripts
            WHERE manuscript_id = ? OR cite_key = ?;
        """, (manuscript_id, manuscript_id))
        ms = cursor.fetchone()
        
        if not ms:
            conn.close()
            print(f"❌ 查無此手稿：'{manuscript_id}'")
            return
            
        # 2. 查詢引用關聯與文獻基本資料 (已整合學術重力分數)
        cursor.execute("""
            SELECT mc.paper_id, p.cite_key, p.title, p.authors, p.year, p.topic_id, mc.citation_context, p.meta_data,
                   json_extract(p.meta_data, '$.academic_prestige.academic_gravity_score') AS gravity_score
            FROM manuscript_citations mc
            LEFT JOIN papers p ON mc.paper_id = p.paper_id
            WHERE mc.manuscript_id = ?
            ORDER BY p.cite_key;
        """, (ms['manuscript_id'],))
        citations = cursor.fetchall()
        
        # 3. 查詢紅軍對抗日誌
        cursor.execute("""
            SELECT log_id, paper_id, aspect_analyzed, reviewer_attack, student_defense, verdict, test_time, meta_data
            FROM red_team_logs
            WHERE manuscript_id = ? OR paper_id = ?;
        """, (ms['manuscript_id'], ms['manuscript_id']))
        red_team_logs = cursor.fetchall()
        
        # 4. 查詢現地實踐與誤差指標
        cursor.execute("""
            SELECT e.evidence_id, e.paper_id, p.cite_key, e.practice_scenario, e.evidence_payload, e.friction_percentage, e.evidence_time
            FROM empirical_evidences e
            LEFT JOIN papers p ON e.paper_id = p.paper_id
            WHERE p.topic_id = ? OR e.paper_id = ?;
        """, (ms['topic_id'], ms['manuscript_id']))
        evidences = cursor.fetchall()
        conn.close()
        
        # 處理 JSON 格式輸出
        if as_json:
            output_data = {
                "manuscript": dict(ms) if ms else None,
                "citations": [dict(c) for c in citations],
                "red_team_logs": [dict(r) for r in red_team_logs],
                "empirical_evidences": [dict(e) for e in evidences]
            }
            print(json.dumps(output_data, ensure_ascii=False, indent=2))
            return
            
        # 處理 Markdown 格式輸出
        from datetime import datetime
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md = []
        md.append(f"# 🧠 主權手稿全景探勘與大腦合龍審計報告 (Brain Report: {ms['manuscript_id']})")
        md.append(f"*評估時間戳記：`{now_str}`* | *定錨手稿編號：`{ms['manuscript_id']}`*\n")
        
        md.append("> [!IMPORTANT]")
        md.append("> 本報告由主權大腦實體探勘工具自動生成。它將 SQLite 資料庫中所有與本手稿相關的「文獻定錨」、「十大學術因子」、「紅軍自審答辯日誌」以及「現地實踐真值」進行了全量對合匯出，旨在消滅資料庫檢索門檻，提供 100% 剛性 Grounding 的無死角學術體檢。\n")
        
        md.append("## 📊 1. 手稿基本元資料 (Manuscript Metadata)")
        md.append(f"- **手稿 ID (Manuscript ID)**: `{ms['manuscript_id']}`")
        md.append(f"- **論文標題 (Title)**: {ms['title']}")
        md.append(f"- **引用鍵 (Cite Key)**: `{ms['cite_key'] if ms['cite_key'] else 'None'}`")
        md.append(f"- **手稿類型 (Type)**: `{ms['manuscript_type']}`")
        md.append(f"- **演化階段 (Stage)**: `{ms['evolution_stage']}`")
        md.append(f"- **前代手稿 ID (Previous ID)**: `{ms['previous_manuscript_id'] if ms['previous_manuscript_id'] else 'None'}`\n")
        
        md.append("## 🗺️ 2. 論點與引文地基對合看板 (Citations Grounding Ledger)")
        md.append("本節列出本手稿在資料庫中物理定錨的所有引用文獻及其引用脈絡。\n")
        md.append("| 序號 | 引用鍵 (Cite Key) | 大腦主鍵 (Paper ID) | 論文標題 (Title) | 學術重力 (Gravity) | 消化狀態 (Stage) | 引用脈絡與關鍵說明 (Citation Context) |")
        md.append("| :---: | :--- | :--- | :--- | :---: | :---: | :--- |")
        
        stage2_list = []
        
        for idx, c in enumerate(citations, 1):
            ckey = c['cite_key'] if c['cite_key'] else c['paper_id']
            pid = c['paper_id']
            title_brief = c['title'][:40] + "..." if c['title'] and len(c['title']) > 40 else (c['title'] if c['title'] else "None")
            
            meta_str = c['meta_data']
            stage = "STAGE_1_PRELIMINARY"
            if meta_str:
                try:
                    meta = json.loads(meta_str)
                    stage = meta.get("stage", "STAGE_1_PRELIMINARY")
                except:
                    pass
            status_icon = "🟢 Stage 2" if stage == "STAGE_2_DEEP" else "🟡 Stage 1"
            
            # 取得學術重力分數
            grav = c['gravity_score']
            grav_str = f"`{grav:.2f}`" if grav is not None else "`N/A`"
            
            ctx_str = c['citation_context'] if c['citation_context'] else "None"
            ctx_clean = ctx_str.replace('\n', '<br>')
            
            md.append(f"| {idx} | `{ckey}` | `{pid}` | *{title_brief}* | {grav_str} | {status_icon} | {ctx_clean} |")
            
            if stage == "STAGE_2_DEEP" and meta_str:
                try:
                    meta = json.loads(meta_str)
                    if "paper_extraction" in meta:
                        stage2_list.append({
                            "cite_key": ckey,
                            "title": c['title'],
                            "extraction": meta["paper_extraction"],
                            "gravity_score": c['gravity_score']
                        })
                except:
                    pass
                    
        md.append("\n---\n")
        
        md.append("## 📖 3. Stage 2 靠泊文獻「十大學術因子」深度通讀 (Ten Academic Factors DTOs)")
        md.append("本節將本手稿所引用的所有 **Stage 2 深度合規文獻** 的十大學術因子 DTO 進行完整展開，供研究者通讀。\n")
        
        if not stage2_list:
            md.append("> [!WARNING]")
            md.append("> 在此手稿的引用文獻中，未找到任何已完成 Stage 2 深度解構的文獻。\n")
        else:
            for i, pdata in enumerate(stage2_list, 1):
                ext = pdata["extraction"]
                verdict = ext.get("sovereign_taste_verdict", {})
                grav_score = pdata.get("gravity_score")
                grav_display = f"`{grav_score:.2f}`" if grav_score is not None else "`N/A`"
                
                md.append(f"### 📄 [{i}] @{pdata['cite_key']}")
                md.append(f"- **標題 (Title)**: {pdata['title']}")
                md.append(f"- **學術重力分數 (Academic Gravity Score)**: {grav_display}")
                md.append(f"- **🎯 1. 核心問題 (Core Question)**:\n  > {ext.get('core_question', 'N/A')}")
                md.append(f"- **🧪 2. 核心方法 (Core Methodology)**:\n  > {ext.get('core_methodology', 'N/A')}")
                
                insights = ext.get('key_insights', [])
                insights_str = ""
                if isinstance(insights, list):
                    insights_str = "\n".join([f"    • {ins}" for ins in insights])
                else:
                    insights_str = f"    • {insights}"
                md.append(f"- **💡 3. 關鍵洞見 (Key Insights)**:\n{insights_str}")
                
                md.append(f"- **🏆 4. 獨特貢獻 (Unique Contribution)**:\n  > {ext.get('unique_contribution', 'N/A')}")
                md.append(f"- **🔬 5. 實證條件 (Empirical Setup)**:\n  > {ext.get('empirical_setup', 'N/A')}")
                md.append(f"- **📊 6. 關鍵結果 (Key Results)**:\n  > {ext.get('key_results', 'N/A')}")
                md.append(f"- **🛑 7. 限制與展望 (Limitations & Outlook)**:\n  > {ext.get('limitations_outlook', 'N/A')}")
                
                refs = ext.get('key_references_to_suck', [])
                ref_list = []
                if isinstance(refs, list):
                    for r in refs:
                        if isinstance(r, dict):
                            ck = r.get("cite_key", "Unknown").replace("@", "")
                            reas = r.get("reason", "")
                            ref_list.append(f"@{ck} ({reas})" if reas else f"@{ck}")
                        else:
                            ref_list.append(str(r).replace("@", ""))
                else:
                    ref_list = [str(refs).replace("@", "")]
                ref_str = ", ".join([f"`@{r}`" for r in ref_list])
                md.append(f"- **🔗 8. 核心參考文獻 (References to Ingest)**: [{ref_str}]")
                md.append(f"- **⚖️ 9. 主權品位評判 (Verdict) [Score: {verdict.get('taste_score', 'N/A')}]**:\n  > \"{verdict.get('critique', '無判詞')}\"\n")
                
        md.append("---\n")
        
        md.append("## 🥊 4. 紅軍自審與君王答辯歷史對抗日誌 (Red Team Defense Logs)")
        md.append("本節列出針對本手稿（或其關聯文獻）在資料庫中登記的所有紅軍自審（Reviewer Attack）與君王防線答辯（Student Defense）日誌。\n")
        
        if not red_team_logs:
            md.append("> [!NOTE]")
            md.append("> 目前無登記之紅軍自審對審紀錄。\n")
        else:
            for idx, r in enumerate(red_team_logs, 1):
                verdict_status = "🟢 PASS" if r['verdict'] == 'PASS' else "🔴 VULNERABLE"
                md.append(f"### 🥊 [{idx}] 日誌 ID: `{r['log_id']}` | 分析面向: `{r['aspect_analyzed']}`")
                md.append(f"- **挑戰目標**: `{r['paper_id'] if r['paper_id'] else 'Manuscript'}`")
                md.append(f"- **裁決狀態**: **{verdict_status}**  (時間: `{r['test_time']}`)")
                
                attack_clean = "\n  > ".join(r['reviewer_attack'].strip().split('\n'))
                defense_clean = "\n  > ".join(r['student_defense'].strip().split('\n'))
                
                md.append(f"- **⚡️ 紅軍拷問質疑 (Reviewer Attack)**:\n  > {attack_clean}")
                md.append(f"- **🛡️ 君王防衛答辯 (Student Defense)**:\n  > {defense_clean}\n")
                
        md.append("---\n")
        
        md.append("## 🛠️ 5. 現地實踐誤差檢視看板 (Empirical Evidence Metrics)")
        md.append("本節列出與本手稿主題相關的現地實踐誤差與物理摩擦指標。\n")
        md.append("| 實證 ID (Evidence ID) | 關聯文獻 (Cite Key) | 實踐情境 (Scenario) | 物理摩擦率 (Friction) | 體檢時間 (Checked At) |")
        md.append("| :---: | :--- | :--- | :--- | :--- |")
        
        if not evidences:
            md.append("| - | - | 目前無登記之現地實踐證據 | - | - |")
        else:
            for e in evidences:
                fric = e['friction_percentage']
                fric_str = f"{fric:.2f}%" if fric is not None else "N/A"
                if fric is not None and fric > 10.0:
                    fric_str += " ⚠️"
                ckey = e['cite_key'] if e['cite_key'] else e['paper_id']
                md.append(f"| `{e['evidence_id']}` | `{ckey}` | {e['practice_scenario']} | {fric_str} | {e['evidence_time']} |")
                
        md.append("\n")
        
        # 決定報告寫入路徑
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if manuscript_id == "ms_sovereign_research_2026" or ms['topic_id'] == "top_sovereign_methodology":
            report_path = os.path.join(base_dir, "manuscripts", "sovereign_research", "sovereign_research_13_brain_report.md")
        else:
            report_path = os.path.join(base_dir, "manuscripts", f"{manuscript_id}_brain_report.md")
            
        # 確保父目錄存在
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        # 寫入檔案
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))
            
        print(f"🎉  主權大腦全景探勘報告產製成功！")
        print(f"  - 手稿 ID: {ms['manuscript_id']}")
        print(f"  - 報告路徑: [brain_report](file://{report_path})")
        print(f"  - 累計定錨引文: {len(citations)} 筆 (已在報告中全量彙整)\n")

def main():
    parser = argparse.ArgumentParser(description="🌊 主權大腦實體探勘命令列工具 (wuulong's Brain CLI)")
    parser.add_argument("-d", "--db", default=DEFAULT_DB_PATH, help="指定 SQLite 資料庫檔案路徑")
    parser.add_argument("-l", "--list", action="store_true", help="列出大腦資料庫中所有 Tables 與 Row 統計")
    parser.add_argument("-p", "--paper", nargs="?", const="", help="查詢特定文獻的註冊與 Stage 2 合規明細 (無引數時列出所有文獻的 ID 與標題)")
    parser.add_argument("-r", "--red", nargs="?", const="ms_sovereign_research_2026", help="查詢紅軍自審日誌 (可帶入手稿 ID，預設為 ms_sovereign_research_2026)")
    parser.add_argument("-s", "--sql", help="直接輸入自訂 SQL 語句進行硬核查詢")
    parser.add_argument("-t", "--topic", nargs="?", const="", help="查詢專案與循序主題看板 (可指定專案 ID 或主題 ID)")
    parser.add_argument("-e", "--evidence", nargs="?", const="", help="查詢現地實踐與誤差指標 (可指定論文 ID 或證據 ID)")
    parser.add_argument("-m", "--manuscript", nargs="?", const="", help="查詢主權手稿演化鏈與引用上下文 (可指定手稿 ID)")
    parser.add_argument("-g", "--report", nargs="?", const="ms_sovereign_research_2026", help="將指定手稿的所有相關 DB 內容匯出為有架構的 Markdown 報告 (預設為 ms_sovereign_research_2026)")
    parser.add_argument("--roots", action="store_true", help="檢查抽象目錄定錨與本機路徑連線狀態")
    parser.add_argument("-c", "--cite-tree", help="查詢特定論文引用文獻樹狀合規看板 (可傳入 paper_id 或 cite_key)")
    parser.add_argument("-v", "--verbose", action="store_true", help="在引用樹查詢中展開印出 Stage 2 文獻的 10 大學術因子")
    parser.add_argument("--json", action="store_true", help="切換為結構化 JSON 輸出格式")
    parser.add_argument("-rd", "--read-depth", nargs="+", help="手動批次更新文獻真實閱讀層次 (可為 cite_key:level 多個鍵值對，或單一 .json 批次檔案。對照：0=UNREAD, 1=DTO_SUMMARY, 2=SKIMMED, 3=BODY_ON_DEEP)")
    
    args = parser.parse_args()
    
    cli = BrainCLI(args.db)
    
    # 參數路由
    if args.list:
        cli.list_brain_tables(args.json)
    elif args.paper is not None:
        cli.query_paper(args.paper, args.json)
    elif args.red:
        cli.query_redteam(args.red, args.json)
    elif args.sql:
        cli.execute_custom_sql(args.sql, args.json)
    elif args.topic is not None:
        cli.query_projects_and_topics(args.topic, args.json)
    elif args.evidence is not None:
        cli.query_empirical_evidences(args.evidence, args.json)
    elif args.manuscript is not None:
        cli.query_manuscripts(args.manuscript, args.json)
    elif args.report is not None:
        cli.generate_report(args.report, args.json)
    elif args.roots:
        cli.check_directory_roots(args.json)
    elif args.cite_tree:
        cli.query_citation_tree(args.cite_tree, depth=2, verbose=args.verbose, as_json=args.json)
    elif args.read_depth is not None:
        cli.update_read_depth(args.read_depth, args.json)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
