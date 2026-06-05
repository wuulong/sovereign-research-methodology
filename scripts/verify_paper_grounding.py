#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手稿引文地基對合檢測工具 (verify_paper_grounding.py)

目的：
- 讀取手稿 sovereign_research_paper.md 中引用的所有 @cite_key。
- 比對大腦 SQLite 真值資料庫，檢驗這些文獻的註冊、就位與 Stage 2 合規狀態。
- 自動生成「引文定錨缺失報告」，防範論文流於空洞自指。
"""

import os
import sqlite3
import re
import json

def extract_cite_keys_from_manuscript(filepath):
    """
    從手稿 Markdown 檔案中提取所有以 @cite_key 形式出現的引文鍵
    """
    if not os.path.exists(filepath):
        print(f"[!] 手稿檔案不存在: {filepath}")
        return []
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 匹配 @cite_key 或 [@cite_key]
    # 例如 @arxiv_Maynard_2026_2601 或 @zotero_Chan_2024_671
    pattern = re.compile(r'@([a-zA-Z0-9_.-]+)')
    matches = pattern.findall(content)
    
    # 除重並過濾掉可能的雜訊
    unique_keys = sorted(list(set(matches)))
    return unique_keys

def main():
    base_dir = "/Users/wuulong/github/bmad-pa"
    manuscript_path = os.path.join(base_dir, "events", "my_research", "manuscripts", "sovereign_research_paper.md")
    db_path = os.path.join(base_dir, "events", "my_research", "data", "Research_Artifacts.db")
    
    print("\n" + "="*80)
    print("🕵️‍♂️  \033[1;36m啟動手稿引文地基對合檢測 (Sovereign Ingestion Alignment Check)\033[0m")
    print("="*80)
    
    # 1. 提取手稿中的引用鍵
    cite_keys = extract_cite_keys_from_manuscript(manuscript_path)
    print(f"📖 手稿位置: [sovereign_research_paper.md](file://{manuscript_path})")
    print(f"  ➔ 成功在手稿中提取到 {len(cite_keys)} 個實體引用鍵。")
    
    if not os.path.exists(db_path):
        print(f"[!] 大腦資料庫不存在: {db_path}")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 2. 進行大腦資料庫比對
    verified_results = []
    missing_db_keys = []
    pending_assets_keys = []
    non_compliant_keys = []
    
    for key in cite_keys:
        # 查詢 papers 註冊狀態
        cursor.execute("""
            SELECT p.paper_id, p.title, p.meta_data, u.download_status, u.url_link
            FROM papers p
            LEFT JOIN paper_urls u ON p.paper_id = u.paper_id AND u.url_type = 'local_pdf'
            WHERE p.cite_key = ?;
        """, (key,))
        
        row = cursor.fetchone()
        if not row:
            missing_db_keys.append(key)
            verified_results.append({
                "cite_key": key,
                "status": "❌ 未在大腦資料庫中註冊 (Missing Ingestion)",
                "details": "需要在 Zotero 中引渡或透過 API 線上探勘寫入 papers 表！",
                "color_status": "\033[1;31m❌ 未註冊\033[0m"
            })
            continue
            
        paper_id, title, meta_str, download_status, url_link = row
        
        # 查詢 meta_data 與 compliance
        meta = {}
        if meta_str:
            try:
                meta = json.loads(meta_str)
            except:
                pass
                
        is_compliant = False
        if meta.get("compliance_status"):
            is_compliant = meta["compliance_status"].get("is_compliant", False)
            
        stage = meta.get("stage", "STAGE_1_PRELIMINARY")
        
        # 研判就位與合規狀態
        if download_status != "DOWNLOADED" or not url_link:
            pending_assets_keys.append(key)
            verified_results.append({
                "cite_key": key,
                "status": "⚠️ 實體資產未就位 (PENDING)",
                "details": "需要執行 hydrate_paper_assets.py 下載實體 PDF 並萃取 MD！",
                "color_status": "\033[1;33m⚠️ 未就位\033[0m"
            })
        elif stage != "STAGE_2_DEEP" or not is_compliant:
            non_compliant_keys.append(key)
            verified_results.append({
                "cite_key": key,
                "status": "🟡 僅完成 Stage 1 輕量閱讀 (Not Stage 2 Compliant)",
                "details": "大腦中無 10 大學術因子，需要對其跑 Stage 2 因子深度洗滌！",
                "color_status": "\033[1;32m🟡 未洗滌\033[0m"
            })
        else:
            verified_results.append({
                "cite_key": key,
                "status": "🟢 完美合規 (Verdict PASS)",
                "details": f"已完成 Stage 2 深度因子解析，大腦學術重力計量為: {meta.get('academic_prestige', {}).get('academic_gravity_score', 0.0)} 分！",
                "color_status": "\033[1;36m🟢 已合規\033[0m"
            })
            
    conn.close()
    
    # 3. 輸出極美對照報告
    print("\n📊 \033[1;35m手稿文獻實體地基對合檢核報告 (Alignment Status List):\033[0m")
    print("-" * 110)
    print(f"{'引文鍵 (Cite Key)':<35} | {'大腦資料庫狀態 (Status)':<30} | {'導引行動 (Action)':<45}")
    print("-" * 110)
    for r in verified_results:
        print(f"{r['cite_key']:<35} | {r['color_status']:<38} | {r['details']}")
    print("-" * 110)
    
    print(f"\n📈 對合檢核統計彙報 (Alignment Metrology):")
    print(f"  - 全局引文總數   : {len(cite_keys)} 篇")
    print(f"  - \033[1;36m完美合規文獻數 : {len(cite_keys) - len(missing_db_keys) - len(pending_assets_keys) - len(non_compliant_keys)} 篇\033[0m")
    print(f"  - \033[1;31m資料庫未註冊數 : {len(missing_db_keys)} 篇 (需要發動 paper_scout)\033[0m")
    print(f"  - \033[1;33m實體 PDF 未就位 : {len(pending_assets_keys)} 篇 (需要發動 hydrate_paper_assets)\033[0m")
    print(f"  - \033[1;32m因子未洗滌數   : {len(non_compliant_keys)} 篇 (需要發動 Stage 2 深度析取)\033[0m")
    
    print("\n" + "="*80)
    print("🎯  \033[1;36m主權引文對合檢核完畢！大腦引文健康度掃描完成。\033[0m")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
