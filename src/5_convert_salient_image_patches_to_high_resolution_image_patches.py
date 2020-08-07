import argparse
from utils import svs_utils, image_patch_predictions_constants, image_patch_file_name_constants, path_utils, \
    svs_image_patch_extractor, enums, image_patch_metadata_object_utils
from distutils.dir_util import copy_tree


parser = argparse.ArgumentParser(
    description="Generate high resolution image patches of an image patch at a lower resolution")
parser.add_argument("-svs", "--svs_input_folder_path", type=str, help=" The path to the SVS input folder.",
                    required=True)
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.",
                    required=True)

parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)

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

svs_input_folder_path = args.svs_input_folder_path
input_folder_path = args.input_folder_path
csv_input_folder_path = input_folder_path + '/' + "saliency_predictions_csvs"
visualizations_folder_path = input_folder_path + '/' + "visualizations"

output_folder_path = args.output_folder_path
to_resolution_level = int(args.resolution_level)
overlapping_percentage = float("{0:.2f}".format(args.overlap_percentage / 100))
window_size = args.window_size

path_utils.halt_script_if_path_does_not_exist(svs_input_folder_path)
path_utils.halt_script_if_path_does_not_exist(csv_input_folder_path)

path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)

tcga_download_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    svs_input_folder_path)

case_image_patch_metadata_objects_csv_paths = path_utils.create_full_paths_to_files_in_directory_path(
    csv_input_folder_path)
CID_indexed_image_patch_metadata_objects_dict = image_patch_metadata_object_utils.case_image_patch_metadata_csv_paths_to_dict_indexed_by_CID(
    case_image_patch_metadata_objects_csv_paths)

for tcga_download_directories_path_index, tcga_download_directory_path in enumerate(
        tcga_download_directory_paths):
    full_image_name_paths = path_utils.create_full_paths_to_files_in_directory_path(tcga_download_directory_path)
    # there might be more than one image in a tcga download directory path (TO-DO: improve current solution)
    first_image_name_path = full_image_name_paths[0]

    case_id = first_image_name_path.split('/')[-1][:-4]
    image_patch_metadata_objects_corresponding_to_CID = CID_indexed_image_patch_metadata_objects_dict[case_id]

    image_patch_metadata_object_with_highest_saliency_prediction = image_patch_metadata_object_utils.get_image_patch_metadata_object_with_the_highest_saliency(
        image_patch_metadata_objects_corresponding_to_CID)

    svs_image_patch_extractor.split_to_jpeg_image_patches(first_image_name_path,
                                                          output_folder_path,
                                                          to_resolution_level,
                                                          overlapping_percentage,
                                                          window_size,
                                                          from_resolution_level=image_patch_metadata_object_with_highest_saliency_prediction.resolution_level,
                                                          patching_area_x=image_patch_metadata_object_with_highest_saliency_prediction.x_coordinate,
                                                          patching_area_y=image_patch_metadata_object_with_highest_saliency_prediction.y_coordinate,
                                                          patching_area_width=image_patch_metadata_object_with_highest_saliency_prediction.width,
                                                          patching_area_height=image_patch_metadata_object_with_highest_saliency_prediction.height)

copy_tree(visualizations_folder_path, output_folder_path + "/visualizations")
