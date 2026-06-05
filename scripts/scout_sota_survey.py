#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - SOTA 綜述文獻線上探勘與落庫工具 (scout_sota_survey.py)

目的：
1. 線上檢索 ArXiv 上的 SOTA 綜述 arXiv:2508.14111 并精準落庫。
2. 作為手稿中對比 SOTA「自主科學代理」的核心 Baseline。
"""

import os
import sqlite3
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def scout_sota():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    arxiv_id = "2508.14111"
    print(f"🚀 [雷達鎖定 SOTA 綜述] 正在從 ArXiv 擷取：{arxiv_id}")
    
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entry = root.find('atom:entry', ns)
        
        if entry is None:
            print("[-] 未能擷取到該 SOTA 綜述。")
            return False
            
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        
        authors_nodes = entry.findall('atom:author', ns)
        authors_list = [node.find('atom:name', ns).text.strip() for node in authors_nodes]
        authors = ", ".join(authors_list)
        
        year = 2025
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        
        cite_key = f"arxiv_AgenticScience_2025_{arxiv_id.split('.')[1][:5]}"
        paper_id = f"arxiv_meta_{arxiv_id}"
        
        bibtex = f"""@article{{{cite_key},
  author = {{{authors}}},
  title = {{{title}}},
  journal = {{arXiv preprint arXiv:{arxiv_id}}},
  year = {{{year}}}
}}"""

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # 註冊 Ingestion 任務
        task_id = f"task_meta_scout_sota_20260526"
        cursor.execute("""
        INSERT OR IGNORE INTO exploration_tasks (task_id, query, status, papers_found, agent_version, error_log, meta_data)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            task_id,
            f"id_list:{arxiv_id}",
            "ONLINE",
            1,
            "Antigravity-v2.0-SOTA-SurveyScout",
            None,
            json.dumps({"target": "AgenticScience_Survey"}, ensure_ascii=False)
        ))
        
        preliminary_relevance = (
            "大膽猜想：本篇為 2025 年最新、最權威的『自主科學發現代理 (Autonomous Scientific Discovery / Agentic Science)』SOTA 綜述。"
            "本論文可在第二章 2.3 節『 AI 作為討論對象與實踐手腳的雙重定位』中將其作為最核心的對比 Baseline，"
            "詳細論證現有 SOTA 框架（如 STORM、ChemCrow）在完全委派 (Black Box Full Delegation) 下造成的『思維主權喪失』，"
            "進而凸顯哈爸大腦『死守主權、Socratic 自審答辯與 Verdict Lock 品位裁決』在真實戰壕研究中的終極優勢。"
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
            "Agentic Science 學術綜述與 SOTA 比對",
            cite_key,
            bibtex,
            json.dumps({
                "stage": "STAGE_1_PRELIMINARY",
                "preliminary_relevance": preliminary_relevance,
                "abstract_snippet": abstract[:300] + "...",
                "source": "arXiv_sota_survey_scout"
            }, ensure_ascii=False)
        ))
        
        if cursor.rowcount > 0:
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
            print(f"[+] 成功引渡 SOTA 綜述文獻落庫：{cite_key}")
            
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[-] 線上 API 連線超時或失敗 ({e})，降級跳過。")
        return False

if __name__ == "__main__":
    scout_sota()
