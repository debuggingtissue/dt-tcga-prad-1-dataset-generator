import sys
import csv
from os import listdir, makedirs, _exit
from os.path import isfile, join, isdir, exists
import ntpath
from shutil import copy, move
from utils import image_patch_file_name_parser, image_patch_file_name_constants

ntpath.basename("a/b/c")


def get_case_ids_with_mutation(mutation_file_path, mutation_of_interest):
    with open(mutation_file_path) as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        rows_with_mutation_of_interest = []
        for row in reader:
            if row[1] == mutation_of_interest:
                rows_with_mutation_of_interest.append(row[0])
        return rows_with_mutation_of_interest


def get_subdirectory_paths(directory):
    subdirectory_paths = [
        join(directory, f) for f in listdir(directory)
        if (isdir(join(directory, f)) and '.DS_Store' not in f)
    ]
    if join(directory, '.DS_Store') in subdirectory_paths:
        subdirectory_paths.remove(join(directory, '.DS_Store'))
    subdirectory_paths = sorted(subdirectory_paths)
    return subdirectory_paths


def get_image_paths(directory):
    image_paths = [
        join(directory, f) for f in listdir(directory) if (isfile(join(directory, f)) and f.endswith(".svs"))
    ]
    if join(directory, '.DS_Store') in image_paths:
        image_paths.remove(join(directory, '.DS_Store'))
    image_paths = sorted(image_paths)
    return image_paths


def get_all_image_paths(case_directory_paths):
    all_image_paths = []
    for case_directory_path in case_directory_paths:
        for image_path in get_image_paths(case_directory_path):
            all_image_paths.append(image_path)
    return all_image_paths


def get_path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def label_images(all_image_patches_with_meta_info_paths, case_ids_with_mutation):
    mutation_true, mutation_false = [], []
    for case_id_with_mutation in case_ids_with_mutation:
        case_id_with_mutation_without_sample_vial = case_id_with_mutation[:-1]
        for image_path in all_image_patches_with_meta_info_paths:
            image_file = image_patch_file_name_parser.get_value_for_key(get_path_leaf(image_path),
                                                                        image_patch_file_name_constants.CASE_ID)
            if case_id_with_mutation_without_sample_vial in image_file:
                mutation_true.append(image_path)

    mutation_false = [item for item in all_image_patches_with_meta_info_paths if item not in mutation_true]
    return mutation_true, mutation_false


def confirm_output_directory(output_directory_path):
    if not exists(output_directory_path):
        makedirs(output_directory_path)
    return output_directory_path


def generate_output_path(output_root_directory_path, mutation_of_interest, has_mutation):
    if has_mutation:
        return confirm_output_directory(output_root_directory_path + "/" + mutation_of_interest + "_true")
    else:
        return confirm_output_directory(output_root_directory_path + "/" + mutation_of_interest + "_false")


def copy_images(source_image_paths, destination_directory_path):
    for source_image_path in source_image_paths:
        image_patch_file_name = source_image_path.split('/')[-1]
        copy(source_image_path, destination_directory_path + "/" + image_patch_file_name)


def move_images(source_image_paths, destination_directory_path):
    for source_image_path in source_image_paths:
        image_patch_file_name = source_image_path.split('/')[-1]
        move(source_image_path, destination_directory_path + "/" + image_patch_file_name)


def label_image_patches(all_image_patches_with_meta_info_paths, mutation_file_path, gene_of_interest, output_path,
                        desired_disk_operation):
    print("\n")
    # print(sys.argv)

    case_ids_with_mutation = get_case_ids_with_mutation(mutation_file_path, gene_of_interest)

    print("===========")
    print("Labeling mutations")
    print("===========\n")

    mutation_true, mutation_false = label_images(all_image_patches_with_meta_info_paths, case_ids_with_mutation)

    print("===========")
    print("Number of cases with " + gene_of_interest + " mutation " + str(len(mutation_true)))
    print("Number of cases without " + gene_of_interest + " mutation " + str(len(mutation_false)))
    print("===========\n")

    output_path_mutation_true = generate_output_path(output_path, gene_of_interest, True)
    output_path_mutation_false = generate_output_path(output_path, gene_of_interest, False)

    if desired_disk_operation == "copy":
        print("===========")
        print("Copying files to " + output_path)
        print("===========\n")

        copy_images(mutation_true, output_path_mutation_true)
        copy_images(mutation_false, output_path_mutation_false)
    elif desired_disk_operation == "move":

        print("===========")
        print("Moving files to " + output_path)
        print("===========\n")

        move_images(mutation_true, output_path_mutation_true)
        move_images(mutation_false, output_path_mutation_false)


    else:
        print("===========")
        print("Non valid disk operation selected, please use -copy or -move")
        print("===========\n")

        _exit(1)

    print("===========")
    print("TCGA mutation labeling has succeeded")
    print("===========\n")
