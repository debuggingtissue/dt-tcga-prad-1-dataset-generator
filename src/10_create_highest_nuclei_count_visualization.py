
from utils import path_utils
from utils import enums
from utils import svs_utils, image_patch_predictions_constants, image_patch_file_name_constants, \
    image_patch_metadata_object_utils, image_patch_metadata_object, image_utils, svs_image_patch_extractor,


parser = argparse.ArgumentParser(description='Label image patches with gene mutation data.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.", required=True)


args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path

path_utils.halt_script_if_path_does_not_exist(input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)

case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    input_folder_path + '/' + "image_patches_with_highest_nuclei_count")

for case_directory_path in case_directory_paths:


copy_tree(input_folder_path + "/image_patches_with_highest_nuclei_count", output_folder_path + "/image_patches_with_highest_nuclei_count")
