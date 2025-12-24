# Fusion 360 MCP 快速參考手冊

本文件提供 Fusion 360 Model Context Protocol (MCP) Add-in 的快速參考指南。

> **範例來源**: [FusionMCPSample](https://github.com/AutodeskFusion360/FusionMCPSample)  
> **詳細文檔**: 請參閱 `Fusion MCP Addin/README.md` 和 `Fusion MCP Addin/tips.md`

---

## 📚 目錄

1. [什麼是 MCP？](#什麼是-mcp)
2. [快速開始](#快速開始)
3. [架構說明](#架構說明)
4. [可用工具](#可用工具)
5. [與 Cursor 整合](#與-cursor-整合)
6. [開發指南](#開發指南)
7. [常見問題](#常見問題)

---

## 🔍 什麼是 MCP？

**Model Context Protocol (MCP)** 是一個標準化協議，讓 AI 助手能夠與外部工具和數據源互動。Fusion MCP Add-in 提供了一個 HTTP API，讓外部應用程式（如 Cursor）能夠通過安全的 HTTP 介面與 Fusion 360 互動。

### 主要特性

- **HTTP 伺服器管理**: 在 Fusion 360 內創建和管理 HTTP 伺服器
- **線程安全執行**: 從背景線程安全執行 Fusion API 調用
- **MCP 伺服器**: 暴露 Model Context Protocol 伺服器供 AI 助手整合
- **資源訪問**: 訪問設計資訊、組件和視窗截圖
- **遠程工具執行**: 遠程執行 Fusion 命令

---

## 🚀 快速開始

### 安裝步驟

1. **複製 Add-in 到 Fusion 目錄**:
   ```bash
   # Windows
   %APPDATA%\Autodesk\Autodesk Fusion\API\AddIns\
   
   # macOS
   ~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns/
   ```

2. **啟動 Fusion 360** 並進入 **Add-Ins** 面板

3. **找到 "Fusion MCP Addin"** 並點擊 **Run**

4. **伺服器啟動**: Add-in 會在 `localhost:9100` 啟動 HTTP 伺服器（端口可在代碼中配置）

### 驗證安裝

啟動後，您應該在 Fusion 360 的 Text Commands 視窗中看到：
```
Fusion MCP Add-in started successfully!

MCP server running on localhost:9100
You can now connect to Fusion.
```

---

## 🏗️ 架構說明

MCP Add-in 由三個主要組件構成：

### 1. TaskManager (`server/task_manager.py`)

提供線程安全的 Fusion API 調用執行機制。

**核心功能**:
- 從 HTTP 請求處理器安全執行 Fusion API 調用
- 使用 Fusion 自定義事件系統進行線程間通信
- 錯誤處理和結果報告

**使用方式**:
```python
from server.task_manager import TaskManager

# 執行任務（線程安全）
result = TaskManager.post_task(
    lambda: some_fusion_api_call(),
    timeout=30.0
)
```

### 2. McpServer (`server/mcp_server.py`)

實現 MCP 協議的 HTTP 伺服器。

**核心功能**:
- 線程化 HTTP 伺服器實現
- 自定義請求處理器支援
- 整合 ThreadingMixIn 以安全訪問 Fusion API

### 3. 主 Add-in (`Fusion MCP Addin.py`)

實現 MCP 兼容的 HTTP 端點。

**核心功能**:
- 健康檢查和狀態端點
- 資源讀取（設計資訊、組件）
- 工具執行（截圖、環境資訊）
- JSON 格式的請求/響應處理

---

## 🛠️ 可用工具

### 1. `execute_api_script`

執行使用 Fusion API 的 Python 腳本。腳本在 Fusion 上下文中運行，具有完整的 API 訪問權限。

**參數**:
- `script` (string, required): 要執行的 Python 腳本源代碼

**返回**: 執行結果，包含成功/失敗狀態和輸出訊息

**範例使用**:
```python
# 創建一個 10cm 的方塊
script = """
import adsk.core
import adsk.fusion

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root_comp = design.rootComponent

# 創建草圖和拉伸...
"""

# 從 AI 助手使用
# "Create a 10cm cube at the origin"
# "List all components in the current design"
# "Extrude the selected sketch 5cm"
```

**腳本要求**:
- 必須包含一個 `run(context)` 函數
- 函數接受單個參數（通常是 `None`）

### 2. `get_screenshot`

捕獲當前 Fusion 視窗的截圖，可選相機方向。

**參數**:
- `view` (string, optional): 相機方向
  - 可選值: `"current"`, `"top"`, `"bottom"`, `"front"`, `"back"`, `"left"`, `"right"`, `"iso-top-left"`, `"iso-top-right"`, `"iso-bottom-left"`, `"iso-bottom-right"`
  - 預設: `"current"`
- `width` (integer, optional): 截圖寬度（像素），範圍 1-4096，預設: 512
- `height` (integer, optional): 截圖高度（像素），範圍 1-4096，預設: 512

**返回**: Base64 編碼的 PNG 圖像數據

**範例使用**:
```python
# 獲取當前視圖截圖
{
    "view": "current",
    "width": 1024,
    "height": 768
}

# 獲取等軸測視圖
{
    "view": "iso-top-right",
    "width": 512,
    "height": 512
}
```

### 3. `get_api_documentation`

搜索 Fusion API 文檔，查找類別、屬性、方法及其描述。幫助 AI 助手發現和理解 Fusion API。

**參數**:
- `search_term` (string, required): 要搜索的術語
  - 可以帶命名空間前綴（如 `"fusion.Application"`）
  - 或類別前綴（如 `"core.Application.activeDocument"`）
- `category` (string, optional): 搜索類別
  - 可選值: `"class_name"`, `"member_name"`, `"description"`, `"all"`
  - 預設: `"all"`

**返回**: 前 3 個結果，包含文檔說明、類別定義、屬性和方法及其簽名

**範例搜索**:
- `"Application"` - 查找 Application 類別
- `"fusion.Sketch.sketchCurves"` - 查找 Sketch 類別的 sketchCurves 成員
- `"extrude"` - 搜索與拉伸相關的項目

---

## 🔌 與 Cursor 整合

### 配置 Cursor

在 Cursor 配置文件中添加 MCP 伺服器：

**配置文件位置**:
- macOS: `~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
- Windows: `%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`

**配置內容**:
```json
{
  "mcpServers": {
    "fusion-mcp-server": {
      "url": "http://localhost:9100/"
    }
  }
}
```

### 使用方式

配置完成後，您可以在 Cursor 中直接與 Fusion 360 互動：

1. **執行 Fusion API 腳本**:
   ```
   在 Fusion 中創建一個 10cm x 10cm x 10cm 的方塊
   ```

2. **獲取設計截圖**:
   ```
   顯示當前設計的等軸測視圖截圖
   ```

3. **查詢 API 文檔**:
   ```
   查找 Fusion API 中關於拉伸的方法
   ```

---

## 💻 開發指南

### 創建自定義工具

1. **在 `tools/` 目錄創建新工具文件**:
   ```python
   # tools/my_custom_tool.py
   from ..mcp_primitives.tool import Tool
   from ..mcp_primitives.registry import register
   
   def handler(param1: str, param2: int) -> dict:
       """處理函數"""
       # 執行邏輯
       return {
           "content": [{"type": "text", "text": "結果"}],
           "isError": False
       }
   
   # 註冊工具
   register(
       Tool(
           name="my_custom_tool",
           description="我的自定義工具描述",
           inputSchema={
               "type": "object",
               "properties": {
                   "param1": {"type": "string", "description": "參數1"},
                   "param2": {"type": "integer", "description": "參數2"}
               },
               "required": ["param1", "param2"]
           },
           handler=handler
       )
   )
   ```

2. **在 `tools/__init__.py` 中導入**:
   ```python
   from . import my_custom_tool
   ```

### 創建自定義資源

1. **在 `resources/` 目錄創建新資源文件**:
   ```python
   # resources/my_resource.py
   from ..mcp_primitives.resource import Resource
   from ..mcp_primitives.registry import register
   
   def handler(uri: str) -> dict:
       """處理資源請求"""
       return {
           "contents": [{"type": "text", "text": "資源內容"}]
       }
   
   # 註冊資源
   register(
       Resource(
           uri="fusion://my-resource",
           name="My Resource",
           description="我的自定義資源",
           mimeType="text/plain",
           handler=handler
       )
   )
   ```

2. **在 `resources/__init__.py` 中導入**:
   ```python
   from . import my_resource
   ```

### 線程安全執行

**重要**: Fusion API 不是線程安全的，所有 Fusion API 調用必須通過 TaskManager 執行。

```python
from server.task_manager import TaskManager
import adsk.core

def my_fusion_operation():
    """在 Fusion 主線程中執行的操作"""
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    # ... 執行 Fusion API 操作
    return "操作完成"

# 從 HTTP 處理器調用（背景線程）
result = TaskManager.post_task(
    my_fusion_operation,
    timeout=30.0
)

if result["success"]:
    output = result["output"]
else:
    error = result["error"]
```

---

## 📝 工具描述最佳實踐

在 MCP 環境中，精心編寫的工具描述對於 AI 助手理解何時以及如何使用每個工具至關重要。

### 好的工具描述應包含：

1. **清晰的目的說明**: 工具做什麼
2. **參數詳細說明**: 每個參數的類型、約束和用途
3. **使用範例**: 具體的使用場景
4. **返回值說明**: 返回數據的格式和內容

### 範例：

```python
Tool(
    name="execute_api_script",
    description="""
    Execute Python scripts using the Fusion API. 
    The script runs in the Fusion context with full API access.
    
    The script must contain a 'run(context)' function that takes a single argument.
    This function will be called automatically when the script is executed.
    
    Example script:
    ```python
    import adsk.core
    import adsk.fusion
    
    def run(context):
        app = adsk.core.Application.get()
        design = adsk.fusion.Design.cast(app.activeProduct)
        # Your code here
    ```
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "script": {
                "type": "string",
                "description": "Python script source code to execute. Must contain a 'run(context)' function."
            }
        },
        "required": ["script"]
    },
    handler=handler
)
```

---

## 🔧 常見問題

### Q: 伺服器無法啟動

**可能原因**:
- 端口 9100 已被佔用
- Fusion 360 沒有必要的權限
- 防火牆阻止連接

**解決方法**:
1. 檢查端口是否被佔用：
   ```bash
   # macOS/Linux
   lsof -i :9100
   
   # Windows
   netstat -ano | findstr :9100
   ```

2. 修改端口（在 `Fusion MCP Addin.py` 中）:
   ```python
   PORT = 9101  # 更改為其他端口
   ```

3. 檢查 Fusion 360 Text Commands 視窗的錯誤訊息

### Q: 命令執行失敗

**可能原因**:
- Fusion API 調用在當前上下文中無效
- 參數傳遞不正確
- 腳本語法錯誤

**解決方法**:
1. 檢查腳本是否包含 `run(context)` 函數
2. 驗證 Fusion API 調用是否適用於當前上下文
3. 查看 Fusion 360 Text Commands 視窗的錯誤訊息

### Q: Cursor 無法連接到 MCP 伺服器

**可能原因**:
- MCP Add-in 未啟動
- 配置文件路徑或格式錯誤
- 網絡連接問題

**解決方法**:
1. 確認 Fusion MCP Add-in 已啟動並顯示成功訊息
2. 驗證 Cursor 配置文件格式正確
3. 測試 HTTP 連接：
   ```bash
   curl http://localhost:9100/health
   ```

### Q: 如何調試工具執行？

**方法**:
1. 查看 Fusion 360 Text Commands 視窗的日誌輸出
2. 在工具處理函數中添加日誌：
   ```python
   import adsk.core
   app = adsk.core.Application.get()
   app.log("調試訊息")
   ```
3. 檢查返回的錯誤訊息

---

## 📂 文件結構

```
Fusion MCP Addin/
├── Fusion MCP Addin.py          # 主 Add-in 文件
├── __init__.py
├── README.md                     # 安裝和使用說明
├── tips.md                       # 使用技巧和最佳實踐
│
├── mcp_primitives/              # MCP 原語定義
│   ├── tool.py                   # Tool 類別定義
│   ├── resource.py               # Resource 類別定義
│   ├── registry.py               # 工具和資源註冊表
│   └── ...
│
├── server/                       # 伺服器實現
│   ├── mcp_server.py            # MCP 伺服器實現
│   ├── task_manager.py          # 任務管理器（線程安全）
│   └── README.md
│
├── tools/                        # 工具實現
│   ├── execute_api_script.py    # 執行 API 腳本工具
│   ├── get_screenshot.py         # 截圖工具
│   ├── get_api_documentation.py # API 文檔搜索工具
│   └── best_practices.md        # 工具開發最佳實踐
│
└── resources/                    # 資源實現
    └── get_screenshot.py        # 截圖資源
```

---

## 🔗 相關資源

- **官方範例**: https://github.com/AutodeskFusion360/FusionMCPSample
- **MCP 協議規範**: https://modelcontextprotocol.io/
- **Fusion 360 API 文檔**: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A
- **Apper 框架**: https://apper.readthedocs.io/en/latest/apper.html

---

## 💡 使用技巧

### 1. 腳本執行最佳實踐

- **使用事務**: 腳本會自動在事務中執行，確保原子性
- **錯誤處理**: 在腳本中添加適當的錯誤處理
- **日誌輸出**: 使用 `app.log()` 輸出調試資訊

### 2. 截圖使用場景

- **設計審查**: 快速獲取設計視圖
- **文檔生成**: 自動生成設計截圖
- **AI 視覺分析**: 讓 AI 助手"看到"設計

### 3. API 文檔搜索

- **發現 API**: 當不確定使用哪個 API 時
- **學習 API**: 了解 API 的用法和參數
- **驗證用法**: 確認 API 調用是否正確

---

## ⚠️ 注意事項

1. **線程安全**: 所有 Fusion API 調用必須通過 TaskManager 執行
2. **錯誤處理**: 始終包含適當的錯誤處理
3. **超時設置**: 長時間運行的操作應設置適當的超時時間
4. **資源清理**: 確保正確清理資源，避免記憶體洩漏

---

**最後更新**: 2024年  
**維護者**: Jason.Lin

