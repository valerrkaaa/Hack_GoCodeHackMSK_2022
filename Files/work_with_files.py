import os


def get_root_dir():
    root_directory_name = 'Hack_GoCodeHackMSK_2022'

    path = os.getcwd()
    dir_name = None
    while dir_name != '':
        path, dir_name = os.path.split(path)
        if dir_name == root_directory_name:
            return os.path.join(path, dir_name)
    raise Exception(f'В пути проекта не найдено корневой папки с именем {root_directory_name}')


def get_full_path(filename):
    return os.path.join(get_root_dir(), filename)


def get_new_pair_of_files():
    folder_path = get_full_path('Files\\NewFiles')
    for _, _, file_list1 in os.walk(folder_path):
        for file1 in file_list1:
            for _, _, file_list2 in os.walk(folder_path):
                for file2 in file_list2:
                    if os.path.dirname(file1) == os.path.dirname(file2):
                        for _, _, file_list3 in os.walk(folder_path):
                            for file3 in file_list2:
                                if os.path.dirname(file1) == os.path.dirname(file2) == os.path.dirname(file3):
                                    if file1 != file2 and file1 != file3 and file2 != file3:
                                        return os.path.join(folder_path, file1), \
                                               os.path.join(folder_path, file2), os.path.join(folder_path, file3)
    return None, None, None


def move_files_to_old_folder(file1, file2, file3):
    os.replace(file1, os.path.join(get_full_path('Files\\OldFiles'), os.path.basename(file1)))
    os.replace(file2, os.path.join(get_full_path('Files\\OldFiles'), os.path.basename(file2)))
    os.replace(file3, os.path.join(get_full_path('Files\\OldFiles'), os.path.basename(file3)))


def main():
    print(get_new_pair_of_files())


if __name__ == '__main__':
    print(os.path.basename(r'D:\Programming\python\Programms\Bots\Hack_GoCodeHackMSK_2022\bot\runner.py'))
    main()
