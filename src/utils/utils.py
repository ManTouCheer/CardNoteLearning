import os


def get_file_list(path):
    """获取指定目录下的所有文件路径列表"""
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith('.txt'):
                continue
            file_list.append(os.path.join(root, file))
    return file_list