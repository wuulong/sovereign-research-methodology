#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕵️‍♂️ 哈爸主權研究大腦 - 方法論 PoC 實體驗證與自指自證審計腳本 (verify_poc_completeness.py)

目的：
1. 實作 sovereign-poc-verifier 技能。
2. 剛性盲檢底層 SQLite 數據有效性與三位一體對合率。
3. 計量本機工具鏈存在率與無摩擦強韌度。
4. 審計手稿論點地圖中大腦 DTO 物理自指合龍度。
5. 計算 MPM (Meta-Proof Maturity) 元自證成熟度，並物理產出驗證報告。
"""

import os
import re
import sys
import json
import sqlite3
from datetime import datetime

def check_db_integrity(db_path, ms_code):
    """
    第一部分：底層 SQLite 有效性檢驗 (滿分 100)
    """
    if not os.path.exists(db_path):
        return 0.0, ["🔴 嚴重錯誤：找不到主權大腦 SQLite 資料庫！"], {}
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    score = 100.0
    suggestions = []
    stats = {}
    
    # 1. 檢測外鍵約束狀態
    try:
        cursor.execute("PRAGMA foreign_key_check;")
        fk_issues = cursor.fetchall()
        if fk_issues:
            deduction = min(20.0, len(fk_issues) * 5.0)
            score -= deduction
            suggestions.append(f"⚠️ 偵測到 {len(fk_issues)} 處外鍵完整性約束毀損！請修復資料庫外鍵對應。")
        else:
            suggestions.append("💚 SQLite 資料庫外鍵完整性檢驗通過 (0 異常)。")
    except Exception as e:
        score -= 20.0
        suggestions.append(f"🔴 PRAGMA foreign_key_check 執行失敗: {e}")
        
    # 2. 檢測 papers.meta_data JSON 合規解析率
    try:
        cursor.execute("SELECT paper_id, meta_data FROM papers;")
        papers = cursor.fetchall()
        total_papers = len(papers)
        parsed_count = 0
        json_failures = 0
        
        for p_id, meta_str in papers:
            if meta_str:
                try:
                    json.loads(meta_str)
                    parsed_count += 1
                except:
                    json_failures += 1
            else:
                # 允許 meta_data 為空，但不算作 JSON 解析失敗
                parsed_count += 1
                
        json_rate = (parsed_count / total_papers * 100) if total_papers > 0 else 100.0
        if json_failures > 0:
            score -= min(15.0, json_failures * 3.0)
            suggestions.append(f"⚠️ 偵測到 {json_failures} 篇文獻的 meta_data JSON 信封解析毀損，已剛性扣分。")
        else:
            suggestions.append("💚 全庫 papers.meta_data JSON 解析合規率達 100.00%。")
        stats["json_compliance_rate"] = json_rate
    except Exception as e:
        score -= 15.0
        suggestions.append(f"🔴 papers 表 JSON 掃描失敗: {e}")
        stats["json_compliance_rate"] = 0.0

    # 3. 三位一體對合率 (Methodology Grounding Rate)
    # 定義：主題 Topics 中，既有 papers 沉澱 + 有 empirical_evidences 實體舉證 + 有 my_manuscripts 手稿關聯的比例
    try:
        cursor.execute("SELECT topic_id, topic_name FROM topics;")
        topics = cursor.fetchall()
        total_topics = len(topics)
        grounded_topics_count = 0
        details = []
        
        for t_id, t_name in topics:
            # 檢查 papers 沉澱
            cursor.execute("SELECT COUNT(*) FROM papers WHERE topic_id = ?;", (t_id,))
            has_papers = cursor.fetchone()[0] > 0
            
            # 檢查實體舉證 (透過 papers JOIN empirical_evidences)
            cursor.execute("""
                SELECT COUNT(*) FROM empirical_evidences e 
                JOIN papers p ON e.paper_id = p.paper_id 
                WHERE p.topic_id = ?;
            """, (t_id,))
            has_evidence = cursor.fetchone()[0] > 0
            
            # 檢查手稿關聯
            cursor.execute("SELECT COUNT(*) FROM my_manuscripts WHERE topic_id = ?;", (t_id,))
            has_ms = cursor.fetchone()[0] > 0
            
            if has_papers and has_evidence and has_ms:
                grounded_topics_count += 1
                details.append(f"  - `[Grounded]` 主題: {t_name} (文獻/實證/手稿三位一體合龍)")
            else:
                missing = []
                if not has_papers: missing.append("文獻沉澱")
                if not has_evidence: missing.append("本地實體實證")
                if not has_ms: missing.append("手稿產出")
                details.append(f"  - `[Pending]` 主題: {t_name} (缺少: {', '.join(missing)})")
                
        grounding_rate = (grounded_topics_count / total_topics * 100) if total_topics > 0 else 100.0
        
        # 剛性扣分限制：三位一體對合率直接乘上加權扣分
        deduction = (100.0 - grounding_rate) * 0.4
        score -= deduction
        
        suggestions.append(f"📊 主題三位一體實質率：{grounding_rate:.2f}% ({grounded_topics_count}/{total_topics} 主題完成合龍)")
        stats["grounding_rate"] = grounding_rate
        stats["grounding_details"] = details
    except Exception as e:
        score -= 20.0
        suggestions.append(f"🔴 三位一體對合檢驗失敗: {e}")
        stats["grounding_rate"] = 0.0
        stats["grounding_details"] = []
        
    conn.close()
    score = max(0.0, min(100.0, score))
    return score, suggestions, stats

def check_toolchain_friction(base_dir):
    """
    第二部分：工具鏈無摩擦率 (滿分 100)
    """
    score = 0.0
    suggestions = []
    
    scripts_to_check = {
        "verify_manuscript_maturity.py": "MCI 審計與成熟度報告產出腳本",
        "brain_cli.py": "資料庫快速探勘命令行工具",
        "hydrate_paper_assets.py": "PDF下載與 Markdown 預萃取就位腳本",
        "hydrate_citations_and_gravity.py": "學術重力 Ga 算分與灌溉腳本",
        "sync_zotero_to_staging.py": "Zotero 本地一鍵同步腳本",
        "harvest_flow_to_db.py": "會後自審日誌與對話脆弱點提取落庫腳本",
        "audit_brain_compliance.py": "全庫 metadata 品質合規性打打標腳本",
        "verify_poc_completeness.py": "方法論 PoC 實體驗證與自指自審審計腳本"
    }
    
    found_count = 0
    missing_scripts = []
    
    for filename, desc in scripts_to_check.items():
        script_path = os.path.join(base_dir, "scripts", filename)
        if os.path.exists(script_path):
            found_count += 1
            # 每個存在給 12.5 分
            score += 12.5
        else:
            missing_scripts.append(filename)
            
    if missing_scripts:
        suggestions.append(f"⚠️ 偵測到 {len(missing_scripts)} 個核心支援腳本遺失：{', '.join(missing_scripts)}")
    else:
        suggestions.append("💚 八大核心支援腳本實體全數就位，工具鏈存在率 100.00%！")
        
    # 可行性編譯與執行檢測：檢查 brain_cli.py 是否可無錯編譯執行
    brain_cli_path = os.path.join(base_dir, "scripts", "brain_cli.py")
    if os.path.exists(brain_cli_path):
        try:
            import subprocess
            # 以 --help 測試其是否可無摩擦執行
            result = subprocess.run([sys.executable, brain_cli_path, "--help"], capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                suggestions.append("💚 核心工具 brain_cli.py 編譯與無摩擦執行測試通過。")
            else:
                score -= 10.0
                suggestions.append("🔴 核心工具 brain_cli.py 執行測試失敗，回傳碼非 0，已進行剛性扣分！")
        except Exception as e:
            score -= 10.0
            suggestions.append(f"🔴 核心工具編譯執行測試異常: {e}")
    else:
        score -= 10.0
        suggestions.append("🔴 由於 brain_cli.py 遺失，無法發動無摩擦執行測試！")
        
    score = max(0.0, min(100.0, score))
    return score, suggestions

def check_self_referentiality(base_dir, ms_code):
    """
    第三部分：手稿第 15 章自指自證度 (滿分 100)
    """
    score = 100.0
    suggestions = []
    
    ms_subdir = os.path.join(base_dir, "manuscripts", ms_code)
    if os.path.exists(ms_subdir) and os.path.isdir(ms_subdir):
        apm_path = os.path.join(ms_subdir, f"{ms_code}_06_argument_map.md")
        manuscript_path = os.path.join(ms_subdir, f"{ms_code}_05_manuscript.md")
    else:
        apm_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_06_argument_map.md")
        manuscript_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_05_manuscript.md")
    
    if not os.path.exists(apm_path):
        return 0.0, ["🔴 嚴重錯誤：找不到手稿論點地圖 argument_map.md，無法進行自指自證審計！"]
        
    with open(apm_path, 'r', encoding='utf-8', errors='ignore') as f:
        apm_content = f.read()
        
    # 1. 檢索是否物理匯入並包含了 DTO JSON 數據 (代表大腦指紋實體定錨)
    # 搜尋大腦 schema 特徵關鍵字，例如 "empirical_evidences" 或 "evidence_payload"
    has_dto = "empirical_evidences" in apm_content or "evidence_payload" in apm_content or "Research_Artifacts.db" in apm_content
    if has_dto:
        suggestions.append("💚 手稿論點地圖中已物理定錨「大腦資料庫實體匯出/指紋」，通過自指自證檢核。")
    else:
        score -= 40.0
        suggestions.append("⚠️ 警告：手稿論點地圖尚未物理包含大腦 SQLite DTO 數據，根基尚未與資料庫雙向合龍！")
        
    # 2. 檢索手稿 TODO 懸置點
    todo_count = len(re.findall(r'(TODO|Draft|\[\s*\])', apm_content, re.IGNORECASE))
    if os.path.exists(manuscript_path):
        with open(manuscript_path, 'r', encoding='utf-8', errors='ignore') as f:
            todo_count += len(re.findall(r'(TODO|Draft|\[\s*\])', f.read(), re.IGNORECASE))
            
    if todo_count > 0:
        deduction = min(30.0, todo_count * 5.0)
        score -= deduction
        suggestions.append(f"⚠️ 偵測到手稿中存在 {todo_count} 個 TODO/Draft 懸置點，破壞了自指自證的完整度！")
    else:
        suggestions.append("💚 手稿聯邦無任何 TODO/Draft 標記，內容自洽完整。")
        
    # 3. 論文第 15 章自指自證度 (檢查 manuscript_citations 有無 topic_id = 'top_sovereign_methodology' 的靠泊文獻)
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # 撈取該手稿在 papers 中引用的 STAGE_2_DEEP 且屬於 sovereign_methodology 的文獻
            cursor.execute("""
                SELECT COUNT(*) FROM papers p
                JOIN manuscript_citations c ON p.paper_id = c.paper_id
                WHERE p.topic_id = 'top_sovereign_methodology' AND json_extract(p.meta_data, '$.stage') = 'STAGE_2_DEEP';
            """)
            sovereign_cites = cursor.fetchone()[0]
            conn.close()
            
            if sovereign_cites >= 3:
                suggestions.append(f"💚 手稿第 15 章已有 {sovereign_cites} 篇主權方法論 STAGE_2_DEEP 頂級引文硬地墊支持！")
            else:
                score -= 30.0
                suggestions.append(f"⚠️ 警告：手稿中屬於主權方法論的 Stage 2 消化引文僅 {sovereign_cites} 篇（目標 \\ge 3 篇），學術地墊硬度不足！")
        except Exception as e:
            score -= 15.0
            suggestions.append(f"🔴 自指引文資料庫審計失敗: {e}")
    else:
        score -= 30.0
        suggestions.append("🔴 由於資料庫遺失，無法完成自指引文資料庫審計！")
        
    score = max(0.0, min(100.0, score))
    return score, suggestions

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    ms_code = "sovereign_research"
    if len(sys.argv) > 1:
        ms_code = sys.argv[1].strip()
        
    print(f"🕵️‍♂️ 啟動哈爸主權方法論 PoC 實體驗證系統 (SMPRR Verifier v1.0, MS_CODE: {ms_code})...")
    
    # 1. 執行三大板塊檢核
    db_score, db_sugs, db_stats = check_db_integrity(db_path, ms_code)
    tool_score, tool_sugs = check_toolchain_friction(base_dir)
    self_score, self_sugs = check_self_referentiality(base_dir, ms_code)
    
    # 2. 計算 MPM 指數
    mpm = (db_score * 0.40) + (tool_score * 0.30) + (self_score * 0.30)
    
    if mpm >= 90.0:
        mpm_tier = "🟢 完美自指自證 (Elite Self-Proof - A+)"
        verdict = "哈教授評語：Verdict PASS！底層資料庫堅若磐石，工具鏈流暢可用，手稿第 15 章自指自證閉環完整。行解合一之極致典範，准予論文合龍釋出！"
    elif mpm >= 70.0:
        mpm_tier = "🟡 良好自證進展 (Solid Proof Progress - B)"
        verdict = "哈教授評語：良好！大腦工具與底層 SQLite 運行基本流暢，但手稿與大腦資料庫的雙向自指合龍（第 15 章 DTO 匯入與主權引文消化）仍有盲區。請儘速補齊！"
    elif mpm >= 45.0:
        mpm_tier = "🟠 自證草創階段 (Proof Under Development - C)"
        verdict = "哈教授評語：自證初建。SQLite 存在多處空洞，工具鏈有缺損，手稿中仍殘留 TODO。請老老實實修補工具並完成自指合龍！"
    else:
        mpm_tier = "🔴 嚴重空殼警告 (Empty Scaffolding - F)"
        verdict = "哈教授評語：致命警告！底層資料庫嚴重毀損，工具鏈癱瘓，手稿與資料庫完全斷線。此狀態下之方法論為空殼泡沫，無任何科學效度，不予通過！"
        
    # 3. 物理寫入報告
    ms_subdir = os.path.join(base_dir, "manuscripts", ms_code)
    if os.path.exists(ms_subdir) and os.path.isdir(ms_subdir):
        report_path = os.path.join(ms_subdir, f"{ms_code}_10_poc_proof_report.md")
    else:
        report_path = os.path.join(base_dir, "manuscripts", f"{ms_code}_10_poc_proof_report.md")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"""# 🕵️‍♂️ 哈爸主權方法論 PoC 實體驗證與自指自證報告 (SMPRR Audit Report)
*評估時間戳記：{now_str}* | *定錨手稿代碼：`{ms_code}`*

> [!NOTE]
> 本報告由 `sovereign-poc-verifier`（主權自證驗證器技能）物理產出。  
> 它剛性盲檢了底層 SQLite 資料庫的物理完整性與三位一體對合率，計量了本機工具鏈的無摩擦存在率，
> 並審計了手稿論點地圖中大腦 DTO 物理自指合龍度。拒絕 AI 八股，以物理數據強制自證！

---

## 📊 1. Meta-Proof Maturity (MPM) 元自證看板

```
┌────────────────────────────────────────────────────────┐
│  MPM 元自證成熟度指數： {mpm:.2f}%                               │
│  當前等級： {mpm_tier}                          │
└────────────────────────────────────────────────────────┘
```

> **{verdict}**

### 📈 三大元板塊加權明細
*   **底層 SQLite 有效性檢驗 (40% 權重)**：`{db_score:.2f}%`
    *   *JSON 解析合規率*: `{db_stats.get('json_compliance_rate', 0.0):.2f}%`
    *   *主題三位一體實質率*: `{db_stats.get('grounding_rate', 0.0):.2f}%`
*   **工具鏈無摩擦高可用性 (30% 權重)**：`{tool_score:.2f}%` (八大核心腳本存在率與執行可用度)
*   **手稿第 15 章自指自證度 (30% 權重)**：`{self_score:.2f}%` (大腦指紋實體定錨度與無 TODO 完備率)

---

## 🏗️ 2. 底層 SQLite 資料庫實體有效性審計
本模組盲檢了 SQLite 中所有 Topics 主題，檢核其是否確實完成「文獻沉澱 ＋ 本地實體舉證 ＋ 手稿產出」的三位一體合龍：

| 主題三位一體合龍明細 |
| :--- |
""")
        for detail in db_stats.get('grounding_details', []):
            f.write(f"{detail}\n")
            
        f.write(f"""
---

## 🛠️ 3. 工具鏈無摩擦高可用性計量
本模組評估本機 `scripts/` 下的工具鏈可用性，排除執行阻礙：

""")
        for sug in tool_sugs:
            f.write(f"- {sug}\n")
            
        f.write(f"""
---

## 📝 4. 手稿第 15 章自指自證度審計
本模組盲檢手稿與大腦 SQLite 數據的雙向自我指涉（Self-Referentiality）合龍度：

""")
        for sug in self_sugs:
            f.write(f"- {sug}\n")
            
        for sug in db_sugs:
            f.write(f"- {sug}\n")
            
        f.write(f"""
---

## 🎯 5. 元自證下一步行動指南
1. **補齊手稿中未引渡的主張**：目前仍有部分核心主張缺乏學術文獻地墊，請引渡高重力文獻定錨。
2. **消滅手稿中的 TODO**：清除手稿中所有 `TODO` 或 `Draft` 標記，以提升自指自證完整度。
3. **完成大腦指紋 DTO 合龍**：確保手稿論點地圖中確實物理匯入並包含了 `Research_Artifacts.db` 的純文字 DTO JSON，完成雙向合龍閉環。
4. **推動未合龍主題的三位一體**：針對處於 `[Pending]` 狀態的主題，補齊其「本地實體實證」或「手稿產出」，以拉升對合率。

*本報告基於 SMPRR 1.0 元自證審計協定生成，特此物理自證。*
""")

    print(f"🎉 元自證審計報告產製成功！已物理寫入: {report_path}")
    print(f"  - MPM 元自證指數: {mpm:.2f}% ({mpm_tier})")
    print(f"  - DB 有效性分數: {db_score:.2f}%")
    print(f"  - 工具無摩擦分: {tool_score:.2f}%")
    print(f"  - 手稿自指自證分: {self_score:.2f}%")

if __name__ == "__main__":
    main()
