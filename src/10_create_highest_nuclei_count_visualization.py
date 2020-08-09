
import argparse
from utils import path_utils
from utils import enums
from utils import svs_utils, image_patch_predictions_constants, image_patch_file_name_constants, \
    image_patch_metadata_object_utils, image_patch_metadata_object, image_utils, svs_image_patch_extractor, svs_loader as svs_l,path_utils,image_patch_file_name_parser
from PIL import Image, ImageDraw
from distutils.dir_util import copy_tree

def annotate_the_region_on_image_patch_with_the_highest_nuclei_count(highest_saliency_image_patch_metadata_object,
                                                                     high_nuclei_count_metadata_object,
                                                                     svs_loader,
                                                                     output_path):
    case_ID = highest_saliency_image_patch_metadata_object.case_id

    output_path = output_path + '/' + case_ID + '/'
    path_utils.create_directory_if_directory_does_not_exist_at_path(output_path)

    image_patch_with_highest_saliency = Image.open(highest_saliency_image_patch_metadata_object.image_patch_path)
    image_patch_with_highest_saliency = image_patch_with_highest_saliency.convert("RGBA")

    svs_path = svs_loader.get_0_indexed_svs_path_for_CID(case_ID)
    svs_image = svs_utils.get_svs_image_of_wsi_from_path(svs_path)

    scaled_high_nuclei_count_metadata_image_patch_data = svs_utils.scale_image_patch_metadata_object_to_new_resolution_level(high_nuclei_count_metadata_object,
                                                              highest_saliency_image_patch_metadata_object.resolution_level,
                                                              svs_image)
    scaled_high_nuclei_count_metadata_image_patch_data.x_coordinate = abs(int(scaled_high_nuclei_count_metadata_image_patch_data.x_coordinate) - int(highest_saliency_image_patch_metadata_object.x_coordinate))
    scaled_high_nuclei_count_metadata_image_patch_data.y_coordinate = abs(int(scaled_high_nuclei_count_metadata_image_patch_data.y_coordinate) - int(highest_saliency_image_patch_metadata_object.y_coordinate))


    image_patch_with_annotation_box_of_highest_nuclei_count = image_utils.draw_annotation_box_onto_image(image_patch_with_highest_saliency, scaled_high_nuclei_count_metadata_image_patch_data)

    thumbnail_with_single_predication_path = output_path + case_ID + "_highest_nuclei_count_annotation.jpeg"
    image_patch_with_annotation_box_of_highest_nuclei_count.save(thumbnail_with_single_predication_path, 'JPEG')

parser = argparse.ArgumentParser(description='Label image patches with gene mutation data.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-svs", "--svs_input_folder_path", type=str, help=" The path to the SVS input folder.",
                    required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.", required=True)

args = parser.parse_args()

input_folder_path = args.input_folder_path
svs_input_folder_path = args.svs_input_folder_path
output_folder_path = args.output_folder_path
visualizations_output_path = output_folder_path + "/visualizations"
copy_tree(input_folder_path + "/visualizations", visualizations_output_path)
highest_nuclei_count_visualization_output_path = visualizations_output_path + "/highest_nuclei_count_annotations_on_most_salient_high_res_image_patch"


svs_loader = svs_l.SVSLoader(svs_input_folder_path)

path_utils.halt_script_if_path_does_not_exist(input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)

most_salient_image_patch_case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    input_folder_path + '/' + "visualizations/most_salient_image_patch_high_res")
CID_indexed_high_saliency_image_patch_metadata_objects_dict = image_patch_metadata_object_utils.case_directory_paths_containing_image_patches_to_dict_indexed_by_CID(most_salient_image_patch_case_directory_paths)

high_nuclei_count_case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(input_folder_path + '/' + "image_patches_with_highest_nuclei_count/")


for high_nuclei_count_case_directory_path in high_nuclei_count_case_directory_paths:
    high_nuclei_count_case_image_patches_paths = path_utils.create_full_paths_to_files_in_directory_path(high_nuclei_count_case_directory_path)
    first_image_patch_path = high_nuclei_count_case_image_patches_paths[0]
    image_name = first_image_patch_path.split('/')[-1]
    image_patch_metadata_object_with_high_nucleus = image_patch_file_name_parser.parse_image_patch_file_name_into_image_patch_metadata_object(image_name)

    corresponding_image_patch_metadata_object_with_highest_saliency = CID_indexed_high_saliency_image_patch_metadata_objects_dict[image_patch_metadata_object_with_high_nucleus.case_id]
    corresponding_image_patch_metadata_object_with_highest_saliency.image_patch_path = path_utils.create_full_paths_to_files_in_directory_path(input_folder_path + "/visualizations/most_salient_image_patch_high_res/" + corresponding_image_patch_metadata_object_with_highest_saliency.case_id )[0]
    annotate_the_region_on_image_patch_with_the_highest_nuclei_count(corresponding_image_patch_metadata_object_with_highest_saliency, image_patch_metadata_object_with_high_nucleus, svs_loader, highest_nuclei_count_visualization_output_path)

copy_tree(input_folder_path + "/image_patches_with_highest_nuclei_count", output_folder_path + "/image_patches_with_highest_nuclei_count")
