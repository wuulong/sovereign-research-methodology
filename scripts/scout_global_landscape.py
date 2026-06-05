#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 全局觀對合檢索與文獻厚化工具 (scout_global_landscape.py)

目的：
1. 對齊 12 大核心 Claims，發動四大理論支柱的精準 ArXiv 在線探勘。
2. 自動解析並以 Stage 1 猜想落庫至 `top_sovereign_methodology` 主題。
3. 根據支柱類型自動生成極具學術硬度的 preliminary_relevance。
"""

import os
import sqlite3
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
import time

def scout_global_landscape():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    # 建立四大理論支柱的雷達檢索矩陣
    pillars = {
        "PILLAR_1_SOVEREIGNTY": [
            ('all:"cognitive offloading" AND all:"language model" AND all:"dependency"', "認知依賴性"),
            ('all:"epistemic vigilance" AND all:"artificial intelligence" AND all:"trust"', "認識警覺度")
        ],
        "PILLAR_2_PHYSICAL": [
            ('("physics-informed" OR "in-situ validation") AND "large language model"', "物理現地真值"),
            ('all:"physical constraints" AND all:"generative AI" AND all:"scientific discovery"', "物理約束生成")
        ],
        "PILLAR_3_INTEGRITY": [
            ('all:"academic integrity" AND all:"generative AI" AND all:"plagiarism"', "學術誠信評估"),
            ('all:"audit trail" AND all:"generative AI" AND all:"provenance"', "資料庫物理審計")
        ],
        "PILLAR_4_FEDERATED": [
            ('all:"personal knowledge graph" AND all:"collaborative" AND all:"version control"', "個人知識圖譜協同"),
            ('all:"metadata provenance" AND all:"Git" AND all:"JSON"', "聯邦 DTO 合流")
        ]
    }
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    total_found = 0
    total_inserted = 0
    
    print("🛰️ [GAES 戰役啟動] 正在發起全局觀對合三維合擊探勘...")
    
    for pillar_key, queries in pillars.items():
        print(f"\n==================================================")
        print(f"🔥 探勘支柱：{pillar_key}")
        print(f"==================================================")
        
        for query_str, query_desc in queries:
            print(f"🔍 雷達鎖定【{query_desc}】檢索中：{query_str}")
            
            encoded_query = urllib.parse.quote(query_str)
            url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&max_results=3"
            
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as response:
                    xml_data = response.read()
                    
                root = ET.fromstring(xml_data)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                entries = root.findall('atom:entry', ns)
                
                if not entries:
                    print(f"  [-] 未檢索到相關文獻。")
                    continue
                    
                print(f"  [+] 成功捕獲 {len(entries)} 筆真實 SOTA 前沿文獻！正在解析落庫...")
                total_found += len(entries)
                
                # 建立 Ingestion 採集任務 (Lineage)
                task_id = f"task_gaes_{pillar_key.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                cursor.execute("""
                INSERT OR IGNORE INTO exploration_tasks (task_id, query, status, papers_found, agent_version, error_log, meta_data)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """, (
                    task_id,
                    query_str,
                    "ONLINE",
                    len(entries),
                    "Antigravity-v2.0-GAES-LandscapeScout",
                    None,
                    json.dumps({"engine": "arXiv_API", "pillar": pillar_key, "run_at": datetime.now().isoformat()}, ensure_ascii=False)
                ))
                
                inserted_count = 0
                for entry in entries:
                    id_url = entry.find('atom:id', ns).text.strip()
                    arxiv_id = id_url.split('/abs/')[-1].split('v')[0]
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                    abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                    
                    authors_nodes = entry.findall('atom:author', ns)
                    authors_list = [node.find('atom:name', ns).text.strip() for node in authors_nodes]
                    authors = ", ".join(authors_list)
                    
                    published_str = entry.find('atom:published', ns).text.strip()
                    year = int(published_str[:4])
                    
                    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                    
                    # 建立 cite_key
                    first_author = authors_list[0].split()[-1] if authors_list else "Unknown"
                    first_author = "".join(c for c in first_author if c.isalnum())
                    cite_key = f"arxiv_{first_author}_{year}_{arxiv_id[:4]}"
                    paper_id = f"arxiv_meta_{arxiv_id}"
                    
                    # 生成 BibTeX
                    bibtex = f"""@article{{{cite_key},
  author = {{{authors}}},
  title = {{{title}}},
  journal = {{arXiv preprint arXiv:{arxiv_id}}},
  year = {{{year}}}
}}"""

                    # 根據支柱自動生成對合大膽猜想
                    preliminary_relevance = ""
                    if pillar_key == "PILLAR_1_SOVEREIGNTY":
                        preliminary_relevance = (
                            f"大膽猜想：本篇探討 AI 輔助下的思維依賴與認識警覺。本論文可在第一章背景與第二章 2.1 節『認知卸載思維邊界』中將其作為"
                            f"學術 Baseline，深入論證在缺乏大腦主權工具時大腦會喪失思維主權，為 $F_s$ Socratic 自審防線提供堅固理論支撐。"
                        )
                    elif pillar_key == "PILLAR_2_PHYSICAL":
                        preliminary_relevance = (
                            f"大膽猜想：本篇探討語言模型中的 In-situ 實體現地真值校準與物理约束。本論文可在第三章 3.2 節『肉身實踐與真值定錨』中"
                            f"做為核心對合 Baseline，論證我們利用 SQLite 中的實測物理誤差比對來剪枝 LLM 幻覺，具備硬核的工程學與物理學正當性。"
                        )
                    elif pillar_key == "PILLAR_3_INTEGRITY":
                        preliminary_relevance = (
                            f"大膽猜想：本篇探討生成式 AI 普及給學術評估與誠信帶來的變革與挑戰。本論文可在第四章 4.1 節『導師的 SQL 照妖鏡』中將其作為"
                            f"教學法現實背景，論證為了重建師生學術信任，建立基於 SQLite 資料庫物理審計 (Physical SQL audit trail) 盲檢的必然性與緊迫性。"
                        )
                    elif pillar_key == "PILLAR_4_FEDERATED":
                        preliminary_relevance = (
                            f"大膽猜想：本篇探討去中心化協同個人知識管理。本論文可在第四章 4.2 節與 4.3 節『聯邦 DTO 重建與知識遺傳』中做為核心技術"
                            f"Baseline，證明以純文字 JSON 貢獻包為載體合流個人 PKGs，在消滅 Git 二進位衝突與實現跳躍式知識傳承上的物理可行性。"
                        )

                    cursor.execute("""
                    INSERT OR IGNORE INTO papers (
                        paper_id, task_id, topic_id, title, authors, year, core_method, cite_key, bibtex, meta_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """, (
                        paper_id,
                        task_id,
                        "top_sovereign_methodology",
                        title,
                        authors,
                        year,
                        f"GAES-{query_desc}",
                        cite_key,
                        bibtex,
                        json.dumps({
                            "stage": "STAGE_1_PRELIMINARY",
                            "preliminary_relevance": preliminary_relevance,
                            "abstract_snippet": abstract[:300] + "...",
                            "source": f"arXiv_gaes_{pillar_key.lower()}"
                        }, ensure_ascii=False)
                    ))
                    
                    if cursor.rowcount > 0:
                        inserted_count += 1
                        # 寫入 URL
                        cursor.execute("""
                        INSERT OR IGNORE INTO paper_urls (
                            url_id, paper_id, root_key, url_link, url_type, download_status, file_size_bytes, meta_data
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                        """, (
                            f"url_{paper_id}_pdf",
                            paper_id,
                            "remote_url",
                            pdf_url,
                            "arxiv_pdf",
                            "PENDING",
                            0,
                            json.dumps({"online_discovered": True}, ensure_ascii=False)
                        ))
                        
                conn.commit()
                print(f"  [+] 成功解析並落庫 {inserted_count} 筆新前沿文獻！")
                total_inserted += inserted_count
                
                # 遵循 API 禮貌，暫停 2 秒
                time.sleep(2)
                
            except Exception as e:
                print(f"  ⚠️ 檢索時連線超時或失敗 ({e})，跳過。")
                
    conn.close()
    print(f"\n==================================================")
    print(f"🎉 GAES 全局觀探勘戰役圓滿成功！")
    print(f"  - 累計捕獲線上文獻：{total_found} 篇")
    print(f"  - 累計實體落庫新前沿文獻：{total_inserted} 篇")
    print(f"==================================================")

if __name__ == "__main__":
    scout_global_landscape()
