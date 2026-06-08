#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈教授手稿全景成熟度與可信度自審審計腳本 (verify_manuscript_maturity.py)

優化亮點：
1. 【真正的 2 層深度遞迴 BFS 探針】：精確追蹤 A -> B -> C 關係，分析底層基底是否完整 Ingestion。
2. 【文獻根系未開發懲罰機制 (Roots Incompleteness Penalty)】：
   - 針對未消化 (PENDING) 的文獻，其理論根系完全未開發，必須以「已消化覆蓋率」作為懲罰因子拉低遞迴就位率，彻底消滅 100% 滿分虛報 Bug！
3. 【紅軍覆蓋率綜合計分】：引進「覆蓋率(60%) + PASS率(40%)」防投機算法。
"""

import os
import re
import sys
import json
import sqlite3
from datetime import datetime

# ==============================================================================
# 【核心輔助函數】
# ==============================================================================
def extract_citations(text):
    raw_keys_1 = re.findall(r'@([a-zA-Z0-9_\.\-]+)', text)
    raw_keys_2 = re.findall(r'\b((?:arxiv|zotero)_[a-zA-Z0-9]+_\d{4}_[a-zA-Z0-9]+)\b', text, re.IGNORECASE)
    
    raw_keys = raw_keys_1 + raw_keys_2
    clean_keys = []
    for key in raw_keys:
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
        if line_str.startswith("## ") or line_str.startswith("### "):
            current_section = line_str.lstrip("#").strip()
            current_claim = None
            
        claim_match = re.search(r'【核心主張\s*\d+】', line_str)
        if claim_match:
            current_claim = {
                "section": current_section,
                "claim": line_str,
                "citations": []
            }
            claims.append(current_claim)
            
        if current_claim is not None:
            cites = extract_citations(line_str)
            for cite in cites:
                if cite not in current_claim["citations"] and "核心主張" not in cite:
                    current_claim["citations"].append(cite)
                    
    return claims

def estimate_file_maturity(file_path, file_basename):
    if not os.path.exists(file_path):
        return 0.0, ["⚠️ 檔案完全遺漏，請盡快創立！"]
        
    if file_basename.endswith(".bib"):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        line_count = len(lines)
        if line_count == 0:
            return 10.0, ["⚠️ 引用 Bib 檔案為空，尚未導出任何引用條目。"]
        elif line_count < 10:
            return 30.0, ["⚠️ 引用條目極少，可能尚未與大腦文獻庫進行引渡定錨。"]
        else:
            return 95.0, ["💚 條目已就位，符合學術編譯基準。"]
            
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    char_len = len(content)
    todo_count = len(re.findall(r'(TODO|Draft|\[\s*\])', content, re.IGNORECASE))
    
    score = 100.0
    suggestions = []
    
    if char_len < 300:
        score -= 50.0
        suggestions.append("⚠️ 內容過短，目前僅為極簡草稿，請厚化論述。")
    elif char_len < 1000:
        score -= 20.0
        suggestions.append("⚠️ 內容略顯單薄，建議進一步補充實踐與細節。")
        
    if todo_count > 0:
        deduction = todo_count * 5.0
        score -= deduction
        suggestions.append(f"⚠️ 偵測到 {todo_count} 個 TODO/Draft 標記，請盡快填補內容空白。")
        
    score = max(score, 30.0)
    score = min(score, 100.0)
    
    if score == 100.0:
        suggestions.append("💚 文件內容豐富且無懸置標記，達到極高成熟度！")
    elif score >= 80.0:
        suggestions.append("💛 文件主體結構完整，僅剩餘少數 TODO 標記待修復。")
        
    return score, suggestions

# ==============================================================================
# 【主審計流程】
# ==============================================================================
def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    ms_code = "sovereign_research"
    if len(sys.argv) > 1:
        ms_code = sys.argv[1].strip()
        
    print(f"🕵️‍♂️ 啟動哈教授學術手稿全景成熟度與可信度審計系統 (SMMCAP v1.0, MS_CODE: {ms_code})...")
    
    if not os.path.exists(db_path):
        print(f"[!] 找不到大腦資料庫: {db_path}")
        return
        
    # 1. 聯邦手稿齊全與成熟度掃描
    federated_files = {
        "manuscript": {"name": "主稿 (Manuscript)", "file": f"{ms_code}_05_manuscript.md"},
        "toc": {"name": "大綱 (ToC)", "file": f"{ms_code}_01_toc.md"},
        "argument_map": {"name": "論點地圖 (Argument Map)", "file": f"{ms_code}_06_argument_map.md"},
        "originality_defense": {"name": "原創防禦地圖 (Originality Defense)", "file": f"{ms_code}_07_originality_defense.md"},
        "deconstruction": {"name": "文獻解構集 (Deconstruction)", "file": f"{ms_code}_03_deconstruction.md"},
        "references_list": {"name": "引文文獻清單 (References List)", "file": f"{ms_code}_02_references_list.md"},
        "reading_protocol": {"name": "閱讀協議 (Reading Protocol)", "file": f"{ms_code}_08_reading_protocol.md"},
        "references_bib": {"name": "標準 References.bib", "file": f"{ms_code}_04_references.bib"}
    }
    
    file_scores = {}
    file_suggestions = {}
    
    for key, info in federated_files.items():
        ms_subdir = os.path.join(base_dir, "manuscripts", ms_code)
        if os.path.exists(ms_subdir) and os.path.isdir(ms_subdir):
            file_path = os.path.join(ms_subdir, info["file"])
        else:
            file_path = os.path.join(base_dir, "manuscripts", info["file"])
        score, sug = estimate_file_maturity(file_path, info["file"])
        file_scores[key] = score
        file_suggestions[key] = sug
        
    avg_doc_maturity = sum(file_scores.values()) / len(file_scores)
    
    # 2. 讀取手稿與地圖以搜集 Citations & Claims
    ms_subdir = os.path.join(base_dir, "manuscripts", ms_code)
    if os.path.exists(ms_subdir) and os.path.isdir(ms_subdir):
        paper_path = os.path.join(ms_subdir, f"{ms_code}_05_manuscript.md")
        provenance_path = os.path.join(ms_subdir, f"{ms_code}_06_argument_map.md")
    else:
        paper_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_05_manuscript.md")
        provenance_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_06_argument_map.md")
    
    all_citations = []
    claims_list = []
    
    if os.path.exists(paper_path):
        with open(paper_path, 'r', encoding='utf-8', errors='ignore') as f:
            all_citations.extend(extract_citations(f.read()))
            
    if os.path.exists(provenance_path):
        with open(provenance_path, 'r', encoding='utf-8', errors='ignore') as f:
            all_citations.extend(extract_citations(f.read()))
        claims_list = parse_claims_and_citations(provenance_path)
        
    all_citations = list(set(all_citations))
    citations_count = len(all_citations)
    
    # ==============================================================================
    # 3. SQLite 資料庫 Grounding 審計
    # ==============================================================================
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # A. Citations 存在性與 Stage 2 消化率比對
    registered_cites_count = 0
    stage2_cites_count = 0
    unregistered_keys = []
    undigested_keys = []
    involved_paper_ids = []
    digested_paper_ids = []
    
    # 閱讀層次統計與權重映射
    LEVEL_WEIGHTS = {
        "BODY_ON_DEEP": 1.0,
        "SKIMMED": 0.7,
        "DTO_SUMMARY": 0.3,
        "UNREAD": 0.0
    }
    read_depth_counts = {
        "BODY_ON_DEEP": 0,
        "SKIMMED": 0,
        "DTO_SUMMARY": 0,
        "UNREAD": 0
    }
    unread_keys = []
    summary_keys = []
    
    for cite in all_citations:
        cursor.execute("""
            SELECT paper_id, meta_data, read_depth_level 
            FROM papers 
            WHERE LOWER(cite_key) = LOWER(?) OR LOWER(paper_id) = LOWER(?);
        """, (cite, cite))
        row = cursor.fetchone()
        
        if row:
            registered_cites_count += 1
            paper_id, meta_str, read_depth_level = row
            involved_paper_ids.append(paper_id)
            
            # 處理閱讀深度
            if not read_depth_level or read_depth_level.upper() not in LEVEL_WEIGHTS:
                level_resolved = "UNREAD"
            else:
                level_resolved = read_depth_level.upper()
                
            read_depth_counts[level_resolved] += 1
            if level_resolved == "UNREAD":
                unread_keys.append(cite)
            elif level_resolved == "DTO_SUMMARY":
                summary_keys.append(cite)
                
            try:
                meta = json.loads(meta_str) if meta_str else {}
                stage = meta.get("stage", "STAGE_1_PRELIMINARY")
                if stage == "STAGE_2_DEEP":
                    stage2_cites_count += 1
                    digested_paper_ids.append(paper_id)
                else:
                    undigested_keys.append(cite)
            except Exception:
                undigested_keys.append(cite)
        else:
            unregistered_keys.append(cite)
            read_depth_counts["UNREAD"] += 1
            unread_keys.append(cite)
            
    cite_grounding_rate = (registered_cites_count / citations_count * 100) if citations_count > 0 else 100.0
    stage2_digestion_rate = (stage2_cites_count / citations_count * 100) if citations_count > 0 else 100.0
    
    # 計算真實閱讀深度分數
    total_weights = sum(read_depth_counts[level] * LEVEL_WEIGHTS[level] for level in LEVEL_WEIGHTS)
    average_reading_score = (total_weights / citations_count * 100) if citations_count > 0 else 100.0
    
    # B. 【真正的 2 層深度遞迴 BFS 探針 + 根系未開發懲罰因子】
    recursive_targets = set()
    recursive_ingested = set()
    recursive_broken_relations = []
    
    # 開發覆蓋率因子 (已消化文獻佔手稿引用總文獻的比例)
    roots_exploration_factor = (stage2_cites_count / citations_count) if citations_count > 0 else 1.0
    
    # 僅對「已消化」的 A 類文獻發動遞迴關係分析，因為未消化的文獻根系完全懸置
    if digested_paper_ids:
        # 第一層：已消化文獻的直接基底 (A ➔ GROUNDED_ON ➔ B)
        placeholders_l1 = ",".join(["?"] * len(digested_paper_ids))
        cursor.execute(f"""
            SELECT target_paper_id 
            FROM paper_relations 
            WHERE source_paper_id IN ({placeholders_l1}) AND relation_type = 'GROUNDED_ON';
        """, digested_paper_ids)
        level1_targets = [r[0] for r in cursor.fetchall()]
        
        for t in level1_targets:
            recursive_targets.add(t)
            
        # 第二層：B 級文獻的底層基底 (B ➔ GROUNDED_ON ➔ C)
        if level1_targets:
            placeholders_l2 = ",".join(["?"] * len(level1_targets))
            cursor.execute(f"""
                SELECT target_paper_id 
                FROM paper_relations 
                WHERE source_paper_id IN ({placeholders_l2}) AND relation_type = 'GROUNDED_ON';
            """, level1_targets)
            level2_targets = [r[0] for r in cursor.fetchall()]
            for t in level2_targets:
                recursive_targets.add(t)
                
        # 檢查這些 targets 的 Ingestion 就位狀態
        for t in recursive_targets:
            cursor.execute("SELECT paper_id FROM papers WHERE paper_id = ? OR LOWER(cite_key) = LOWER(?);", (t, t))
            if cursor.fetchone():
                recursive_ingested.add(t)
            else:
                cursor.execute("""
                    SELECT source_paper_id 
                    FROM paper_relations 
                    WHERE target_paper_id = ? AND relation_type = 'GROUNDED_ON' LIMIT 1;
                """, (t,))
                src_row = cursor.fetchone()
                src = src_row[0] if src_row else "unknown"
                recursive_broken_relations.append((src, t))
                
    recursive_target_total = len(recursive_targets)
    recursive_target_ingested = len(recursive_ingested)
    
    # 原始已開發根系就位率
    raw_recursive_rate = (recursive_target_ingested / recursive_target_total * 100) if recursive_target_total > 0 else 100.0
    
    # 🔴 最終遞迴閱讀就位率 = 原始已開發率 * 根系開發覆蓋率 (消除 100% 滿分虛報 Bug)
    recursive_digestion_rate = raw_recursive_rate * roots_exploration_factor
    
    # C. 【紅軍對抗與答辯覆蓋率剛性審計 - 防投機投巧】
    manuscript_id = f"ms_{ms_code}_2026"
    cursor.execute("SELECT manuscript_id FROM my_manuscripts WHERE manuscript_id = ? OR LOWER(cite_key) = LOWER(?);", (manuscript_id, ms_code))
    m_row = cursor.fetchone()
    db_ms_id = m_row[0] if m_row else manuscript_id
    
    cursor.execute("SELECT verdict FROM red_team_logs WHERE manuscript_id = ?;", (db_ms_id,))
    ms_logs = cursor.fetchall()
    has_ms_log = len(ms_logs) > 0
    ms_pass_count = sum(1 for r in ms_logs if r[0] == 'PASS')
    
    cites_with_logs_count = 0
    all_red_team_logs = []
    
    for cite in all_citations:
        cursor.execute("SELECT paper_id FROM papers WHERE LOWER(cite_key) = LOWER(?) OR LOWER(paper_id) = LOWER(?);", (cite, cite))
        p_row = cursor.fetchone()
        if p_row:
            p_id = p_row[0]
            cursor.execute("SELECT verdict FROM red_team_logs WHERE paper_id = ?;", (p_id,))
            p_logs = cursor.fetchall()
            if p_logs:
                cites_with_logs_count += 1
                all_red_team_logs.extend(p_logs)
                
    cite_coverage_rate = (cites_with_logs_count / citations_count) if citations_count > 0 else 1.0
    ms_coverage_rate = 1.0 if has_ms_log else 0.0
    red_team_coverage = cite_coverage_rate * 0.7 + ms_coverage_rate * 0.3
    
    total_logs = len(ms_logs) + len(all_red_team_logs)
    pass_logs = ms_pass_count + sum(1 for r in all_red_team_logs if r[0] == 'PASS')
    red_team_pass_rate = (pass_logs / total_logs * 100) if total_logs > 0 else 0.0
    
    if total_logs == 0:
        red_team_score = 0.0
    else:
        red_team_score = (red_team_coverage * 100 * 0.6) + (red_team_pass_rate * 0.4)
        
    # D. Claims Grounding 完整率
    perfect_claims_count = 0
    total_claims_count = len(claims_list)
    claims_issues = []
    
    for c in claims_list:
        cites = c["citations"]
        if not cites:
            claims_issues.append((c["claim"], "🔴 嚴重錯誤：此核心主張缺乏任何引經據典理論地墊！"))
            continue
            
        all_proved = True
        for cite in cites:
            cursor.execute("""
                SELECT paper_id, meta_data 
                FROM papers 
                WHERE LOWER(cite_key) = LOWER(?) OR LOWER(paper_id) = LOWER(?);
            """, (cite, cite))
            row = cursor.fetchone()
            if row:
                try:
                    meta = json.loads(row[1]) if row[1] else {}
                    if meta.get("stage", "STAGE_1_PRELIMINARY") != "STAGE_2_DEEP":
                        all_proved = False
                except Exception:
                    all_proved = False
            else:
                all_proved = False
                
        if all_proved:
            perfect_claims_count += 1
        else:
            claims_issues.append((c["claim"], "⚠️ 警告：主張所涉及的引用中，有尚未通過 Stage 2 深度解構的文獻！"))
            
    claims_grounding_rate = (perfect_claims_count / total_claims_count * 100) if total_claims_count > 0 else 100.0
    
    conn.close()
    
    # ==============================================================================
    # 4. MCI 指數剛性加權計算
    # ==============================================================================
    brain_grounding_score = (
        cite_grounding_rate * 0.15 +
        stage2_digestion_rate * 0.20 +
        average_reading_score * 0.20 +
        recursive_digestion_rate * 0.15 +
        red_team_score * 0.20 +
        claims_grounding_rate * 0.10
    )
    
    mci = (avg_doc_maturity * 0.50) + (brain_grounding_score * 0.50)
    
    if mci >= 90.0:
        mci_tier = "🟢 頂級可信 (Elite Credibility - A+)"
        verdict_summary = "哈教授評語：Verdict PASS！文件齊備且大腦地基無比堅實，行解合一的典範，准予進行最終學術編譯與發表！"
    elif mci >= 70.0:
        mci_tier = "🟡 良好進展 (Solid Progress - B)"
        verdict_summary = "哈教授評語：良好！文件骨架已完備，但大腦 Grounding 與紅軍自審仍有未消化盲區。請儘速補齊 Stage 2 與紅軍 Verdict！"
    elif mci >= 45.0:
        mci_tier = "🟠 草創初期 (Under Development - C)"
        verdict_summary = "哈教授評語：寫作初期。文件多處懸置，大腦引文大多處於 PENDING 階段。請針對改善建議老老實實地厚化地墊！"
    else:
        mci_tier = "🔴 嚴重警告 (Epistemic Island - F)"
        verdict_summary = "哈教授評語：認知掏空警告！文件裝模作樣且大腦完全處於空殼或未對抗狀態。此狀態之手稿毫無學術可信度，不予通過！"
        
    # ==============================================================================
    # 5. 產出報告 Markdown 寫入
    # ==============================================================================
    ms_subdir = os.path.join(base_dir, "manuscripts", ms_code)
    if os.path.exists(ms_subdir) and os.path.isdir(ms_subdir):
        report_path = os.path.join(ms_subdir, f"{ms_code}_09_maturity_report.md")
    else:
        report_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_09_maturity_report.md")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"""# 🕵️‍♂️ 哈教授手稿全景成熟度與可信度審計報告 (SMMCAP Audit Report)
*評估時間戳記：{now_str}* | *定錨手稿代碼：`{ms_code}`*

> [!NOTE]
> 本報告由哈教授「SMMCAP 1.0 審計引擎」物理產出。它剛性掃描了「八大聯邦手稿資產」的完備性，
> 並對合了大腦 SQLite 資料庫的 Grounding 深度與紅軍自審防線，以肉身實踐強行校正 AI 八股幻想，拒絕虛浮黑話。

---

## 📊 1. Maturity & Credibility Index (MCI) 大腦綜合看板

```
┌────────────────────────────────────────────────────────┐
│  MCI 大腦成熟與可信度指數： {mci:.2f}%                             │
│  當前等級： {mci_tier}                          │
└────────────────────────────────────────────────────────┘
```

> **{verdict_summary}**

### 📈 雙板塊加權明細
*   **聯邦文件成熟度分 (50% 權重)**：`{avg_doc_maturity:.2f}%` (手稿聯邦 8 大資產之寫作完備度)
*   **大腦 Grounding 綜合分 (50% 權重)**：`{brain_grounding_score:.2f}%` (大腦資料庫之實體地基信度)
    *   *Cite 註冊存在率 (15% 權重)*: `{cite_grounding_rate:.2f}%` ({registered_cites_count}/{citations_count})
    *   *Stage 2 消化率 (20% 權重)*: `{stage2_digestion_rate:.2f}%` ({stage2_cites_count}/{citations_count})
    *   *真實閱讀深度分 (20% 權重)*: `{average_reading_score:.2f}%` (各層次權重加權分)
    *   *遞迴閱讀就位率 (15% 權重)*: `{recursive_digestion_rate:.2f}%` (已開發根系率: {raw_recursive_rate:.1f}%, 根系覆蓋率: {roots_exploration_factor*100:.1f}%)
    *   *紅軍對抗綜合得分 (20% 權重)*: `{red_team_score:.2f}%` (涵蓋率: {red_team_coverage*100:.1f}%, 答辯率: {red_team_pass_rate:.1f}%)
    *   *Claims Grounding 完整率 (10% 權重)*: `{claims_grounding_rate:.2f}%` (總 Claims: {total_claims_count} 條, 完美: {perfect_claims_count} 條)

---

## 📂 2. 聯邦手稿資產齊全度與成熟度掃描
本模組掃描了 `manuscripts/` 目錄下的八大資產，檢核其是否齊備並估算完成進度：

| 聯邦文件名稱 | 實體檔案名稱 | 成熟度進度 | 關鍵改善與評價診斷 |
| :--- | :--- | :---: | :--- |
""")
        for key, info in federated_files.items():
            score = file_scores[key]
            sugs_str = " ".join(file_suggestions[key])
            f.write(f"| **{info['name']}** | `{info['file']}` | `{score:.1f}%` | {sugs_str} |\n")
            
        f.write(f"""
---

## 🧠 3. 大腦資料庫地基與 Grounding 審計明細

### 1. 引用文獻註冊與 STAGE_2 合規體檢 (Citations Grounding)
*   手稿與 Claims Map 共解析出 **{citations_count}** 篇引用。
*   已在 SQLite 資料庫註冊的文獻：**{registered_cites_count}** 篇 (未註冊: **{len(unregistered_keys)}** 篇)。
*   已完成 Stage 2 深度解構與合規洗滌的文獻：**{stage2_cites_count}** 篇 (待消化: **{len(undigested_keys)}** 篇)。

""")
        if unregistered_keys:
            f.write("> [!CAUTION]\n> **🔴 偵測到未註冊的幽靈引文！**\n> 以下文獻出現在手稿或地圖中，但大腦資料庫無註冊記錄，請盡快執行 API 探勘入庫：\n")
            for k in unregistered_keys:
                f.write(f"> - `{k}`\n")
            f.write("\n")
            
        if undigested_keys:
            f.write("> [!WARNING]\n> **⚠️ 偵測到尚未消化（Stage 2 待消化）的文獻！**\n> 以下文獻尚未進行 10 大核心因子高精降維萃取，請儘速發動 `hydrate_paper_assets` 消化：\n")
            for k in undigested_keys:
                f.write(f"> - `{k}`\n")
            f.write("\n")

        f.write(f"""### 2. 真實文獻閱讀深度體檢 (Reading Depth Audit)
*   **真實閱讀深度分**：`{average_reading_score:.2f}%`
*   各閱讀層次之文獻統計：
    *   🟢 **真實身讀 (BODY_ON_DEEP)**：`{read_depth_counts['BODY_ON_DEEP']}` 篇 (權重 1.0)
    *   🟡 **真實簡讀 (SKIMMED)**：`{read_depth_counts['SKIMMED']}` 篇 (權重 0.7)
    *   🟠 **僅看摘要 (DTO_SUMMARY)**：`{read_depth_counts['DTO_SUMMARY']}` 篇 (權重 0.3)
    *   🔴 **完全未讀 (UNREAD)**：`{read_depth_counts['UNREAD']}` 篇 (權重 0.0)

""")
        if unread_keys:
            f.write("> [!CAUTION]\n> **🔴 以下引用文獻處於完全未讀 (UNREAD) 狀態！**\n> 請親自閱讀並使用 CLI 更新閱讀狀態（如 `-rd cite_key:2` 或 `3`）：\n")
            for k in unread_keys:
                f.write(f"> - `{k}`\n")
            f.write("\n")
            
        if summary_keys:
            f.write("> [!WARNING]\n> **⚠️ 以下引用文獻僅閱讀了 AI 摘要 (DTO_SUMMARY)！**\n> 建議深入簡讀或精讀關鍵論文，以提升研究真實度：\n")
            for k in summary_keys:
                f.write(f"> - `{k}`\n")
            f.write("\n")

        f.write(f"""### 3. 重要文獻遞迴閱讀鏈 (Recursive Digestion Audit - BFS 2-Level)
*   **遞迴閱讀就位率**：`{recursive_digestion_rate:.2f}%` (剛性懲罰：因 {len(undigested_keys)} 篇文獻未消化，其理論根系完全懸空，已乘上已開發覆蓋率 {roots_exploration_factor*100:.1f}%)
*   已開發 A 類文獻之 2 層深度有向關係網絡共涉及 **{recursive_target_total}** 篇底層文獻。
*   其中已在 DB 完成 Ingestion 且就位的文獻：**{recursive_target_ingested}** 篇。

""")
        if recursive_broken_relations:
            f.write("> [!IMPORTANT]\n> **⚠️ 偵測到遞迴閱讀鏈斷裂！**\n> 以下核心文獻的下層演化基底尚未完成 Ingestion，可能導致理論根基浮空，請補充 Ingestion：\n")
            for src, tgt in recursive_broken_relations:
                f.write(f"> - 來源文獻 `{src}` ➔ 其 GROUNDED_ON 基底 `{tgt}` 尚未 Ingestion 就位！\n")
            f.write("\n")

        f.write(f"""### 4. 紅軍自審防線與 Verdict 答辯硬度 (Red-Team Audit)
*   **紅軍自審綜合得分**：`{red_team_score:.2f}%` (防投機投巧計分，覆蓋率佔 60%，答辯 PASS 率佔 40%)
*   **紅軍日誌總數**：**{total_logs}** 筆 (手稿日誌: {len(ms_logs)} 筆, 引文日誌: {len(all_red_team_logs)} 筆)。
*   **自審 PASS 數**：**{pass_logs}** 筆。
*   **整體紅軍自審覆蓋率**：`{red_team_coverage*100:.2f}%`
    *   *引文對抗覆蓋率*: `{cite_coverage_rate*100:.2f}%` ({cites_with_logs_count}/{citations_count} 篇)
    *   *手稿本體覆蓋率*: `{ms_coverage_rate*100:.2f}%`
    *   *答辯 PASS 率*: `{red_team_pass_rate:.2f}%`

""")
        if total_logs > 0 and red_team_coverage < 0.5:
            f.write("> [!CAUTION]\n> **🔴 警告：紅軍對抗覆蓋率過低！**\n> 雖然您現有的答辯日誌都順利通過 (PASS)，但您僅對極少數的文獻進行了紅軍挑戰。這在學術自律中屬於『投機行為』，MCI 指數已對此進行了剛性扣分限制。請儘速為更多 Claims 與 Citations 進行自審答辯！\n\n")

        f.write(f"""### 5. 論文主張 Grounding 完整性 (Claims Grounding Integrity)
*   **主張對合率**：`{claims_grounding_rate:.2f}%` (共 {total_claims_count} 個核心主張)。

""")
        if claims_issues:
            f.write("> [!WARNING]\n> **⚠️ 核心主張 Grounding 缺陷明細：**\n")
            for clm, msg in claims_issues:
                f.write(f"> - 主張: `{clm}`\n>   ➔ 診斷: {msg}\n")
            f.write("\n")

        f.write("""---

## 🎯 4. 哈教授下一步行動指南
1. **防堵根系浮空漏洞**：由於存在大量未消化 (PENDING) 文獻，其底層理論根系完全懸置（就位率被乘上開發因子遭到剛性扣分）。請儘速將這些文獻發動 Stage 2 深度解構與 Ingestion，以提升根系開發覆蓋率。
2. **防堵紅軍投機漏洞**：若紅軍對抗覆蓋率過低，請針對手稿中未對抗的核心主張（Claims）以及頂級引用（Citations）在 `red_team_logs` 中建立自審對抗，並答辯解鎖，以強拉紅軍覆蓋率分數。
3. **補齊未註冊的幽靈引文**：若存在 unregistered 的引文，請使用 `scout_semantic_scholar.py` 探勘落庫。
4. **修補遞迴閱讀鏈**：若偵測到 `GROUNDED_ON` 基底斷裂，請對應 Ingestion 目標文獻，厚化理論地墊。
5. **消滅 TODO 與 Claims 漏洞**：清除手稿中的所有 `TODO`，並為所有 Claim 地圖中無引用的主張補充頂級文獻支持。

*本報告基於 SMMCAP 1.0 自動化審計协议生成，特此證明。*
""")

    print(f"🎉 成熟度審計報告產製成功！已物理寫入: {report_path}")
    print(f"  - MCI 綜合指數: {mci:.2f}% ({mci_tier})")
    print(f"  - 文件成熟度分: {avg_doc_maturity:.2f}%")
    print(f"  - 大腦 Grounding 分: {brain_grounding_score:.2f}%")
    print(f"    - 真實閱讀深度分: {average_reading_score:.2f}%")

if __name__ == "__main__":
    main()
