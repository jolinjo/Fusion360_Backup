# Project-Archiver
The archiver script will open all Fusion 360 3D data in a project and export it as STEP to a local location of your choosing. 

[How to install](#How-to-install)  
[How to use](#How-to-use)  
[Updates & Improvements / 更新與改進](#Updates)  
[For Developers](#For-Developers)

----

### How to install<a name="How-to-install"></a>
1. Click the latest link and download the [latest distribution](https://github.com/tapnair/Project-Archiver/blob/master/dist/Project-Archiver-2.0.1.zip)

*Note you should download from the link above.  The regular git downloads won't get the apper submodule*

2. Unzip the archive to a permanent location on your computer

**For some reason this zip file can get corrupted by github direct download.
If you are unable to unzip the file, you should just clone the entire repo or download a zip of the entire repo.
Then you can navigate to the /dist folder to find the actual correct zip file.
Extract that file to your computer and continue below.**

### Fusion 360  

1. Launch Fusion 360.
2. On the main toolbar click the **Scripts and Addins** button in the **Addins** Pane

	![](Project-Archiver/resources/scripts-addins_button.png)

3. Select the **Addins tab** and click the "add"  

    ![](Project-Archiver/resources/scripts-addins.png)

4. Browse to the **Project-Archiver** sub-folder in the unzipped folder

   ![](Project-Archiver/resources/pick_add_in.png)

5. Select the addin in the list and click run.  
6. Dismiss the Addins dialog.  
7. Click the ProjectArchiver Tab and you should see **Archive** Panel and command.

	![](Project-Archiver/resources/button.png)

----

### How to use<a name="How-to-use"></a>

1. **Select Project / 選擇專案** (New Feature / 新功能)
   - Use the **Select Project** dropdown menu to choose which project you want to archive.
   - 使用「選擇專案」下拉選單選擇要備份的專案。
   - By default, the currently active project is selected.
   - 預設情況下，會選擇當前活動的專案。

2. **Choose Output Path / 選擇輸出路徑**
   - **Option 1**: Click the **Browse Folder** button to open a folder selection dialog and choose your output directory.
   - **選項 1**: 點擊「瀏覽文件夾」按鈕打開文件夾選擇對話框，選擇輸出目錄。
   - **Option 2**: Manually type a path into the **Output Folder** field.
   - **選項 2**: 在「輸出路徑」欄位中手動輸入路徑。
   - For OSX this might be: **/Users/*username*/Desktop/Test/**
   - For Windows this might be something like **C:\Test**

3. **Select Export Types / 選擇導出類型**
   - Under **Export Types** select the different file types you want to export. You can select multiple types.
   - 在「導出類型」下選擇要導出的不同文件類型。可以選擇多種類型。

4. **File Name Options / 文件名選項**
   - File Name Options allow you to specify the naming convention for output files.
   - 文件名選項允許您指定輸出文件的命名規則。
   - If you select 'Document Name' you can choose whether or not to append the version number to the file name.
   - 如果選擇「文件名」，可以選擇是否在文件名中附加版本號。

5. **Preserve Folder Structure / 保留文件夾結構** (Optional / 可選)
   - Check "Preserve folder structure?" if you want to maintain the original folder hierarchy in the output.
   - 如果想在輸出中保留原始文件夾層次結構，請勾選「保留文件夾結構？」。

6. **Click OK / 點擊確定**
   - Click **OK** to start the export process.
   - 點擊「確定」開始導出過程。

Fusion will open and export each 3D design. Depending on the size of design and bandwidth this can take some time. 
Fusion 360 will be busy for the duration of the script running, so it would be advisable to run this on a dedicated machine that you can leav to run for some time. 

### Updates & Improvements / 更新與改進<a name="Updates"></a>

This fork includes several important improvements and bug fixes:

此版本包含以下重要改進和錯誤修復：

#### ✨ New Features / 新功能

1. **Project Selection / 專案選擇功能**
   - **English**: Added a project dropdown menu that allows users to select which project to archive, instead of only using the active project.
   - **中文**: 新增專案下拉選單，允許用戶選擇要備份的專案，不再僅限於當前活動專案。
   - Users can now choose from all available projects in the dropdown menu.
   - 用戶現在可以從下拉選單中選擇所有可用的專案。

2. **Folder Selection Dialog / 文件夾選擇對話框**
   - **English**: Added a "Browse Folder" button that opens a system folder selection dialog, making it easier to choose the output path without manually typing the full path.
   - **中文**: 新增「瀏覽文件夾」按鈕，可打開系統文件夾選擇對話框，無需手動輸入完整路徑即可選擇輸出路徑。
   - The dialog remembers the last selected path and provides a more user-friendly way to select output directories.
   - 對話框會記住上次選擇的路徑，提供更友好的方式選擇輸出目錄。

#### 🐛 Bug Fixes / 錯誤修復

1. **Memory Leak Fix / 記憶體洩漏修復**
   - **English**: Fixed a critical memory issue where opened files were not automatically closed after export. This caused memory exhaustion when processing large numbers of files, leading to program crashes.
   - **中文**: 修復了關鍵的記憶體問題：導出後文件不會自動關閉。處理大量文件時會導致記憶體耗盡，造成程序崩潰。
   - Files are now automatically closed after each export operation using a `try-finally` block to ensure proper cleanup.
   - 現在每個文件導出後會自動關閉，使用 `try-finally` 區塊確保正確清理。

2. **Module Import Fix / 模組導入修復**
   - **English**: Fixed the `ImportError: cannot import name 'AppObjects' from 'apper'` error by properly initializing the apper submodule and adjusting the path configuration in `startup.py`.
   - **中文**: 修復了 `ImportError: cannot import name 'AppObjects' from 'apper'` 錯誤，通過正確初始化 apper 子模組並調整 `startup.py` 中的路徑配置。
   - The apper submodule is now properly initialized and the import paths are correctly configured.
   - apper 子模組現在已正確初始化，導入路徑已正確配置。

#### 📝 Technical Details / 技術細節

- **Auto-close Implementation**: Each file is closed immediately after export using `document.close(False)` in a `finally` block to ensure cleanup even if errors occur.
- **自動關閉實現**: 每個文件在導出後立即使用 `document.close(False)` 關閉，放在 `finally` 區塊中確保即使發生錯誤也能正確清理。

- **Project Selection**: The project selection uses `ao.app.data.dataProjects` to list all available projects and allows users to select any project for archiving.
- **專案選擇**: 專案選擇功能使用 `ao.app.data.dataProjects` 列出所有可用專案，允許用戶選擇任何專案進行備份。

- **Folder Dialog**: Uses Fusion 360's `ui.createFolderDialog()` API to provide native folder selection functionality.
- **文件夾對話框**: 使用 Fusion 360 的 `ui.createFolderDialog()` API 提供原生文件夾選擇功能。

### For Developers<a name="For-Developers"></a>
Clone the repo

Update the apper submodule by browsing to the 'Project-Archiver' sub directory in the unzipped directory and executing:

    git submodule add https://github.com/tapnair/apper
   
## License
Samples are licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.

## Written by

Written by [Patrick Rainsberry](https://twitter.com/prrainsberry) <br /> (Autodesk Fusion 360 Product Manager)

See more useful [Fusion 360 Utilities](https://tapnair.github.io/index.html)


Analytics
[![Analytics](https://ga-beacon.appspot.com/UA-41076924-3/project-archiver)](https://github.com/igrigorik/ga-beacon)



