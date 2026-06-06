# 🧱 methodology_51: 現地對合與物理誤差摩擦計量 (Empirical Evidences & Friction Calibration Specification)

本規格書詳細定義了主權大腦如何將「肉身實踐現地真值」與「資料庫實體」進行剛性對合，並給出物理誤差摩擦計量公式與聯覺裁決規範。

---

## 🏛️ 1. 現地實踐對合與防偽 (Empirical Evidence Grounding)

AI 常在無摩擦的「完美理論空間」中編織謊言。為打破此虛假泡泡，本方法論強制要求：
- 手稿中的關鍵主張（特別是實驗與實作部分），必須在 `empirical_evidences` 表中註冊對應的「本地實測真值資料列」。
- 該資料列記錄了實作時的硬體主機（`host_name`）、操作者（`author_name`）、實測耗時（`execution_duration_sec`）以及運行參數。此為證明手稿論點「非 AI 虛空捏造」的實體鐵證。

---

## 📐 2. 物理摩擦計量公式 (Physical Friction Measure)

在 `empirical_evidences` 中，我們藉由量化「本地實測值」與「文獻理論值」之間的偏差，來定位我們的原創貢獻突破口 (Gap)：

$$\text{Friction \%} = \left| \frac{\text{本地實測/模擬真值} - \text{背景文獻理論值}}{\text{背景文獻理論值}} \right| \times 100\%$$

### 2.1 摩擦計量之本體價值
- **戳破 AI 幻覺**：AI 常將理論值視為 100% 可行，但本地實踐的 `Friction %` 能真實反映環境限制（如網路延遲、記憶體溢出、精度損失）。
- **定位學術貢獻**：若本地實踐的 Friction 高達 40%，代表該文獻的方法存在嚴重環境摩擦；而我們手稿若能提出將其降至 10% 的改良方法，即是堅不可摧的 Novelty。

---

## 👁️ 3. 視覺聯覺裁決 (Qualitative Sensory Judgment)

除了定量數值外，本系統特別引入 **「視覺聯覺裁決 (Sensory Decision)」**：
- **實體欄位**：`empirical_evidences` 表中的 `artifact_visual_path`。
- **機制**：該欄位必須指向本地生成的實體圖資路徑（如：曾文溪流域高程分級圖、示波器實測波形圖、性能對比折線圖）。
- **學者直覺行使**：導師在審查手稿時，不需要去檢查幾十萬行的代碼，只需點開圖資路徑，在 1 秒鐘內行使人類頂級學者的「視覺聯覺直覺」，即可判定該實踐的真偽與品位，拒絕對無感數據進行盲信。
