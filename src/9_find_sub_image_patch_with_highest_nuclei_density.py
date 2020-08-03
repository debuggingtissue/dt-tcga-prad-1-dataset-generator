import argparse
from utils import path_utils, image_patch_file_name_parser, image_patch_metadata_object
import shutil


def get_image_patch_path_with_highest_nuclei_count(image_patch_paths):
    image_patch_path_with_highest_nuclei_count = None
    highest_nuclei_count = 0
    for image_patch_path in image_patch_paths:
        image_patch_file_name = image_patch_path.split('/')[-1]
        predicted_nuclei_count = int(
            image_patch_file_name_parser.parse_image_patch_for_nuclei_count_prediction(image_patch_file_name))
        if predicted_nuclei_count >= highest_nuclei_count:
            image_patch_path_with_highest_nuclei_count = image_patch_path
            highest_nuclei_count = predicted_nuclei_count

    return image_patch_path_with_highest_nuclei_count


def get_path_for_all_image_patches_with_specific_image_mode(all_image_patches_mode_paths, image_mode):
    all_image_patches_for_specific_image_mode_directory_path = None
    for image_mode_path in all_image_patches_mode_paths:
        image_mode_in_path = image_mode_path.split('/')[-1]
        if image_mode == image_mode_in_path:
            all_image_patches_for_specific_image_mode_directory_path = image_mode_path
            break
        elif image_mode == image_mode_in_path:
            all_image_patches_for_specific_image_mode_directory_path = image_mode_path
            break
    return all_image_patches_for_specific_image_mode_directory_path


def get_target_image_patch_path(all_image_patch_paths_for_specific_image_mode, target_image_patch_metadata_object):
    for image_patch_path in all_image_patch_paths_for_specific_image_mode:
        image_patch_file_name = image_patch_path.split('/')[-1]
        patch_file_name_to_dict = image_patch_file_name_parser.parse_image_patch_file_name_to_dict(
            image_patch_file_name)
        image_patch_metadata_object = image_patch_metadata_object.image_patch_metadata_object_from_image_patch_dict(
            patch_file_name_to_dict)

        isMatch = image_patch_metadata_object.x_coordinate == target_image_patch_metadata_object.x_coordinate and image_patch_metadata_object.y_coordinate == target_image_patch_metadata_object.y_coordinate
        if isMatch:
            result_image_patch_old_path = image_patch_path
            return result_image_patch_old_path


def output_image_patch_with_highest_predicted_nuclei_count(image_patches_path, output_diretory_path,
                                                           all_image_patches_for_case_id_directory_path, image_mode):
    image_patch_paths = path_utils.create_full_paths_to_files_in_directory_path(image_patches_path)
    image_patch_path_with_highest_nuclei_count = get_image_patch_path_with_highest_nuclei_count(image_patch_paths)

    image_patch_file = image_patch_path_with_highest_nuclei_count.split('/')[-1]

    all_image_patches_mode_paths = path_utils.create_full_paths_to_directories_in_directory_path(
        all_image_patches_for_case_id_directory_path)
    directory_path_for_all_image_patches_with_specific_image_mode = get_path_for_all_image_patches_with_specific_image_mode(
        all_image_patches_mode_paths, image_mode)

    all_image_patches_with_specific_image_mode_paths = path_utils.create_full_paths_to_files_in_directory_path(
        directory_path_for_all_image_patches_with_specific_image_mode)

    parse_target_image_patch_file_name_to_dict = image_patch_file_name_parser.parse_image_patch_file_name_to_dict(
        image_patch_file)
    target_image_patch_metadata_object = image_patch_metadata_object.image_patch_metadata_object_from_image_patch_dict(
        parse_target_image_patch_file_name_to_dict)

    target_image_patch_path = get_target_image_patch_path(all_image_patches_with_specific_image_mode_paths,
                                                          target_image_patch_metadata_object)

    new_image_patch_path = output_diretory_path + "/" + image_patch_file

    shutil.copy(target_image_patch_path, new_image_patch_path)


parser = argparse.ArgumentParser(description="Finding the image patch with the highest nuclei density for each case")
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)
parser.add_argument("-im", "--image_mode",
                    type=str,
                    help="Image mode to be outputted, may differ from the image mode used to segment the image"
                         "Choose between rgb or grayscale",
                    required=True)

parser.add_argument("-aip", "--all_image_patches",
                    type=str,
                    help="All preprocessed image patches"
                         "Contains rgb or grayscale image patches (may vary)",
                    required=True)

args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path
image_mode = args.image_mode
all_image_patches_path = args.all_image_patches

path_utils.halt_script_if_path_does_not_exist(input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)
output_folder_path_for_images_with_highest_nuclei_count = output_folder_path + '/' + "image_patches_with_highest_nuclei_count"
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path_for_images_with_highest_nuclei_count)


case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(input_folder_path)
for case_directory_path in case_directory_paths:
    path_to_image_patches = case_directory_path + "/" + "images_original"

    case_id = case_directory_path.split('/')[-1]
    case_id_output_path = output_folder_path_for_images_with_highest_nuclei_count + "/" + case_id
    path_utils.create_directory_if_directory_does_not_exist_at_path(case_id_output_path)
    all_image_patches_for_case_id_directory_path = all_image_patches_path + "/" + case_id
    output_image_patch_with_highest_predicted_nuclei_count(path_to_image_patches, case_id_output_path,
                                                           all_image_patches_for_case_id_directory_path, image_mode)
copy_tree(input_folder_path + "/visualizations", output_folder_path + "/visualizations")
