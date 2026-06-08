# 🌊 scripts/brain_cli_manual: 主權大腦實體探勘命令列工具使用手冊 (Brain CLI Manual)

## 📌 1. 工具定位與核心哲學

主權大腦實體探勘命令列工具 ([brain_cli.py](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/scripts/brain_cli.py)) 是為研究者（君王）量身打造的本地 SQLite 資料庫查驗工具。

其核心哲學在於：**100% 零 Token 消耗、毫秒級響應、剛性 DTO 結構檢驗與實體物理防線對合**。藉由將抽象的大腦十一表（實為十四表）資訊以極具質感的純文字 ASCII 表格、樹狀圖以及明細帳本呈現，消除人機協作過程中的記憶磨損與語意漂移。

---

## 🚀 2. 聯邦重構與合流冷啟動

在初次複製 Git 倉庫或想要重置本地資料庫時， papers 資料庫可能僅是空的骨架。請在 `sovereign-research-methodology` 目錄下執行以下指令進行一鍵重構：

```bash
python3 rebuild_lab_brain.py
```
此步驟會自動呼叫 `setup_research_db.py` 重建 DDL，並自動掃描 `contributions/` 下的所有純文字 JSON 貢獻包（如 `contrib_top_sovereign_methodology.json`），將學術文獻、十大學術因子與關係鏈安全寫入合流。

---

## 📖 3. 命令列參數與用法全集 (CLI Reference)

```bash
python3 brain_cli.py [-d DB_PATH] [功能參數] [--json]
```

### ⚙️ 基礎配置參數
*   **`-d`, `--db [DB_PATH]`**：指定 SQLite 資料庫檔案路徑。
    *(預設已設定為實體路徑 `/Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/data/Research_Artifacts.db`，一般免填)*
*   **`--json`**：切換為結構化 JSON 輸出格式，方便與其他 Agent 系統或程式對接。

---

### 🔍 核心查詢指令

| 參數選項 | 功能名稱 | 說明與適用情境 |
| :--- | :--- | :--- |
| **`-l`, `--list`** | **十一表全景看板** | 列出資料庫中所有 Tables、當前 Row 統計與欄位摘要。適用於快速掌握資料庫全貌。 |
| **`-t`, `--topic [ID]`** | **專案與循序主題看板** | 列出所有研究專案及其下的子主題、邏輯演進順序 (`sequence_order`) 與聚焦變數。可帶入專案 ID 進行過濾。 |
| **`-p`, `--paper [cite_key]`** | **文獻合規明細檢索** | 精準查詢特定背景論文的 Ingestion Stage 與 Stage 2 合規明細（含品位評判 verdict）。 |
| **`-e`, `--evidence [ID]`** | **現地實踐誤差檢視** | 檢視所有肉身實踐情境與誤差指標 (`friction_percentage`)。若物理偏離度高於 `10.0%` 會顯示 `⚠️` 警告。 |
| **`-r`, `--red [ms_id]`** | **紅軍對抗答辯日誌** | 查詢與紅軍對審的答辯軌跡明細（Reviewer Attack / Student Defense）。預設為 `ms_sovereign_research_2026`。 |
| **`-m`, `--manuscript [ID]`** | **手稿有向演化看板** | 列出正在撰寫或已發表的手稿與前導手稿演化鏈；指定手稿 ID 時可展示其引用的文獻與「引用心智脈絡」對照表。 |
| **`--roots`** | **抽象路徑移植性體檢** | 掃描 `directory_roots`，利用 `os.path.exists()` 實體檢測本地路徑是否斷線，顯示 `🟢 OK` 或 `🔴 斷線`。 |
| **`-c`, `--cite-tree [key]`** | **文獻引用合規樹狀圖** | 合併文獻 `key_references_to_suck` 與 `paper_relations` 的關聯，遞迴繪製 ASCII 引用樹，標示其在 DB 中的合規狀態 (`🟢 Stage 2` / `🟡 Stage 1` / `❌ 未註冊`)。 |
| **`-v`, `--verbose`** | **十大學術因子通讀** | 需搭配 `-c` 使用。在引用樹下方以條目排版輸出樹中所有已消化 `Stage 2` 文獻的完整十大學術因子 DTO，免除重複手動檢索的認知摩擦。 |
| **`-s`, `--sql [SQL_str]`** | **實體 SQL 照妖鏡** | 直接輸入自訂 SQL 語句進行硬核查詢與資料治理。 |
| **`-g`, `--report [ms_id]`** | **全景 Markdown 探勘報告** | 將指定手稿的所有相關 DB 內容（含手稿 Meta、引文地基對合看板、十大學術因子 DTO、紅軍對審日誌與現地誤差）匯出為有結構的 Markdown 報告。預設為 `ms_sovereign_research_2026`。 |
| **`-rd`, `--read-depth [args]`** | **真實文獻閱讀深度更新** | 批次更新文獻的真實閱讀層次。可傳入多個 `cite_key:level`（如 `key:3`）或單一 JSON 檔案路徑。 |

---

## 💡 4. 實戰用法範例 (Examples)

### 1. 檢視施工現場與專案演進
```bash
python3 scripts/brain_cli.py -t
```
這會印出精美的專案與循序主題演進看板，幫您快速辨識當前處於哪一個 active 戰場。

### 2. 檢測跨電腦移植之路徑狀態
```bash
python3 scripts/brain_cli.py --roots
```
這會逐一檢查 Zotero 儲存庫路徑與實驗室 NAS 路徑在本機是否在線，保障移植順暢。

### 3. 一鍵通讀某篇文獻的所有參考文獻的十大因子
當您要精讀 `@CAG2024RAG` 並確保自己讀過其下所有參考資料的十大學術因子時：
```bash
python3 scripts/brain_cli.py -c CAG2024RAG -v
```
**輸出範例：**
```
🌳 --- 引用文獻樹狀合規看板 (Cite Tree) ---
CAG2024RAG (不用做 RAG！當快取增強生成 (CAG) 成為知識任務之所需...) [🟢 Stage 2 (已合規)]
├── DeepSeek2025R1 (DeepSeek-R1：透過強化學習激發大語言模型之推理能力...) [🟡 Stage 1 (未洗滌)]
└── zotero_Lewis_2020_rag (zotero_Lewis_2020_rag...) [❌ 未在大腦資料庫中註冊]

================================================================================
📖  十大學術因子 DTO 深度通讀看板 (Ten Academic Factors DTO)
================================================================================

[1] 📄 文獻引用鍵: @CAG2024RAG
    標題: 不用做 RAG！當快取增強生成 (CAG) 成為知識任務之所需
    ----------------------------------------------------------------------
    1. 🎯 核心問題 (Core Question):
       "在長文本語言模型時代，快取增強生成 (CAG) 是否能全面取代傳統檢索增強生成 (RAG) 以免除分塊與檢索摩擦力？"
    ...
```

### 4. 彈性自訂 SQL 查詢
配合專案根目錄下的 [brain_queries.sql](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/brain_queries.sql)，複製其中的查詢範本並貼上執行：
```bash
python3 scripts/brain_cli.py -s "SELECT cite_key, json_extract(meta_data, '$.stage') AS ingestion_stage FROM papers WHERE json_extract(meta_data, '$.compliance_status.is_compliant') = 1;"
```

### 5. 匯出全景 Markdown 探勘報告
當需要對某一論文手稿的引文地基與審查防線進行全景式審閱，並以標題階層方便在 Obsidian 中點選瀏覽時，可以執行 `-g` 指令：
```bash
python3 scripts/brain_cli.py -g ms_sovereign_research_2026
```
**執行成果與輸出：**
*   **生成檔案路徑**：[sovereign_research_13_brain_report.md](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/manuscripts/sovereign_research/sovereign_research_13_brain_report.md)
*   **報告內容**：包含手稿基本資料、91 篇定錨文獻與學術重力分數對照矩陣、各篇 Stage 2 文獻的十大學術因子 DTO 展開、紅軍對審日誌與現地誤差檢測表，免除在 SQLite 資料庫中反覆下 SQL 檢索的難度。

### 6. 手動/批次更新文獻閱讀層次 (Reading Depth Updates)

您可以手動更新文獻的真實閱讀深度以修正 MCI 剛性指標。閱讀層次定義如下：
*   `0` ➔ `UNREAD` (未讀，權重 0.0)
*   `1` ➔ `DTO_SUMMARY` (看過十大因子摘要，權重 0.3)
*   `2` ➔ `SKIMMED` (真實簡讀/速讀，權重 0.7)
*   `3` ➔ `BODY_ON_DEEP` (真實身讀/精讀，權重 1.0)

**多筆更新語法範例（命令列鍵值對）：**
```bash
python3 scripts/brain_cli.py -rd zotero_Listgarten_2024_635:3 zotero_Lewis_2020_rag:2
```

**大量更新語法範例（JSON 批次檔案）：**
```bash
python3 scripts/brain_cli.py -rd batch_read.json
```
JSON 檔案格式例如下：
```json
{
  "zotero_Listgarten_2024_635": 3,
  "zotero_Lewis_2020_rag": "SKIMMED"
}
```

---

## 🛠️ 5. 大腦資料庫 DDL 參考

大腦各表格的實體 schema 詳見專案目錄下的 [schema.sql](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/schema.sql)。
如果您需要新增查詢指令或修改 DQL 邏輯，可直接參考並修改 [brain_cli.py](file:///Users/wuulong/github/bmad-pa/events/my_research/sovereign-research-methodology/scripts/brain_cli.py)。
