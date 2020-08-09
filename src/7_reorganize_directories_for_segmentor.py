import argparse
from utils import path_utils, image_preprocessing_utils
import shutil
from distutils.dir_util import copy_tree


parser = argparse.ArgumentParser(description='Scale image patches for nuclei detection.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)
parser.add_argument("-im", "--image_mode", type=str, help="Image mode to be used for the input image when using the segmentator"
                                                          "Choose between rgb or grayscale",
required = True)


args = parser.parse_args()

input_folder_path = args.input_folder_path

images_input_folder_path = args.input_folder_path + '/' + "preprocessed_high_res_image_patches" + "/"
output_folder_path = args.output_folder_path
reorganized_image_patches = args.output_folder_path + '/' + "preproessesed_image_patches_organized_for_classifier" + "/"

image_mode = args.image_mode

path_utils.halt_script_if_path_does_not_exist(images_input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)
case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(images_input_folder_path)

for case_directory_path in case_directory_paths:
    full_image_patch_paths = None
    if (image_mode == "rgb"):
        full_image_patch_paths = path_utils.create_full_paths_to_files_in_directory_path(case_directory_path + "/rgb")
    elif (image_mode == "grayscale"):
        full_image_patch_paths = path_utils.create_full_paths_to_files_in_directory_path(
            case_directory_path + "/grayscale")

    for full_input_image_patch_path in full_image_patch_paths:
        case_id = full_input_image_patch_path.split('/')[-3]
        case_id_directory_path = reorganized_image_patches + "/" + case_id
        path_utils.create_directory_if_directory_does_not_exist_at_path(case_id_directory_path)

        image_patch_file = full_input_image_patch_path.split('/')[-1][:-4]
        image_patch_root_path = case_id_directory_path + "/" + image_patch_file
        path_utils.create_directory_if_directory_does_not_exist_at_path(case_id_directory_path)

        case_images_path = image_patch_root_path + "/" + "images"
        path_utils.create_directory_if_directory_does_not_exist_at_path(case_images_path)

        image_patch_file = full_input_image_patch_path.split('/')[-1]
        new_image_patch_path = case_images_path + "/" + image_patch_file

        shutil.copy(full_input_image_patch_path, new_image_patch_path)

copy_tree(images_input_folder_path, output_folder_path + "/preprocessed_high_res_image_patches")
# copy_tree(images_input_folder_path, output_folder_path + "/visualizations/preprocessed_high_res_image_patches")
copy_tree(input_folder_path + "/visualizations", output_folder_path + "/visualizations")

