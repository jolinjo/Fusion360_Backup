# Fusion 360 API 快速查詢手冊

本文件整合了 Apper API 參考和範例程式索引，方便快速查找和使用。

> **範例來源**: [Fusion360APIClass](https://github.com/tapnair/Fusion360APIClass)  
> **API 文檔**: [Apper 官方文檔](https://apper.readthedocs.io/en/latest/apper.html)

---

## 📚 目錄

1. [快速查找](#快速查找)
2. [範例程式索引](#範例程式索引)
3. [常用 API 速查](#常用-api-速查)
4. [完整 API 參考](#完整-api-參考)
   - [FusionApp](#fusionapp)
   - [Fusion360CommandBase](#fusion360commandbase)
   - [AppObjects](#appobjects)
   - [工具函數](#工具函數)
5. [開發流程](#開發流程)
6. [常見問題](#常見問題)
7. [快速備忘錄](#快速備忘錄)

---

## 🔍 快速查找

### 按功能查找

| 功能需求 | 範例位置 | API 參考 |
|---------|---------|---------|
| 創建基本 Add-in | `examples/03 - Addins/BlockSimpleAddinDone/` | [FusionApp](#fusionapp) |
| 創建帶對話框的命令 | `examples/03 - Addins/BlockSimpleAddinStart/` | [Fusion360CommandBase](#fusion360commandbase) |
| 使用 Apper 框架 | `examples/03 - Addins/BlockTemplateAddinDone/` | [FusionApp](#fusionapp) |
| 基本腳本（無 UI） | `examples/02 - Scripts/Block/` | [AppObjects](#appobjects) |
| CAM 操作 | `examples/04 - CAM/CAM_Info/` | [AppObjects.cam](#appobjects) |
| 外部 API 調用 | `examples/05 - External APIs/ChuckNorris/` | [lib_import](#工具函數) |
| 導出文件 | 當前專案 `BackupTool/commands/ExportCommand.py` | [AppObjects.export_manager](#appobjects) |

### 按場景查找

| 場景 | 解決方案 | 相關範例 |
|-----|---------|---------|
| 創建幾何體 | `root_comp.features.extrudeFeatures` | `Block.py`, `BlockSimpleAddinDone.py` |
| 讀取 CAM 資訊 | `cam_product.allOperations` | `CAM_Info.py` |
| 調用外部 API | 使用 `lib_import` 裝飾器 | `ChuckNorris.py` |
| 處理專案和文件 | `app.data.dataProjects` | `ExportCommand.py` |
| 創建命令對話框 | `on_create()` 方法 | `BlockSimpleAddinStart.py` |

---

## 📖 範例程式索引

### 02 - Scripts（腳本範例）

這些是基本的 Fusion 360 腳本，不需要 UI，直接執行。

#### `Block/Block.py`
**功能**: 創建一個簡單的方塊  
**關鍵技術**:
- 獲取設計和根組件
- 創建草圖和線條
- 創建拉伸特徵

**核心代碼片段**:
```python
design = adsk.fusion.Design.cast(app.activeProduct)
root_comp = design.rootComponent
sketches = root_comp.sketches
xy_plane = root_comp.xYConstructionPlane
sketch = sketches.add(xy_plane)
# ... 創建線條和拉伸
```

#### `Block_input/Block_input.py`
**功能**: 帶輸入參數的方塊創建腳本  
**關鍵技術**: 使用 `ui.messageBox` 獲取用戶輸入

#### `Block_Params/Block_Params.py`
**功能**: 使用參數化創建方塊  
**關鍵技術**: 使用 Fusion 360 參數系統

---

### 03 - Addins（Add-in 範例）

這些範例展示如何創建帶 UI 的 Fusion 360 Add-in。

#### `BlockSimpleAddinDone/BlockSimpleAddinDone.py`
**功能**: 最簡單的 Add-in，創建一個按鈕執行命令  
**關鍵技術**:
- 使用原生 Fusion 360 API 創建命令
- 事件處理器（`CommandCreatedHandler`, `CommandExecuteHandler`）
- 命令定義和控件管理

**學習重點**:
- 如何註冊命令到 UI
- 如何處理命令事件
- 如何清理資源

**文件位置**: `examples/03 - Addins/BlockSimpleAddinDone/BlockSimpleAddinDone.py`

#### `BlockSimpleAddinStart/BlockSimpleAddinStart.py`
**功能**: 帶輸入對話框的 Add-in  
**關鍵技術**: 在 `command_created` 中創建輸入項

#### `BlockTemplateAddinDone/BlockTemplateAddinDone.py`
**功能**: 使用 Apper 框架的完整 Add-in 模板  
**關鍵技術**:
- 使用 Apper 框架結構
- 模組化命令組織
- 工具函數庫使用

**文件結構**:
```
BlockTemplateAddinDone/
├── BlockTemplateAddinDone.py    # 主文件
├── config.py                     # 配置
├── commands/                     # 命令目錄
│   ├── __init__.py
│   ├── block/
│   └── cylinder/
└── lib/                          # 工具庫
    └── fusion360utils/
```

**學習重點**:
- Apper 框架的使用方式
- 如何組織多個命令
- 如何使用工具函數庫

---

### 04 - CAM（CAM 範例）

這些範例展示如何操作 Fusion 360 的 CAM 功能。

#### `CAM_Info/CAM_Info.py`
**功能**: 讀取 CAM 操作資訊  
**關鍵技術**:
- 獲取 CAM 產品：`adsk.cam.CAM.cast(document.products.itemByProductType('CAMProductType'))`
- 遍歷所有操作：`cam_product.allOperations`
- 計算加工時間：`cam_product.getMachiningTime()`
- 讀取操作參數：`operation.parameters.itemByName()`

**核心代碼片段**:
```python
cam_product = adsk.cam.CAM.cast(document.products.itemByProductType('CAMProductType'))
cam_product.generateAllToolpaths(True)

for operation in cam_product.allOperations:
    machining_time = cam_product.getMachiningTime(operation, feed_scale, rapid_feed, tool_change_time)
    feed_rate_parameter = operation.parameters.itemByName('tool_feedCutting')
```

**文件位置**: `examples/04 - CAM/CAM_Info/CAM_Info.py`

#### `CAM_Basic_Milling/CAM_Basic_Milling.py`
**功能**: 創建基本銑削操作

#### `CAM_Post/CAM_Post.py`
**功能**: 後處理 CAM 操作

#### `CAM_Libraries/CAM_Libraries.py`
**功能**: 使用 CAM 庫

#### `CAM_Workflow_Sample/CAM_Workflow_Sample.py`
**功能**: 完整的 CAM 工作流程範例

---

### 05 - External APIs（外部 API 範例）

這些範例展示如何從 Fusion 360 Add-in 調用外部 API。

#### `ChuckNorris/ChuckNorris.py`
**功能**: 調用外部 API 獲取 Chuck Norris 笑話  
**關鍵技術**:
- 使用 `lib_import` 裝飾器導入第三方庫
- 使用 `requests` 庫調用 REST API
- 處理 JSON 響應

**核心代碼片段**:
```python
@lib_import(SCRIPT_DIRECTORY)
def make_request(url, headers=None):
    import requests
    r = requests.get(url, headers=headers)
    return r

r = make_request('https://api.chucknorris.io/jokes/random')
r_json = r.json()
joke = r_json['value']
```

**學習重點**:
- 如何在 Fusion 360 中使用第三方庫
- `lib_import` 裝飾器的使用
- 外部 API 調用模式

**文件位置**: `examples/05 - External APIs/ChuckNorris/ChuckNorris.py`

#### `ChatWithFusion_LocalImport/ChatWithFusion_LocalImport.py`
**功能**: 使用本地導入方式調用 OpenAI API

#### `ChatWithFusion_Subprocess/ChatWithFusion_Subprocess.py`
**功能**: 使用子進程方式調用外部 API

---

## ⚡ 常用 API 速查

### FusionApp

#### 初始化應用
```python
import apper
my_addin = apper.FusionApp('AppName', 'CompanyName', debug=False)
```

#### 添加命令
```python
my_addin.add_command(
    'Command Name',
    CommandClass,
    {
        'cmd_id': 'unique_id',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'PanelName',
        'cmd_resources': 'command_icons',
        'command_visible': True,
        'command_promoted': True,
    }
)
```

#### 運行/停止
```python
def run(context):
    my_addin.run_app()

def stop(context):
    my_addin.stop_app()
```

---

### Fusion360CommandBase

#### 基本結構
```python
class MyCommand(apper.Fusion360CommandBase):
    def on_create(self, command, inputs):
        # 創建 UI 輸入項
        inputs.addStringValueInput('input_id', 'Label', 'default_value')
    
    def on_execute(self, command, inputs, args, input_values):
        # 執行命令邏輯
        value = input_values['input_id']
        # ... 處理邏輯
    
    def on_input_changed(self, command, inputs, changed_input, input_values):
        # 響應輸入變化
        if changed_input.id == 'input_id':
            # 更新 UI
            pass
```

#### 常用輸入類型
```python
# 字符串輸入
inputs.addStringValueInput('text_id', 'Text Label', 'default')

# 數值輸入
inputs.addValueInput('value_id', 'Value Label', units, default_value)

# 下拉選單
dropdown = inputs.addDropDownCommandInput('dropdown_id', 'Label', 
    adsk.core.DropDownStyles.TextListDropDownStyle)
dropdown.listItems.add('Option 1', True)  # True = 預設選中

# 複選框下拉選單
checkbox_dropdown = inputs.addDropDownCommandInput('checkbox_id', 'Label',
    adsk.core.DropDownStyles.CheckBoxDropDownStyle)
checkbox_dropdown.listItems.add('Option 1', False)

# 布林值輸入（複選框）
inputs.addBoolValueInput('bool_id', 'Checkbox Label', True, '', False)

# 按鈕（使用 BoolValueInput 作為觸發器）
button = inputs.addBoolValueInput('button_id', 'Button Label', False, '', False)
```

---

### AppObjects

#### 初始化
```python
from apper import AppObjects
ao = AppObjects()
```

#### 常用屬性速查

| 屬性 | 類型 | 用途 | 範例 |
|-----|------|------|------|
| `ao.document` | `adsk.fusion.Document` | 當前活動文檔 | `doc.name` |
| `ao.design` | `adsk.fusion.Design` | 當前設計 | `design.rootComponent` |
| `ao.root_comp` | `adsk.fusion.Component` | 根組件 | `root_comp.bRepBodies` |
| `ao.export_manager` | `adsk.fusion.ExportManager` | 導出管理器 | `export_mgr.createSTEPExportOptions()` |
| `ao.ui` | `adsk.core.UserInterface` | 用戶界面 | `ui.messageBox()`, `ui.createFolderDialog()` |
| `ao.app` | `adsk.core.Application` | 應用程序 | `app.data.dataProjects` |
| `ao.cam` | `adsk.cam.CAM` | CAM 產品 | `cam.allOperations` |

#### 常用操作

**獲取專案和文件**:
```python
ao = AppObjects()
# 所有專案
projects = ao.app.data.dataProjects
# 活動專案
active_project = ao.app.data.activeProject
# 專案根文件夾
root_folder = active_project.rootFolder
# 遍歷文件夾
for i in range(root_folder.dataFolders.count):
    folder = root_folder.dataFolders.item(i)
# 遍歷文件
for i in range(root_folder.dataFiles.count):
    file = root_folder.dataFiles.item(i)
    if file.fileExtension == 'f3d':
        # 處理 .f3d 文件
```

**導出文件**:
```python
ao = AppObjects()
export_mgr = ao.export_manager

# STEP 導出
step_options = export_mgr.createSTEPExportOptions('/path/to/file.step')
export_mgr.execute(step_options)

# IGES 導出
iges_options = export_mgr.createIGESExportOptions('/path/to/file.igs')
export_mgr.execute(iges_options)

# STL 導出
stl_options = export_mgr.createSTLExportOptions(ao.design.rootComponent, '/path/to/file.stl')
export_mgr.execute(stl_options)
```

**創建幾何體**:
```python
ao = AppObjects()
root_comp = ao.root_comp

# 創建草圖
sketches = root_comp.sketches
sketch = sketches.add(root_comp.xYConstructionPlane)

# 創建線條
lines = sketch.sketchCurves.sketchLines
point1 = adsk.core.Point3D.create(0, 0, 0)
point2 = adsk.core.Point3D.create(10, 0, 0)
line = lines.addByTwoPoints(point1, point2)

# 獲取輪廓
profile = sketch.profiles.item(0)

# 創建拉伸
extrudes = root_comp.features.extrudeFeatures
extrude_input = extrudes.createInput(profile, 
    adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
distance = adsk.core.ValueInput.createByReal(10)
extent_def = adsk.fusion.DistanceExtentDefinition.create(distance)
extrude_input.setOneSideExtent(extent_def, 
    adsk.fusion.ExtentDirections.PositiveExtentDirection)
extrudes.add(extrude_input)
```

**文件夾選擇對話框**:
```python
ao = AppObjects()
folder_dialog = ao.ui.createFolderDialog()
folder_dialog.title = 'Select Folder'
result = folder_dialog.showDialog()
if result == adsk.core.DialogResults.DialogOK:
    selected_folder = folder_dialog.folder
```

---

### 工具函數

#### `get_default_dir(app_name)`
```python
import apper
default_dir = apper.get_default_dir('MyApp')
# 返回: '/Users/username/MyApp'
```

#### `read_settings(app_name)` / `write_settings(app_name, settings)`
```python
import apper
# 讀取
settings = apper.read_settings('MyApp')
# 寫入
apper.write_settings('MyApp', {'key': 'value'})
```

#### `item_id(item, group_name)` / `get_item_by_id(item_id, app_name)`
```python
import apper
ao = AppObjects()
body = ao.root_comp.bRepBodies.item(0)

# 分配 ID
unique_id = apper.item_id(body, 'MyApp')

# 稍後獲取
retrieved_body = apper.get_item_by_id(unique_id, 'MyApp')
```

#### `open_doc(data_file)`
```python
import apper
document = apper.open_doc(data_file)
```

---

## 📚 完整 API 參考

### FusionApp

`FusionApp` 是創建 Fusion 360 Add-in 的基礎類別。

#### 初始化

```python
import apper

my_addin = apper.FusionApp(
    name='YourAppName',      # Add-in 名稱
    company='YourCompany',    # 公司或組織名稱
    debug=False               # 是否啟用調試模式（True 會顯示更多互動反饋）
)
```

#### 主要方法

##### `add_command(name, command_class, options)`

添加命令到應用程式中。

**參數**:
- `name` (str): 命令名稱
- `command_class`: 繼承自 `apper.Fusion360CommandBase` 或 `apper.PaletteCommandBase` 的類別
- `options` (dict): 命令選項（見下方選項說明）

**常用選項**:
```python
{
    'cmd_description': '命令描述',
    'cmd_id': 'unique_command_id',           # 唯一命令 ID
    'workspace': 'FusionSolidEnvironment',   # 工作空間名稱
    'toolbar_panel_id': 'PanelName',         # 工具欄面板 ID
    'cmd_resources': 'command_icons',        # 圖標資源文件夾
    'command_visible': True,                 # 命令是否可見
    'command_promoted': True,                # 命令是否提升顯示
}
```

**範例**:
```python
my_addin.add_command(
    'Export Active Project',
    ExportCommand,
    {
        'cmd_description': 'Exports all Fusion Documents in the currently active project',
        'cmd_id': 'export_cmd_1',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'Archive',
        'cmd_resources': 'command_icons',
        'command_visible': True,
        'command_promoted': True,
    }
)
```

##### `command_id_from_name(name)`

根據命令名稱返回完整的 `cmd_id`。

**參數**:
- `name` (str): 在選項中設置的 `cmd_id` 值

**返回**: 完整的 `cmd_id`（格式：`CompanyName_AppName_cmd_id`）

**範例**:
```python
full_cmd_id = my_addin.command_id_from_name('export_cmd_1')
# 返回: 'YourCompany_YourAppName_export_cmd_1'
```

##### `run_app()`

啟動 Add-in。

##### `stop_app()`

停止 Add-in 並清理所有創建的 UI 元素。

##### 偏好設定相關方法

```python
# 初始化偏好設定
my_addin.initialize_preferences(defaults, force=False)

# 獲取所有偏好設定
all_prefs = my_addin.get_all_preferences()

# 獲取特定群組的偏好設定
group_prefs = my_addin.get_group_preferences('group_name')

# 保存偏好設定
my_addin.save_preferences('group_name', new_prefs, merge=True)
```

**範例**:
```python
# 初始化偏好設定
defaults = {
    'output_path': '/Users/username/Desktop',
    'default_format': 'STEP',
    'preserve_structure': True
}
my_addin.initialize_preferences(defaults)

# 保存偏好設定
my_addin.save_preferences('ExportSettings', {
    'output_path': '/new/path',
    'default_format': 'IGES'
}, merge=True)

# 讀取偏好設定
prefs = my_addin.get_group_preferences('ExportSettings')
output_path = prefs.get('output_path', '/default/path')
```

##### 事件註冊方法

```python
# 註冊命令事件
my_addin.add_command_event('event_id', event_type, event_class)

# 註冊文檔事件
my_addin.add_document_event('event_id', event_type, event_class)

# 註冊工作空間事件
my_addin.add_workspace_event('event_id', 'workspace_name', event_class)

# 註冊自定義事件（帶線程）
my_addin.add_custom_event('event_id', event_class, auto_start=True)

# 註冊自定義事件（不帶線程）
my_addin.add_custom_event_no_thread('event_id', event_class)

# 註冊 Web 請求事件
my_addin.add_web_request_event('event_id', event_type, event_class)
```

---

### Fusion360CommandBase

繼承此類別來創建自定義命令。

#### 必須實現的方法

##### `on_create(command, inputs)`

命令創建時調用，用於設置命令的 UI 輸入項。

**參數**:
- `command`: `adsk.core.Command` 對象
- `inputs`: `adsk.core.CommandInputs` 對象

**範例**:
```python
def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
    # 添加字符串輸入
    inputs.addStringValueInput('output_folder', 'Output Folder:', '/path/to/folder')
    
    # 添加下拉選單
    dropdown = inputs.addDropDownCommandInput(
        'file_types_input', 
        'Export Types',
        adsk.core.DropDownStyles.CheckBoxDropDownStyle
    )
    dropdown.listItems.add('STEP', True)
    dropdown.listItems.add('IGES', False)
    
    # 添加布林值輸入（複選框）
    inputs.addBoolValueInput('preserve_structure', 'Preserve folder structure?', True, '', True)
```

##### `on_execute(command, inputs, args, input_values)`

命令執行時調用，處理命令邏輯。

**參數**:
- `command`: `adsk.core.Command` 對象
- `inputs`: `adsk.core.CommandInputs` 對象
- `args`: 命令參數
- `input_values`: 字典，包含所有輸入項的值

**範例**:
```python
def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, 
               args, input_values):
    output_folder = input_values['output_folder']
    preserve_structure = input_values['preserve_structure']
    
    # 執行導出邏輯
    export_files(output_folder, preserve_structure)
```

##### `on_input_changed(command, inputs, changed_input, input_values)`

當輸入項改變時調用，用於動態更新 UI。

**參數**:
- `command`: `adsk.core.Command` 對象
- `inputs`: `adsk.core.CommandInputs` 對象
- `changed_input`: 改變的輸入項
- `input_values`: 當前所有輸入項的值

**範例**:
```python
def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs,
                     changed_input, input_values):
    if changed_input.id == 'name_option_id':
        # 根據選擇的名稱選項顯示/隱藏版本號輸入
        version_input = inputs.itemById('write_version')
        if changed_input.selectedItem.name == 'Document Name':
            version_input.isVisible = True
        else:
            version_input.isVisible = False
```

#### 其他可用方法

- `on_preview(command, inputs, args, input_values)`: 預覽時調用
- `on_activate(command, inputs, args, input_values)`: 命令激活時調用
- `on_deactivate(command, inputs, args, input_values)`: 命令停用時調用
- `on_destroy(command, inputs, reason, input_values)`: 命令銷毀時調用

---

### AppObjects

`AppObjects` 類別封裝了許多常用的 Fusion 360 應用對象，方便快速訪問。

#### 初始化

```python
from apper import AppObjects

ao = AppObjects()
```

#### 常用屬性

##### `document`

當前活動文檔（`adsk.fusion.Document`）。

```python
ao = AppObjects()
doc = ao.document
if doc:
    print(f"Document name: {doc.name}")
```

##### `design`

當前活動設計（`adsk.fusion.Design`）。

```python
ao = AppObjects()
design = ao.design
if design:
    root_comp = design.rootComponent
```

##### `root_comp`

根組件（`adsk.fusion.Component`）。

```python
ao = AppObjects()
root_comp = ao.root_comp
bodies = root_comp.bRepBodies
```

##### `product`

產品對象（`adsk.core.Product`）。

```python
ao = AppObjects()
product = ao.product
```

##### `export_manager`

導出管理器（`adsk.fusion.ExportManager`）。

```python
ao = AppObjects()
export_mgr = ao.export_manager

# 創建 STEP 導出選項
step_options = export_mgr.createSTEPExportOptions('/path/to/output.step')
export_mgr.execute(step_options)
```

##### `ui`

用戶界面對象（`adsk.core.UserInterface`）。

```python
ao = AppObjects()
ui = ao.ui

# 顯示訊息框
ui.messageBox('Export completed!')

# 創建文件夾選擇對話框
folder_dialog = ui.createFolderDialog()
folder_dialog.title = 'Select Output Folder'
result = folder_dialog.showDialog()
if result == adsk.core.DialogResults.DialogOK:
    selected_folder = folder_dialog.folder
```

##### `app`

應用程序對象（`adsk.core.Application`）。

```python
ao = AppObjects()
app = ao.app

# 獲取所有專案
projects = app.data.dataProjects

# 獲取活動專案
active_project = app.data.activeProject
```

##### `cam`

CAM 對象（`adsk.cam.CAM`），僅在 CAM 環境中可用。

```python
ao = AppObjects()
cam = ao.cam
if cam:
    # 處理 CAM 相關操作
    pass
```

##### `f_units_manager`

Fusion 單位管理器（`adsk.fusion.FusionUnitsManager`），僅在設計環境中可用。

```python
ao = AppObjects()
units_mgr = ao.f_units_manager
if units_mgr:
    # 處理單位相關操作
    pass
```

---

### 工具函數

#### `get_default_dir(app_name)`

在用戶主目錄中創建並返回應用程式專用的目錄。

**參數**:
- `app_name` (str): 應用程式名稱

**返回**: 目錄路徑（字符串）

**範例**:
```python
import apper

default_dir = apper.get_default_dir('BackupTool')
# 返回類似: '/Users/username/BackupTool'
```

#### `get_log_file(app_name)`

獲取預設日誌文件的路徑。

**參數**:
- `app_name` (str): 應用程式名稱

**返回**: 日誌文件路徑

#### `get_settings_file(app_name)`

創建（或獲取）應用程式目錄中的設定文件名。

**參數**:
- `app_name` (str): 應用程式名稱

**返回**: 設定文件路徑

#### `read_settings(app_name)` / `write_settings(app_name, settings)`

讀取/寫入設定文件。

**範例**:
```python
import apper

# 讀取設定
settings = apper.read_settings('BackupTool')

# 寫入設定
new_settings = {'output_path': '/path/to/output', 'format': 'STEP'}
apper.write_settings('BackupTool', new_settings)
```

#### `item_id(item, group_name)` / `get_item_by_id(item_id, app_name)`

為 Fusion 360 對象分配或獲取唯一標識符（UUID）。

**範例**:
```python
import apper

ao = AppObjects()
body = ao.root_comp.bRepBodies.item(0)

# 分配 ID
unique_id = apper.item_id(body, 'BackupTool')

# 稍後根據 ID 獲取對象
retrieved_body = apper.get_item_by_id(unique_id, 'BackupTool')
```

#### `get_a_uuid()`

生成一個 base64 格式的 UUID。

**返回**: UUID 字符串

#### `open_doc(data_file)`

打開一個數據文件。

**參數**:
- `data_file`: `adsk.core.DataFile` 對象

**範例**:
```python
import apper

# 從專案中獲取文件
project = ao.app.data.activeProject
data_file = project.rootFolder.dataFiles.item(0)

# 打開文件
document = apper.open_doc(data_file)
```

#### `import_dxf(dxf_file, component, plane, is_single_sketch_result=False)`

導入 DXF 文件，每個圖層創建一個草圖。

**參數**:
- `dxf_file` (str): DXF 文件的完整路徑
- `component`: 目標組件
- `plane`: 導入平面（`ConstructionPlane` 或 `BRepFace`）
- `is_single_sketch_result` (bool): 如果為 True，將所有圖層合併為單一草圖

**返回**: 創建的草圖集合（`ObjectCollection`）

#### `start_group()` / `end_group(start_index)`

開始/結束時間軸群組。

**範例**:
```python
import apper

# 開始群組
start_idx = apper.start_group()

# ... 執行多個操作 ...

# 結束群組
apper.end_group(start_idx)
```

#### `lib_import`（用於導入第三方庫）

```python
from contextlib import ContextDecorator
import sys
import os

class lib_import(ContextDecorator):
    def __init__(self, app_path, library_folder='lib'):
        self.path = os.path.join(app_path, library_folder)
    
    def __enter__(self):
        sys.path.insert(0, self.path)
        return self
    
    def __exit__(self, *exc):
        if self.path in sys.path:
            sys.path.remove(self.path)
        return False

# 使用
@lib_import(SCRIPT_DIRECTORY)
def my_function():
    import requests  # 從 lib 目錄導入
    # ...
```

---

## 🚀 開發流程

### 1. 創建基本 Add-in（使用 Apper）

```python
# BackupTool.py
import apper
import config
from .commands.MyCommand import MyCommand

my_addin = apper.FusionApp(config.app_name, config.company_name, False)

my_addin.add_command(
    'My Command',
    MyCommand,
    {
        'cmd_id': 'my_cmd',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'MyPanel',
        'cmd_resources': 'command_icons',
        'command_visible': True,
        'command_promoted': True,
    }
)

def run(context):
    my_addin.run_app()

def stop(context):
    my_addin.stop_app()
```

### 2. 創建命令類

```python
# commands/MyCommand.py
import apper
from apper import AppObjects
import adsk.core

class MyCommand(apper.Fusion360CommandBase):
    def on_create(self, command, inputs):
        ao = AppObjects()
        inputs.addStringValueInput('input_id', 'Input Label', 'default')
    
    def on_execute(self, command, inputs, args, input_values):
        ao = AppObjects()
        value = input_values['input_id']
        ao.ui.messageBox(f'You entered: {value}')
```

### 3. 完整命令範例

```python
import apper
from apper import AppObjects
import adsk.core
import adsk.fusion

class MyExportCommand(apper.Fusion360CommandBase):
    
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        """創建命令 UI"""
        ao = AppObjects()
        
        # 添加輸出路徑輸入
        default_dir = apper.get_default_dir('MyApp')
        inputs.addStringValueInput('output_folder', 'Output Folder:', default_dir)
        
        # 添加文件類型選擇
        file_types = inputs.addDropDownCommandInput(
            'file_types', 
            'Export Types',
            adsk.core.DropDownStyles.CheckBoxDropDownStyle
        )
        file_types.listItems.add('STEP', True)
        file_types.listItems.add('IGES', False)
        file_types.listItems.add('STL', False)
    
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs,
                   args, input_values):
        """執行命令邏輯"""
        ao = AppObjects()
        
        # 獲取輸入值
        output_folder = input_values['output_folder']
        file_types = inputs.itemById('file_types').listItems
        
        # 檢查是否有活動文檔
        if not ao.document:
            ao.ui.messageBox('Please open a document first.')
            return
        
        # 執行導出
        export_mgr = ao.export_manager
        
        # 根據選擇的文件類型導出
        if file_types.item(0).isSelected:  # STEP
            step_options = export_mgr.createSTEPExportOptions(
                output_folder + ao.document.name + '.step'
            )
            export_mgr.execute(step_options)
        
        if file_types.item(1).isSelected:  # IGES
            iges_options = export_mgr.createIGESExportOptions(
                output_folder + ao.document.name + '.igs'
            )
            export_mgr.execute(iges_options)
        
        ao.ui.messageBox('Export completed!')
```

### 4. 使用專案和文件夾

```python
ao = AppObjects()
app = ao.app

# 獲取所有專案
all_projects = app.data.dataProjects

# 遍歷專案
for project in all_projects:
    print(f"Project: {project.name}")
    
    # 獲取專案根文件夾
    root_folder = project.rootFolder
    
    # 遍歷文件夾
    for i in range(root_folder.dataFolders.count):
        folder = root_folder.dataFolders.item(i)
        print(f"  Folder: {folder.name}")
    
    # 遍歷文件
    for i in range(root_folder.dataFiles.count):
        data_file = root_folder.dataFiles.item(i)
        if data_file.fileExtension == 'f3d':
            print(f"  File: {data_file.name}")
```

### 5. 測試和調試

- 在 Fusion 360 中載入 Add-in
- 檢查錯誤訊息
- 使用 `apper.FusionApp(..., debug=True)` 啟用調試模式

---

## 📝 常見問題

### Q: 如何獲取當前活動文檔？
```python
ao = AppObjects()
document = ao.document
```

### Q: 如何創建文件夾選擇對話框？
```python
ao = AppObjects()
folder_dialog = ao.ui.createFolderDialog()
folder_dialog.title = 'Select Folder'
result = folder_dialog.showDialog()
if result == adsk.core.DialogResults.DialogOK:
    folder = folder_dialog.folder
```

### Q: 如何遍歷專案中的所有文件？
```python
ao = AppObjects()
project = ao.app.data.activeProject
root_folder = project.rootFolder

def iterate_folder(folder):
    # 遍歷文件
    for i in range(folder.dataFiles.count):
        file = folder.dataFiles.item(i)
        if file.fileExtension == 'f3d':
            print(file.name)
    
    # 遞歸遍歷子文件夾
    for i in range(folder.dataFolders.count):
        subfolder = folder.dataFolders.item(i)
        iterate_folder(subfolder)

iterate_folder(root_folder)
```

### Q: 如何導出當前文檔？
```python
ao = AppObjects()
export_mgr = ao.export_manager
step_options = export_mgr.createSTEPExportOptions('/path/to/output.step')
export_mgr.execute(step_options)
```

### Q: 如何打開文件並確保關閉？
```python
document = None
try:
    document = app.documents.open(data_file, True)
    # ... 執行操作
finally:
    if document:
        document.close(False)  # False = 不保存更改
```

---

## ⚠️ 注意事項

1. **記憶體管理**: 打開的文件要記得關閉，避免記憶體洩漏
   ```python
   try:
       document = app.documents.open(data_file, True)
       # ... 執行操作 ...
   finally:
       if document:
           document.close(False)
   ```

2. **錯誤處理**: 始終使用 try-except 處理可能的異常
   ```python
   try:
       ao = AppObjects()
       design = ao.design
       if design:
           # 執行操作
   except Exception as e:
       ao.ui.messageBox(f'Error: {str(e)}')
   ```

3. **對象有效性**: 在使用 Fusion 360 對象前檢查是否為 None
   ```python
   ao = AppObjects()
   if ao.document and ao.design:
       # 安全使用對象
   ```

4. **線程安全**: Fusion 360 API 不是線程安全的，所有操作應在主線程執行

---

## 🔗 相關資源

- **Apper 官方文檔**: https://apper.readthedocs.io/en/latest/apper.html
- **範例程式庫**: https://github.com/tapnair/Fusion360APIClass
- **Apper 源碼**: https://github.com/tapnair/apper
- **Fusion 360 API 文檔**: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A

---

## 📌 快速備忘錄

### 命令選項常用值

```python
# 工作空間
'FusionSolidEnvironment'      # 設計環境
'CAMEnvironment'              # CAM 環境
'DrawingEnvironment'          # 工程圖環境

# 下拉選單樣式
adsk.core.DropDownStyles.TextListDropDownStyle      # 單選下拉
adsk.core.DropDownStyles.CheckBoxDropDownStyle     # 複選下拉

# 對話框結果
adsk.core.DialogResults.DialogOK
adsk.core.DialogResults.DialogCancel

# 訊息框類型
adsk.core.MessageBoxButtonTypes.OKButtonType
adsk.core.MessageBoxIconTypes.InformationIconType
```

### 文件擴展名
- `.f3d` - Fusion 360 設計文件
- `.step` / `.stp` - STEP 文件
- `.iges` / `.igs` - IGES 文件
- `.stl` - STL 文件
- `.sat` - SAT 文件

---

**最後更新**: 2024年  
**維護者**: Fusion360Tools 開發團隊
