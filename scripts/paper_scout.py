#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 論文探勘與高擬真資料灌入工具 (paper_scout.py)
"""

import os
import sys
import argparse
import urllib.request
import urllib.parse
import json
import sqlite3
from datetime import datetime

# ==============================================================================
# 哈爸專屬三大真實研究專案 - 本地離線高高擬真資料集
# ==============================================================================

MOCK_PROJECTS = [
    {
        "project_id": "prj_tdhi",
        "project_name": "TDHI 台灣數位健康生態系實踐沙箱",
        "description": "台灣數位健康研究院 (TDHI) 的概念驗證 (PoC) 實踐沙箱。包含豐榮虛擬醫院 (TFVH) 門診分流路由、四分離資料庫、個資邊緣去識別化遮蔽，以及健保處方前置攔截審查機制。",
        "search_spec": {
            "keywords": ["Digital Health", "TFVH router", "claim prescreener", "REDCap harmonizer", "de-identification"],
            "exclude": ["telemedicine hardware"],
            "min_year": 2022
        },
        "architecture_spec": {
            "hospital_model": "TFVH (豐榮虛擬醫院)",
            "patient_target": "蓬萊 004 (多發性骨髓瘤)",
            "privacy_standard": "隱私標籤剝離投射法",
            "db_architecture": "四分離 SQLite 物理隔離庫"
        }
    },
    {
        "project_id": "prj_river_exploration",
        "project_name": "AI 流域學與河流探索專案",
        "description": "利用 AI 與多模態大模型進行台灣山區水文與河流流域的標準化探索。整合流域圖資、Open Data 擷取，以及『書＋資料庫＋遊記』三位一體實踐方法論。",
        "search_spec": {
            "keywords": ["mountain hydrology", "river exploration", "QGIS VRT style", "triad methodology", "GPS track"],
            "exclude": ["oceanography"],
            "min_year": 2020
        },
        "architecture_spec": {
            "methodology": "書-DB-遊記三位一體",
            "gis_platform": "QGIS & sqlite-vec",
            "target_rivers": ["Zengwen River (曾文溪)", "Tainan historical channels (台南古河道)"],
            "true_value_calibration": "WalkGIS 航跡與現地尺規校正"
        }
    },
    {
        "project_id": "prj_ai_enablement",
        "project_name": "AI 應用與賦能研究專案",
        "description": "研究個人 AI 賦能（BMAD 方法論、裝備化 Skill CLI）、企業 GenAI 轉型治理架構，以及 DeepSeek-R1 與推理時計算（Test-Time Compute）最佳化等前沿 AI 研究方法。",
        "search_spec": {
            "keywords": ["personal AI enablement", "enterprise GenAI", "DeepSeek-R1 reasoning", "CAG vs RAG", "test-time compute"],
            "exclude": ["hardware training", "asics"],
            "min_year": 2024
        },
        "architecture_spec": {
            "methodology_framework": "BMAD-method / Haba-Quadrilogy",
            "core_technologies": ["DeepSeek-R1", "Cache-Augmented Generation (CAG)", "Sovereign-Agentic-CLI"],
            "evaluation_metrics": ["Inference-time compute scaling", "Retrieval robustness"]
        }
    }
]

MOCK_TOPICS = [
    # prj_tdhi Topics
    {
        "topic_id": "top_deidentification",
        "project_id": "prj_tdhi",
        "topic_name": "邊緣 PHI 去識別化與隱私漫遊",
        "sequence_order": 1,
        "status": "COMPLETED",
        "focus_spec": {
            "focus_variables": ["deidentification_rate", "REDCap_harmonization_speed"],
            "equations": ["K-Anonymity_Metric", "L-Diversity"],
            "auto_tags": ["Privacy-Deid", "Clinical-AI"]
        }
    },
    {
        "topic_id": "top_clinical_routing",
        "project_id": "prj_tdhi",
        "topic_name": "診間語音病歷結構化與科室 AI 路由",
        "sequence_order": 2,
        "status": "ACTIVE",
        "focus_spec": {
            "focus_variables": ["routing_accuracy", "SOAP_structural_completeness"],
            "equations": ["TFVHOutpatientRouter_Algorithm"],
            "auto_tags": ["Medical-Reasoning", "FHIR-Smart"]
        }
    },
    # prj_river_exploration Topics
    {
        "topic_id": "top_river_gis_prep",
        "project_id": "prj_river_exploration",
        "topic_name": "河流流域 GIS 數據準備與 QGIS 樣式注入",
        "sequence_order": 1,
        "status": "COMPLETED",
        "focus_spec": {
            "focus_variables": ["VRT_rendering_speed", "sqlite-vec_search_latency"],
            "equations": ["Spatial_Distance_Formula"],
            "auto_tags": ["GIS-OpenData", "Triad-Methodology"]
        }
    },
    {
        "topic_id": "top_multimodal_hydrology",
        "project_id": "prj_river_exploration",
        "topic_name": "多模態 AI 山區水文觀測與現地真值比對",
        "sequence_order": 2,
        "status": "ACTIVE",
        "focus_spec": {
            "focus_variables": ["water_flow_pixel_deviation", "high_drive_non_linear_errors"],
            "equations": ["Bioheat_Transfer_Equation", "Manning_Equation_Flow_Rate"],
            "auto_tags": ["Mountain-Hydrology", "Multimodal-CV", "Fieldwork-TrueValue"]
        }
    },
    # prj_ai_enablement Topics
    {
        "topic_id": "top_personal_empowerment",
        "project_id": "prj_ai_enablement",
        "topic_name": "個人 AI 賦能與裝備化 Skill 封裝",
        "sequence_order": 1,
        "status": "COMPLETED",
        "focus_spec": {
            "focus_variables": ["skill_execution_friction", "cognitive_retention_rate"],
            "equations": ["BMAD_System_Entropy_Reduction"],
            "auto_tags": ["Sovereign-AI", "Prompt-Engineering"]
        }
    },
    {
        "topic_id": "top_enterprise_transformation",
        "project_id": "prj_ai_enablement",
        "topic_name": "企業 GenAI 轉型與 CAG vs RAG 知識架構評估",
        "sequence_order": 2,
        "status": "ACTIVE",
        "focus_spec": {
            "focus_variables": ["CAG_retrieval_latency", "RAG_hallucination_rate"],
            "equations": ["Cache_Hit_Efficiency_Metric"],
            "auto_tags": ["Enterprise-GenAI", "CAG-vs-RAG"]
        }
    },
    {
        "topic_id": "top_reasoning_models",
        "project_id": "prj_ai_enablement",
        "topic_name": "DeepSeek-R1 與推理時計算思考鏈擴展",
        "sequence_order": 3,
        "status": "PLANNED",
        "focus_spec": {
            "focus_variables": ["test_time_compute_token_length", "complex_reasoning_accuracy"],
            "equations": ["RL_Reward_Model_Loss"],
            "auto_tags": ["DeepSeek-R1", "Test-Time-Compute"]
        }
    }
]

MOCK_PAPERS = [
    {
        "paper_id": "zotero_huatuo_gpt_o1",
        "cite_key": "HuatuoGPTo1_2024",
        "topic_id": "top_clinical_routing",
        "title": "HuatuoGPT-o1：大模型在醫療複雜推理應用之探索",
        "authors": "Huatuo-AI Team",
        "year": 2024,
        "core_method": "醫療領域推理思考鏈激發技術 (Medical complex reasoning chain-of-thought)",
        "bibtex": """@article{HuatuoGPTo1_2024,
  author = {Huatuo-AI Team},
  title = {HuatuoGPT-o1, Towards Medical Complex Reasoning with LLMs},
  journal = {arXiv preprint arXiv:2412.25000},
  year = {2024}
}""",
        "meta_data": {
            "clinical_reasoning_accuracy": 92.5,
            "target_diseases": ["Multiple Myeloma (多發性骨髓瘤)", "Leukemia"],
            "reasoning_model": "HuatuoGPT-o1"
        },
        "abstract": "本論文展示了醫療大語言模型在複雜臨床推理中的表現。我們透過優化醫學邏輯思考鏈 (o1-like CoT)，使模型在面對血液癌症多發性骨髓瘤 (如同蓬萊004病患) 的用藥路徑與給付預審時，能自主引導思考，大幅降低傳統 LLM 的醫學幻覺，為虛擬醫院 TFVH 的診間助理提供了極高可信度的臨床決策支持。",
        "urls": [
            {"type": "arxiv_pdf", "link": "https://arxiv.org/pdf/2412.25000.pdf"},
            {"type": "local_pdf", "link": "file:///Users/wuulong/Zotero/storage/HuatuoGPT_o1_2024.pdf"}
        ],
        "tags": ["Clinical-AI", "Medical-Reasoning", "FHIR-Smart"]
    },
    {
        "paper_id": "zotero_multimodal_hydrology",
        "cite_key": "Wuulong2024Hydrology",
        "topic_id": "top_multimodal_hydrology",
        "title": "多模態大模型於水文學之應用：GPT-4V, Gemini, LLaVa 比較研究",
        "authors": "吳烏龍 (W. Wuulong), 張學術 (H. Chang)",
        "year": 2024,
        "core_method": "多模態視覺大型語言模型於山區水文觀測應用 (GPT-4V/Gemini 對比評估)",
        "bibtex": """@article{Wuulong2024Hydrology,
  author = {Wuulong, W. and Chang, H.},
  title = {The Implementation of Multimodal Large Language Models for Hydrological Applications: A Comparative Study of GPT-4 Vision, Gemini, LLaVa, and Multimodal-GPT},
  journal = {Journal of Hydrological Engineering},
  year = {2024},
  volume = {29},
  pages = {305--320}
}""",
        "meta_data": {
            "theoretical_water_flow_error": 12.5,
            "vision_models": ["GPT-4V", "Gemini Pro Vision", "LLaVa-1.5"],
            "study_area": "曾文溪流域與台南古河道"
        },
        "abstract": "本論文探討將多模態大模型應用於山區水文觀測（特別是河道流量與枯水期特徵影像分析）的表現。研究表明，多模態大語言模型在解析空拍河道影像與辨識流路時具備極高潛力，但在枯水期極易將泥沙淤積誤判為水流通道。本研究推導了多模態模型流量估算偏差，並指出必須結合現地 WalkGIS 軌跡與高程尺規進行真值校正。",
        "urls": [
            {"type": "publisher", "link": "https://ascelibrary.org/journal/jhyeaq/mock_wuulong_2024"},
            {"type": "local_pdf", "link": "file:///Users/wuulong/Zotero/storage/Hydrology_Implementation_2024.pdf"}
        ],
        "tags": ["Mountain-Hydrology", "Multimodal-CV", "Fieldwork-TrueValue"]
    },
    {
        "paper_id": "zotero_deepseek_r1",
        "cite_key": "DeepSeek2025R1",
        "topic_id": "top_reasoning_models",
        "title": "DeepSeek-R1：透過強化學習激發大語言模型之推理能力",
        "authors": "DeepSeek-AI",
        "year": 2025,
        "core_method": "強化學習激發 Reasoning 推理能力 (RL Reasoning CoT)",
        "bibtex": """@article{DeepSeek2025R1,
  author = {DeepSeek-AI},
  title = {DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning},
  journal = {arXiv preprint arXiv:2501.12900},
  year = {2025}
}""",
        "meta_data": {
            "reasoning_accuracy": 97.3,
            "rl_framework": "GRPO (Group Relative Policy Optimization)",
            "test_time_compute_scaling": "Incentivized by RL"
        },
        "abstract": "本研究開發了 DeepSeek-R1，透過大規模強化學習，在不依賴監督微調的前提下，自主激發模型生成極長思考鏈（CoT）進行複雜推理的能力。在個人 AI 賦能與自審治理中，引導此推理模型進行 Test-Time Compute 最佳化，能讓研究生與專業工作者在高難度學術推導中死守思考主權，防範大腦被空洞的 AI 黑話所掏空。",
        "urls": [
            {"type": "arxiv_pdf", "link": "https://arxiv.org/pdf/2501.12900.pdf"},
            {"type": "local_pdf", "link": "file:///Users/wuulong/Zotero/storage/DeepSeek_R1_2025.pdf"}
        ],
        "tags": ["DeepSeek-R1", "Test-Time-Compute", "Sovereign-AI"]
    },
    {
        "paper_id": "zotero_dont_do_rag",
        "cite_key": "CAG2024RAG",
        "topic_id": "top_enterprise_transformation",
        "title": "不用做 RAG！當快取增強生成 (CAG) 成為知識任務之所需",
        "authors": "Sophia Yang, Tech Research Team",
        "year": 2024,
        "core_method": "快取增強生成 (Cache-Augmented Generation, CAG) 架構",
        "bibtex": """@article{CAG2024RAG,
  author = {Yang, Sophia and Research, Tech},
  title = {Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks},
  journal = {Journal of Enterprise AI Architectures},
  year = {2024},
  volume = {3},
  pages = {45--58}
}""",
        "meta_data": {
            "latency_reduction_percentage": 40.0,
            "max_context_tokens": 1000000,
            "retrieval_robustness": 98.2
        },
        "abstract": "本論文探討在大模型長上下文（Context）與 KV Cache 爆發的時代，以快取增強生成 (CAG) 取代複雜 RAG 架構的可行性。CAG 將整個企業或個人的知識庫快取在 LLM 的 Context 中，大幅降低了傳統 RAG 中 chunking、embedding 與 vector search 所產生的誤差與延遲。這為企業 AI 轉型提供了極高可靠性、零檢索摩擦的全新知識治理路徑。",
        "urls": [
            {"type": "arxiv_pdf", "link": "https://arxiv.org/pdf/2412.18000.pdf"},
            {"type": "local_pdf", "link": "file:///Users/wuulong/Zotero/storage/Dont_Do_RAG_2024.pdf"}
        ],
        "tags": ["CAG-vs-RAG", "Enterprise-GenAI", "Sovereign-AI"]
    }
]

MOCK_EVIDENCES = [
    {
        "evidence_id": "evid_run_1",
        "paper_id": "zotero_multimodal_hydrology",
        "practice_scenario": {
            "study_basin": "Zengwen River Midstream",
            "multimodal_model": "GPT-4V",
            "elevation_reference": "DEM_20M",
            "dry_season": True
        },
        "evidence_payload": {
            "measured_flow_rate_cms": 1.2,
            "estimated_flow_rate_cms": 1.05,
            "sand_mistake_detected": True,
            "walkgis_track_corrected": True
        },
        "friction_percentage": 12.50
    },
    {
        "evidence_id": "evid_run_2",
        "paper_id": "zotero_dont_do_rag",
        "practice_scenario": {
            "enterprise_doc_count": 500,
            "total_token_size": 850000,
            "query_type": "complex_cross_referencing",
            "cag_kv_cache": True
        },
        "evidence_payload": {
            "cag_latency_ms": 350.0,
            "rag_latency_ms": 580.0,
            "cag_accuracy": 98.2,
            "rag_accuracy": 85.4
        },
        "friction_percentage": 14.98
    }
]

MOCK_RED_TEAM_LOGS = [
    {
        "log_id": "crit_haba_1",
        "paper_id": "zotero_multimodal_hydrology",
        "aspect_analyzed": "AI流域探索中的多模態幻覺防禦",
        "reviewer_attack": "哈教授指出：『利用 GPT-4V 進行流量特徵與流路辨識時，枯水期的泥沙淤積極易被誤判為水流通道。若缺乏現地尺規與 WalkGIS 航跡對合，數據偏離度將失控。你必須在 Topic 2 中設計影像特徵除錯與防禦退避！』",
        "student_defense": "哈爸進行品位裁決後防禦：『我們導入了枯水期影像對比濾鏡，並結合本地 WalkGIS 實地走讀的航跡點進行 DEM 高程校正。模擬比對顯示，加入高程校正後，流量估算偏差從 12.5% 大幅降至 3.2% 以內，成功克服此幻覺脆弱點，已通過自審！』",
        "verdict": "PASS"
    }
]

MOCK_MY_MANUSCRIPTS = [
    {
        "manuscript_id": "ms_conf_haba_2026",
        "topic_id": "top_river_gis_prep",
        "title": "基於書-DB-遊記三位一體之台灣山區河流流域 AI 探索 PoC 實踐",
        "cite_key": "Haba2026Conf",
        "manuscript_type": "Conference",
        "evolution_stage": "Published",
        "previous_manuscript_id": None,
        "meta_data": {
            "conference_name": "台灣開源地理空間資訊年會 (OSGeo Taiwan)",
            "overleaf_url": "https://www.overleaf.com/project/mock_haba_conf_2026"
        }
    },
    {
        "manuscript_id": "ms_journal_haba_2026",
        "topic_id": "top_multimodal_hydrology",
        "title": "多模態大語言模型在山區水文觀測中之現地真值對合與誤差補償技術",
        "cite_key": "Haba2026Journal",
        "manuscript_type": "Journal",
        "evolution_stage": "Writing",
        "previous_manuscript_id": "ms_conf_haba_2026",
        "meta_data": {
            "target_journal": "IEEE Transactions on Geoscience and Remote Sensing",
            "overleaf_url": "https://www.overleaf.com/project/mock_haba_journal_2026"
        }
    }
]

MOCK_MANUSCRIPT_CITATIONS = [
    {
        "manuscript_id": "ms_conf_haba_2026",
        "paper_id": "zotero_multimodal_hydrology",
        "citation_context": "作為 AI 山區河流流量辨識多模態比較之核心背景文獻。"
    },
    {
        "manuscript_id": "ms_journal_haba_2026",
        "paper_id": "zotero_dont_do_rag",
        "citation_context": "比對大模型對合水文數據時，評估是否應採用 CAG 快取以提升檢索健全性。"
    }
]

# ==============================================================================
# 資料表結構自動化初始化
# ==============================================================================

def init_db_schema_if_needed(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if len(tables) >= 5:
            conn.close()
            return # 已有 tables 結構
    except Exception:
        pass
        
    print(f"🌱 偵測到全新資料庫，正在套用 DDL 結構: {db_path}")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_dir, "schema.sql")
    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        conn.commit()
        print("✅ DDL 表格結構建立成功！")
    else:
        print(f"⚠️ 找不到 schema.sql 於 {schema_path}，跳過表格初始化。")
    conn.close()

# ==============================================================================
# 離線灌入哈爸三大專案資料集
# ==============================================================================

def clean_and_rebuild_mock(db_path):
    init_db_schema_if_needed(db_path)
    print(f"🧹 正在連線 SQLite，清理舊範例資料: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = OFF;")
    
    tables_to_clean = [
        "manuscript_citations", "my_manuscripts", "red_team_logs", 
        "empirical_evidences", "paper_tags", "paper_urls", "papers", 
        "topics", "projects", "directory_roots", "exploration_tasks"
    ]
    for table in tables_to_clean:
        try:
            cursor.execute(f"DELETE FROM {table};")
        except Exception as e:
            print(f"⚠️ 清理 {table} 時發生錯誤: {e}")
            
    print("✅ 資料清理完成。開始灌入【哈爸專屬三大真實專案與 Zotero 前沿文獻範例】...")
    
    try:
        # 1. 寫入 Ingestion Task
        task_id = "task_haba_sandbox_init_2026"
        cursor.execute("""
        INSERT INTO exploration_tasks (task_id, query, status, papers_found, agent_version, error_log, meta_data)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            task_id,
            "AI river exploration DeepSeek reasoning",
            "OFFLINE_FALLBACK",
            4,
            "Antigravity-v2.0-HabaBrain",
            None,
            json.dumps({"sandbox_rebuild": True, "haba_custom": True}, ensure_ascii=False)
        ))
        
        # 2. 寫入 directory_roots (如果 setup_research_db 沒載入則在此補載)
        roots_to_insert = [
            ("workspace_root", "STUDENT_LOCAL", "haba", "/Users/wuulong/github/bmad-pa/", {"description": "哈爸個人專案代碼庫根目錄"}),
            ("zotero_storage", "STUDENT_LOCAL", "haba", "/Users/wuulong/Zotero/storage/", {"description": "哈爸個人 Zotero 本地文獻 PDF 儲存目錄"}),
            ("lab_nas", "STUDENT_LOCAL", "haba", "/Volumes/VRES_NAS/archive/", {"description": "哈爸個人或實驗室 NAS 伺服器掛載路徑"}),
            ("remote_url", "GLOBAL_WEB", "internet", "", {"description": "網際網路線上遠端 HTTP 資源入口"})
        ]
        for r_key, o_type, o_name, abs_path, meta in roots_to_insert:
            cursor.execute("SELECT root_key FROM directory_roots WHERE root_key = ?;", (r_key,))
            if not cursor.fetchone():
                cursor.execute("""
                INSERT INTO directory_roots (root_key, owner_type, owner_name, absolute_path, meta_data)
                VALUES (?, ?, ?, ?, ?);
                """, (r_key, o_type, o_name, abs_path, json.dumps(meta, ensure_ascii=False)))

        # 3. 寫入哈爸專屬 projects
        for p in MOCK_PROJECTS:
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
            
        # 4. 寫入 Topics
        for t in MOCK_TOPICS:
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
            
        # 5. 寫入背景文獻 Papers & Tags & URLs
        for p in MOCK_PAPERS:
            cursor.execute("""
            INSERT INTO papers (paper_id, task_id, topic_id, title, authors, year, core_method, cite_key, bibtex, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                p["paper_id"],
                task_id,
                p["topic_id"],
                p["title"],
                p["authors"],
                p["year"],
                p["core_method"],
                p["cite_key"],
                p["bibtex"],
                json.dumps(p["meta_data"], ensure_ascii=False)
            ))
            
            # URLs
            for idx, url in enumerate(p["urls"]):
                link = url["link"]
                zotero_prefix = "file:///Users/wuulong/Zotero/storage/"
                if link.startswith(zotero_prefix):
                    root_key = "zotero_storage"
                    relative_link = link.replace(zotero_prefix, "")
                else:
                    root_key = "remote_url"
                    relative_link = link
                    
                cursor.execute("""
                INSERT INTO paper_urls (url_id, paper_id, root_key, url_link, url_type, download_status, file_size_bytes, meta_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    f"url_{p['paper_id']}_{idx + 1}",
                    p["paper_id"],
                    root_key,
                    relative_link,
                    url["type"],
                    "DOWNLOADED" if root_key == "zotero_storage" else "PENDING",
                    204800 if root_key == "zotero_storage" else 0,
                    json.dumps({"verified_in_zotero": True}, ensure_ascii=False)
                ))
                
            # Tags
            for tag in p["tags"]:
                cursor.execute("""
                INSERT INTO paper_tags (paper_id, tag_name, meta_data)
                VALUES (?, ?, ?);
                """, (
                    p["paper_id"],
                    tag,
                    json.dumps({"source": "Zotero_Import_Tagger"}, ensure_ascii=False)
                ))
                
        # 6. 寫入本地肉身實踐與實體舉證 Evidences
        for e in MOCK_EVIDENCES:
            cursor.execute("""
            INSERT INTO empirical_evidences (evidence_id, paper_id, practice_scenario, evidence_payload, friction_percentage, meta_data)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (
                e["evidence_id"],
                e["paper_id"],
                json.dumps(e["practice_scenario"], ensure_ascii=False),
                json.dumps(e["evidence_payload"], ensure_ascii=False),
                e["friction_percentage"],
                json.dumps({"sandbox_rebuild": True, "evaluator": "haba"}, ensure_ascii=False)
            ))
            
        # 7. 寫入自審對抗 Red Team Logs
        for r in MOCK_RED_TEAM_LOGS:
            cursor.execute("""
            INSERT INTO red_team_logs (log_id, paper_id, aspect_analyzed, reviewer_attack, student_defense, verdict, meta_data)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                r["log_id"],
                r["paper_id"],
                r["aspect_analyzed"],
                r["reviewer_attack"],
                r["student_defense"],
                r["verdict"],
                json.dumps({"evaluator_role": "哈教授"}, ensure_ascii=False)
            ))
            
        # 8. 寫入手稿 Manuscripts & Citations
        for m in MOCK_MY_MANUSCRIPTS:
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
                json.dumps(m["meta_data"], ensure_ascii=False)
            ))
            
        for c in MOCK_MANUSCRIPT_CITATIONS:
            cursor.execute("""
            INSERT INTO manuscript_citations (manuscript_id, paper_id, citation_context, meta_data)
            VALUES (?, ?, ?, ?);
            """, (
                c["manuscript_id"],
                c["paper_id"],
                c["citation_context"],
                json.dumps({"verified_in_tex": True}, ensure_ascii=False)
            ))
            
        conn.commit()
        print("🎉 恭喜！【哈爸專屬三大真實專案與 Zotero 前沿文獻範例】100% 繁體中文高階數據導入成功！")
        print("----------------------------------------------------------------------")
        print("📊 prj_tdhi          ➔ TDHI 台灣數位健康生態系實踐沙箱")
        print("📊 prj_river_exp     ➔ AI 流域學與河流探索專案")
        print("📊 prj_ai_enablement ➔ AI 應用與賦能研究專案")
        print("----------------------------------------------------------------------\n")
        
    except Exception as e:
        print(f"❌ 導入範例數據失敗: {e}")
        conn.rollback()
    finally:
        conn.close()

# ==============================================================================
# 線上 ArXiv REST API 檢索與 Ingestion 落地邏輯 (保留以應對工作流 A)
# ==============================================================================

def query_arxiv_online(query_str, limit=5):
    encoded_query = urllib.parse.quote(query_str)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results={limit}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns)
        
        papers_found = []
        for entry in entries:
            id_url = entry.find('atom:id', ns).text.strip()
            arxiv_id = id_url.split('/abs/')[-1].split('v')[0]
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            authors_nodes = entry.findall('atom:author', ns)
            authors_list = [node.find('atom:name', ns).text.strip() for node in authors_nodes]
            authors = ", ".join(authors_list)
            published_str = entry.find('atom:published', ns).text.strip()
            year = int(published_str[:4])
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            
            first_author = authors_list[0].split()[-1] if authors_list else "Unknown"
            first_author = "".join(c for c in first_author if c.isalnum())
            cite_key = f"{first_author}{year}{arxiv_id[:4]}"
            
            bibtex = f"""@article{{{cite_key},
  author = {{{authors}}},
  title = {{{title}}},
  journal = {{arXiv preprint arXiv:{arxiv_id}}},
  year = {{{year}}}
}}"""

            papers_found.append({
                "paper_id": f"arxiv_{arxiv_id}",
                "cite_key": cite_key,
                "title": title,
                "authors": authors,
                "year": year,
                "abstract": abstract,
                "pdf_url": pdf_url,
                "bibtex": bibtex,
                "tags": ["arxiv", "auto-scout"]
            })
        return papers_found
    except Exception:
        return None

def main():
    parser = argparse.ArgumentParser(description="哈爸專屬 Paper Scout 文獻探勘工具")
    parser.add_argument("--query", type=str, help="搜尋論文關鍵字")
    parser.add_argument("--limit", type=int, default=5, help="最大返回筆數")
    parser.add_argument("--save-db", action="store_true", help="將文獻沉澱落庫")
    parser.add_argument("--output", type=str, default="markdown", choices=["markdown", "json"], help="輸出格式")
    parser.add_argument("--force-mock", action="store_true", help="強制啟用本地模擬模式")
    parser.add_argument("--rebuild-mock", action="store_true", help="一鍵重建哈爸專屬三大專案高擬真數據")
    
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    if args.rebuild_mock:
        clean_and_rebuild_mock(db_path)
        return
        
    if not args.query:
        print("❌ 錯誤：請提供 --query 參數進行檢索，或使用 --rebuild-mock 重建範例數據。")
        return
        
    init_db_schema_if_needed(db_path)
    
    # 執行真實查詢或 Fallback 到 Mock
    all_papers = []
    real_papers = None
    if not args.force_mock:
        real_papers = query_arxiv_online(args.query, args.limit)
        
    if real_papers:
        print(f"🎉 成功從線上獲取 {len(real_papers)} 筆文獻！")
        for p in real_papers:
            all_papers.append({
                "paper_id": p["paper_id"],
                "cite_key": p["cite_key"],
                "title": p["title"],
                "authors": p["authors"],
                "year": p["year"],
                "pdf_url": p["pdf_url"],
                "tags": p["tags"]
            })
    else:
        print("⚠️ 啟用哈爸離線高擬真文獻庫進行對應...")
        for p in MOCK_PAPERS:
            all_papers.append({
                "paper_id": p["paper_id"],
                "cite_key": p["cite_key"],
                "title": p["title"],
                "authors": p["authors"],
                "year": p["year"],
                "pdf_url": p["urls"][0]["link"],
                "tags": p["tags"]
            })
            
    if args.output == "json":
        print(json.dumps(all_papers, indent=2, ensure_ascii=False))
    else:
        print(f"\n### 📚 Paper Scout 線上文獻檢索成果 (資料庫: {os.path.basename(db_path)})")
        print("| 來源 | 發表年份 | 標題 | 作者 | 關鍵連結 |")
        print("| :--- | :---: | :--- | :--- | :--- |")
        for p in all_papers:
            source = "ArXiv API" if real_papers else "Haba Sandbox"
            print(f"| {source} | {p['year']} | [{p['title']}]({p['pdf_url']}) | {p['authors']} | [下載PDF]({p['pdf_url']}) |")

if __name__ == "__main__":
    main()
