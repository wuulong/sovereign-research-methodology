# 🧱 methodology_31: 理論地墊與 BFS 有向演化拓撲演算法 (Theory Grounding & BFS Topology Specification)

本規格書定義了主權大腦如何藉由圖形關係代數，檢測文獻引用的「理論地墊完備度」，並詳述 BFS (廣度優先檢索) 二層拓撲演算法之判定規則。

---

## 🏛️ 1. 理論地墊與根系懸空 (Theory Grounding Concept)

傳統學術引用往往流於平面式地堆疊（例如：*「A說了X，B說了Y」*），卻忽略了知識本身的演化血統與傳承根系。AI 常在此虛假引用中編織幻覺，導致整個研究大底空洞無光。

主權大腦藉由 `paper_relations` 表中的有向關係邊（如 `relation_type = 'GROUNDED_ON'`），將平面引用轉化為一個**「有向無環圖 (DAG) 的演化網路」**。系統藉此強制驗證：我們引用的每一篇當代文獻，其底層支撐的經典理論地墊是否同樣存在於資料庫中，且是否確實經過人類研究者的洗滌精讀。

---

## 🧬 2. 有向 BFS 2-Level 拓撲演算法

為了物理量化文獻的根系健全度，大腦審計工具運行「遞迴有向 BFS 演算法」，對手稿引用的文獻進行向後兩層的根系探查：

```
手稿 (Manuscript) ──引用──➔ 文獻 A (Layer 2)
                            │
                       (GROUNDED_ON)
                            ▼
                        文獻 B (理論地墊第一層)
                            │
                       (GROUNDED_ON)
                            ▼
                        文獻 C (理論地墊第二層)
```

### 2.1 演算法運作規則
1.  **收集引文集**：掃描手稿中所有註冊的 `@cite_key`，並取得其在資料庫 `papers` 表中的 `paper_id`。
2.  **BFS 拓撲向後延伸**：
    *   **Level 1 探查**：對每一篇引文 $A$，在 `paper_relations` 中檢索所有滿足 `source_paper_id = A` 且 `relation_type = 'GROUNDED_ON'` 的關係邊，找到被依賴的經典文獻 $B$。
    *   **Level 2 探查**：再以 $B$ 作為起點，重複檢索其依賴的經典奠基文獻 $C$。
3.  **根系浮空判定與懲罰**：
    *   如果探查到的經典文獻 $B$ 或 $C$ 在大腦資料庫中**「不存在」**，或其在 `papers` 表中的狀態**「非 `STAGE_2_DEEP`」**（即未完成 Stage 2 降維解構與品位裁決）。
    *   則系統判定該處發生**「理論根系斷裂 / 根系浮空」**，並剛性扣減手稿的「遞迴閱讀就位率」，進而大幅拉低手稿成熟度 MCI 總分，阻斷論文發表。

---

## 💻 3. 遞迴 SQL 檢索實作範例 (Recursive CTE)

大腦底層透過 SQLite 的遞迴通用資料表運算式 (Recursive CTE) 實現秒級的拓撲根系完整度追溯：

```sql
WITH RECURSIVE PaperAncestors(source_id, target_id, depth) AS (
  -- 起點：手稿直接引用的文獻 A
  SELECT source_paper_id, target_paper_id, 1
  FROM paper_relations
  WHERE source_paper_id = 'Liu_2023_LLaVA' AND relation_type = 'GROUNDED_ON'
  
  UNION ALL
  
  -- 遞迴步驟：向後追溯被依賴的文獻
  SELECT pr.source_paper_id, pr.target_paper_id, pa.depth + 1
  FROM paper_relations pr
  JOIN PaperAncestors pa ON pr.source_paper_id = pa.target_id
  WHERE pr.relation_type = 'GROUNDED_ON' AND pa.depth < 2
)
SELECT pa.source_id, pa.target_id, p.status, pa.depth
FROM PaperAncestors pa
LEFT JOIN papers p ON pa.target_id = p.paper_id;
```
