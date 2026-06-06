# 🧱 methodology_61: 去中心化大腦與純文字 DTO 還原機制 (Decentralized Brain DTO & Rebuild Specification)

本規格書詳細定義了主權大腦如何解決 SQLite 二進位檔案之 Git 衝突問題，並詳述去中心化純文字 DTO 還原與冷啟動重建流程。

---

## 🏛️ 1. SQLite 二進位 Git 衝突痛點

在多人或多代理人協作的科研環境中，SQLite 二進位檔案（`Research_Artifacts.db`）無法在 Git 上進行傳統的行層級（Line-by-Line）對比與 Merge。

如果直接將 `.db` 提交至 Git：
- 兩位協作者同時修改了不同的文獻或關係，提交時會發生不可調和的 Git 二進位衝突。
- 強制覆寫會導致其中一方的研究成果（如剛寫好的品位裁決或引文）被完全抹除。

為此，主權大腦採取**「二進位與文字流解耦」**的去中心化設計。

---

## 💾 2. 純文字 DTO 還原封套

大腦資料庫不直接參與 Git 版本控制，而是透過純文字 JSON 格式的 **DTO (Data Transfer Object)** 作為資料的中介傳承載體：

- **核心檔案**：[contrib_top_sovereign_methodology.json](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/data/contributions/contrib_top_sovereign_methodology.json)
- **職責**：將十一表中的所有 papers、topics、relations、evidences 等資料，以結構化的純文字 JSON 列出。當有多人修改時，Git 可以在 JSON 檔案上完美進行 conflict 標記與 merge。

---

## 🔄 3. 一鍵 Rebuild 冷啟動重建心流

實驗室共用大腦的維護與還原採用以下雙向閉環心流：

```
      【 本地 SQLite 大腦 】 ── 灌溉/定錨 ──➔ 【 導出為純文字 DTO JSON 】
             ▲                                         │
             │ ( rebuild_lab_brain.py )           ( Git Commit & Push )
             │                                         ▼
      【 重建本地無衝突 DB 】 ◄── Git Pull ─── 【 遠端 Git 聯邦共有庫 】
```

### 3.1 步驟一：本地大腦更新與灌溉
協作者在本地執行 `!paper_digest` 或 `!paper_map`，更新本地 SQLite 資料庫的文獻狀態、引文或實踐證據。

### 3.2 步驟二：導出純文字 DTO (Export)
協作者在提交 Git 前，執行：
```bash
python3 scripts/export_contributions.py --topic top_sovereign_methodology
```
這會將本地資料庫中經過更新的 91 筆核心文獻、關係與實踐數據，匯出覆寫回 `contrib_top_sovereign_methodology.json` 檔案。

### 3.3 步驟三：Git 提交與合流 (Push & Merge)
協作者在 Git 上提交並推送 `contrib_top_sovereign_methodology.json`。若發生衝突，在該 JSON 檔上進行行對比 merge，解決後推送。

### 3.4 步驟四：一鍵還原重建 (Rebuild)
其他協作者拉取最新程式碼後，在本地執行一鍵重建腳本：
```bash
python3 rebuild_lab_brain.py
```
該腳本會清空本地的 `Research_Artifacts.db`，重新建立十一張表，並將最新的無衝突 `contrib_top_sovereign_methodology.json` 完美灌入，實現實驗室共有大腦 100% 的物理還原。
