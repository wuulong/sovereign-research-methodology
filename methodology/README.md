# 📐 主權科研方法論規格說明書清單 (Methodology Directory)

本目錄存放了主權科研大腦（Sovereign Research Brain）的系統需求規格書、元資料 schema 設計規範以及關係本體定義檔。

---

## 🧬 為什麼我們需要這些規格書？(The System Why)

在傳統的研究方法中，研究的流程往往是隨意的、機率性的。在使用生成式 AI 協作時，研究者如果不提供剛性的「物理框架約束」，LLM 就會像脫韁野馬一樣胡亂生成，導致程式碼或手稿在編譯時爆發嚴重的 domain-knowledge 耦合衝突。

本目錄下的規格說明書（01-04）構成了主權科研大腦的**「憲法與骨架」**。它們剛性定義了十一表 SQLite 資料庫的欄位約束與外鍵關係本體，強制讓 AI 在我們劃定的「主權格子」內進行高精細度的填充，保證人機共建的可靠與自洽。

---

## 📂 2 大方法論規格檔矩陣 (The Specification Matrix)

### 1. [01] 系統需求與目標：`methodology_01_requirements.md`
*   **Why it exists**: 明確宣示主權大腦的設計目標，界定「思維主權邊界」與「防範認知空洞化」的頂層需求。

### 2. [02] 系統架構、中繼資料 Schema 與本體規格手冊：`methodology_02_system_architecture_navigator.md`
*   **Why it exists**: 這是主權科研大腦的運行憲章，系統性整合了：
    1. **四星協同運作模型**：四大主權 Skill（Navigator, Auditor, Builder, Verifier）的運作工序與規則。
    2. **十一表中繼資料 Schema 規格**：剛性定義 `meta_data` 的 JSON 規格，是自主品質治理的底層鐵幕。
    3. **文獻關聯本體規格**：定義 `paper_relations` 的八大關係，是 BFS 算分與判定理論根系浮空的代數基礎。
    4. **實戰心流與物理摩擦**：記錄手稿誕生實戰生命週期與物理偏離度計量。

---

## 🪐 線上 GitHub 連結
本方法論的所有系統需求與 DDL 設計均已開源。您可以直接在 GitHub 上點閱 [Sovereign Research Methodology Specifications](https://github.com/wuulong/sovereign-research-methodology/tree/main/methodology)，繼承這套代表學術主權的最硬核系統美學設計。
