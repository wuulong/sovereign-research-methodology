#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 主權科研大腦：歷程還原與自證表格提取工具 (extract_evolution_history.py)
----------------------------------------------------------------------
本腳本為大腦「自治自證」之核心工具，負責：
1. 靜態定錨五大關鍵演化代（已進行去識別化保密過濾，不含敏感企業與特定細節）。
2. 動態調用本地 Git log 提取本 Repo (Submodule) 的真實提交歷史。
3. 動態讀取 SQLite 資料庫 (Research_Artifacts.db) 中的紅軍對抗自審 Verdict PASS 記錄。
4. 自動對合時間線，編譯產出 Markdown 時間軸表格，並更新手稿第二章。
"""

import os
import sqlite3
import subprocess
import re

# 專案路徑定義
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPTS_DIR)
DB_PATH = os.path.join(REPO_DIR, "data", "Research_Artifacts.db")
MANUSCRIPT_PATH = os.path.join(REPO_DIR, "manuscripts", "sovereign_research", "sovereign_research_12_evolution_history.md")

# 台灣慣用語轉換字典（將中國用語轉換為台灣用語）
TAIWAN_REPLACEMENTS = {
    "信息": "資訊",
    "項目": "專案",
    "優化": "最佳化",
    "軟件": "軟體",
    "接口": "介面",
    "渠道": "管道",
    "鏈接": "連結",
    "屏幕": "螢幕",
    "數據": "資料",
    "支持": "支援",
    "用戶": "使用者",
    "文檔": "文件",
    "閉環": "完整鏈結",
    "組件": "元件",
    "性能": "效能",
    "質量": "品質",
    "建模": "模型化",
    "範式": "典範",
    "生命周期": "生命週期",
    "佈景": "場景",
    "解碼": "解讀",
    "代碼": "程式碼",
}

def taiwanize_content(content):
    """將內容中的中國用語轉換為台灣慣用語"""
    if not content:
        return ""
    cleaned = content
    for old, new in TAIWAN_REPLACEMENTS.items():
        cleaned = cleaned.replace(old, new)
    return cleaned

# 敏感詞彙保密過濾器 (去識別化對照)
SENSITIVE_PATTERNS = {
    r"(?i)fusheng": "某製造業企業",
    r"復盛": "某製造業企業",
    r"MET-00[0-9]": "系統架構模組",
    r"EXT-00[0-9]": "外部資訊模組",
    r"SIM-00[0-9]": "模擬實踐資料",
}

def clean_sensitive_text(text):
    """將敏感詞彙與用語進行去識別化與台灣本土化處理"""
    if not text:
        return ""
    cleaned = text
    for pattern, replacement in SENSITIVE_PATTERNS.items():
        cleaned = re.sub(pattern, replacement, cleaned)
    cleaned = taiwanize_content(cleaned)
    return cleaned

# 1. 靜態定錨去識別化之五大關鍵演化里程碑
STATIC_MILESTONES = [
    {
        "datetime": "2026-05-10 14:00:00",
        "source": "計畫起源",
        "event": "QMEMS 實驗室學術痛點挖掘（T260510-HHH03）",
        "description": "提出研究生濫用 AI 導致認知掏空的問題。確立 Layer 0-1-2 三層靠泊 Ingestion 流水線、學術重力場 Ga 排序公式以及最初的學者領主宣言草案。",
        "commit_hash": "N/A"
    },
    {
        "datetime": "2026-05-14 10:30:00",
        "source": "企業轉型",
        "event": "某製造業企業 AI 實踐與資料庫大腦原型（T260514-HHH01）",
        "description": "導入 ID-Prefix 標準編碼與模擬實踐數據（SIM）設計以保護企業隱私。首度在 SQLite 中實作大腦資料庫化與 L1-L4 知識分層架構。",
        "commit_hash": "N/A"
    },
    {
        "datetime": "2026-05-20 09:15:00",
        "source": "移植最佳化",
        "event": "10 表聯邦與跨裝置移植性解決（T260520-HHH01）",
        "description": "建構 paper_scout.py 與 academic-research-navigator。為了平抑不同電腦的環境路徑斷線噩夢，導入 directory_roots 目錄抽象解耦設計，並加入 Duffing 實測物理誤差數據，對位專書第 14 章。",
        "commit_hash": "N/A"
    },
    {
        "datetime": "2026-05-26 11:00:00",
        "source": "自審對抗",
        "event": "十一表 Schema 升級與紅軍 Verdict Lock 戰役（T260526-HHH01）",
        "description": "升級為十一表大腦，建立 empirical_evidences 替代舊模擬表。開發 MCI 與 MPM 看板。遭遇 SMMCAP Stale 報告舊數據殘留問題，強制下修 MCI，並於 Socratic 對抗答辯後成功解除合併阻斷鎖。",
        "commit_hash": "N/A"
    },
    {
        "datetime": "2026-06-05 18:00:00",
        "source": "事實修正",
        "event": "06/05 審查會議推遲與開源分離整理（T260526-HHH01 延續）",
        "description": "原定與教授之 face-to-face 盲檢會面因故推遲。於 06/06 先行進行去中心化整理、獨立開源 Repo 分離與公開發表，並將正式面談審查留待下一個階段。",
        "commit_hash": "N/A"
    }
]

def fetch_db_logs():
    """從 SQLite 中提取紅軍對抗與答辯紀錄"""
    db_records = []
    if not os.path.exists(DB_PATH):
        print(f"⚠️ [警告] 找不到實體資料庫於 {DB_PATH}，將跳過資料庫日誌讀取。")
        return db_records

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 檢查 red_team_logs 表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='red_team_logs';")
        if not cursor.fetchone():
            print("⚠️ [警告] 資料庫中無 red_team_logs 表。")
            return db_records

        # 撈取 Verdict PASS 且有答辯的記錄
        query = """
        SELECT test_time, log_id, verdict, reviewer_attack, student_defense 
        FROM red_team_logs 
        ORDER BY test_time ASC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            test_time, log_id, verdict, attack, defense = row
            # 進行去識別化過濾
            clean_finding = clean_sensitive_text(attack)
            clean_defense = clean_sensitive_text(defense)
            
            db_records.append({
                "datetime": test_time if len(test_time) > 10 else f"{test_time} 12:00:00",
                "source": "SQLite DB",
                "event": f"紅軍對抗 ({log_id})",
                "description": f"紅軍質疑: {clean_finding[:60]}... | 學生答辯: {clean_defense[:60]}... [判決: {verdict}]",
                "commit_hash": "N/A"
            })
            
        conn.close()
        print(f"ℹ️ 成功從 SQLite 載入 {len(db_records)} 筆自審答辯歷史。")
    except Exception as e:
        print(f"❌ [錯誤] 讀取資料庫失敗: {e}")
    
    return db_records

def fetch_git_logs():
    """從 Submodule 提取真實的 Git Commit 紀錄（按天合併摘要）"""
    git_records = []
    try:
        # 使用 git log 提取日期 (YYYY-MM-DD), 訊息與 hash
        cmd = ["git", "log", "--date=format:%Y-%m-%d", "--pretty=format:%ad|%s|%h"]
        res = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True, check=True)
        
        lines = res.stdout.strip().split("\n")
        daily_commits = {}  # date -> list of (msg, hash)
        
        for line in lines:
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 3:
                ad, msg, commit_hash = parts
                clean_msg = clean_sensitive_text(msg).strip()
                if not clean_msg:
                    continue
                if ad not in daily_commits:
                    daily_commits[ad] = []
                daily_commits[ad].append((clean_msg, commit_hash))
                
        for date, commits in daily_commits.items():
            # commits 是 git log 逆序（最新的在最前）
            # 我們將其反轉，按時間順序合併訊息
            unique_msgs = []
            seen = set()
            for msg, _ in reversed(commits):
                if msg not in seen:
                    seen.add(msg)
                    unique_msgs.append(msg)
            
            # 合併描述
            if len(unique_msgs) == 1:
                summary_desc = unique_msgs[0]
            else:
                summary_desc = "當日完成多項更新： " + "；".join(unique_msgs)
                
            # 使用當天最新一次提交的 hash
            latest_hash = commits[0][1]
            
            git_records.append({
                "datetime": f"{date} 23:59:59",  # 為了排序，設為當天最後時間
                "source": "Git Submodule",
                "event": "程式碼提交",
                "description": summary_desc,
                "commit_hash": latest_hash
            })
            
        print(f"ℹ️ 成功從 Git 歷史載入並合併為 {len(git_records)} 筆每日 Commit 紀錄。")
    except Exception as e:
        print(f"⚠️ [警告] 無法提取 Git 歷史紀錄: {e}")
    
    return git_records

def generate_evolution_table():
    """整合所有資料源，產生 Markdown 表格"""
    all_events = []
    
    # 載入所有資料源
    all_events.extend(STATIC_MILESTONES)
    all_events.extend(fetch_db_logs())
    all_events.extend(fetch_git_logs())
    
    # 按時間排序
    all_events.sort(key=lambda x: x["datetime"])
    
    # 建立 Markdown 表格
    table_content = []
    table_content.append("| 時間戳記 | 紀錄來源 | 演化事件 | 實體歷程與 Why 設計意圖 | 實體指紋 (Git Commit) |")
    table_content.append("| :--- | :--- | :--- | :--- | :--- |")
    
    for ev in all_events:
        # 換行轉換以防 Markdown 表格崩壞
        desc = ev["description"].replace("\n", " ").replace("|", "\\|")
        event_name = ev["event"].replace("|", "\\|")
        table_content.append(f"| {ev['datetime']} | {ev['source']} | {event_name} | {desc} | `{ev['commit_hash']}` |")
        
    return "\n".join(table_content)

def update_manuscript(table_str):
    """將生成的表格更新寫入手稿"""
    if not os.path.exists(MANUSCRIPT_PATH):
        print(f"❌ [錯誤] 找不到手稿檔案於: {MANUSCRIPT_PATH}")
        return

    try:
        with open(MANUSCRIPT_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        start_tag = "<!-- START_EVOLUTION_TABLE -->"
        end_tag = "<!-- END_EVOLUTION_TABLE -->"

        if start_tag not in content or end_tag not in content:
            print("❌ [錯誤] 手稿中無對應的 `<!-- START_EVOLUTION_TABLE -->` 標籤對。")
            return

        pattern = re.compile(rf"{start_tag}.*?{end_tag}", re.DOTALL)
        replacement = f"{start_tag}\n\n{table_str}\n\n{end_tag}"
        new_content = pattern.sub(replacement, content)
        # 強制進行台灣用語轉換
        new_content = taiwanize_content(new_content)

        with open(MANUSCRIPT_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"🎉 成功更新手稿 {MANUSCRIPT_PATH} 中的建構歷程對合表！")
    except Exception as e:
        print(f"❌ [錯誤] 更新手稿失敗: {e}")

if __name__ == "__main__":
    print("🧠 開始進行主權科研大腦歷史軌跡逆向提煉...")
    table_md = generate_evolution_table()
    update_manuscript(table_md)
    print("✨ 提煉完成。")
