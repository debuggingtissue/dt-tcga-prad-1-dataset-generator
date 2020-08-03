# Fork from https://github.com/BMIRDS/deepslide

from utils import path_utils, enums, svs_utils, image_patch_file_name_builder, svs_image_patch_extractor
import argparse

parser = argparse.ArgumentParser(
    description='Split a WSI at a specific resolution in a .SVS file into .JPEG tiles.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.",
                    required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)

parser.add_argument("-s", "--start_at_image_name", type=str, default=None, help="Resume from a certain filename."
                                                                                " Default value is None.")
parser.add_argument("-r", "--resolution_level", type=int, default=0, choices=[0, 1, 2, 3],

                    help="Resolution level for image to be split."
                         " Low level equals high resolution, lowest level is 0. Choose between {0, 1, 2, 3}."
                         " Default value is 0.")

parser.add_argument("-op", "--overlap_percentage", type=int, default=0,
                    help="Overlapping percentage between patches."
                         " Default value is 0.")

parser.add_argument("-ws ", "--window_size", type=int, default=10000,
                    help="Size for square window"
                         " Default value is 10000.")

args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path
start_at_image_name = args.start_at_image_name
to_resolution_level = args.resolution_level
overlapping_percentage = float("{0:.2f}".format(args.overlap_percentage / 100))
window_size = args.window_size

path_utils.halt_script_if_path_does_not_exist(input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)

full_tcga_download_directories_paths = path_utils.create_full_paths_to_directories_in_directory_path(input_folder_path)
for full_tcga_download_directories_path in full_tcga_download_directories_paths:
    full_image_name_paths = path_utils.create_full_paths_to_files_in_directory_path(full_tcga_download_directories_path)
    for full_image_name_path in full_image_name_paths:
        file_type = full_image_name_path[-4:]
        if file_type == ".svs":
            output_path = output_folder_path + '/'
            svs_image_patch_extractor.split_to_jpeg_image_patches(full_image_name_path, output_path, to_resolution_level,
                                                                  overlapping_percentage, window_size)
