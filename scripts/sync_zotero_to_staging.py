#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - Zotero 聯邦公海文獻一鍵同步落庫工具 (sync_zotero_to_staging.py)

目的：
從哈爸本機 `/Users/wuulong/Zotero/zotero.sqlite` 中提取所有文獻與 PDF 附件，
一鍵無摩擦同步寫入本地主權庫的 papers 表，統一掛載在 `top_haba_staging` (公海緩衝區)。
"""

import os
import sqlite3
import json
import re
from datetime import datetime

ZOTERO_DB_PATH = "/Users/wuulong/Zotero/zotero.sqlite"

def get_zotero_authors(zotero_cursor, item_id):
    """從 Zotero 資料庫讀取某個 item 的作者名單"""
    zotero_cursor.execute("""
        SELECT c.lastName, c.firstName 
        FROM itemCreators ic
        JOIN creators c ON ic.creatorID = c.creatorID
        WHERE ic.itemID = ?
        ORDER BY ic.orderIndex;
    """, (item_id,))
    rows = zotero_cursor.fetchall()
    authors = []
    for last, first in rows:
        last_name = last.strip() if last else ""
        first_name = first.strip() if first else ""
        if last_name and first_name:
            authors.append(f"{last_name}, {first_name}")
        elif last_name:
            authors.append(last_name)
    return authors

def get_zotero_attachments(zotero_cursor, item_id):
    """讀取某個 item 下關聯的本地 PDF 相對路徑 (包含 Zotero 隨機 8 碼金鑰子目錄)"""
    zotero_cursor.execute("""
        SELECT ia.itemID, i.key, ia.path
        FROM itemAttachments ia
        JOIN items i ON ia.itemID = i.itemID
        WHERE ia.parentItemID = ? AND ia.path IS NOT NULL AND ia.path LIKE 'storage:%';
    """, (item_id,))
    rows = zotero_cursor.fetchall()
    attachments = []
    for att_id, key, path in rows:
        filename = path.replace("storage:", "")
        # 拼接為 Zotero 實體相對路徑: <key>/<filename>
        relative_path = f"{key}/{filename}"
        attachments.append((att_id, relative_path))
    return attachments

def sync_zotero():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    if not os.path.exists(ZOTERO_DB_PATH):
        print(f"[-] 錯誤：找不到 Zotero 本地資料庫於: {ZOTERO_DB_PATH}")
        return
        
    print(f"[*] 連線 Zotero 庫：{ZOTERO_DB_PATH}")
    z_conn = sqlite3.connect(ZOTERO_DB_PATH)
    z_cursor = z_conn.cursor()
    
    print(f"[*] 連線本地主權庫：{target_db_path}")
    t_conn = sqlite3.connect(target_db_path)
    t_cursor = t_conn.cursor()
    t_cursor.execute("PRAGMA foreign_keys = OFF;") # 關閉外鍵以Bulk寫入
    
    # 1. 撈取 Zotero 所有文獻項目 (排除 note=1, attachment=3, annotation=14)
    print("[*] 正在撈取 Zotero 文獻數據...")
    z_cursor.execute("""
        SELECT i.itemID, i.itemTypeID, f.fieldName, idv.value
        FROM items i
        JOIN itemData id ON i.itemID = id.itemID
        JOIN fields f ON id.fieldID = f.fieldID
        JOIN itemDataValues idv ON id.valueID = idv.valueID
        WHERE i.itemTypeID NOT IN (1, 3, 14);
    """)
    rows = z_cursor.fetchall()
    
    # 重組 items 數據
    zotero_items = {}
    for item_id, type_id, field_name, val in rows:
        if item_id not in zotero_items:
            zotero_items[item_id] = {"item_id": item_id, "type_id": type_id}
        zotero_items[item_id][field_name] = val
        
    print(f"[+] 總共自 Zotero 讀取出 {len(zotero_items)} 筆文獻。")
    
    # 2. 建立 Ingestion 採集任務 (Lineage)
    task_id = f"task_zotero_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    t_cursor.execute("""
    INSERT INTO exploration_tasks (task_id, query, status, papers_found, agent_version, error_log, meta_data)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        task_id,
        "Zotero_Local_Sync_All",
        "ONLINE",
        len(zotero_items),
        "Antigravity-v2.0-ZoteroSyncEngine",
        None,
        json.dumps({"sync_time": datetime.now().isoformat()}, ensure_ascii=False)
    ))
    
    # 3. 逐一寫入文獻與 URLs
    inserted_papers = 0
    inserted_urls = 0
    
    for z_id, data in zotero_items.items():
        title = data.get("title", "").strip()
        if not title:
            continue
            
        date_str = data.get("date", "").strip()
        # 提取年份
        year = 2024
        if date_str:
            year_match = re.search(r"\b(19|20)\d{2}\b", date_str)
            if year_match:
                year = int(year_match.group(0))
                
        # 取得作者
        authors_list = get_zotero_authors(z_cursor, z_id)
        authors = "; ".join(authors_list) if authors_list else "Unknown Authors"
        
        # 取得出版刊物
        pub = data.get("publicationTitle") or data.get("conferenceName") or "N/A"
        
        # 建立 cite_key (第一作者姓氏 + 年份 + itemID)
        first_author = "Unknown"
        if authors_list:
            # 取得姓氏並清理非英文字元
            first_author = authors_list[0].split(",")[0].strip()
            first_author = "".join(c for c in first_author if c.isalnum())
            
        cite_key = f"zotero_{first_author}_{year}_{z_id}"
        paper_id = f"zotero_{z_id}"
        
        # 建立 BibTeX
        bibtex = f"""@article{{{cite_key},
  author = {{{authors}}},
  title = {{{title}}},
  journal = {{{pub}}},
  year = {{{year}}}
}}"""

        # 寫入 papers
        t_cursor.execute("""
        INSERT OR IGNORE INTO papers (
            paper_id, task_id, topic_id, title, authors, year, core_method, cite_key, bibtex, meta_data
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            paper_id,
            task_id,
            "top_haba_staging", # 統一掛載在「哈爸文獻緩衝區」公海
            title,
            authors,
            year,
            "Zotero一鍵自動同步落庫",
            cite_key,
            bibtex,
            json.dumps({"zotero_item_id": z_id, "date_str": date_str, "publication": pub}, ensure_ascii=False)
        ))
        
        if t_cursor.rowcount > 0:
            inserted_papers += 1
            
        # 處理 URLs 與本地 PDF 附件
        attachments = get_zotero_attachments(z_cursor, z_id)
        for att_id, rel_path in attachments:
            t_cursor.execute("""
            INSERT OR IGNORE INTO paper_urls (
                url_id, paper_id, root_key, url_link, url_type, download_status, file_size_bytes, meta_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                f"url_{paper_id}_{att_id}",
                paper_id,
                "zotero_storage", # 定錨於 Zotero 本地儲存
                rel_path,
                "local_pdf",
                "DOWNLOADED",
                102400, # 預設虛擬大小
                json.dumps({"zotero_att_id": att_id}, ensure_ascii=False)
            ))
            if t_cursor.rowcount > 0:
                inserted_urls += 1
                
    t_conn.commit()
    
    # 關閉連線
    z_conn.close()
    t_conn.close()
    
    print(f"\n[+] Zotero 聯邦公海同步完畢！")
    print(f"  - 新增落庫背景文獻 (papers) 數量：{inserted_papers} 筆 (緩衝區：top_haba_staging)")
    print(f"  - 新增落庫實體本地 PDF URLs 數量：{inserted_urls} 筆 (路徑抽象根：zotero_storage)")
    print("[*] 哈爸隨時可以使用 SQL `UPDATE papers SET topic_id = '<專案Topic>' WHERE cite_key = '<文獻鍵>'` 動態靠泊至主權碼頭！\n")

if __name__ == "__main__":
    sync_zotero()
