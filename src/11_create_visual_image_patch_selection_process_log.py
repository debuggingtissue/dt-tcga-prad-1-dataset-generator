import argparse
from utils import path_utils, image_preprocessing_utils, gene_mutation_image_patch_labeler, image_utils
from PIL import Image, ImageDraw
from distutils.dir_util import copy_tree


def create_image_patch_selection_process_log_image(case_id):
    saliency_prediction_overview_visualization_directory_path = input_folder_path + "/visualizations/saliency_prediction_overview_visualization/" + case_id
    most_salient_high_res_image_patch_directory_path = input_folder_path + "/visualizations/most_salient_image_patch_high_res/" + case_id
    most_salient_high_res_image_patch_with_annotation_directory_path = input_folder_path + "/visualizations/highest_nuclei_count_annotations_on_most_salient_high_res_image_patch/" + case_id
    image_patch_with_highest_nuclei_count_directory_path = input_folder_path + "/visualizations/image_patches_with_highest_nuclei_count/images_original/" + case_id
    image_patch_with_highest_nuclei_count_directory_with_prediction_masks_path = input_folder_path + "/visualizations/image_patches_with_highest_nuclei_count/images_annotated/" + case_id

    saliency_prediction_overview_visualization_path = path_utils.create_full_paths_to_files_in_directory_path(saliency_prediction_overview_visualization_directory_path)[0]
    most_salient_high_res_image_patch_path = path_utils.create_full_paths_to_files_in_directory_path(most_salient_high_res_image_patch_directory_path)[0]
    most_salient_high_res_image_patch_with_annotation_path = path_utils.create_full_paths_to_files_in_directory_path(most_salient_high_res_image_patch_with_annotation_directory_path)[0]
    image_patch_with_highest_nuclei_count_path = path_utils.create_full_paths_to_files_in_directory_path(image_patch_with_highest_nuclei_count_directory_path)[0]
    image_patch_with_highest_nuclei_count_with_prediction_masks_path = path_utils.create_full_paths_to_files_in_directory_path(image_patch_with_highest_nuclei_count_directory_with_prediction_masks_path)[0]


    saliency_prediction_overview_visualization_image = Image.open(saliency_prediction_overview_visualization_path)
    # most_salient_high_res_image_patch_image = Image.open(most_salient_high_res_image_patch_path)
    # most_salient_high_res_image_patch_with_annotation_image = Image.open(
    #     most_salient_high_res_image_patch_with_annotation_path)
    # image_patch_with_highest_nuclei_count_image = Image.open(image_patch_with_highest_nuclei_count_path)
    # image_patch_with_highest_nuclei_count_with_prediction_masks_image = Image.open(
    #     image_patch_with_highest_nuclei_count_with_prediction_masks_path)

    high_res_image_patch_images_merged_horizontally = image_utils.merge_images_horizontally(
        [most_salient_high_res_image_patch_path, most_salient_high_res_image_patch_with_annotation_path])
    image_patch_with_highest_nuclei_count_image_images_merged_horizontally = image_utils.merge_images_horizontally(
        [image_patch_with_highest_nuclei_count_path,
         image_patch_with_highest_nuclei_count_with_prediction_masks_path])
    selection_processing_log_image = image_utils.merge_images_vertically(
        [saliency_prediction_overview_visualization_image,
         high_res_image_patch_images_merged_horizontally,
         image_patch_with_highest_nuclei_count_image_images_merged_horizontally])

    return selection_processing_log_image


parser = argparse.ArgumentParser(description='Create visual image patch selection process log.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.", required=True)

args = parser.parse_args()

input_folder_path = args.input_folder_path
visualizations_input_folder_path = args.input_folder_path + "/visualizations"
output_folder_path = args.output_folder_path
visualizations_output_path = output_folder_path + "/visualizations/selection_process_log_image/"

path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(visualizations_output_path)


saliency_prediction_overview_visualization_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    input_folder_path + "/visualizations/saliency_prediction_overview_visualization")
list_of_case_ids = [case_id_path.split('/')[-1] for case_id_path in saliency_prediction_overview_visualization_paths]
for case_id in list_of_case_ids:
    image_patch_selection_process_log_image = create_image_patch_selection_process_log_image(case_id)
    image_patch_selection_process_log_image.save(visualizations_output_path + case_id +".png", 'PNG')
copy_tree(visualizations_input_folder_path, output_folder_path + "/visualizations")
copy_tree(input_folder_path + "/image_patches_with_highest_nuclei_count", output_folder_path + "/image_patches_with_highest_nuclei_count")


