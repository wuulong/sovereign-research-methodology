#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 資料庫初始化工具 (setup_research_db.py)

目的：
1. 載入 schema.sql 建立全新十一表結構。
2. 預載哈爸的環境路徑對合 (directory_roots)。
3. 預載哈爸專屬三大真實專案與一格 Zotero 公海緩衝專案，作為永恆地基。
"""

import os
import sqlite3
import json

# ==============================================================================
# 哈爸專屬四大專案與 Topics 永恆骨架 (新增 prj_sync 緩衝區)
# ==============================================================================
PROJECTS_SEED = [
    {
        "project_id": "prj_tdhi",
        "project_name": "TDHI 台灣數位健康生態系實踐沙箱",
        "description": "台灣數位健康研究院 (TDHI) 的 PoC 實踐沙箱。包含門診分流路由、四分離資料庫、個資邊緣去識別化遮蔽，以及健保處方前置攔截審查機制。",
        "search_spec": {"keywords": ["Digital Health", "TFVH router", "de-identification"], "min_year": 2022},
        "architecture_spec": {"hospital_model": "TFVH", "patient_target": "蓬萊 004", "db_architecture": "四分離 SQLite"}
    },
    {
        "project_id": "prj_river_exploration",
        "project_name": "AI 流域學與河流探索專案",
        "description": "利用 AI 與多模態大模型進行台灣山區水文與河流流域的標準化探索（曾文溪、台南古河道）。整合 GIS 圖資、Open Data，以及『書＋資料庫＋遊記』三位一體實踐。",
        "search_spec": {"keywords": ["mountain hydrology", "river exploration", "triad methodology"], "min_year": 2020},
        "architecture_spec": {"methodology": "書-DB-遊記三位一體", "gis_platform": "QGIS & sqlite-vec"}
    },
    {
        "project_id": "prj_ai_enablement",
        "project_name": "AI 應用與賦能研究專案",
        "description": "研究個人 AI 賦能（BMAD 方法論、裝備化 Skill CLI）、組織級知識治理架構，以及 DeepSeek-R1 與推理時計算最佳化等前沿 AI 研究方法。",
        "search_spec": {"keywords": ["personal AI enablement", "organizational knowledge governance", "DeepSeek-R1 reasoning"], "min_year": 2024},
        "architecture_spec": {"methodology_framework": "BMAD-method / Haba-Quadrilogy", "core_technologies": ["DeepSeek-R1", "CAG"]}
    },
    {
        "project_id": "prj_sync",
        "project_name": "Zotero 聯邦公海文獻同步專案",
        "description": "作為哈爸 Zotero 外部他者知識海的一鍵同步緩衝區 (Staging Area)。所有同步文獻均以 Zotero 原始編碼落庫在此，可動態重定向引渡靠泊至其他主權專案碼頭。",
        "search_spec": {"keywords": ["all_zotero_sync"], "min_year": 1900},
        "architecture_spec": {"sync_engine": "sync_zotero_to_staging.py", "buffer_mode": "Abstract Staging Gate"}
    }
]

TOPICS_SEED = [
    # prj_tdhi Topics
    {
        "topic_id": "top_deidentification",
        "project_id": "prj_tdhi",
        "topic_name": "邊緣 PHI 去識別化與隱私安全漫遊",
        "sequence_order": 1,
        "status": "COMPLETED",
        "focus_spec": {"focus_variables": ["deidentification_rate"], "equations": ["K-Anonymity"], "auto_tags": ["Privacy-Deid"]}
    },
    {
        "topic_id": "top_clinical_routing",
        "project_id": "prj_tdhi",
        "topic_name": "診間語音病歷結構化與科室 AI 路由",
        "sequence_order": 2,
        "status": "ACTIVE",
        "focus_spec": {"focus_variables": ["routing_accuracy"], "equations": ["TFVHOutpatientRouter"], "auto_tags": ["Clinical-AI"]}
    },
    # prj_river_exploration Topics
    {
        "topic_id": "top_river_gis_prep",
        "project_id": "prj_river_exploration",
        "topic_name": "河流流域 GIS 數據準備與 QGIS 樣式注入",
        "sequence_order": 1,
        "status": "COMPLETED",
        "focus_spec": {"focus_variables": ["VRT_rendering_speed"], "equations": ["Spatial_Distance"], "auto_tags": ["GIS-OpenData"]}
    },
    {
        "topic_id": "top_multimodal_hydrology",
        "project_id": "prj_river_exploration",
        "topic_name": "多模態 AI 山區水文觀測與現地真值比對",
        "sequence_order": 2,
        "status": "ACTIVE",
        "focus_spec": {"focus_variables": ["water_flow_pixel_deviation"], "equations": ["Manning_Equation"], "auto_tags": ["Mountain-Hydrology"]}
    },
    # prj_ai_enablement Topics
    {
        "topic_id": "top_personal_empowerment",
        "project_id": "prj_ai_enablement",
        "topic_name": "個人 AI 賦能與裝備化 Skill 封裝",
        "sequence_order": 1,
        "status": "COMPLETED",
        "focus_spec": {"focus_variables": ["skill_execution_friction"], "equations": ["BMAD_Entropy"], "auto_tags": ["Sovereign-AI"]}
    },
    {
        "topic_id": "top_organizational_knowledge",
        "project_id": "prj_ai_enablement",
        "topic_name": "組織級知識庫架構與 CAG vs RAG 知識架構評估",
        "sequence_order": 2,
        "status": "ACTIVE",
        "focus_spec": {"focus_variables": ["CAG_latency"], "equations": ["Cache_Hit_Efficiency"], "auto_tags": ["Knowledge-Engineering"]}
    },
    {
        "topic_id": "top_reasoning_models",
        "project_id": "prj_ai_enablement",
        "topic_name": "DeepSeek-R1 與推理時計算思考鏈擴展",
        "sequence_order": 3,
        "status": "PLANNED",
        "focus_spec": {"focus_variables": ["test_time_compute_length"], "equations": ["RL_Reward_Loss"], "auto_tags": ["DeepSeek-R1"]}
    },
    # prj_sync Topics
    {
        "topic_id": "top_haba_staging",
        "project_id": "prj_sync",
        "topic_name": "哈爸 Zotero 聯邦公海文獻緩衝區",
        "sequence_order": 1,
        "status": "ACTIVE",
        "focus_spec": {"focus_variables": ["sync_friction", "ingestion_volume"], "equations": [], "auto_tags": ["Zotero-Sync"]},
        "meta_data": "Zotero 原始同步文獻的公海收容所，用於動態靠泊重定向。"
    },
    # prj_ai_enablement 新增主題
    {
        "topic_id": "top_sovereign_methodology",
        "project_id": "prj_ai_enablement",
        "topic_name": "主權 AI 協作研究方法論與大腦 DTO 對合",
        "sequence_order": 4,
        "status": "ACTIVE",
        "focus_spec": {"focus_variables": ["MCI_index", "SMMCAP_compliance"], "equations": ["MCI_formula"], "auto_tags": ["Sovereign-Research"]},
        "meta_data": "本方法論的核心論文寫作主戰場。"
    }
]

MANUSCRIPTS_SEED = [
    {
        "manuscript_id": "ms_conf_haba_2026",
        "topic_id": "top_sovereign_methodology",
        "title": "基於書-DB-遊記三位一體之台灣山區河流流域 AI 探索 PoC 實踐",
        "cite_key": "Haba2026Conf",
        "manuscript_type": "Conference",
        "evolution_stage": "Published",
        "previous_manuscript_id": None
    },
    {
        "manuscript_id": "ms_sovereign_research_2026",
        "topic_id": "top_sovereign_methodology",
        "title": "AI 時代的學術革命：基於本地主權大腦、品位裁決與遞迴重構的人機協作研究方法論",
        "cite_key": "ms_sovereign_research_2026",
        "manuscript_type": "Journal",
        "evolution_stage": "Writing",
        "previous_manuscript_id": "ms_conf_haba_2026"
    }
]

def setup_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    schema_path = os.path.join(base_dir, "schema.sql")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    if os.path.exists(db_path):
        print(f"🧹 偵測到既有資料庫，正在進行清理以重新載入 DDL: {db_path}")
        try:
            os.remove(db_path)
        except Exception as e:
            print(f"⚠️ 無法刪除舊資料庫檔案: {e}")
            
    print(f"🌱 正在連線並初始化 SQLite 資料庫: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if os.path.exists(schema_path):
        print(f"💾 載入 DDL 定義檔: {schema_path}")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print("✅ 十一表主權聯邦結構 DDL 初始化成功！")
    else:
        raise FileNotFoundError(f"找不到 schema.sql 於: {schema_path}")
        
    print("🚀 正在預先配置哈爸的環境路徑路由 (directory_roots)...")
    roots_to_insert = [
        ("workspace_root", "STUDENT_LOCAL", "haba", "/Users/wuulong/github/bmad-pa/", {"description": "哈爸個人專案程式碼庫根目錄"}),
        ("zotero_storage", "STUDENT_LOCAL", "haba", "/Users/wuulong/Zotero/storage/", {"description": "哈爸個人 Zotero 本地文獻 PDF 儲存目錄"}),
        ("lab_nas", "STUDENT_LOCAL", "haba", "/Volumes/VRES_NAS/archive/", {"description": "哈爸個人或實驗室 NAS 伺服器掛載路徑"}),
        ("remote_url", "GLOBAL_WEB", "internet", "", {"description": "網際網路線上遠端 HTTP 資源入口"})
    ]
    for r_key, o_type, o_name, abs_path, meta in roots_to_insert:
        cursor.execute("""
        INSERT INTO directory_roots (root_key, owner_type, owner_name, absolute_path, meta_data)
        VALUES (?, ?, ?, ?, ?);
        """, (r_key, o_type, o_name, abs_path, json.dumps(meta, ensure_ascii=False)))
        
    print("🚀 正在預先寫入哈爸專屬三大真實專案與 Topics 永恆骨架...")
    for p in PROJECTS_SEED:
        cursor.execute("""
        INSERT INTO projects (project_id, project_name, description, search_spec, architecture_spec, meta_data)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (
            p["project_id"],
            p["project_name"],
            p["description"],
            json.dumps(p["search_spec"], ensure_ascii=False),
            json.dumps(p["architecture_spec"], ensure_ascii=False),
            json.dumps({"owner": "haba", "role": "哈教授"}, ensure_ascii=False)
        ))
        
    for t in TOPICS_SEED:
        cursor.execute("""
        INSERT INTO topics (topic_id, project_id, topic_name, sequence_order, focus_spec, status, meta_data)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            t["topic_id"],
            t["project_id"],
            t["topic_name"],
            t["sequence_order"],
            json.dumps(t["focus_spec"], ensure_ascii=False),
            t["status"],
            json.dumps({"stage_notes": "哈爸專屬專案分期里程碑"}, ensure_ascii=False)
        ))
        
    print("🚀 正在預先寫入哈爸手稿演化鏈種子資料...")
    for m in MANUSCRIPTS_SEED:
        cursor.execute("""
        INSERT INTO my_manuscripts (manuscript_id, topic_id, title, cite_key, manuscript_type, evolution_stage, previous_manuscript_id, meta_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            m["manuscript_id"],
            m["topic_id"],
            m["title"],
            m["cite_key"],
            m["manuscript_type"],
            m["evolution_stage"],
            m["previous_manuscript_id"],
            json.dumps({"owner": "haba", "overleaf_url": "https://overleaf.com/project/ms_sovereign_2026"}, ensure_ascii=False)
        ))
        
    conn.commit()
    conn.close()
    print("🎉 資料庫 DDL、專案與 Topics 永恆骨架設定完全成功！\n")

if __name__ == "__main__":
    setup_db()
