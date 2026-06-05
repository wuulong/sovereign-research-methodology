#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈教授主權自審與論點溯源盲檢工具 (verify_argument_provenance.py)

目的：
1. 讀取論文初稿 sovereign_research_paper.md 與論點溯源地圖 argument_provenance_map.md。
2. 自動解析其中的「核心主張 (Claims)」與「學術引用 (Citations)」。
3. 連線 SQLite 大腦資料庫，盲檢每一筆引用是否已註冊，且是否已閱讀消化 (compliance_status.is_compliant 達 STAGE_2_DEEP)。
4. 產出「哈教授學術盲檢自審報告 (argument_audit_report.md)」，為寫作與證明硬度提供終極防線。
"""

import os
import re
import json
import sqlite3
from datetime import datetime

def extract_citations(text):
    # 模式 1: 匹配 @cite_key
    raw_keys_1 = re.findall(r'@([a-zA-Z0-9_\.\-]+)', text)
    # 模式 2: 匹配直接出現且合乎 standard cite_key 結構的字串 (如 arxiv_Maynard_2026_2601)
    raw_keys_2 = re.findall(r'\b((?:arxiv|zotero)_[a-zA-Z0-9]+_\d{4}_[a-zA-Z0-9]+)\b', text, re.IGNORECASE)
    
    raw_keys = raw_keys_1 + raw_keys_2
    clean_keys = []
    for key in raw_keys:
        # 清除結尾的標點符號，例如引導括號或逗號
        clean_key = re.sub(r'[\.\,\:\;\)\]\s]+$', '', key)
        if clean_key and clean_key not in clean_keys:
            clean_keys.append(clean_key)
    return clean_keys

def parse_claims_and_citations(provenance_path):
    claims = []
    current_section = "未定位章節"
    current_claim = None
    
    if not os.path.exists(provenance_path):
        return claims
        
    with open(provenance_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line_str = line.strip()
        # 解析章節
        if line_str.startswith("## ") or line_str.startswith("### "):
            current_section = line_str.lstrip("#").strip()
            current_claim = None  # 重置活動中的主張
            
        # 解析主張
        claim_match = re.search(r'【核心主張\s*\d+】', line_str)
        if claim_match:
            current_claim = {
                "section": current_section,
                "claim": line_str,
                "citations": []
            }
            claims.append(current_claim)
            
        # 若當前有活動中的主張，收集其後續行中的引用鍵，直到遇見下一個章節
        if current_claim is not None:
            cites = extract_citations(line_str)
            for cite in cites:
                # 避免將主張描述文字誤判為引用，且去重
                if cite not in current_claim["citations"] and "核心主張" not in cite:
                    current_claim["citations"].append(cite)
                    
    return claims

def main():
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    # 支援動態 MS_CODE 尋車對合
    ms_code = "sovereign_research"
    if len(sys.argv) > 1:
        ms_code = sys.argv[1].strip()
        
    paper_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_manuscript.md")
    provenance_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_argument_map.md")
    report_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_audit_report.md")
    
    print(f"🕵️‍♂️ 啟動哈教授學術自審與論點地圖盲檢引擎 (MS_CODE: {ms_code})...")
    
    if not os.path.exists(paper_path):
        print(f"[!] 找不到手稿檔案: {paper_path}")
        return
        
    if not os.path.exists(provenance_path):
        print(f"[!] 找不到論點地圖檔案: {provenance_path}")
        return
        
    if not os.path.exists(db_path):
        print(f"[!] 找不到大腦資料庫: {db_path}")
        return

    # 1. 讀取手稿中的引用
    with open(paper_path, 'r', encoding='utf-8') as f:
        paper_text = f.read()
    paper_citations = extract_citations(paper_text)
    print(f"  ➔ 手稿 `{os.path.basename(paper_path)}` 解析出 {len(paper_citations)} 個引文定位。")

    # 2. 讀取論點地圖中的主張與引用
    claims = parse_claims_and_citations(provenance_path)
    map_citations = []
    for c in claims:
        for cite in c["citations"]:
            if cite not in map_citations:
                map_citations.append(cite)
    print(f"  ➔ 論點地圖 `{os.path.basename(provenance_path)}` 解析出 {len(claims)} 個核心主張，涉及 {len(map_citations)} 篇引用。")

    # 合併所有需要盲檢的引用
    all_citations = sorted(list(set(paper_citations + map_citations)))
    print(f"  ➔ 聯邦合併去重後，共需盲檢 {len(all_citations)} 篇核心文獻地基。")

    # 3. 連線資料庫進行盲檢
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    audit_results = {}
    compliant_count = 0
    registered_count = 0
    
    for cite_key in all_citations:
        cursor.execute("""
            SELECT paper_id, title, authors, year, topic_id, meta_data 
            FROM papers 
            WHERE LOWER(cite_key) = LOWER(?) OR LOWER(cite_key) = LOWER(?) OR LOWER(paper_id) = LOWER(?)
        """, (cite_key, f"zotero_{cite_key}", cite_key))
        row = cursor.fetchone()
        
        if not row:
            # 嘗試模糊匹配
            cursor.execute("SELECT paper_id, title, authors, year, topic_id, meta_data FROM papers WHERE cite_key LIKE ?", (f"%{cite_key}%",))
            row = cursor.fetchone()
            
        if row:
            paper_id, title, authors, year, topic_id, meta_str = row
            registered_count += 1
            is_compliant = False
            stage = "STAGE_1_PRELIMINARY"
            missing_fields = []
            
            if meta_str:
                try:
                    meta = json.loads(meta_str)
                    stage = meta.get("stage", "STAGE_1_PRELIMINARY")
                    compliance = meta.get("compliance_status", {})
                    is_compliant = compliance.get("is_compliant", False)
                    missing_fields = compliance.get("missing_fields", [])
                except Exception as e:
                    pass
            
            if is_compliant:
                compliant_count += 1
                status_icon = "💚 FULLY PROVED"
            else:
                status_icon = "⚠️ PENDING DIGESTION"
                
            audit_results[cite_key] = {
                "registered": True,
                "paper_id": paper_id,
                "title": title,
                "authors": authors,
                "year": year,
                "topic_id": topic_id,
                "stage": stage,
                "is_compliant": is_compliant,
                "missing_fields": missing_fields,
                "status_icon": status_icon
            }
        else:
            audit_results[cite_key] = {
                "registered": False,
                "status_icon": "❌ UNREGISTERED",
                "is_compliant": False
            }

    # 4. 生成自審報告
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_md = []
    report_md.append(f"# 🕵️‍♂️ 哈教授學術盲檢自審與品質對合報告 (Academic Grounding Audit Report)")
    report_md.append(f"*評估時間戳記：{now_str}* | *定錨手稿編號：`ms_sovereign_research_2026`*\n")
    report_md.append("> [!IMPORTANT]")
    report_md.append("> 本報告是哈教授「30 秒 SQL 照妖鏡」的自動化實體展現。它盲檢了手稿與證明文件中的所有引文，")
    report_md.append("> 強制校對其在大腦資料庫中的註冊狀態與 Stage 2 深度解構合規性，以肉身實測與物理硬度剪枝 AI 八股幻想。\n")
    
    # 統計區
    compliance_rate = (compliant_count / len(all_citations) * 100) if all_citations else 0
    registration_rate = (registered_count / len(all_citations) * 100) if all_citations else 0
    
    report_md.append("## 📊 1. 學術硬度與大腦對合體檢看板")
    report_md.append(f"| 體檢項目 | 數量 | 比例 / 合規率 | 狀態判定 |")
    report_md.append(f"| :--- | :---: | :---: | :---: |")
    report_md.append(f"| 聯邦提取總引用數 | {len(all_citations)} 篇 | 100% | - |")
    report_md.append(f"| 資料庫已註冊文獻 | {registered_count} 篇 | {registration_rate:.2f}% | " + ("🟢 正常" if registration_rate == 100 else "🔴 警告：存在未註冊空殼") + " |")
    report_md.append(f"| Stage 2 深度合規文獻 (已消化) | {compliant_count} 篇 | {compliance_rate:.2f}% | " + ("🟢 優異" if compliance_rate > 50 else "⚠️ 警告：待消化文獻過高") + " |")
    report_md.append(f"| 待解構文獻 (Pending Stage 2) | {len(all_citations) - compliant_count} 篇 | {(100 - compliance_rate):.2f}% | - |")
    report_md.append("\n---\n")
    
    # 論點矩陣區
    report_md.append("## 🗺️ 2. 關鍵主張與引經據典對照矩陣 (Claims Grounding Matrix)")
    report_md.append("本矩陣掃描了證明文件中的核心主張，追蹤其背後引用的文獻是否在大腦中被妥善證明：\n")
    report_md.append("| 證明文件章節 | 核心主張 (Claim) | 涉及引用 (Citations) | 大腦對合狀態 (Grounding Status) |")
    report_md.append("| :--- | :--- | :--- | :--- |")
    
    for c in claims:
        sec = c["section"]
        claim_clean = re.sub(r'^(\*|#|\-|\s)+', '', c["claim"])
        cites_str = ", ".join([f"`@{k}`" for k in c["citations"]]) if c["citations"] else "⚠️ 無引用！"
        
        status_list = []
        for cite in c["citations"]:
            res = audit_results.get(cite, {"status_icon": "❌ UNREGISTERED"})
            status_list.append(f"{cite}: {res['status_icon']}")
            
        status_str = "<br>".join(status_list) if status_list else "🔴 缺乏理論地墊"
        report_md.append(f"| {sec} | {claim_clean} | {cites_str} | {status_str} |")
        
    report_md.append("\n---\n")

    # 文獻明細明細區
    report_md.append("## 📑 3. 引文資料庫合規明細帳本 (Database Invariant Ledger)")
    report_md.append("以下為本次體檢掃描出的所有文獻在 SQLite 資料庫中的物理註冊明細：\n")
    report_md.append("| 引用鍵 (Cite Key) | 大腦主鍵 (Paper ID) | 論文標題 (Title) | 循序主題 (Topic ID) | 體檢狀態 (Audit Status) |")
    report_md.append("| :--- | :--- | :--- | :--- | :--- |")
    
    unregistered_keys = []
    pending_keys = []
    
    for cite_key in all_citations:
        res = audit_results[cite_key]
        if not res["registered"]:
            report_md.append(f"| `@{cite_key}` | - | - | - | ❌ **UNREGISTERED** (未註冊於 DB) |")
            unregistered_keys.append(cite_key)
        else:
            title_clean = res["title"][:50] + "..." if len(res["title"]) > 50 else res["title"]
            report_md.append(f"| `@{cite_key}` | `{res['paper_id']}` | *{title_clean}* | `{res['topic_id']}` | {res['status_icon']} (`{res['stage']}`) |")
            if not res["is_compliant"]:
                pending_keys.append(cite_key)
                
    report_md.append("\n---\n")

    # 行動指南
    report_md.append("## 🎯 4. 哈教授缺失診斷與下一步行動指南")
    if not unregistered_keys and not pending_keys:
        report_md.append("> [!TIP]")
        report_md.append("> **恭喜！你已達成行解合一的最高境界！** 本論文與證明文件中的所有引文皆在大腦資料庫中")
        report_md.append("> 妥善註冊，且全部通過 Stage 2 十大學術因子深度解構洗滌。理論地墊無比堅實，無懈可擊！")
    else:
        if unregistered_keys:
            report_md.append("> [!CAUTION]")
            report_md.append("> **紅色警告：存在未註冊的空殼引用！**")
            report_md.append("> 以下引文出現在你的手稿或論點地圖中，但在 SQLite 中找不到任何實體記錄：")
            for k in unregistered_keys:
                report_md.append(f"> - `@{k}`")
            report_md.append("> **行動建議**：請立即執行 `sync_zotero_to_staging.py` 或發動引渡靠泊，將這些文獻註冊入庫，消除空殼！\n")
            
        if pending_keys:
            report_md.append("> [!WARNING]")
            report_md.append("> **黃色警告：存在尚未通過 Stage 2 深度解構的文獻！**")
            report_md.append("> 以下文獻雖然存在於資料庫，但你（或 AI 腳爪）尚未對其進行 Stage 2 深度研讀與 10 大學術因子降維萃取：")
            for k in pending_keys:
                report_md.append(f"> - `@{k}`")
            report_md.append("> **行動建議**：請發動 `hydrate_paper_assets.py` 就位其實體 PDF，並使用 `literature_deconstruct_and_save.py` 進行深度因子灌溉落庫！\n")

    # 寫入檔案
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_md))
        
    print(f"\n🎉 盲檢自審報告產產製成功！已寫入至: {report_path}")
    print(f"  - 註冊率: {registration_rate:.2f}% ({registered_count}/{len(all_citations)})")
    print(f"  - 合規率: {compliance_rate:.2f}% ({compliant_count}/{len(all_citations)})")
    
    conn.close()

if __name__ == "__main__":
    main()
