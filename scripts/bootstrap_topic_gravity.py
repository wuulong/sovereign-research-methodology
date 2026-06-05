#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈爸主權研究大腦 - 主題敏感型學術重力冷啟動工具 (bootstrap_topic_gravity.py)

目的：
1. 實踐「方法一：LLM 冷啟動（LLM-Driven Warm Start）」，在啟動特定研究主題時，
   由專家 AI 預載期刊（VENUE）與機構（INSTITUTION）的重力偏置評分。
2. 避免全域硬性評分的弊端，針對不同研究主題，實施動態加權，精準篩選前沿文獻，排除八股與雜訊。
"""

import os
import sys
import sqlite3
import argparse

# 專家定義的主題敏感型重力偏置對照表 (Expert Seed Biases)
# 支持台灣觀點與繁體中文，避免中國用語。
EXPERT_BIAS_REGISTRY = {
    "top_sovereign_methodology": {
        "name": "主權研究方法論之學術對位與防掏空機制",
        "biases": [
            # 期刊/會議 (VENUE)
            ("arxiv", "VENUE", 1.5, "主權寫作講求時效性與前沿探索，給予預印本適度的主題加分。"),
            ("acm computing surveys", "VENUE", 2.0, "系統性文獻綜述對方法論建構與定義有決定性價值。"),
            ("transactions on software engineering", "VENUE", 1.5, "探討軟體工程與多人 Git/JSON 協作工程的硬核期刊。"),
            ("nature", "VENUE", -2.0, "跨學科頂刊偏向科普政策或宏觀空洞論述，在此工程方法論主題上指導意義低，排除雜訊。"),
            ("science", "VENUE", -2.0, "同 Nature，避免大腦被缺乏實務工程細節的科普空話掏空。"),
            # 研究機構 (INSTITUTION)
            ("OpenAI", "INSTITUTION", 2.0, "大型語言模型技術與前沿架構的核心推動者，其研究具強烈代表性。"),
            ("Google DeepMind", "INSTITUTION", 2.0, "Agentic AI 與強化學習的科學堡壘，其論點極具學術硬度。"),
            ("MIT", "INSTITUTION", 1.0, "CSAIL 實驗室在個人認知與軟體系統工程上的開拓性研究。")
        ]
    },
    "top_river_gis_prep": {
        "name": "河流流域 GIS 數據準備與 QGIS 樣式注入",
        "biases": [
            # 期刊/會議 (VENUE)
            ("Journal of Hydrology", "VENUE", 3.0, "全球水文與河流模擬的最高殿堂，在物理降雨逕流模擬上有絕對权威。"),
            ("International Journal of Geographical Information Science", "VENUE", 2.5, "地理資訊科學的黃金期刊，高度契合空間脈絡對合。"),
            ("Water Resources Research", "VENUE", 2.0, "水資源與河川模擬之核心優良刊物。"),
            ("NeurIPS", "VENUE", -2.5, "AI 頂會極度缺乏現地物理與台灣水文地理約束的工程細節，適度扣分以防空話。"),
            ("CVPR", "VENUE", -2.5, "同 NeurIPS，防止無實體邊界約束的生成式視覺八股。"),
            # 研究機構 (INSTITUTION)
            ("中央研究院", "INSTITUTION", 3.0, "台灣百年歷史地圖與本土 GIS 圖資的無可爭議之權威與始祖。"),
            ("台灣大學", "INSTITUTION", 1.5, "其地理系與水文組在台灣本土河川水文研究上有著最扎實的現地實測資料。")
        ]
    },
    "top_multimodal_hydrology": {
        "name": "多模態 AI 山區水文觀測與現地真值比對",
        "biases": [
            # 期刊/會議 (VENUE)
            ("Journal of Hydrology", "VENUE", 3.0, "水文物理與現地觀測的權威期刊，對現地真值比對至關重要。"),
            ("Remote Sensing of Environment", "VENUE", 2.5, "遙測與環境感測的頂級期刊，支援多模態遙測資料之對合。"),
            ("NeurIPS", "VENUE", -2.0, "純 AI 頂會缺乏現地物理量測邊界約束，需適度降權以重塑物理邊界。"),
            # 研究機構 (INSTITUTION)
            ("中央研究院", "INSTITUTION", 3.0, "台灣 GIS 與遙測空間運算之本土權威。"),
            ("台灣大學", "INSTITUTION", 1.5, "提供台灣山區現地量測與逕流觀測的最強學術基地。")
        ]
    }
}

def main():
    parser = argparse.ArgumentParser(description="哈爸主權研究大腦 - 主題敏感型學術重力冷啟動工具")
    parser.add_argument("--topic", type=str, default="top_sovereign_methodology", 
                        choices=list(EXPERT_BIAS_REGISTRY.keys()),
                        help="指定要冷啟動的 Topic ID")
    parser.add_argument("--all-topics", action="store_true", help="一次為所有支援的主題注入偏置")
    
    args = parser.parse_args()
    
    # 決定資料庫路徑
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "Research_Artifacts.db")
    
    if not os.path.exists(db_path):
        print(f"[!] 大腦資料庫不存在: {db_path}，請先執行 setup_research_db.py")
        sys.exit(1)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    topics_to_bootstrap = []
    if args.all_topics:
        topics_to_bootstrap = list(EXPERT_BIAS_REGISTRY.keys())
    else:
        topics_to_bootstrap = [args.topic]
        
    print(f"🚀 開始執行學術重力之【方法一：LLM 冷啟動（LLM-Driven Warm Start）】")
    print(f"[*] 連線大腦資料庫: {db_path}\n")
    
    for t_id in topics_to_bootstrap:
        config = EXPERT_BIAS_REGISTRY[t_id]
        print(f"📌 主題 ID: {t_id} ({config['name']})")
        print(f"  正在注入 {len(config['biases'])} 筆專家品位偏置資料...")
        
        # 確保 topics 資料表中有這個 topic_id
        cursor.execute("SELECT topic_id FROM topics WHERE topic_id = ?;", (t_id,))
        if not cursor.fetchone():
            print(f"  [!] 警告: 資料庫中的 topics 表尚無 '{t_id}'，請先初始化專案主題！跳過此主題。")
            continue
            
        success_count = 0
        for entity_name, entity_type, bias_score, desc in config['biases']:
            try:
                cursor.execute("""
                INSERT OR REPLACE INTO topic_gravity_overrides (
                    topic_id, entity_name, entity_type, bias_score, description
                ) VALUES (?, ?, ?, ?, ?);
                """, (t_id, entity_name.lower(), entity_type, bias_score, desc))
                success_count += 1
            except Exception as e:
                print(f"    [!] 寫入 {entity_name} 失敗: {e}")
                
        print(f"  ➔ 🎉 成功注入 {success_count} / {len(config['biases'])} 筆偏置資料！")
        
    try:
        conn.commit()
        print("\n🎉 所有的主題敏感型學術重力偏置皆已安全物理落庫！")
    except Exception as e:
        conn.rollback()
        print(f"\n[!] 提交交易失敗: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
