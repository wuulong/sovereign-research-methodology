#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 手稿引文定錨與 references.bib 自動導出工具 (anchor_manuscript_citations.py)

目的：
1. 解析論點地圖 `sovereign_research_06_argument_map.md` 提取每篇論文的核心主張與前人理論/重構脈絡。
2. 對主題下目前所有的文獻，根據其在 Map 中的角色或 Stage 2 DTO 資訊，自動生成有意義的 citation_context。
3. 將文獻與手稿 `ms_sovereign_research_2026` 在 `manuscript_citations` 中進行物理定錨。
4. 自動從 SQLite 中撈取已引用的 BibTeX 條目，導出為學術標準的 `manuscripts/references.bib` 檔案！
"""

import os
import re
import json
import sqlite3

def parse_argument_map(map_path):
    """
    解析 argument map Markdown，提取每一篇引用文獻的 dialectic 脈絡。
    回傳 dict: { cite_key: context_text }
    """
    if not os.path.exists(map_path):
        print(f"⚠️  警告：找不到論點地圖檔案: {map_path}")
        return {}
        
    with open(map_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    
    cite_contexts = {}
    current_claim = ""
    dialectic_lines = []
    in_dialectic = False
    current_cites = []
    
    def extract_keys(text):
        raw_1 = re.findall(r'@([a-zA-Z0-9_\.\-]+)', text)
        raw_2 = re.findall(r'\b((?:arxiv|zotero)_[a-zA-Z0-9]+_\d{4}_[a-zA-Z0-9]+)\b', text, re.IGNORECASE)
        keys = list(set(raw_1 + raw_2))
        return [k.strip('.,:;)]') for k in keys if k]

    for line in lines:
        stripped = line.strip()
        
        # 1. 發現新核心主張
        if "【核心主張" in stripped:
            if current_cites:
                context_str = f"【主張】{current_claim}\n"
                if dialectic_lines:
                    context_str += "\n".join(dialectic_lines)
                for ck in current_cites:
                    if ck not in cite_contexts:
                        cite_contexts[ck] = []
                    cite_contexts[ck].append(context_str)
            
            claim_match = re.search(r'【核心主張\s*\d+】(.*)', stripped)
            if claim_match:
                current_claim = claim_match.group(0).strip('* #-\t ')
            else:
                current_claim = stripped.strip('* #-\t ')
            current_cites = []
            dialectic_lines = []
            in_dialectic = False
            continue
            
        # 2. 發現證明路徑
        if "**證明路徑" in stripped or "Provenance" in stripped:
            in_dialectic = False
            current_cites = extract_keys(line)
            continue
            
        # 3. 發現辯證與重構邏輯標題
        if "**辯證與重構邏輯**" in stripped:
            in_dialectic = True
            continue
            
        # 4. 收集辯證內容
        if in_dialectic:
            if stripped.startswith('*') or stripped.startswith('-') or stripped.startswith('1.'):
                dialectic_lines.append("- " + stripped.strip('*-\t1. '))
            elif stripped:
                dialectic_lines.append("  " + stripped)
                
    # 處理最後一個主張
    if current_cites:
        context_str = f"【主張】{current_claim}\n"
        if dialectic_lines:
            context_str += "\n".join(dialectic_lines)
        for ck in current_cites:
            if ck not in cite_contexts:
                cite_contexts[ck] = []
            cite_contexts[ck].append(context_str)
            
    # 合併同一個 cite_key 的多個主張引用
    merged_contexts = {}
    for ck, ctx_list in cite_contexts.items():
        unique_ctx = []
        for c in ctx_list:
            if c not in unique_ctx:
                unique_ctx.append(c)
        merged_contexts[ck] = "\n---\n".join(unique_ctx)
        
    return merged_contexts

def anchor_and_export():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    ms_code = "sovereign_research"
    ms_subdir = os.path.join(base_dir, "manuscripts", ms_code)
    if os.path.exists(ms_subdir) and os.path.isdir(ms_subdir):
        bib_path = os.path.join(ms_subdir, f"{ms_code}_04_references.bib")
        map_path = os.path.join(ms_subdir, f"{ms_code}_06_argument_map.md")
    else:
        bib_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_references.bib")
        map_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_argument_map.md")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    manuscript_id = "ms_sovereign_research_2026"
    
    # 1. 查詢當前主題 top_sovereign_methodology 下的所有論文
    cursor.execute("""
    SELECT paper_id, cite_key, title, meta_data 
    FROM papers 
    WHERE topic_id = 'top_sovereign_methodology'
    """)
    papers = cursor.fetchall()
    print(f"📊  檢索到主題下共有 {len(papers)} 篇文獻，準備進行實體定錨...")
    
    # 2. 解析論點地圖中所有引用的學術脈絡
    map_contexts = parse_argument_map(map_path)
    print(f"🔍  從論點地圖中解析出 {len(map_contexts)} 篇文獻的學術辯證脈絡。")
    
    # 3. 批次寫入與更新 manuscript_citations
    inserted_count = 0
    updated_count = 0
    
    for paper_id, cite_key, title, meta_str in papers:
        citation_context = None
        
        # A. 優先從 Argument Map 中匹配
        found_key = None
        for mk in map_contexts.keys():
            if mk.lower() == cite_key.lower():
                found_key = mk
                break
                
        if found_key:
            citation_context = map_contexts[found_key]
        else:
            # B. 其次若為 Stage 2，則從其 Meta DTO 提取有意義的欄位
            if meta_str:
                try:
                    meta = json.loads(meta_str)
                    stage = meta.get("stage", "STAGE_1_PRELIMINARY")
                    if stage == "STAGE_2_DEEP" and "paper_extraction" in meta:
                        ext = meta["paper_extraction"]
                        core_q = ext.get("core_question", "").strip()
                        unique_c = ext.get("unique_contribution", "").strip()
                        critique = ext.get("sovereign_taste_verdict", {}).get("critique", "").strip()
                        
                        dto_ctx = []
                        if core_q:
                            dto_ctx.append(f"🎯 核心問題: {core_q}")
                        if unique_c:
                            dto_ctx.append(f"🏆 獨特貢獻: {unique_c}")
                        if critique:
                            crit_brief = critique[:120] + "..." if len(critique) > 120 else critique
                            dto_ctx.append(f"⚖️ 品位評判: {crit_brief}")
                            
                        if dto_ctx:
                            citation_context = "\n".join(dto_ctx)
                except:
                    pass
                    
        # C. 以上皆無則使用合理 fallback
        if not citation_context:
            citation_context = f"[Stage 1 背景文獻] 作為學術脈絡探索與主題背景定錨支撐。"
            
        # 寫入或更新
        cursor.execute("""
        INSERT OR IGNORE INTO manuscript_citations (manuscript_id, paper_id, citation_context, meta_data)
        VALUES (?, ?, ?, ?);
        """, (manuscript_id, paper_id, citation_context, None))
        
        # 強制更新最新脈絡
        cursor.execute("""
        UPDATE manuscript_citations 
        SET citation_context = ? 
        WHERE manuscript_id = ? AND paper_id = ?;
        """, (citation_context, manuscript_id, paper_id))
        
        updated_count += 1
            
    conn.commit()
    print(f"💾  大腦引文定錨成功！累計更新並物理對合 {updated_count} 筆引文脈絡至手稿 {manuscript_id} 下！")
    
    # 4. 撈取所有已定錨論文的 BibTeX，並拼裝成 references.bib
    cursor.execute("""
    SELECT p.cite_key, p.bibtex 
    FROM papers p
    JOIN manuscript_citations c ON p.paper_id = c.paper_id
    WHERE c.manuscript_id = ?
    """, (manuscript_id,))
    bibtex_entries = cursor.fetchall()
    
    print(f"🚀  正在自動拼裝 references.bib，目前已定錨引文總數：{len(bibtex_entries)} 篇...")
    
    bib_content = "% ==============================================================================\n"
    bib_content += f"% 哈爸主權大腦自動生成 BibTeX 參考文獻庫 - references.bib\n"
    bib_content += f"% 生成時間: 2026-06-06\n"
    bib_content += f"% 手稿定錨 ID: {manuscript_id}\n"
    bib_content += "% ==============================================================================\n\n"
    
    for cite_key, bibtex in bibtex_entries:
        bib_content += f"% Cite Key: {cite_key}\n"
        bib_content += bibtex.strip() + "\n\n"
        
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(bib_content)
        
    conn.close()
    print(f"🎉  學術標準參考文獻庫導出成功！")
    print(f"  - 實體路徑：{bib_path}")
    print(f"  - 累計寫入條目：{len(bibtex_entries)} 筆\n")

if __name__ == "__main__":
    anchor_and_export()

