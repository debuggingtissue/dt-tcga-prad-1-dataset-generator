import argparse
from utils import path_utils, image_preprocessing_utils, gene_mutation_image_patch_labeler
import shutil
from distutils.dir_util import copy_tree


parser = argparse.ArgumentParser(description='Label image patches with gene mutation data.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.", required=True)
parser.add_argument("-mf", "--mutation_file_path", type=str, help="Path to file providing genetic information",
                    required=True)
parser.add_argument("-goi", "--gene_of_interest", type=str, help="The mutation to label by", required=True)
parser.add_argument("-do", "--disc_operation", type=str, help="move or copy", required=True)

args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path

labeled_dataset_output_folder_path = args.output_folder_path + "/labeled_SPOP_mutation_state_dataset"
mutation_file_directory_path = args.mutation_file_path
gene_of_interest = args.gene_of_interest
disc_operation = args.disc_operation

image_patch_input_folder_path = input_folder_path + "/image_patches_with_highest_nuclei_count/images_original"
path_utils.halt_script_if_path_does_not_exist(image_patch_input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)
case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(image_patch_input_folder_path)
mutation_file_path = path_utils.create_full_paths_to_files_in_directory_path(mutation_file_directory_path)[0]

all_image_patches_with_meta_info_paths = []
for case_directory_path in case_directory_paths:
    print(case_directory_path)
    image_patch_with_meta_info_path = path_utils.create_full_paths_to_files_in_directory_path(case_directory_path)[0]
    all_image_patches_with_meta_info_paths.append(image_patch_with_meta_info_path)

gene_mutation_image_patch_labeler.label_image_patches(all_image_patches_with_meta_info_paths, mutation_file_path,
                                                      gene_of_interest, labeled_dataset_output_folder_path, disc_operation)
copy_tree(input_folder_path + "/visualizations", output_folder_path + "/visualizations")
