#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 手稿引文定錨與 references.bib 自動導出工具 (anchor_manuscript_citations.py)

目的：
1. 將主題下目前所有的 28 篇文獻，與手稿 `ms_sovereign_research_2026` 在 `manuscript_citations` 中進行物理綁定。
2. 自動從 SQLite 中撈取這 28 篇文獻的 BibTeX 條目，導出為學術標準的 `manuscripts/references.bib` 檔案！
"""

import os
import sqlite3

def anchor_and_export():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    bib_path = os.path.join(base_dir, "manuscripts", "references.bib")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    manuscript_id = "ms_sovereign_research_2026"
    
    # 1. 查詢當前主題 top_sovereign_methodology 下的所有論文
    cursor.execute("""
    SELECT paper_id, cite_key, title 
    FROM papers 
    WHERE topic_id = 'top_sovereign_methodology'
    """)
    papers = cursor.fetchall()
    print(f"📊 檢索到主題下共有 {len(papers)} 篇文獻，準備實體定錨至手稿 {manuscript_id}...")
    
    # 2. 批次寫入 manuscript_citations
    inserted_count = 0
    for paper_id, cite_key, title in papers:
        citation_context = f"作為手稿論文之『{cite_key}』物理定錨引用支撐。"
        cursor.execute("""
        INSERT OR IGNORE INTO manuscript_citations (manuscript_id, paper_id, citation_context, meta_data)
        VALUES (?, ?, ?, ?);
        """, (manuscript_id, paper_id, citation_context, None))
        if cursor.rowcount > 0:
            inserted_count += 1
            
    conn.commit()
    print(f"💾 大腦引文定錨成功！累計將 {inserted_count} 筆新引文綁定至手稿 {manuscript_id} 下！")
    
    # 3. 撈取所有已綁定論文的 BibTeX，並拼裝成 references.bib
    cursor.execute("""
    SELECT p.cite_key, p.bibtex 
    FROM papers p
    JOIN manuscript_citations c ON p.paper_id = c.paper_id
    WHERE c.manuscript_id = ?
    """, (manuscript_id,))
    bibtex_entries = cursor.fetchall()
    
    print(f"🚀 正在自動拼裝 references.bib，目前已綁定引文總數：{len(bibtex_entries)} 篇...")
    
    bib_content = "% ==============================================================================\n"
    bib_content += f"% 哈爸主權大腦自動生成 BibTeX 參考文獻庫 - references.bib\n"
    bib_content += f"% 生成時間: 2026-05-26\n"
    bib_content += f"% 手稿定錨 ID: {manuscript_id}\n"
    bib_content += "% ==============================================================================\n\n"
    
    for cite_key, bibtex in bibtex_entries:
        bib_content += f"% Cite Key: {cite_key}\n"
        bib_content += bibtex.strip() + "\n\n"
        
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(bib_content)
        
    conn.close()
    print(f"🎉 學術標準參考文獻庫導出成功！")
    print(f"  - 實體路徑：{bib_path}")
    print(f"  - 累計寫入條目：{len(bibtex_entries)} 筆\n")

if __name__ == "__main__":
    anchor_and_export()
