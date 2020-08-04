
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

most_salient_image_patch_case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    input_folder_path + '/' + "visualizations/most_salient_image_patch_high_res")
CID_indexed_image_patch_metadata_objects_dict = image_patch_metadata_object_utils.case_directory_paths_containing_image_patches_to_dict_indexed_by_CID(most_salient_image_patch_case_directory_paths)

high_nuclei_count_case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    input_folder_path + '/' + "image_patches_with_highest_nuclei_count")
for high_nuclei_count_case_directory_path in high_nuclei_count_case_directory_paths:
    first_image_patch_path = image_patch_paths[0]
    image_name = first_image_patch_path.split('/')[-1]
    image_patch_metadata_object_with_high_nucleus = image_patch_metadata_object_utils.parse_image_patch_file_name_into_image_patch_metadata_object(image_name)
    corresponding_image_patch_metadata_object_with_highest_saliency = CID_indexed_high_saliency_image_patch_metadata_objects_dict[image_patch_metadata_object_with_high_nucleus.case_id]
    image_patch_metadata_object_with_highest_saliency = corresponding_image_patch_metadata_object_with_highest_saliency.first_image_patch_path
    annotate_the_region_on_image_patch_with_the_highest_nuclei_count()



copy_tree(input_folder_path + "/image_patches_with_highest_nuclei_count", output_folder_path + "/image_patches_with_highest_nuclei_count")
