# 📐 規範支柱：主權科研範式與大腦方法論規格大憲章 (Methodology Manual)

> [!IMPORTANT]
> **主權科研大腦的「憲法規格手冊」**  
> 本手冊物理固化了主權大腦方法論（Methodology）的範式定義、關係本體與十一表數據治理的最高核心規則。  
> 任何關於研究規則、資料庫 Schema 或文獻演化BFS拓撲的修改與改良，皆物理固化於此，作為指導具體手稿寫作與自證的「最高規格大憲章」。

---

## 🏛️ 1. methodology/ 規格大憲章架構

方法論本體目錄下存放了方法論的核心規格檔案，研究生與 AI 助理在進行任何具體論文寫作或實踐前，必須以此作為最高指導規範：

1.  **`methodology_01_requirements.md`** ➔ **主權研究系統規格需求書**
2.  **`methodology_02_metadata_schema_spec.md`** ➔ **元數據結構規格書**
3.  **`methodology_03_relation_ontology.md`** ➔ **關係演化拓撲本體規格書**
4.  **`methodology_04_system_architecture_navigator.md`** ➔ **主權大腦系統架構與運作手冊**
5.  **`build_log/`** ➔ **方法論演化歷史日誌**（從 `01` 開始編起，如 `01_methodology_manuscript_separation_plan.md` 為物理分離決策）。

---

## 🧠 2. 核心規範的 WHY 深度本體解析 (為什麼要這樣設計？)

### ❓ 1. 為什麼要在野性實踐前，剛性建立《系統規格需求書》(Requirements)？
*   **學術痛點**：絕大多數人機協作研究之所以淪為 AI 代理人「自動製造」的黑話廢紙，根源在於「隨意性（Ad-hoc）」。沒有邊界的 Prompt 心流碰撞只會帶來無限增值的語意泡沫，人機協作很快就會陷入認知掏空的沼澤。
*   **WHY 的本體價值**：`methodology_01_requirements.md` 是我們劃定專案工程邊界的「大憲章」。它剛性規定了主權科研系統的需求、功能與分類規格，物理界定了人、AI 代理人、本機工具鏈三者間的防禦縱深。唯有在動手前物理綁定系統需求，才能確保後續的研究有章可循、步步有證，強行校正散裝研究的認識漂移。

### ❓ 2. 為什麼大腦必須採用 SQLite 十一表 Schema 與 papers.meta_data JSON 信封進行數據治理？
*   **學術痛點**：純文本的 Markdown 筆記（如 Obsidian 雙向連結）雖然直覺，但本質上是「軟語意」的。它缺乏強約束的實體完整性（Entity Integrity）與外鍵約束（Foreign Key Constraints），極易產生空洞 claiming 或外鍵斷線。這種結構在面對大批量複雜論文寫作時，無法發動剛性的自動化審計與盲檢。
*   **WHY 的本體價值**：`methodology_02_metadata_schema_spec.md` 為大腦十一表定義了鋼鐵般的 Schema 規範，特別是將 papers.meta_data JSON 欄位信封化。這意味著：
    *   每一篇文獻的學術 prestige（被引用數、載體分值、重力 $G_a$）與 digestion 狀態（STAGE_1_PRELIMINARY 或 STAGE_2_DEEP），在大腦中都有「唯一實體地址」。
    *   papers、empirical_evidences、my_manuscripts 與 red_team_logs 四大核心表通過外鍵強烈對合。
    *   這排除了 RAG 的幻覺空間，讓手稿的每一處主張都能以 `PRAGMA foreign_key_check` 的物理數據進行 Grounding 校正，拒絕任何嘴砲與空殼學術！

### ❓ 3. 為什麼文獻演化需要定義 BFS 2層有向拓撲本體 (`GROUNDED_ON`)？
*   **學術痛點**：傳統的論文引用清單是平面、無結構的。這種「為引而引」的平面引用，掩蓋了文獻與文獻間實質的「演化繼承關係」。寫作者往往只看最新文獻的結論，卻對其底層奠基的經典理論一無所知，導致理論根基浮空，淪為學術泡沫的傳播者。
*   **WHY 的本體價值**：`methodology_03_relation_ontology.md` 剛性定義了文獻演化有向關係本體（特別是 `GROUNDED_ON` 有向邊）。這將平面引用升格為有向演化網絡。
    *   透過 **BFS 2-Level（二層廣度優先搜尋探針）** 算法，大腦能從「已消化」的 A 類核心文獻出發，精確追蹤 A ➔ B ➔ C 的有向演化地基（B 與 C 作為底層基底是否存在於資料庫中）。
    *   這提供了剛性盲檢「理論根系是否斷裂」的拓撲依據，強迫研究生與 AI 代理人老老實實地回溯經典原始文獻，完成「穿透式精讀」，拒絕快餐式、孤島式的學術速成。

---
*主權方法論規格大憲章・Methodology Manual 物理固化*
