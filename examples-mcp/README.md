# Fusion 360 MCP 範例

本目錄包含 Fusion 360 Model Context Protocol (MCP) Add-in 的參考實現。

> **來源**: [AutodeskFusion360/FusionMCPSample](https://github.com/AutodeskFusion360/FusionMCPSample)  
> **授權**: MIT License

---

## 📖 快速參考

- **📚 [MCP 快速參考手冊](./MCP_QUICK_REFERENCE.md)**: 完整的 MCP 使用指南和開發文檔

---

## 🎯 什麼是 MCP？

**Model Context Protocol (MCP)** 是一個標準化協議，讓 AI 助手能夠與外部工具和數據源互動。這個 Add-in 提供了一個 HTTP API，讓外部應用程式（如 Cursor）能夠通過安全的 HTTP 介面與 Fusion 360 互動。

---

## 🚀 快速開始

### 安裝

1. 將 `Fusion MCP Addin` 資料夾複製到 Fusion 360 Add-ins 目錄：
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion\API\AddIns\`
   - **macOS**: `~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns/`

2. 在 Fusion 360 中啟動 Add-in

3. 配置 Cursor 連接（見下方）

### 配置 Cursor

在 Cursor 配置文件中添加：

```json
{
  "mcpServers": {
    "fusion-mcp-server": {
      "url": "http://localhost:9100/"
    }
  }
}
```

---

## 📁 目錄結構

```
examples-mcp/
├── README.md                    # 本文件
├── MCP_QUICK_REFERENCE.md      # 快速參考手冊
├── LICENSE                      # MIT 授權
└── Fusion MCP Addin/            # Add-in 源碼
    ├── Fusion MCP Addin.py     # 主文件
    ├── README.md               # 安裝說明
    ├── tips.md                 # 使用技巧
    ├── mcp_primitives/         # MCP 原語
    ├── server/                 # 伺服器實現
    ├── tools/                  # 工具實現
    └── resources/              # 資源實現
```

---

## 🛠️ 可用工具

1. **execute_api_script**: 執行 Fusion API Python 腳本
2. **get_screenshot**: 捕獲視窗截圖
3. **get_api_documentation**: 搜索 Fusion API 文檔

詳細說明請參閱 [MCP_QUICK_REFERENCE.md](./MCP_QUICK_REFERENCE.md)。

---

## 📚 相關文檔

- **快速參考**: [MCP_QUICK_REFERENCE.md](./MCP_QUICK_REFERENCE.md)
- **安裝說明**: [Fusion MCP Addin/README.md](./Fusion%20MCP%20Addin/README.md)
- **使用技巧**: [Fusion MCP Addin/tips.md](./Fusion%20MCP%20Addin/tips.md)
- **工具最佳實踐**: [Fusion MCP Addin/tools/best_practices.md](./Fusion%20MCP%20Addin/tools/best_practices.md)

---

## 🔗 相關資源

- **官方倉庫**: https://github.com/AutodeskFusion360/FusionMCPSample
- **MCP 協議**: https://modelcontextprotocol.io/
- **Fusion 360 API**: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A

---

**最後更新**: 2024年
