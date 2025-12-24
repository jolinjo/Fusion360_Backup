# Fusion 360 API 範例程式

本目錄包含來自 [Fusion360APIClass](https://github.com/tapnair/Fusion360APIClass) 的實用範例程式，涵蓋從基礎腳本到完整 Add-in 的各種場景。

> **來源**: [tapnair/Fusion360APIClass](https://github.com/tapnair/Fusion360APIClass)  
> **作者**: [Patrick Rainsberry](https://twitter.com/prrainsberry) (Autodesk Fusion 360 Business Development)  
> **授權**: MIT License

---

## 📁 目錄結構

```
examples/
├── 02 - Scripts/          # 基礎腳本範例（無 UI）
├── 03 - Addins/            # Add-in 範例（帶 UI）
├── 04 - CAM/               # CAM 操作範例
├── 05 - External APIs/     # 外部 API 調用範例
└── resources/              # 資源文件
```

---

## 📖 範例說明

### 02 - Scripts（腳本範例）

這些是基本的 Fusion 360 腳本，不需要 UI，直接在 Fusion 360 中執行。

| 範例 | 說明 | 關鍵技術 |
|-----|------|---------|
| `Block/` | 創建簡單方塊 | 草圖、拉伸特徵 |
| `Block_input/` | 帶輸入的方塊創建 | 用戶輸入處理 |
| `Block_Params/` | 參數化方塊創建 | Fusion 360 參數系統 |

**使用方式**:
1. 在 Fusion 360 中打開「Scripts and Add-ins」
2. 選擇「Scripts」標籤
3. 點擊「+」添加腳本
4. 選擇對應的 `.py` 文件
5. 點擊「Run」

---

### 03 - Addins（Add-in 範例）

這些範例展示如何創建帶 UI 的 Fusion 360 Add-in。

| 範例 | 說明 | 技術特點 |
|-----|------|---------|
| `BlockSimpleAddinDone/` | 最簡單的 Add-in | 原生 Fusion 360 API，事件處理器 |
| `BlockSimpleAddinStart/` | 帶輸入對話框的 Add-in | 命令輸入項創建 |
| `BlockTemplateAddinDone/` | 使用 Apper 框架的完整模板 | Apper 框架，模組化結構 |

**學習路徑**:
1. 先看 `BlockSimpleAddinDone/` 了解基本結構
2. 再看 `BlockSimpleAddinStart/` 學習輸入處理
3. 最後看 `BlockTemplateAddinDone/` 學習 Apper 框架

**使用方式**:
1. 將整個資料夾複製到 Fusion 360 Add-ins 目錄
2. 在 Fusion 360 中打開「Scripts and Add-ins」
3. 選擇「Add-ins」標籤
4. 點擊「+」添加 Add-in
5. 選擇對應的資料夾
6. 點擊「Run」

---

### 04 - CAM（CAM 範例）

這些範例展示如何操作 Fusion 360 的 CAM 功能。

| 範例 | 說明 | 關鍵功能 |
|-----|------|---------|
| `CAM_Info/` | 讀取 CAM 操作資訊 | 遍歷操作、計算加工時間、讀取參數 |
| `CAM_Basic_Milling/` | 創建基本銑削操作 | 創建 CAM 操作 |
| `CAM_Post/` | 後處理 CAM 操作 | 後處理器使用 |
| `CAM_Libraries/` | 使用 CAM 庫 | CAM 庫操作 |
| `CAM_Workflow_Sample/` | 完整 CAM 工作流程 | 端到端 CAM 工作流程 |

**注意**: 這些範例需要在包含 CAM 產品的文檔中運行。

---

### 05 - External APIs（外部 API 範例）

這些範例展示如何從 Fusion 360 Add-in 調用外部 API。

| 範例 | 說明 | 技術特點 |
|-----|------|---------|
| `ChuckNorris/` | 調用外部 API 獲取笑話 | `lib_import` 裝飾器、`requests` 庫 |
| `ChatWithFusion_LocalImport/` | 本地導入方式調用 OpenAI | 本地庫導入 |
| `ChatWithFusion_Subprocess/` | 子進程方式調用外部 API | 子進程通信 |

**重要提示**:
- 使用 `lib_import` 裝飾器來導入第三方庫
- 需要先安裝第三方庫到 `lib` 目錄：
  ```bash
  cd <addin_directory>
  python3 -m pip install -t ./lib requests
  ```

---

## 🚀 快速開始

### 1. 運行基礎腳本

```python
# 範例: examples/02 - Scripts/Block/Block.py
# 這是最簡單的範例，創建一個方塊

import adsk.core
import adsk.fusion

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root_comp = design.rootComponent

# 創建草圖和拉伸...
```

### 2. 創建簡單 Add-in

參考 `examples/03 - Addins/BlockSimpleAddinDone/` 了解基本結構。

### 3. 使用 Apper 框架

參考 `examples/03 - Addins/BlockTemplateAddinDone/` 和當前專案的 `BackupTool/BackupTool.py`。

---

## 📚 相關文檔

- **快速查詢**: [../QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - 整合的 API 參考和範例索引
- **API 參考**: [../APER_API_REFERENCE.md](../APER_API_REFERENCE.md) - 完整的 Apper API 文檔
- **Apper 文檔**: https://apper.readthedocs.io/en/latest/apper.html
- **Fusion 360 API**: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A

---

## 💡 學習建議

1. **從簡單開始**: 先運行 `02 - Scripts` 中的範例，了解基本 API 使用
2. **理解事件處理**: 學習 `03 - Addins/BlockSimpleAddinDone/` 中的事件處理機制
3. **掌握 Apper 框架**: 深入研究 `03 - Addins/BlockTemplateAddinDone/` 了解最佳實踐
4. **參考實際專案**: 查看當前專案的 `BackupTool/commands/ExportCommand.py` 了解實際應用

---

## ⚠️ 注意事項

1. **Python 版本**: Fusion 360 使用 Python 3.x，確保代碼兼容
2. **API 變更**: Fusion 360 API 可能會更新，某些範例可能需要調整
3. **錯誤處理**: 所有範例都應包含適當的錯誤處理
4. **記憶體管理**: 打開的文件要記得關閉，避免記憶體洩漏

---

## 🔗 相關資源

- [Fusion360APIClass 原始倉庫](https://github.com/tapnair/Fusion360APIClass)
- [Apper 框架源碼](https://github.com/tapnair/apper)
- [Fusion 360 API 論壇](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/123)
- [Patrick Rainsberry 的 Fusion 360 工具集](https://tapnair.github.io/index.html)

---

**最後更新**: 2024年
