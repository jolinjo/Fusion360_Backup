# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Copyright (c) 2020 by Patrick Rainsberry.                                   ~
#  Modified by Jason.Lin                                                       ~
#  :license: Apache2, see LICENSE for more details.                            ~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  SampleCommand2.py                                                           ~
#  This file is a component of BackupTool (Fusion360Tools).                  ~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

import adsk.core
import adsk.fusion
import adsk.cam

import apper
from apper import AppObjects

import config

SKIPPED_FILES = []
FAILED_FILES = []  # 追蹤失敗的檔案，格式: [{'name': '文件名', 'path': '完整路徑', 'error': '錯誤信息'}]


def export_folder(root_folder, output_folder, file_types, write_version, name_option, folder_preserve, folder_path="", project_name=""):
    global FAILED_FILES
    ao = AppObjects()
    app = adsk.core.Application.get()

    # 先將文件夾和文件轉換為列表，避免在迭代過程中對象狀態改變
    try:
        folders_list = []
        for i in range(root_folder.dataFolders.count):
            try:
                folder = root_folder.dataFolders.item(i)
                if folder is not None:
                    folders_list.append(folder)
            except:
                continue
        
        for folder in folders_list:
            # 構建當前文件夾的路徑
            current_folder_path = folder_path + "/" + folder.name if folder_path else folder.name

            if folder_preserve:
                new_folder = os.path.join(output_folder, folder.name, "")

                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)
            else:
                new_folder = output_folder

            export_folder(folder, new_folder, file_types, write_version, name_option, folder_preserve, current_folder_path, project_name)
    except Exception as e:
        # 記錄文件夾迭代錯誤
        FAILED_FILES.append({
            'name': 'Folder iteration error',
            'path': folder_path if folder_path else project_name,
            'error': 'Error iterating folders: {}'.format(str(e))
        })
    
    # 先將文件列表轉換為列表，避免在迭代過程中對象狀態改變
    try:
        files_list = []
        for i in range(root_folder.dataFiles.count):
            try:
                file = root_folder.dataFiles.item(i)
                if file is not None:
                    files_list.append(file)
            except:
                continue
        
        for file in files_list:
            try:
                # 驗證文件對象是否有效
                if file is None:
                    continue
                    
                file_ext = file.fileExtension
                if file_ext != "f3d":
                    continue
            except Exception as e:
                # 文件對象無效，跳過
                continue
            
            if file_ext == "f3d":
                # 構建文件的完整路徑（專案名稱 + 文件夾路徑 + 文件名）
                try:
                    file_name = file.name
                except:
                    file_name = "Unknown"
                    
                if folder_path:
                    file_path = folder_path + "/" + file_name
                else:
                    file_path = file_name
                
                # 如果有專案名稱，添加到路徑開頭
                if project_name:
                    file_path = project_name + "/" + file_path
                
                document = open_doc(file)
                if document is not None:
                    try:
                        output_name = get_name(write_version, name_option)
                        export_active_doc(output_folder, file_types, output_name)
                        
                    except ValueError as e:
                        # 記錄失敗的檔案
                        FAILED_FILES.append({
                            'name': file_name,
                            'path': file_path,
                            'error': str(e)
                        })
                    except AttributeError as e:
                        # 記錄失敗的檔案
                        FAILED_FILES.append({
                            'name': file_name,
                            'path': file_path,
                            'error': str(e)
                        })
                        # 確保在異常情況下也能關閉文件
                        try:
                            if not document.isSaved:
                                document.close(False)
                            else:
                                document.close(False)
                        except:
                            pass
                        break
                    except Exception as e:
                        # 記錄失敗的檔案
                        FAILED_FILES.append({
                            'name': file_name,
                            'path': file_path,
                            'error': str(e)
                        })
                    finally:
                        # 無論成功或失敗，都關閉文件以釋放記憶體
                        try:
                            if document is not None:
                                # 不保存更改，直接關閉（因為我們只是導出，不需要修改原文件）
                                document.close(False)
                        except:
                            pass
                else:
                    # 無法打開文件，記錄為失敗
                    FAILED_FILES.append({
                        'name': file_name,
                        'path': file_path,
                        'error': 'Failed to open file'
                    })
    except Exception as e:
        # 記錄文件迭代錯誤
        try:
            folder_name = folder_path if folder_path else project_name
        except:
            folder_name = "Unknown"
        FAILED_FILES.append({
            'name': 'File iteration error',
            'path': folder_name,
            'error': 'Error iterating files: {}'.format(str(e))
        })


def open_doc(data_file):
    app = adsk.core.Application.get()

    try:
        document = app.documents.open(data_file, True)
        if document is not None:
            document.activate()
        return document
    except:
        pass
        # TODO add handling
        return None


def export_active_doc(folder, file_types, output_name):
    global SKIPPED_FILES

    ao = AppObjects()
    export_mgr = ao.export_manager

    export_functions = [export_mgr.createIGESExportOptions,
                        export_mgr.createSTEPExportOptions,
                        export_mgr.createSATExportOptions,
                        export_mgr.createSMTExportOptions,
                        export_mgr.createFusionArchiveExportOptions,
                        export_mgr.createSTLExportOptions]
    export_extensions = ['.igs', '.step', '.sat', '.smt', '.f3d', '.stl']

    for i in range(file_types.count-2):

        if file_types.item(i).isSelected:
            export_name = folder + output_name + export_extensions[i]
            export_name = dup_check(export_name)
            export_options = export_functions[i](export_name)
            export_mgr.execute(export_options)

    if file_types.item(file_types.count - 2).isSelected:

        if ao.document.allDocumentReferences.count > 0:
            SKIPPED_FILES.append(ao.document.name)

        else:
            export_name = folder + output_name + '.f3d'
            export_name = dup_check(export_name)
            export_options = export_mgr.createFusionArchiveExportOptions(export_name)
            export_mgr.execute(export_options)

    if file_types.item(file_types.count - 1).isSelected:
        stl_export_name = folder + output_name + '.stl'
        stl_options = export_mgr.createSTLExportOptions(ao.design.rootComponent, stl_export_name)
        export_mgr.execute(stl_options)


def dup_check(name):
    if os.path.exists(name):
        base, ext = os.path.splitext(name)
        base += '-dup'
        name = base + ext
        dup_check(name)
    return name


def get_name(write_version, option):
    ao = AppObjects()
    output_name = ''

    if option == 'Document Name':

        doc_name = ao.app.activeDocument.name

        if not write_version:
            doc_name = doc_name[:doc_name.rfind(' v')]
        output_name = doc_name

    elif option == 'Description':
        output_name = ao.root_comp.description

    elif option == 'Part Number':
        output_name = ao.root_comp.partNumber

    else:
        raise ValueError('Something strange happened')

    return output_name


def update_name_inputs(command_inputs, selection):
    command_inputs.itemById('write_version').isVisible = False

    if selection == 'Document Name':
        command_inputs.itemById('write_version').isVisible = True


class ExportCommand(apper.Fusion360CommandBase):

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs,
                         changed_input, input_values):
        if changed_input.id == 'name_option_id':
            update_name_inputs(inputs, changed_input.selectedItem.name)
        elif changed_input.id == 'browse_folder_button':
            # 用戶點擊了瀏覽文件夾按鈕
            ao = AppObjects()
            
            # 立即重置按鈕狀態（因為它只是用來觸發對話框）
            browse_button = inputs.itemById('browse_folder_button')
            if browse_button:
                browse_button.value = False
            
            # 創建文件夾選擇對話框
            folder_dialog = ao.ui.createFolderDialog()
            folder_dialog.title = 'Select Output Folder'
            
            # 設置初始目錄（如果已有路徑）
            current_folder = input_values.get('output_folder', '')
            if current_folder and os.path.exists(current_folder):
                folder_dialog.initialDirectory = current_folder
            elif current_folder:
                # 如果路徑不存在，嘗試使用父目錄
                parent_dir = os.path.dirname(current_folder)
                if parent_dir and os.path.exists(parent_dir):
                    folder_dialog.initialDirectory = parent_dir
            else:
                # 如果沒有當前路徑，使用默認目錄
                default_dir = apper.get_default_dir(config.app_name)
                if default_dir and os.path.exists(default_dir):
                    folder_dialog.initialDirectory = default_dir
            
            # 顯示對話框
            dialog_result = folder_dialog.showDialog()
            
            # 檢查用戶是否選擇了文件夾
            if dialog_result == adsk.core.DialogResults.DialogOK:
                selected_folder = folder_dialog.folder
                # 確保路徑以路徑分隔符結尾
                if not selected_folder.endswith(os.path.sep):
                    selected_folder += os.path.sep
                # 更新輸出路徑輸入框
                output_folder_input = inputs.itemById('output_folder')
                if output_folder_input:
                    output_folder_input.value = selected_folder

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        global SKIPPED_FILES
        ao = AppObjects()

        output_folder = input_values['output_folder']
        folder_preserve = input_values['folder_preserve_id']

        # TODO broken?????
        file_types = inputs.itemById('file_types_input').listItems

        write_version = input_values['write_version']
        name_option = input_values['name_option_id']
        
        # 獲取選擇的專案（如果用戶選擇了專案）
        project_dropdown = inputs.itemById('project_selection_id')
        if project_dropdown is not None and project_dropdown.selectedItem is not None:
            # 從選中的專案名稱獲取專案對象
            selected_project_name = project_dropdown.selectedItem.name
            selected_project = None
            for project in ao.app.data.dataProjects:
                if project.name == selected_project_name:
                    selected_project = project
                    break
            
            if selected_project is not None:
                root_folder = selected_project.rootFolder
            else:
                # 如果找不到選中的專案，使用活動專案
                root_folder = ao.app.data.activeProject.rootFolder
        else:
            # 如果沒有專案選擇輸入，使用活動專案（向後兼容）
            root_folder = ao.app.data.activeProject.rootFolder

        # Make sure we have a folder not a file
        if not output_folder.endswith(os.path.sep):
            output_folder += os.path.sep

        # Create the base folder for this output if doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 獲取專案名稱用於顯示路徑
        project_name = ""
        if selected_project is not None:
            project_name = selected_project.name
        elif ao.app.data.activeProject is not None:
            project_name = ao.app.data.activeProject.name
        
        export_folder(root_folder, output_folder, file_types, write_version, name_option, folder_preserve, "", project_name)

        # 構建結果訊息
        result_message = ""
        
        # 檢查是否有失敗的檔案
        if len(FAILED_FILES) > 0:
            result_message = "Export Completed with Errors / 導出完成，但有錯誤：\n\n"
            result_message += "Failed Files / 失敗的檔案 ({})：\n".format(len(FAILED_FILES))
            result_message += "失敗檔案數量：{}\n\n".format(len(FAILED_FILES))
            
            for i, failed_file in enumerate(FAILED_FILES, 1):
                result_message += "{}. {}\n".format(i, failed_file['name'])
                result_message += "   Path / 路徑: {}\n".format(failed_file['path'])
                result_message += "   Error / 錯誤: {}\n\n".format(failed_file['error'])
        else:
            # 沒有失敗的檔案，顯示成功訊息
            result_message = "Export Completed Successfully! / 導出成功完成！\n\n"
            result_message += "All files have been exported successfully. / 所有檔案已成功導出。\n"
        
        # 檢查是否有跳過的檔案（F3D 格式，因為有外部參考）
        if len(SKIPPED_FILES) > 0:
            if len(FAILED_FILES) > 0:
                result_message += "\n"
            result_message += "Skipped Files (F3D with external references) / 跳過的檔案（F3D 格式，包含外部參考）：\n"
            result_message += "跳過的檔案數量：{}\n\n".format(len(SKIPPED_FILES))
            for i, skipped_file in enumerate(SKIPPED_FILES, 1):
                result_message += "{}. {}\n".format(i, skipped_file)
        
        # 顯示結果訊息
        ao.ui.messageBox(result_message)

        close_command = ao.ui.commandDefinitions.itemById(self.fusion_app.command_id_from_name(config.close_cmd_id))
        close_command.execute()

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        global SKIPPED_FILES, FAILED_FILES
        SKIPPED_FILES.clear()
        FAILED_FILES.clear()
        default_dir = apper.get_default_dir(config.app_name)
        
        ao = AppObjects()
        
        # 添加專案選擇下拉選單
        project_dropdown = inputs.addDropDownCommandInput('project_selection_id', 'Select Project',
                                                          adsk.core.DropDownStyles.TextListDropDownStyle)
        project_list = project_dropdown.listItems
        
        # 獲取所有可用的專案
        active_project_name = None
        if ao.app.data.activeProject is not None:
            active_project_name = ao.app.data.activeProject.name
        
        # 添加所有專案到下拉選單
        for project in ao.app.data.dataProjects:
            is_selected = (project.name == active_project_name)
            project_list.add(project.name, is_selected)

        # 添加輸出路徑輸入框
        inputs.addStringValueInput('output_folder', 'Output Folder:', default_dir)
        
        # 添加瀏覽文件夾按鈕（使用 BoolValueInput 作為按鈕觸發器）
        browse_button = inputs.addBoolValueInput('browse_folder_button', 'Browse Folder', False, '', False)
        browse_button.tooltip = 'Click to browse and select output folder'

        drop_input_list = inputs.addDropDownCommandInput('file_types_input', 'Export Types',
                                                         adsk.core.DropDownStyles.CheckBoxDropDownStyle)
        drop_input_list = drop_input_list.listItems
        drop_input_list.add('IGES', False)
        drop_input_list.add('STEP', True)
        drop_input_list.add('SAT', False)
        drop_input_list.add('SMT', False)
        drop_input_list.add('F3D', False)
        drop_input_list.add('STL', False)

        name_option_group = inputs.addDropDownCommandInput('name_option_id', 'File Name Option',
                                                                   adsk.core.DropDownStyles.TextListDropDownStyle)
        name_option_group.listItems.add('Document Name', True)
        name_option_group.listItems.add('Description', False)
        name_option_group.listItems.add('Part Number', False)
        name_option_group.isVisible = True

        preserve_input = inputs.addBoolValueInput('folder_preserve_id', 'Preserve folder structure?', True, '', True)
        preserve_input.isVisible = True

        version_input = inputs.addBoolValueInput('write_version', 'Write versions to output file names?', True, '', False)
        version_input.isVisible = False

        update_name_inputs(inputs, 'Document Name')
