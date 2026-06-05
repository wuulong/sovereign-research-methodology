#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 去中心化協同個人知識圖譜線上探勘與落庫工具 (scout_decentralized_papers.py)

目的：
1. 線上檢索 ArXiv 關於 "personal knowledge graph" 與 "collaborative" 的前沿論文。
2. 自動落庫至 `top_sovereign_methodology` 主題下，填補大腦的文獻真空盲區。
"""

import os
import sqlite3
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

def query_and_save_decentralized_papers():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    # 探勘關鍵字設計 (雷達精準鎖定)
    query_str = 'all:"personal knowledge graph" AND all:"collaborative"'
    print(f"🚀 [PSIV 雷達啟動] 正在 ArXiv 檢索：{query_str}")
    
    encoded_query = urllib.parse.quote(query_str)
    url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&max_results=5"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns)
        
        if not entries:
            # 降級嘗試更廣泛的詞組
            print("[o] 精準詞組無結果，降級嘗試較廣泛組合...")
            query_str = 'all:"personal knowledge" AND all:"decentralized"'
            encoded_query = urllib.parse.quote(query_str)
            url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&max_results=5"
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=15) as response:
                xml_data = response.read()
            root = ET.fromstring(xml_data)
            entries = root.findall('atom:entry', ns)
            
        if not entries:
            print("[-] 線上檢索未返回任何結果，降級回報。")
            return False
            
        print(f"[+] 成功捕獲 {len(entries)} 筆去中心化/協作個人知識庫相關文獻！正在進行結構化落庫...")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # 建立 Ingestion 採集任務 (Lineage)
        task_id = f"task_meta_scout_decent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cursor.execute("""
        INSERT INTO exploration_tasks (task_id, query, status, papers_found, agent_version, error_log, meta_data)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            task_id,
            query_str,
            "ONLINE",
            len(entries),
            "Antigravity-v2.0-PSIV-DecentralizedScout",
            None,
            json.dumps({"engine": "arXiv_API", "target_topic": "top_sovereign_methodology", "run_at": datetime.now().isoformat()}, ensure_ascii=False)
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
                "去中心化個人知識協同",
                cite_key,
                bibtex,
                json.dumps({
                    "stage": "STAGE_1_PRELIMINARY",
                    "preliminary_relevance": f"大膽猜想：本篇探討去中心化或個人知識協同，可用於第四章 4.2 節『去中心化聯邦 DTO 重建』與 4.3 節『跳躍式知識遺傳』中，作為學術大腦合流的技術理論支撐，證明多裝置/多研究者共有知識圖譜的物理可行性。",
                    "abstract_snippet": abstract[:300] + "...",
                    "source": "arXiv_decentral_scout"
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
        conn.close()
        print(f"💾 大腦落庫成功！累計新增 {inserted_count} 筆真實去中心化協同個人知識庫相關論文至 `top_sovereign_methodology` 主題下！\n")
        return True
    except Exception as e:
        print(f"⚠️ 線上 API 連線超時或失敗 ({e})，降級回報。")
        return False

if __name__ == "__main__":
    query_and_save_decentralized_papers()
