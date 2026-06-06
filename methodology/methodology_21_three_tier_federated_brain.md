# 🧱 methodology_21: 三層聯邦大腦架構 (3-Tier Ingestion & Federated Brain Architecture)

本規格書定義了主權科研大腦的知識管理層次與「三層聯邦引渡流程」。為確保進入大腦的知識皆經過嚴格的「穿透式洗滌」，大腦對文獻進行三層結構化隔離：

---

## 🏛️ 1. 三層結構化定義 (The 3-Tier Structure)

```
[公海緩衝區：Layer 0] ➔ 載入 Zotero 原始文獻資訊，狀態預設為 PENDING 待消化。
          │
          ▼
[主權碼頭靠泊：Layer 1] ➔ 透過主題 topic_id 定錨，重定向靠泊至特定研究主題下。
          │
          ▼
[穿透解構自審：Layer 2] ➔ 深度解構十大學術因子，與紅軍自審對抗，升級為 STAGE_2_DEEP。
```

### 1.1 Layer 0：公海緩衝區 (Pending Ocean)
- **物理定位**：`papers` 表中 `status = 'PENDING'` 且未與任何 `topics` 繫結的資料列。
- **資料來源**：透過 Zotero API 或本地同步腳本，將 PDF 詮釋資料抽引寫入。
- **職責**：作臨時文獻暫存，尚未被主權大腦打上任何本地主題標籤，屬於待洗滌的原始資料。

### 1.2 Layer 1：主權碼頭靠泊區 (Active Docking)
- **物理定位**：`papers` 表中已與特定 `topic_id` 建立關聯，且 `status = 'PENDING'` 的資料列。
- **轉化條件**：系統根據 `projects` 宣告的主題關鍵字契約，將文獻精準重定向，靠泊至對應的主題分區，完成 Layer 1 定錨。
- **職責**：確立文獻在研究領域中的演化起點，為精讀與算分做好準備。

### 1.3 Layer 2：穿透解構自審區 (Deep Ingestion / STAGE_2_DEEP)
- **物理定位**：`papers` 表中 `status = 'STAGE_2_DEEP'`，且其 `meta_data` JSON 欄位中 100% 填滿「十大學術因子」與「學者品位裁決」的資料列。
- **轉化條件**：執行 `!paper_digest` 人機共讀，降維提取 10 大核心學術因子，完成紅軍對抗自審。
- **職責**：作為大腦的「一等主權知識公民」，此狀態文獻獲准拼裝入 `references.bib` 並支援手稿編譯，解鎖手稿成熟度 MCI 評分警告。
