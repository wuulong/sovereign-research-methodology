#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
學術引用傳播與實體化萃取工具 (extract_citations_to_records.py)

目的：
- 讀取指定 papers.paper_id 的 meta_data.citations。
- 依據引用數與當前研究主題的匹配度，動態計量學術重力偏置。
- 篩選出 Top 3 篇高價值文獻，自動將其「升格實體化」寫入 papers 與 paper_urls 資料表（狀態設為 PENDING）。
- 擴充大腦待探索文獻池，開啟無摩擦的學術迭代閱讀輪盤！
"""

import os
import sys
import sqlite3
import json
import re
import math
from datetime import datetime

# 研究主題敏感關鍵字加權定義
THEME_KEYWORDS = ["Personal AI", "Sovereign AI", "Agentic Science", "Communicative Agents", "CAG", "LLM", "Multi-Agent", "Workflow", "RAG", "Science", "Discovery"]

def calculate_academic_gravity(title, citation_count, year):
    """
    動態計量引用文獻的學術重力評分
    """
    # 1. 基準引用數得分：使用對數計量防止極端偏置 (Base = log10(citation_count + 1))
    citation_score = math.log10(citation_count + 1) * 2.0 if citation_count else 3.0
    
    # 2. 主題關鍵字匹配加權 (+2.0 分/個)
    theme_score = 0.0
    matched_keywords = []
    for kw in THEME_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', title, re.IGNORECASE):
            theme_score += 2.0
            matched_keywords.append(kw)
            
    # 3. 年份前沿性加權 (+1.5 分，若發表於 2024 及之後)
    recency_score = 0.0
    if year:
        if year >= 2024:
            recency_score = 1.5
        elif year >= 2020:
            recency_score = 0.5
            
    total_gravity = citation_score + theme_score + recency_score
    return round(total_gravity, 2), matched_keywords

def clean_authors_to_citekey(authors_str):
    """
    將作者文字清洗為符合 BibTeX 規範的單字（如 Liu）
    """
    if not authors_str:
        return "Unknown"
    # 拿第一個作者
    first_author = authors_str.split(";")[0].split(",")[0].strip()
    # 排除特殊字元
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', first_author)
    return clean_name if clean_name else "Unknown"

def auto_classify_and_tag_paper(conn, paper_id, title, cite_key):
    """
    雙軌分類自動化標記：
    1. 平面式標籤：提取核心關鍵字（如 LLM, RAG, CAG）寫入 paper_tags。
    2. 階層式標籤：根據關鍵字匹配，決定階層分類，剛性比對 taxonomy_framework 前綴，安全寫入。
    """
    cursor = conn.cursor()
    
    # 預設關鍵字與階層匹配關係
    mapping = [
        ("Agentic Science", "AI應用/個人賦能/智能體科學", ["Agentic Science", "Autonomous Discovery"]),
        ("LLaVA", "AI應用/個人賦能/主權治理", ["Visual Instruction Tuning", "LLaVA", "Multimodal"]),
        ("CAMEL", "AI應用/個人賦能/角色交談", ["Communicative Agents", "CAMEL", "Role-Playing"]),
        ("DeepSeek-R1", "AI應用/推理模型/強化學習", ["DeepSeek-R1", "Reinforcement Learning", "Reasoning"]),
        ("CAG", "AI應用/企業轉型/CAG快取", ["CAG", "Cache-Augmented Generation", "KV Cache"]),
        ("RAGAS", "AI應用/企業轉型/RAG評估", ["RAGAS", "Retrieval-Augmented Generation", "Evaluation"]),
        ("Cosmos", "水文河流/多模態觀測/世界模型", ["Cosmos", "World Model", "Physical Simulator"]),
        ("WalkGIS", "水文河流/GIS圖資/現地走讀", ["WalkGIS", "DEM", "River basin"])
    ]
    
    assigned_hierarchical = None
    flat_keywords = []
    
    # 1. 匹配分析
    for aspect, hierarchical_tag, keywords in mapping:
        # 比對 title 或 cite_key
        match = False
        if re.search(re.escape(aspect), title, re.IGNORECASE) or re.search(re.escape(aspect), cite_key, re.IGNORECASE):
            match = True
        else:
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', title, re.IGNORECASE):
                    match = True
                    break
        if match:
            assigned_hierarchical = hierarchical_tag
            flat_keywords.extend(keywords)
            break
            
    # 預設 Fallback 階層
    if not assigned_hierarchical:
        assigned_hierarchical = "AI應用/個人賦能/未分類"
        flat_keywords.extend(["Research", "Sovereign"])
        
    # 2. 剛性前綴檢驗 (防禦語意漂移)
    prefix = "/".join(assigned_hierarchical.split("/")[:2])
    cursor.execute("SELECT path FROM taxonomy_framework WHERE path = ?;", (prefix,))
    if not cursor.fetchone():
        assigned_hierarchical = "AI應用/個人賦能/未分類"
        
    # 3. 寫入 paper_tags 表
    try:
        # 寫入階層式標籤
        cursor.execute("""
            INSERT OR REPLACE INTO paper_tags (paper_id, tag_name, meta_data)
            VALUES (?, ?, ?);
        """, (paper_id, assigned_hierarchical, json.dumps({"type": "hierarchical", "assigned_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}, ensure_ascii=False)))
        
        # 寫入平面關鍵字
        for kw in set(flat_keywords):
            cursor.execute("""
                INSERT OR REPLACE INTO paper_tags (paper_id, tag_name, meta_data)
                VALUES (?, ?, ?);
            """, (paper_id, kw, json.dumps({"type": "flat", "assigned_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}, ensure_ascii=False)))
            
        print(f"  ➔ 🕵️‍♂️ 成功自動為新文獻 [{cite_key}] 打上階層標籤 '{assigned_hierarchical}'")
    except Exception as e:
        print(f"  [!] 寫入雙軌分類標籤失敗: {e}")


def main():
    if len(sys.argv) < 2:
        print("💡 使用說明 (Usage):")
        print("  python3 extract_citations_to_records.py [paper_id] (例如 zotero_471)")
        sys.exit(1)
        
    source_paper_id = sys.argv[1]
    
    base_dir = "/Users/wuulong/github/bmad-pa"
    db_path = os.path.join(base_dir, "events", "my_research", "data", "Research_Artifacts.db")
    
    if not os.path.exists(db_path):
        print(f"[!] 大腦資料庫不存在: {db_path}")
        sys.exit(1)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. 讀取來源 paper 的基本資料與 meta_data
    cursor.execute("""
        SELECT paper_id, cite_key, title, task_id, topic_id, meta_data 
        FROM papers 
        WHERE paper_id = ? OR cite_key = ?;
    """, (source_paper_id, source_paper_id))
    
    row = cursor.fetchone()
    if not row:
        print(f"[!] 找不到來源文獻: {source_paper_id}")
        conn.close()
        sys.exit(1)
        
    paper_id, cite_key, title, source_task_id, source_topic_id, meta_str = row
    print(f"📖 讀取來源文獻: [{cite_key}] {title}")
    print(f"  - 繼承 Ingestion 採集血統 (Task ID) : {source_task_id}")
    print(f"  - 繼承 子主題邏輯定錨 (Topic ID) : {source_topic_id}")
    
    meta = {}
    if meta_str:
        try:
            meta = json.loads(meta_str)
        except:
            pass
            
    citations = meta.get("citations", [])
    if not citations:
        print(f"[!] 該文獻的 meta_data 中無暫存之 citations 清單。請先對該文獻執行資產就位收集！")
        conn.close()
        sys.exit(1)
        
    print(f"  ➔ 🕵️‍♂️ 成功在 meta_data 中偵測到 {len(citations)} 筆引用文獻。")
    print(f"  ⚙️ 正在進行學術重力計量與主題對合...")
    
    # 2. 對所有引用進行計量與排序
    evaluated_citations = []
    for index, ref in enumerate(citations):
        ref_title = ref.get("title", "").strip()
        if not ref_title:
            continue
            
        citation_count = ref.get("citationCount", 0)
        year = ref.get("year")
        authors = ref.get("authors", "").strip()
        venue = ref.get("venue", "").strip()
        
        gravity, matched_kws = calculate_academic_gravity(ref_title, citation_count, year)
        
        evaluated_citations.append({
            "raw_index": index,
            "title": ref_title,
            "authors": authors if authors else "Unknown",
            "year": year if year else 2025,
            "venue": venue if venue else "Unknown",
            "citation_count": citation_count,
            "gravity": gravity,
            "matched_keywords": matched_kws
        })
        
    # 依據學術重力從高到低排序
    evaluated_citations.sort(key=lambda x: x["gravity"], reverse=True)
    
    # 3. 挑選 Top 3 進行升格實體化
    top_n = 3
    promoted_citations = evaluated_citations[:top_n]
    
    print(f"\n🏆 學術重力篩選 Top {top_n} 升格候選文獻：")
    print("-" * 100)
    for idx, pc in enumerate(promoted_citations):
        print(f"  [{idx+1}] 重力: {pc['gravity']} | 引用數: {pc['citation_count']} | 年份: {pc['year']}")
        print(f"      標題: {pc['title']}")
        if pc['matched_keywords']:
            print(f"      主題對合: {', '.join(pc['matched_keywords'])}")
        print("-" * 100)
        
    print(f"\n🌊 開始執行資料庫實體化灌溉與 DTO 合流...")
    
    try:
        promoted_count = 0
        duplicate_count = 0
        
        for pc in promoted_citations:
            # 依據作者與年份生成 cite_key 與 paper_id
            author_clean = clean_authors_to_citekey(pc["authors"])
            year_str = str(pc["year"])
            
            # 命名規範：zotero_extracted_Author_Year_Hash
            title_hash = str(abs(hash(pc["title"])) % 1000)
            target_cite_key = f"zotero_extracted_{author_clean}_{year_str}_{title_hash}"
            target_paper_id = f"zotero_extracted_{author_clean}_{year_str}_{title_hash}"
            
            # 檢查是否已存在
            cursor.execute("SELECT paper_id FROM papers WHERE cite_key = ? OR title = ?;", (target_cite_key, pc["title"]))
            if cursor.fetchone():
                duplicate_count += 1
                continue
                
            # 組裝 BibTeX 骨架
            bibtex_skeleton = f"""@article{{{target_cite_key},
  title = {{{pc['title']}}},
  author = {{{pc['authors']}}},
  year = {{{pc['year']}}},
  journal = {{{pc['venue']}}}
}}"""
            
            # 組裝 compliance_status 與 preliminary_relevance
            new_meta = {
                "compliance_status": {
                    "is_compliant": False,
                    "checked_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "missing_fields": ["paper_extraction"],
                    "validation_message": "Stage 2 Deep factors not deconstructed yet | Extracted from citations"
                },
                "stage": "STAGE_1_PRELIMINARY",
                "preliminary_relevance": f"由經典文獻 [{cite_key}] 的 Citations 清單中自動學術重力加權升格。原論文重力評估得分為 {pc['gravity']} 分，主題對合關鍵字：{', '.join(pc['matched_keywords'])}。",
                "academic_prestige": {
                    "citation_count": pc["citation_count"],
                    "venue_name": pc["venue"],
                    "venue_tier": "Normal_Journal",
                    "venue_bias_applied": 0.0,
                    "institution_name": "Unknown",
                    "institution_tier": "Tier_3_Normal",
                    "institution_bias_applied": 0.0,
                    "academic_gravity_score": pc["gravity"],
                    "hydration_source": "extracted_citation_propagation"
                }
            }
            
            # 1. 寫入 papers 表
            cursor.execute("""
                INSERT INTO papers (
                    paper_id, task_id, topic_id, title, authors, year, cite_key, bibtex, meta_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                target_paper_id,
                source_task_id,
                source_topic_id,
                pc["title"],
                pc["authors"],
                pc["year"],
                target_cite_key,
                bibtex_skeleton,
                json.dumps(new_meta, ensure_ascii=False)
            ))
            
            # 2. 寫入 paper_urls 表 (標註為 PENDING 狀態，待未來就位下載)
            url_id = f"url_local_{target_paper_id.lower()}"
            cursor.execute("""
                INSERT INTO paper_urls (
                    url_id, paper_id, root_key, url_link, url_type, download_status, file_size_bytes, meta_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                url_id,
                target_paper_id,
                "workspace_root",
                "",  # 本地 PDF 鏈結先留空
                "local_pdf",
                "PENDING",
                0,
                json.dumps({"description": f"由 {cite_key} 的 citations 傳播生成，待下載探勘"})
            ))
            
            # 3. 自動進行雙軌分類與標籤對合
            auto_classify_and_tag_paper(conn, target_paper_id, pc["title"], target_cite_key)
            
            promoted_count += 1
            print(f"  ➔ 🎉 成功實體化升格: [{target_cite_key}]")
            
        conn.commit()
        print(f"\n🎉 引用文獻實體化大合流完成！")
        print(f"  - 成功升格寫入: {promoted_count} 篇新文獻")
        print(f"  - 排除重複文獻: {duplicate_count} 篇")
        print(f"  - 所有新升格文獻已被標記為 'PENDING'，且其 preliminary_relevance 物理定錨完成！")
        
    except Exception as e:
        conn.rollback()
        print(f"[!] 實體化合流失敗: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
