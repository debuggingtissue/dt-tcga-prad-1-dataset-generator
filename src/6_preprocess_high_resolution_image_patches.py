from PIL import Image
import argparse
from os.path import join
from utils import path_utils, image_preprocessing_utils


def output_preprocessed_image_patch_to_output_directory(full_image_path,
                                                        output_directory_path,
                                                        downscale_to_size):
    input_image = Image.open(full_image_path)

    scaled_image = image_preprocessing_utils.scale_image(input_image, downscale_to_size)

    case_id = full_image_path.split('/')[-2]
    image_patch_id = full_image_path.split('/')[-1][:-4]

    output_case_subfolder_path = join(output_directory_path, case_id)
    path_utils.create_directory_if_directory_does_not_exist_at_path(output_case_subfolder_path)

    output_case_subfolder_rgb_path = join(output_case_subfolder_path, "rgb")
    output_case_subfolder_grayscale_path = join(output_case_subfolder_path, "grayscale")

    path_utils.create_directory_if_directory_does_not_exist_at_path(output_case_subfolder_rgb_path)
    path_utils.create_directory_if_directory_does_not_exist_at_path(output_case_subfolder_grayscale_path)

    output_image_name_rgb_path = join(output_case_subfolder_rgb_path,
                                      image_patch_id + '.png')
    scaled_image.save(output_image_name_rgb_path)

    scaled_image_grayscale = scaled_image.convert('LA')
    output_image_name_grayscale_path = join(output_case_subfolder_grayscale_path,
                                            image_patch_id + '.png')
    scaled_image_grayscale.save(output_image_name_grayscale_path)


parser = argparse.ArgumentParser(description='Scale image patches for nuclei detection.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)

parser.add_argument("-ds", "--downscale_to_size", type=int, default=0,
                    help="Size to scale first centermost image crop down to."
                         " Default value is 0.")

args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path
downscale_to_size = args.downscale_to_size

path_utils.halt_script_if_path_does_not_exist(input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)
case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(input_folder_path)

for case_directory_path in case_directory_paths:
    full_image_patch_paths = path_utils.create_full_paths_to_files_in_directory_path(case_directory_path)
    for full_image_patch_path in full_image_patch_paths:
        output_path = output_folder_path + '/'
        output_preprocessed_image_patch_to_output_directory(full_image_patch_path,
                                                            output_folder_path,
                                                            downscale_to_size)
