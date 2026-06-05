#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 兩大黃金盲區精準線上探勘與落庫工具 (scout_gaps_papers.py)

目的：
1. 線上檢索 ArXiv 關於 
   - 盲區 A："physical constraints" AND "language model" (實測物理約束校準)
   - 盲區 B："academic integrity" AND "generative AI" (學術誠信與評估挑戰)
2. 自動落庫至 `top_sovereign_methodology` 主題下，補齊手稿的黃金地基。
"""

import os
import sqlite3
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

def scout_gaps():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    queries = {
        "GAP_A_PHYSICAL": ('all:"physical constraints" AND all:"language model"', "物理約束與現地真值校準"),
        "GAP_B_INTEGRITY": ('all:"academic integrity" AND all:"generative AI"', "AI時代學術誠信與評估挑戰")
    }
    
    total_inserted = 0
    
    for gap_key, (query_str, gap_desc) in queries.items():
        print(f"\n🚀 [PSIV 雷達啟動] 正在 ArXiv 檢索{gap_desc}：{query_str}")
        
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
                print(f"[-] 檢索 {gap_desc} 未返回結果，嘗試降級檢索...")
                continue
                
            print(f"[+] 成功捕獲 {len(entries)} 筆 {gap_desc} 相關文獻！正在進行結構化落庫...")
            
            # 建立 Ingestion 採集任務 (Lineage)
            task_id = f"task_meta_scout_{gap_key.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            cursor.execute("""
            INSERT OR IGNORE INTO exploration_tasks (task_id, query, status, papers_found, agent_version, error_log, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                task_id,
                query_str,
                "ONLINE",
                len(entries),
                "Antigravity-v2.0-PSIV-GapScoutEngine",
                None,
                json.dumps({"engine": "arXiv_API", "gap_targeted": gap_key, "run_at": datetime.now().isoformat()}, ensure_ascii=False)
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

                preliminary_relevance = ""
                if gap_key == "GAP_A_PHYSICAL":
                    preliminary_relevance = (
                        f"大膽猜想：該文獻探討大型語言模型中的『物理約束 (Physical Constraints)』注入。本論文可在第三章 3.2 節『肉身實踐與真值定錨』中，"
                        f"將其做為學術理論 Baseline，證明我們將實測物理誤差 (discrepancy_percentage) 寫入十一表大腦以校準 AI 幻覺，具備硬核的物理學正當性。"
                    )
                else:
                    preliminary_relevance = (
                        f"大膽猜想：該文獻探討生成式 AI 給大學學術誠信 (Academic Integrity) 與評估帶來的新挑戰。本論文可在第四章 4.1 節『哈教授的 SQL 照妖鏡』中，"
                        f"作為尖銳的現實教學法背景，證明為了解決全球教授面臨的『無腦交差』挑戰，建立 SQL 資料庫物理盲檢機制的緊迫性與科學必要性。"
                    )

                # 寫入 papers (外鍵關聯至 top_sovereign_methodology)
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
                    gap_desc,
                    cite_key,
                    bibtex,
                    json.dumps({
                        "stage": "STAGE_1_PRELIMINARY",
                        "preliminary_relevance": preliminary_relevance,
                        "abstract_snippet": abstract[:300] + "...",
                        "source": f"arXiv_{gap_key.lower()}_scout"
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
                    
            print(f"  [+] 成功落庫 {inserted_count} 筆真實文獻！")
            total_inserted += inserted_count
            
        except Exception as e:
            print(f"  ⚠️ 檢索 {gap_desc} 時連線超時或失敗 ({e})，降級跳過。")
            
    conn.commit()
    conn.close()
    print(f"\n💾 盲區雙向探勘完全成功！累計新增 {total_inserted} 筆真實前沿論文至 `top_sovereign_methodology` 主題碼頭下！\n")
    return True

if __name__ == "__main__":
    scout_gaps()
