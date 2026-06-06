# 🧱 methodology_71: MCI 手稿成熟與可信度指標 (MCI Manuscript Maturity Metric Specification)

本規格書詳細定義了手稿成熟與可信度指數 (Manuscript Credibility Index, MCI) 的剛性加權演算法，用以評估研究成果在寫作與理論地基上的完備性。

---

## 🏛️ 1. MCI 看板與發表門檻

手稿成熟與可信度指數 (MCI) 結合了「手稿寫作進度」與「大腦文獻 Grounding 狀態」，是導師監督學生、判定手稿是否可以發表發行的物理依據。

> [!IMPORTANT]
> **發表合規電閘**  
> 手稿的 MCI 目標值必須達到 **`90.00% (🟢 Elite)`**，系統才認可論文具備足夠的成熟度與防禦深度，准予合龍輸出與投稿發表。

---

## 📐 2. MCI 剛性加權計分公式

MCI 指標的總分由「手稿文件成熟度」與「大腦 Grounding 綜合度」各佔 50% 權重構成：

$$\text{MCI} = (\text{聯邦文件成熟度分} \times 0.50) + (\text{大腦 Grounding 綜合分} \times 0.50)$$

---

## 🔍 3. 指標子項細部計算法

### 3.1 聯邦文件成熟度分 (Federated Files Maturity, 50% 權重)
大腦審計工具實體掃描 `manuscripts/` 下的 8 大聯邦手稿檔案（ToC, APM, Reading Protocol 等），計算：
- **字數完備度**：檢查各章節是否達到預設之字數門檻，排除空殼檔案。
- **TODO 懸置點扣分**：檢查檔案中是否殘留 `TODO`、`FIXME` 或 `[待補]` 等標記，每發現一處進行剛性扣分。

### 3.2 大腦 Grounding 綜合分 (Database Grounding, 50% 權重)
大腦 Grounding 綜合分由以下五個剛性子項加權構成：

1.  **Cite 註冊存在率 (Citation Existence Rate, 20% 子權重)**：
    驗證手稿中標註的 `@cite_key` 是否 100% 存在於 SQLite 資料庫的 `papers` 表中，揪出「幽靈引文」（有引無文）。
2.  **Stage 2 消化率 (Stage 2 Ingestion Rate, 30% 子權重 - [最高權重])**：
    計算手稿引用的文獻中，已完成 Stage 2 深度解構（狀態為 `STAGE_2_DEEP`）的文獻比例。此項剛性阻斷了「未讀先引」的學術投機。
3.  **遞迴閱讀就位率 (Recursive Reading Readiness, 20% 子權重)**：
    $$\text{遞迴就位率} = \text{原始已開發率} \times \text{已消化覆蓋率因子}$$
    當引用文獻時，系統會以 BFS 有向拓撲向後探查兩層。若被依賴的經典文獻未消化或不存在，則引入「已消化覆蓋率」作為乘積懲罰因子，剛性下修就位率，防止理論地基浮空。
4.  **紅軍對抗綜合得分 (Red Team Defense Score, 20% 子權重)**：
    $$\text{紅軍得分} = (\text{自審文獻覆蓋率} \times 0.6) + (\text{自審 PASS 率} \times 0.4)$$
    為防範學生只自審一篇無關緊要的文獻即宣稱 100% 通過，本公式給予「自審覆蓋率」高達 60% 的控制權重。覆蓋文獻量不足時，紅軍得分將被強力制約。
5.  **Claims Grounding 完整率 (Claims Grounding Rate, 10% 子權重)**：
    檢查手稿中 100% 的學術主張 (Claims)，是否皆在 `manuscript_citations` 中有對應的聯結，且背後支援的文獻是 `STAGE_2_DEEP` 或是 `empirical_evidences` 中實測誤差符合門檻的實踐真值。
