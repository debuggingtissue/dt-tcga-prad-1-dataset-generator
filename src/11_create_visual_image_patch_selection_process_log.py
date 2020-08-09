import argparse
from utils import path_utils, image_preprocessing_utils, gene_mutation_image_patch_labeler


def create_image_patch_selection_process_log_image(case_id):

    saliency_prediction_overview_visualization_path = input_folder_path + "/visualizations/saliency_prediction_overview_visualization/" + case_id
    most_salient_high_res_image_patch_path = input_folder_path + "/visualizations/most_salient_image_patch_high_res/" + case_id
    most_salient_high_res_image_patch_with_annotation_path = input_folder_path + "/visualizations/highest_nuclei_count_annotations_on_most_salient_high_res_image_patch/" + case_id
    image_patch_with_highest_nuclei_count = input_folder_path + "/visualizations/image_patches_with_highest_nuclei_count/images_original/" + case_id
    image_patch_with_highest_nuclei_count_with_prediction_masks = input_folder_path + "/visualizations/image_patches_with_highest_nuclei_count/images_original/" + case_id



parser = argparse.ArgumentParser(description='Create visual image patch selection process log.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.", required=True)

args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path

saliency_prediction_overview_visualization_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    input_folder_path + "/visualizations/saliency_prediction_overview_visualization")
list_of_case_ids = [case_id_path.split('/')[-1] for case_id_path in saliency_prediction_overview_visualization_paths]
for case_id in list_of_case_ids:
    image_patch_selection_process_log_image = create_image_patch_selection_process_log_image(case_id)







