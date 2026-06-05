#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - Zotero 相關文獻之「動態重定向靠泊」工具 (redirect_zotero_papers.py)

目的：
從公海緩衝區 (top_haba_staging) 中篩選與 "RAG", "Evaluation", "Retrieval", "Agent" 相關的經典真實論文，
將其 topic_id 動態更新為 "top_sovereign_methodology"（主權研究方法論主題碼頭）。
並列出該主題下目前所有的論文（含線上 ArXiv 探勘的 5 篇與引渡的 Zotero 論文）。
"""

import os
import sqlite3
import json

def redirect_and_verify():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. 搜尋與關鍵字相關的公海緩衝區論文
    keywords = ["RAG", "Evaluation", "Retrieval", "Agent", "Memory", "Offload"]
    print("🔍 正在公海緩衝區 (top_haba_staging) 中檢索相關文獻...")
    
    query = """
    SELECT paper_id, title, authors, year, cite_key 
    FROM papers 
    WHERE topic_id = 'top_haba_staging'
    """
    cursor.execute(query)
    all_staging_papers = cursor.fetchall()
    
    target_papers = []
    for paper_id, title, authors, year, cite_key in all_staging_papers:
        # 簡單的關鍵字匹配 (不區分大小寫)
        match = False
        matched_kw = []
        for kw in keywords:
            if kw.lower() in title.lower():
                match = True
                matched_kw.append(kw)
        
        if match:
            target_papers.append((paper_id, title, authors, year, cite_key, ", ".join(matched_kw)))
            
    print(f"[+] 共發現 {len(target_papers)} 篇與主題相關的緩衝文獻：")
    for i, (pid, title, authors, year, ck, kws) in enumerate(target_papers[:15]): # 限制列出前 15 篇
        print(f"  {i+1}. [{ck}] ({year}) - {title[:80]}... [匹配: {kws}]")
    if len(target_papers) > 15:
        print(f"  ... 以及其他 {len(target_papers) - 15} 篇論文。")
        
    if not target_papers:
        print("[-] 未在緩衝區中檢索到匹配文獻。")
        conn.close()
        return

    # 2. 執行更新 (動態重定向靠泊)
    paper_ids_to_redirect = [p[0] for p in target_papers]
    print(f"\n🚀 正在將此 {len(paper_ids_to_redirect)} 篇文獻的 topic_id 更新為 'top_sovereign_methodology'...")
    
    cursor.executemany("""
    UPDATE papers 
    SET topic_id = 'top_sovereign_methodology', core_method = 'Zotero引渡靠泊'
    WHERE paper_id = ?;
    """, [(pid,) for pid in paper_ids_to_redirect])
    
    conn.commit()
    print(f"💾 大腦更新成功！已成功引渡 {cursor.rowcount} 篇 Zotero 真實文獻！")
    
    # 3. 驗證並列出目前 top_sovereign_methodology 下的所有文獻
    print("\n📊 驗證：查詢 'top_sovereign_methodology' 主題下的所有文獻...")
    cursor.execute("""
    SELECT paper_id, title, authors, year, core_method, cite_key
    FROM papers
    WHERE topic_id = 'top_sovereign_methodology'
    ORDER BY core_method, year DESC;
    """)
    docked_papers = cursor.fetchall()
    
    print(f"[+] 目前已靠泊至『主權協作研究方法論』主題碼頭的論文總數：{len(docked_papers)} 篇")
    
    # 分類統計
    arxiv_count = sum(1 for p in docked_papers if p[4] == '線上類似方法論探勘')
    zotero_count = sum(1 for p in docked_papers if p[4] == 'Zotero引渡靠泊')
    print(f"  - 線上 API 探勘論文：{arxiv_count} 篇")
    print(f"  - Zotero 引渡靠泊論文：{zotero_count} 篇\n")
    
    for i, (pid, title, authors, year, method, ck) in enumerate(docked_papers):
        print(f"  [{i+1}] [{method}] {ck} ({year}): {title[:90]}...")
        
    conn.close()

if __name__ == "__main__":
    redirect_and_verify()
