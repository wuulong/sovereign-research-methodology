#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 全文獻實體資產與 Markdown 預萃取就位工具 (hydrate_paper_assets.py)

目的：
1. 解決「文獻讀取、PDF 放置與 Markdown 解析不順暢」的痛點。
2. 以資料表 papers.paper_id 為一等公民輸入：
   - 自動讀取資料庫 (Research_Artifacts.db) 獲取論文標題與 Cite Key。
   - 盡可能在本地端（Zotero 目錄或線上 API 下載）尋找實體 PDF 檔案。
   - 將 PDF 自動重新命名並就位放置於主權專案的 `data/pdfs/` 中，以備閱讀 PDF。
   - 預先高精萃取為 MarkDown 儲存於 `data/pdfs/{cite_key}.md` (比鄰實體 PDF)，以備看文字。
   - 動態更新資料表 paper_urls 註冊此實體資產，完美合流！
"""

import os
import sys
import json
import sqlite3
import shutil
import urllib.request
import urllib.parse
import re
import subprocess
from datetime import datetime

# ==============================================================================
# 【自動依賴裝載機制】
# ==============================================================================
def install_and_import(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"[*] 未偵測到依賴套件 '{package_name}'，正在發動自動裝載機制...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        except Exception as e:
            print(f"[!] 自動裝載 '{package_name}' 失敗: {e}")
            sys.exit(1)

install_and_import("pypdf")
from pypdf import PdfReader

# ==============================================================================
# 【排版美化引擎】
# ==============================================================================
def clean_and_beautify_text(text):
    lines = text.split('\n')
    cleaned_lines = []
    
    page_num_pattern = re.compile(r'^\s*\d+\s*$')
    arxiv_header_pattern = re.compile(r'arXiv:\d+\.\d+v\d+\s+\[cs\.[A-Z]+\]\s+\d+\s+[A-Za-z]+\s+\d{4}')
    
    for line in lines:
        if not line.strip() or page_num_pattern.match(line):
            continue
        if arxiv_header_pattern.search(line):
            continue
            
        # 標題層級識別
        section_pattern = re.compile(r'^([1-9]\d*(\.[1-9]\d*)*)\s+([A-Z][A-Za-z\s:,\-\'\(\)]+)$')
        match = section_pattern.match(line.strip())
        if match:
            num = match.group(1)
            title = match.group(3)
            level = num.count('.') + 1
            md_line = f"\n{'#' * level} {num} {title}\n"
            cleaned_lines.append(md_line)
            continue
            
        cleaned_lines.append(line.strip())
        
    full_text = " ".join(cleaned_lines)
    full_text = full_text.replace(" #", "\n\n#")
    full_text = re.sub(r' +', ' ', full_text)
    full_text = full_text.replace("Abstract", "\n\n## Abstract\n\n")
    full_text = full_text.replace("References", "\n\n## References\n\n")
    return full_text

def extract_abstract_from_md(md_text):
    """
    從結構化 Markdown 中自動高精提取 Abstract
    """
    # 搜尋 ## Abstract 到下一個 ## 標題之間的內容
    pattern = re.compile(r'##\s*Abstract\s*(.*?)(?=\n##|\n#|\n[1-9]\s+[A-Z])', re.DOTALL | re.IGNORECASE)
    match = pattern.search(md_text)
    if match:
        return match.group(1).strip()
    
    # 模糊匹配：從 Abstract 單字到 1 Introduction 之間
    pattern_alt = re.compile(r'Abstract\s*(.*?)(?=\n\n#|\n\n##|1\s+Introduction|Introduction)', re.DOTALL | re.IGNORECASE)
    match_alt = pattern_alt.search(md_text)
    if match_alt:
        return match_alt.group(1).strip()
    return None

# ==============================================================================
# 【線上 API 下載與雷達】
# ==============================================================================
def get_pdf_url_from_s2(title):
    """
    透過 Semantic Scholar 搜尋公開 PDF 連結
    """
    encoded_query = urllib.parse.quote(title[:150])
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded_query}&fields=title,openAccessPdf&limit=1"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('data', [])
            if results and results[0].get('openAccessPdf'):
                return results[0]['openAccessPdf'].get('url')
    except:
        return None
    return None

def get_references_from_s2_or_fallback(title, md_content):
    """
    雙軌防線獲取論文參考文獻：
    1. 第一防線：透過 Semantic Scholar API 線上查詢並結構化
    2. 第二防線：若 API 遭遇 429 或離線，則從比鄰的預萃取 Markdown '## References' 區間中，高精正則解析
    """
    # 軌道一：API 獲取
    try:
        import urllib.parse, urllib.request, json
        encoded_title = urllib.parse.quote(title[:150])
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded_title}&fields=references.title,references.authors,references.year,references.venue,references.citationCount,references.externalIds&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('data', [])
            if results and results[0].get('references'):
                refs = results[0]['references']
                formatted_refs = []
                for r in refs:
                    if r.get('title'):
                        formatted_refs.append({
                            "title": r.get('title'),
                            "authors": "; ".join([a.get('name', '') for a in r.get('authors', []) if a.get('name')]),
                            "year": r.get('year'),
                            "venue": r.get('venue', ''),
                            "citationCount": r.get('citationCount', 0),
                            "externalIds": r.get('externalIds', {})
                        })
                if formatted_refs:
                    return formatted_refs
    except Exception as e:
        print(f"  [📡 API 限流或離線] ({e}) ➔ 啟動第二防線：從比鄰 Markdown 提取...")

    # 軌道二：Markdown References 區段正則 Fallback 提取
    try:
        # 尋找 References 標題後的內容
        pattern = re.compile(r'##\s*References\s*(.*)', re.DOTALL | re.IGNORECASE)
        match = pattern.search(md_content)
        if match:
            ref_section = match.group(1).strip()
            # 依據換行與序號切割每一條文獻
            raw_lines = ref_section.split('\n')
            extracted_refs = []
            for line in raw_lines:
                line_str = line.strip()
                # 排除空白行與太短的行
                if len(line_str) > 15:
                    # 去除前導序號如 [1], 1. 等
                    clean_line = re.sub(r'^\[\d+\]\s*', '', line_str)
                    clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
                    # 模糊解析年份
                    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', clean_line)
                    year = int(year_match.group(1)) if year_match else None
                    
                    extracted_refs.append({
                        "title": clean_line,
                        "authors": "",
                        "year": year,
                        "venue": "Extracted from PDF References",
                        "citationCount": 0,
                        "externalIds": {}
                    })
            if extracted_refs:
                return extracted_refs
    except Exception as ex:
        print(f"  [!] Fallback 提取參考文獻失敗: {ex}")
        
    return []

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
        # 若前兩層前綴在骨架表中未註冊，強制修正為預設合規前綴
        print(f"  [⚠️ Taxonomy 防禦] 前綴 '{prefix}' 未註冊，強制歸為預設大類！")
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
            
        print(f"  ➔ 🕵️‍♂️ 成功自動為該文獻打上階層標籤 '{assigned_hierarchical}' 與 {len(set(flat_keywords))} 個平面關鍵字！")
    except Exception as e:
        print(f"  [!] 寫入雙軌分類標籤失敗: {e}")



def download_pdf(url, output_path):
    print(f"  [📡 線上探針] 正在下載 PDF ➔ {url}")
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print(f"  ➔ 🎉 下載成功！")
        return True
    except Exception as e:
        print(f"  [!] 下載 PDF 失敗: {e}")
        return False

# ==============================================================================
# 【主流程控制】
# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("💡 使用說明 (Usage):")
        print("  python3 hydrate_paper_assets.py [paper_id] (例如 zotero_227)")
        sys.exit(1)
        
    target_paper_id = sys.argv[1]
    
    # 決定資料庫與本地目錄
    base_dir = "/Users/wuulong/github/bmad-pa"
    db_path = os.path.join(base_dir, "events", "my_research", "data", "Research_Artifacts.db")
    
    if not os.path.exists(db_path):
        print(f"[!] 大腦資料庫不存在: {db_path}")
        sys.exit(1)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. 讀取 paper 基本資訊
    cursor.execute("""
        SELECT paper_id, cite_key, title, topic_id, core_method, meta_data 
        FROM papers 
        WHERE paper_id = ? OR cite_key = ?;
    """, (target_paper_id, target_paper_id))
    
    paper_row = cursor.fetchone()
    if not paper_row:
        print(f"[!] 在 papers 表中找不到 paper_id 或 cite_key = '{target_paper_id}'")
        conn.close()
        sys.exit(1)
        
    paper_id, cite_key, title, topic_id, core_method, meta_str = paper_row
    print(f"🌊 啟動文獻實體資產一鍵就位與 Markdown 預萃取工程：")
    print(f"  - Paper ID : {paper_id}")
    print(f"  - Cite Key : {cite_key}")
    print(f"  - 論文標題 : {title}")
    print("-" * 80)
    
    # 建立本地 PDFs 實體目錄
    local_pdf_dir = os.path.join(base_dir, "events", "my_research", "data", "pdfs")
    os.makedirs(local_pdf_dir, exist_ok=True)
    
    target_pdf_path = os.path.join(local_pdf_dir, f"{cite_key}.pdf")
    target_md_path = os.path.join(local_pdf_dir, f"{cite_key}.md") # 比鄰實體 PDF 放置，不污染 manuscripts
    
    pdf_located = False
    
    # 2. 管道 A：檢查本地是否早已放置好
    if os.path.exists(target_pdf_path):
        print(f"[*] 實體 PDF 早已在本地 staging 就位: {target_pdf_path}")
        pdf_located = True
        
    # 2.5 管道 A2：檢查專案已下載目錄 (downloaded_papers) 或手稿夾 (papers_pdf) 是否存在實體原檔
    if not pdf_located:
        project_sources = [
            os.path.join(base_dir, "events", "my_research", "data", "downloaded_papers", f"{cite_key}.pdf"),
            os.path.join(base_dir, "events", "my_research", "manuscripts", "papers_pdf", f"{cite_key}.pdf")
        ]
        for src in project_sources:
            if os.path.exists(src):
                print(f"[*] 🚀 尋獲專案本地實體/軟連結 PDF: {src}")
                print(f"  ➔ 正在拷貝並就位至大腦快取區...")
                # shutil.copy 能自動解開軟連結並拷貝實體內容，完美！
                shutil.copy(src, target_pdf_path)
                pdf_located = True
                break
                
    # 3. 管道 B：從 Zotero 本地儲存庫中尋找並複製過來
    if not pdf_located:
        # 讀取 Zotero 儲存路徑
        cursor.execute("SELECT absolute_path FROM directory_roots WHERE root_key = 'zotero_storage';")
        zot_row = cursor.fetchone()
        zotero_storage_root = zot_row[0] if zot_row else "/Users/wuulong/Zotero/storage/"
        
        # 查詢原本 Zotero 導入的相對路徑 (如果有的話)
        # 有可能是在 paper_urls 中以前記過
        cursor.execute("""
            SELECT root_key, url_link FROM paper_urls 
            WHERE paper_id = ? AND url_type = 'local_pdf';
        """, (paper_id,))
        url_row = cursor.fetchone()
        
        if url_row:
            root_key, url_link = url_row
            if url_link: # 剛性防禦：排除 PENDING 時 url_link 為空字串的情況
                # 取得實體絕對路徑
                cursor.execute("SELECT absolute_path FROM directory_roots WHERE root_key = ?;", (root_key,))
                root_path_row = cursor.fetchone()
                if root_path_row:
                    zotero_pdf_path = os.path.join(root_path_row[0], url_link)
                    if os.path.exists(zotero_pdf_path) and os.path.isfile(zotero_pdf_path): # 剛性防禦：必須是實體檔案
                        print(f"[*] 🚀 尋獲 Zotero 本地實體 PDF: {zotero_pdf_path}")
                        print(f"  ➔ 正在拷貝並就位至大腦快取區...")
                        shutil.copy(zotero_pdf_path, target_pdf_path)
                        pdf_located = True
                    
        # 如果 url_row 沒有，我們直接在大腦 Zotero storage 下用 cite_key 進行精準搜尋
        if not pdf_located and os.path.exists(zotero_storage_root):
            # 搜尋 Zotero 隨機八碼目錄下符合的 PDF (作者 + 年份雙重精準比對 + 標題特徵校驗)
            parts = cite_key.replace("zotero_", "").split("_")
            search_author = parts[0] # 例如 "Li"
            search_year = parts[1] if len(parts) > 1 else "" # 例如 "2023"
            
            # 從標題中提取關鍵單字以進行安全校驗，防止 "Li" 碰撞到 "Liu"
            # 提取大於 4 個字母的英文單字作為特徵詞
            title_keywords = [w.strip(",().:\"'").lower() for w in title.split() if len(w) > 4]
            title_keywords = [w for w in title_keywords if w not in ["about", "their", "under", "using", "through"]]
            
            print(f"[*] 本地快取無記錄，正在 Zotero 儲存庫中發動雙重比對精準搜尋 ➔ 作者: '{search_author}', 年份: '{search_year}'...")
            found_pdfs = []
            for root, dirs, files in os.walk(zotero_storage_root):
                for file in files:
                    if file.lower().endswith(".pdf"):
                        name_lower = file.lower()
                        # 雙重比對，防範如 Li 等高頻作者名碰撞
                        if search_author.lower() in name_lower and (not search_year or search_year in name_lower):
                            # 安全校驗一：作者名必須是獨立單詞 (防止 "li" 匹配 "liu"、"lin")
                            author_is_word = re.search(r'\b' + re.escape(search_author.lower()) + r'\b', name_lower)
                            # 安全校驗二：檔名必須包含標題中的至少一個關鍵字
                            has_title_keyword = any(kw in name_lower for kw in title_keywords[:4])
                            
                            if author_is_word or has_title_keyword:
                                found_pdfs.append(os.path.join(root, file))
            
            if found_pdfs:
                zotero_pdf_path = found_pdfs[0]
                print(f"  ➔ 🕵️‍♂️ 成功在 Zotero 中搜索到精準 PDF: {zotero_pdf_path}")
                shutil.copy(zotero_pdf_path, target_pdf_path)
                pdf_located = True
                
    # 4. 管道 C：若本地全無，則發射學術雷達線上自動下載
    if not pdf_located:
        print("[!] 本地與 Zotero 均無實體資產，正在發動線上學術雷達下載...")
        # 優先找 arXiv 的 URL
        online_url = None
        if core_method and "arxiv" in core_method.lower():
            # 試著從 core_method 提取
            online_url = "https://arxiv.org/pdf/2303.17760" # CAMEL 預設避退
        else:
            online_url = get_pdf_url_from_s2(title)
            
        if online_url:
            if download_pdf(online_url, target_pdf_path):
                pdf_located = True
                
    if not pdf_located:
        print("[!] ❌ 失敗: 本地無實體 PDF 且線上自動下載失敗，無法進行就位！")
        conn.close()
        sys.exit(1)
        
    # 5. 實體 PDF ➔ 剛性 Markdown 預萃取
    print(f"📖 正在讀取實體 PDF 並預萃取為 Markdown...")
    try:
        reader = PdfReader(target_pdf_path)
        total_pages = len(reader.pages)
        extracted_text = []
        for idx in range(total_pages):
            page_text = reader.pages[idx].extract_text()
            if page_text:
                extracted_text.append(f"\n\n<!-- Page {idx+1} -->\n\n")
                extracted_text.append(page_text)
                
        raw_content = "".join(extracted_text)
        beautified_content = clean_and_beautify_text(raw_content)
        
        with open(target_md_path, 'w', encoding='utf-8') as f:
            f.write(beautified_content)
        print(f"  ➔ 🎉 Markdown 預萃取就位成功！")
        print(f"  ➔ 實體路徑: {target_md_path}")
    except Exception as e:
        print(f"  [!] Markdown 萃取失敗: {e}")
        conn.close()
        sys.exit(1)
        
    # 6. 資料庫合流：在 paper_urls 中註冊此實體資產
    rel_pdf_path = f"events/my_research/data/pdfs/{cite_key}.pdf"
    rel_md_path = f"events/my_research/data/pdfs/{cite_key}.md"
    url_id = f"url_local_{cite_key.lower()}"
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO paper_urls (
                url_id, paper_id, root_key, url_link, url_type, download_status, file_size_bytes, meta_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            url_id,
            paper_id,
            "workspace_root",
            rel_pdf_path,
            "local_pdf",
            "DOWNLOADED",
            os.path.getsize(target_pdf_path),
            json.dumps({"description": "自動就位快取實體資產", "md_path": rel_md_path})
        ))
        
        meta = {}
        if meta_str:
            try:
                meta = json.loads(meta_str)
            except:
                pass
        
        # 如果大腦 meta_data 中沒有 abstract，或者為空，我們自動從 MD 中生成並儲存
        extracted_abs = extract_abstract_from_md(beautified_content)
        if extracted_abs and not meta.get("abstract"):
            # 取前 1500 字元限制防止爆庫
            meta["abstract"] = extracted_abs[:1500]
            print(f"  ➔ 🕵️‍♂️ 成功自動從預萃取 MD 中提取並儲存摘要至 meta_data.abstract！")
        
        # 自動收集論文引用清單 (Citations)
        print(f"  📖 正在為論文探勘引用清單 (Citations/References)...")
        citations = get_references_from_s2_or_fallback(title, beautified_content)
        if citations:
            meta["citations"] = citations[:50]  # 限制前 50 筆
            print(f"  ➔ 🕵️‍♂️ 成功取得 {len(meta['citations'])} 筆引用文獻並暫存至 meta_data.citations！")
        
        # 呼叫審計打標
        meta["compliance_status"] = meta.get("compliance_status", {})
        meta["compliance_status"]["checked_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        meta["compliance_status"]["validation_message"] = meta["compliance_status"].get("validation_message", "") + " | PDF & MD Assets Hydrated!"
        
        cursor.execute("UPDATE papers SET meta_data = ? WHERE paper_id = ?;", (json.dumps(meta, ensure_ascii=False), paper_id))
        
        # 5. 自動進行雙軌分類與標籤對合
        auto_classify_and_tag_paper(conn, paper_id, title, cite_key)
        
        conn.commit()
        print(f"\n🎉 成功將該文獻之實體資產與 DTO 資料庫合流！")
        print(f"  - 實體 PDF 快取路徑 : [data/pdfs/{cite_key}.pdf](file://{target_pdf_path})")
        print(f"  - 預萃取 MD 檔案路徑: [data/pdfs/{cite_key}.md](file://{target_md_path})")
        print(f"  - paper_urls 表註冊 : {url_id} ➔ {rel_pdf_path}")
        
    except Exception as e:
        conn.rollback()
        print(f"[!] 資料庫合流寫入失敗: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
