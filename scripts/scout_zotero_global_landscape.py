#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 本地 Zotero 全局觀對合檢索與引渡靠泊工具 (scout_zotero_global_landscape.py)

目的：
1. 作為線上 API 超時/rate limit (429) 的離線避退機制。
2. 站在四大理論支柱的全局觀高度，對公海緩衝區的 202 篇真實 Zotero 文獻發動精準 SQL 檢索。
3. 將匹配到的 Zotero 經典論文動態引渡靠泊至 `top_sovereign_methodology`，徹底厚化手稿地基。
"""

import os
import sqlite3
import json

def scout_local_zotero_gaps():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 定義四大支柱在本地 Zotero 的 SQL 模糊檢索詞
    pillars = {
        "PILLAR_1_SOVEREIGNTY (認知卸載思維主權)": {
            "keywords": ["offload", "vigilance", "dependency", "cognitive", "human"],
            "clause": " OR ".join([f"title LIKE '%{kw}%'" for kw in ["offload", "vigilance", "dependency", "cognitive", "human"]])
        },
        "PILLAR_2_PHYSICAL (現地真值與物理約束)": {
            "keywords": ["physical", "constraint", "simulation", "model", "experi", "empirical"],
            "clause": " OR ".join([f"title LIKE '%{kw}%'" for kw in ["physical", "constraint", "simulation", "model", "experi", "empirical"]])
        },
        "PILLAR_3_INTEGRITY (學術誠信與照妖鏡教育背景)": {
            "keywords": ["integrity", "cheat", "assess", "plagiarism", "education", "audit", "trust"],
            "clause": " OR ".join([f"title LIKE '%{kw}%'" for kw in ["integrity", "cheat", "assess", "plagiarism", "education", "audit", "trust"]])
        },
        "PILLAR_4_FEDERATED (聯邦 DTO 與知識合流協作)": {
            "keywords": ["collaborat", "decentral", "personal", "graph", "provenance", "lineage", "git"],
            "clause": " OR ".join([f"title LIKE '%{kw}%'" for kw in ["collaborat", "decentral", "personal", "graph", "provenance", "lineage", "git"]])
        }
    }
    
    print("🛡️ [離線避退機制啟動] 正在對公海緩衝區的 202 篇 Zotero 進行全局觀對合檢索...")
    
    total_redirected = 0
    
    for pillar_name, spec in pillars.items():
        print(f"\n==================================================")
        print(f"🔥 檢索支柱：{pillar_name}")
        print(f"==================================================")
        
        # 查詢 top_haba_staging 中符合此支柱關鍵字的論文
        query = f"""
        SELECT paper_id, title, cite_key, authors, year 
        FROM papers 
        WHERE topic_id = 'top_haba_staging' AND ({spec['clause']})
        """
        cursor.execute(query)
        matches = cursor.fetchall()
        
        if not matches:
            print("  [-] 未檢索到匹配的本地文獻。")
            continue
            
        print(f"  [+] 成功檢索到 {len(matches)} 篇相關的 Zotero 經典文獻！正在發動引渡靠泊...")
        
        for pid, title, cite_key, authors, year in matches:
            # 建立大膽猜想對合
            preliminary_relevance = (
                f"離線對合猜想：本篇 Zotero 經典文獻符合『{pillar_name}』支柱。本論文將其引渡，"
                f"作為...章節的實體背景對比，證明哈爸主權大腦在該領域完美繼承了 Zotero 既有的科學資產。"
            )
            
            # 更新 papers
            cursor.execute("""
            UPDATE papers 
            SET topic_id = 'top_sovereign_methodology', 
                core_method = 'Zotero全局引渡靠泊',
                meta_data = ?
            WHERE paper_id = ?
            """, (json.dumps({
                "stage": "STAGE_1_PRELIMINARY",
                "preliminary_relevance": preliminary_relevance,
                "source": "Zotero_local_scout"
            }, ensure_ascii=False), pid))
            
            if cursor.rowcount > 0:
                total_redirected += 1
                print(f"    [+] [Bern Redirected] {cite_key} ({year}) - {title[:80]}...")
                
    conn.commit()
    conn.close()
    
    print(f"\n==================================================")
    print(f"🎉 離線全局對合引渡戰役圓滿成功！")
    print(f"  - 累計引渡靠泊 Zotero 經典文獻：{total_redirected} 篇")
    print(f"  - 現已完成大腦全局文獻大廈厚化！")
    print(f"==================================================")

if __name__ == "__main__":
    scout_local_zotero_gaps()
