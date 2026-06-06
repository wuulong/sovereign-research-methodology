# 🧱 methodology_72: MPM 元自證成熟度指標 (MPM PoC Proof Metric Specification)

本規格書詳細定義了元自證成熟度指數 (Methodology Proof Maturity, MPM) 的剛性加權演算法，用以評估學術研究與工具鏈在「物理可重現性」與「大腦自指自證度」上的完備程度。

---

## 🏛️ 1. MPM 看板與自指自洽

元自證成熟度指數 (MPM) 用於評估方法論本身作為新型科研典範的實體可用性與自指完整鏈結度。它向評審與讀者自證：本篇研究的結論並非憑空撰寫，而是由這套系統、這個 SQLite 資料庫「物理長出來的」。

> [!IMPORTANT]
> **元自證發表門檻**  
> 手稿的 MPM 總分目標值必須達到 **`90.00% (🟢 Elite)`**，系統才認可該研究已達成「行解合一、完全自指自洽」，解除發表阻斷。

---

## 📐 2. MPM 剛性加權計分公式

MPM 指標由三個剛性維度加權構成，各自代表了資料庫硬度、工具可用性與自指自合度：

$$\text{MPM} = (\text{SQLite 有效性} \times 0.40) + (\text{工具鏈無摩擦率} \times 0.30) + (\text{手稿自指自證度} \times 0.30)$$

---

## 🔍 3. 指標子項細部計算法

### 3.1 SQLite 有效性 (SQLite Integrity, 40% 權重)
大腦審計工具執行資料庫硬體完整性檢核：
- 執行 `PRAGMA foreign_key_check` 與 `PRAGMA integrity_check`，驗證十一張表完美對合，無任何外鍵斷線、資料損毀或孤立節點。
- 檢測 Topics 與實踐證據的三位一體合龍率。

### 3.2 工具鏈無摩擦率 (Toolchain Friction Rate, 30% 權重)
實體掃描並逐個測試本機的核心 Python 支援腳本（如 `brain_cli.py`、`hydrate_paper_assets.py` 等 8 大核心腳本）：
- 驗證這些腳本在當前系統環境下是否存在、是否可被編譯執行（無 SyntaxError 且能輸出 Version/Help）。
- 物理確保這套大腦工具鏈在其他成員的電腦上也能「一鍵跑通、無摩擦重現」，拒絕學術概念泡沫。

### 3.3 手稿自指自證度 (Manuscript Self-Referential Degree, 30% 權重)
盲檢手稿主體（如 `sovereign_research_05_manuscript.md`）的最後章節：
- 驗證手稿中是否確實嵌入了本地 SQLite 資料庫匯出之純文字 DTO JSON 的**「實體資料指紋 (Checksum/Fingerprint)」**。
- 這向評審物理證明：「本篇論文所用的資料跟架構，與此 SQLite 資料庫 100% 物理對齊，不含人工捏造的雜訊」。
