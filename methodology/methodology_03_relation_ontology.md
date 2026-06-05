# 🔗 學術文獻關聯本體規格書 (Sovereign Academic Relation Ontology Specification)

**定錨手稿編號**：`ms_sovereign_research_2026`  
**目的**：定義本地 SQLite 大腦資料庫中 `paper_relations` 表格的關係分類體系。透過這套本體（Ontology），研究者與 AI 協同器能將平面堆疊的文獻庫升格為立體、有向演化、具備批判張力的「學術演化有向無環圖 (DAG)」，作為撰寫高品質文獻綜述（Literature Review）與論點溯源的物理依據。

---

## 🌐 1. 五大分區與八種核心關係定義 (The 8 Relation Types)

在 `paper_relations` 資料表中，每一筆關係由 `source_paper_id` (起點/新文獻) 指向 `target_paper_id` (終點/被引用之舊文獻)，其關係類型 `relation_type` 強制約束為以下八種之一：

### 🔴 第一分區：繼承與技術演進類 (Inheritance & Evolution)
*本分區代表知識的累積、技術樹的向下紮根與向上伸展。*

1.  **`GROUNDED_ON` (基於 / 理論地墊)**
    *   **定義**：$A$ 論文的核心方法、關鍵理論或數學公式，是直接建立在 $B$ 論文開創的核心模型或基礎設施之上的。
    *   **資料契約範例**：LLaVA [@zotero_Liu_2023_471] `GROUNDED_ON` CLIP (視覺) 與 Vicuna (語言)。
2.  **`IMPROVES` (改進 / 技術擴展)**
    *   **定義**：$A$ 論文保留了 $B$ 論文的核心框架，但針對 $B$ 的特定缺陷（如運算延遲、極限精準度不足、長尾邊界失效）進行了改良或局部技術擴充。
    *   **資料契約範例**：DPO (Direct Preference Optimization) `IMPROVES` RLHF。
3.  **`SIMPLIFIES` (簡化 / 降維極簡)**
    *   **定義**：$A$ 指出 $B$ 的系統架構過於昂貴、複雜或冗贅，並提出一套極致簡化的替代技術，且效能或精度幾乎無損。
    *   **資料契約範例**：CAG (快取增強生成) [@zotero_Chan_2024_671] `SIMPLIFIES` RAG。

---

### 🔵 第二分區：批判與對抗邊界類 (Critique & Boundary)
*本分區代表學術上的反駁、限縮與認識警覺性的喚醒。*

4.  **`REFUTES` (反駁 / 理論挑戰)**
    *   **定義**：$A$ 論文通過嚴密的實證觀測、代數推導或反例，證實 $B$ 論文的核心結論在特定條件下是錯誤的、存在致命漏洞，或其物理假設完全不成立。
    *   **資料契約範例**：*Lost in the Middle* (2023) `REFUTES` 長文本大模型具備完美無摩擦檢索的宣稱。
5.  **`LIMITS` (限縮 / 定義臨界失效)**
    *   **定義**：$A$ 並非完全否定 $B$，而是界定了 $B$ 的方法或理論在真實物理世界中的「適用邊界與臨界失效點 (Breakdown Point)」。
    *   **資料契約範例**：我們的主權協作研究手稿 `LIMITS` RAGAS 評估 [@zotero_Es_2023_4]（指出 RAGAS 完全依賴大模型裁判在缺乏實體現地真值約束時會發生成幻覺自指失效）。

---

### 🟢 第三分區：平行競爭與替代類 (Competition & Alternatives)
*本分區代表同一技術戰壕中，平行學術路線的對立。*

6.  **`COMPETES` (競爭 / 平行替代方案)**
    *   **定義**：$A$ 與 $B$ 針對同一個核心痛點，提出了完全不同、平行且互不隸屬的技術解決路徑。
    *   **資料契約範例**：Transformer `COMPETES` Mamba (狀態空間模型)；RAG `COMPETES` 參數微調 (Fine-tuning)。

---

### 🟡 第四分區：跨界融合與雜交類 (Synthesis & Hybridization)
*本分區代表高維度的範式創新，將兩個平行宇宙進行合流。*

7.  **`SYNTHESIZES` (融合 / 跨界雜交)**
    *   **定義**：$A$ 論文將原本平行獨立、甚至互不相干的 $B$ 論文與 $C$ 論文進行跨界雜交合流，孕育出全新研究物種。
    *   **資料契約範例**：我們的主權協作研究方法論 `SYNTHESIZES` SQLite 關係代數（代數與關係約束）與 大語言模型推理（高維語意空間）。

---

### 🟣 第五分區：實證與垂直落地類 (Empirical & Realization)
*本分區代表理論向實踐現場的下沉，與物理真值的強制對位。*

8.  **`APPLIES` (應用 / 垂直落地)**
    *   **定義**：$A$ 論文是 $B$ 論文（通常是通用理論、大一統框架或基礎模型）在特定垂直領域、現地實務中的具體應用與實證。
    *   **資料契約範例**：BioBERT `APPLIES` BERT 於生醫文獻；我們在曾文溪流域的水文數值模擬 `APPLIES` 了 Saint-Venant 降雨逕流偏微分方程。

---

## 💾 2. SQLite DTO 關聯註冊格式規範 (JSON DTO Schema)

當關係被寫入 `paper_relations.meta_data` 時，應採用標準的 JSON 封套，以支援品質審計與體檢：

```json
{
  "compliance_status": {
    "is_compliant": true,
    "checked_at": "2026-05-27T00:15:00Z",
    "missing_fields": [],
    "validation_message": "Relation compliant and verified"
  },
  "provenance_details": {
    "assertion_chapter": "第 2.1 節",
    "cognitive_sovereignty_level": "RED_TEAM_VERIFIED",
    "empirical_evidence_linked": "ev_taxonomy_tree_2026"
  }
}
```
