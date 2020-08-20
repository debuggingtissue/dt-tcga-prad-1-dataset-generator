import os
import sys
from os import listdir
from os.path import isfile, join, isdir


def halt_script_if_path_does_not_exist(path):
    if not os.path.exists(path):
        sys.exit("Error: Path doesn't exist, " + path)

def does_path_exist(path):
    return os.path.exists(path)

def create_directory_if_directory_does_not_exist_at_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_directory_paths_in_directory(directory_path):
    directory_paths = [f for f in sorted(listdir(directory_path)) if isdir(join(directory_path, f))]
    return directory_paths


def get_file_names_in_directory(path_to_directory):
    file_names = [f for f in sorted(listdir(path_to_directory)) if isfile(join(path_to_directory, f))]
    if '.DS_Store' in file_names:
        file_names.remove('.DS_Store')
    return file_names


def create_full_paths_to_directories_in_directory_path(path_to_directory):
    directory_names = get_directory_paths_in_directory(path_to_directory)
    full_directory_paths = []
    for directory_name in directory_names:
        full_directory_path = path_to_directory + '/' + directory_name
        full_directory_paths.append(full_directory_path)
    full_directory_paths_sorted_by_file_name = sort_paths_by_file_name(full_directory_paths)
    return full_directory_paths_sorted_by_file_name


def create_full_paths_to_files_in_directory_path(path_to_directory):
    file_names = get_file_names_in_directory(path_to_directory)
    full_file_paths = []
    for file_name in file_names:
        full_image_path = path_to_directory + '/' + file_name
        full_file_paths.append(full_image_path)
    return full_file_paths


def sort_paths_by_file_name(file_paths):
    return sorted(file_paths, key=lambda i: os.path.splitext(os.path.basename(i))[0])
