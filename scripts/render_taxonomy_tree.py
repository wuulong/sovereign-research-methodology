#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
階層子領域樹狀拓撲自動渲染器 (render_taxonomy_tree.py)

目的：
- 連線 sqlite 大腦真值庫，查詢所有帶有 '/' 階層路徑的 paper_tags 記錄。
- 在記憶體中建立多叉分類樹，並統計各層級沉澱的文獻筆數。
- 在終端機與報告中渲染出驚艷、清晰的 ASCII 子領域分類樹狀拓撲圖，並高亮出各領域學術重力最高的 Top 文獻！
"""

import os
import sqlite3
import json

def build_tree(rows):
    """
    將帶有層級路徑與 paper 資訊的 rows 組裝成嵌套字典樹 (Trie)
    """
    tree = {}
    for tag_name, paper_id, cite_key, title, gravity in rows:
        parts = tag_name.split("/")
        current = tree
        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            is_leaf = (i == len(parts) - 1)
            
            if part not in current:
                current[part] = {
                    "count": 0,
                    "nodes": {},
                    "papers": []
                }
            
            current[part]["count"] += 1
            if is_leaf:
                current[part]["papers"].append({
                    "cite_key": cite_key,
                    "title": title,
                    "gravity": gravity if gravity is not None else 0.0
                })
            current = current[part]["nodes"]
    return tree

def print_tree(nodes, indent="", is_last=True):
    """
    遞迴打印 ASCII 樹狀結構，帶有極致的 Visual Wow-effect
    """
    # 先按照 key 排序，維持結構穩定性
    keys = sorted(nodes.keys())
    for idx, key in enumerate(keys):
        node = nodes[key]
        is_node_last = (idx == len(keys) - 1)
        
        # 決定分支符號
        branch = "└── " if is_node_last else "├── "
        print(f"{indent}{branch}📂 \033[1;34m{key}\033[0m \033[0;32m({node['count']} 篇)\033[0m")
        
        # 打印該節點下的所有論文
        next_indent = indent + ("    " if is_node_last else "│   ")
        papers = sorted(node["papers"], key=lambda x: x["gravity"], reverse=True)
        for p_idx, p in enumerate(papers):
            p_branch = "└── " if (p_idx == len(papers) - 1 and not node["nodes"]) else "├── "
            # 高亮學術重力高的主力論證文獻 (Gravity >= 6.0)
            if p["gravity"] >= 6.0:
                print(f"{next_indent}{p_branch}🏆 \033[1;33m[{p['cite_key']}]\033[0m {p['title']} \033[1;35m(重力: {p['gravity']})\033[0m")
            else:
                print(f"{next_indent}{p_branch}📄 [{p['cite_key']}] {p['title']} (重力: {p['gravity']})")
                
        # 遞迴子節點
        if node["nodes"]:
            print_tree(node["nodes"], next_indent, is_node_last)

def main():
    base_dir = "/Users/wuulong/github/bmad-pa"
    db_path = os.path.join(base_dir, "events", "my_research", "data", "Research_Artifacts.db")
    
    if not os.path.exists(db_path):
        print(f"[!] 大腦資料庫不存在: {db_path}")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查詢所有有層級特性 (包含 '/') 的 paper_tags，並對合 papers 中的學術重力
    cursor.execute("""
        SELECT 
            t.tag_name,
            t.paper_id,
            p.cite_key,
            p.title,
            CAST(json_extract(p.meta_data, '$.academic_prestige.academic_gravity_score') AS REAL) as gravity
        FROM paper_tags t
        JOIN papers p ON t.paper_id = p.paper_id
        WHERE t.tag_name LIKE '%/%'
        ORDER BY t.tag_name;
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    print("\n" + "="*80)
    print("⛰️  \033[1;36m哈爸的主權大腦：子領域階層拓撲樹狀圖 (Taxonomy Tree)\033[0m")
    print("="*80)
    
    if not rows:
        print("  [!] 目前資料庫中尚無任何帶有階層特徵 (/) 的標籤記錄。")
        print("      請先透過 Ingestion 或 citations 實體化為文獻打上層級標籤！")
        print("="*80 + "\n")
        return
        
    tree = build_tree(rows)
    print_tree(tree)
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
