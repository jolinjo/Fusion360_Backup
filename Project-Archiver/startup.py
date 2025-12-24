import os
import sys


def _remove_from_path(name):
    if name in sys.path:
        sys.path.remove(name)
        _remove_from_path(name)


def get_app_path(app_file):
    app_path = os.path.dirname(app_file)
    return app_path


def _remove_paths(app_path):
    _remove_from_path(app_path)
    apper_path = os.path.join(app_path, 'apper')
    _remove_from_path(apper_path)
    apper_module_path = os.path.join(apper_path, 'apper')
    _remove_from_path(apper_module_path)
    _remove_from_path(os.path.join(app_path, 'lib'))


def _add_paths(app_path):
    sys.path.insert(0, app_path)
    # 添加 apper/apper 目錄到路徑，因為 apper 模組在 apper/apper/ 中
    # 這樣 import apper 就能找到 apper/apper/__init__.py
    apper_path = os.path.join(app_path, 'apper')
    apper_module_path = os.path.join(apper_path, 'apper')
    if os.path.exists(apper_module_path):
        # 將 apper/apper 的父目錄添加到路徑，這樣 import apper 能找到 apper/apper/__init__.py
        sys.path.insert(0, apper_path)
    else:
        # 如果 apper/apper 不存在，仍然添加 apper 目錄
        sys.path.insert(0, apper_path)
    sys.path.insert(0, os.path.join(app_path, 'lib'))


def setup_app(app_file):
    app_path = get_app_path(app_file)

    _remove_paths(app_path)

    if sys.modules.get('apper', False):
        # TODO possibly add a message to inform user that there is a potential conflict
        # Do some kind of version check?
        del sys.modules['apper']

    _add_paths(app_path)


def cleanup_app(app_file):
    app_path = get_app_path(app_file)
    _remove_paths(app_path)

