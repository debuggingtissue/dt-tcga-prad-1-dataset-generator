import argparse
import os
from os.path import isfile, join
import openslide
from utils import path_utils
from utils import enums
from utils import svs_utils, image_patch_predictions_constants, image_patch_file_name_constants, \
    image_patch_metadata_object_utils, image_patch_metadata_object, image_utils, svs_image_patch_extractor


def create_jpeg_thumbnail_of_wsi(full_image_name_path):
    img = openslide.OpenSlide(full_image_name_path)
    thumbnail = img.associated_images["thumbnail"]

    return thumbnail


def draw_saliency_prediction_annotation_boxes_onto_thumbnail(svs_image,
                                                             thumbnail,
                                                             image_patch_metadata_objects,
                                                             accuracy_percentage_threshold):
    for image_patch_metadata_object in image_patch_metadata_objects:

        saliency_prediction = image_patch_metadata_object.prediction_value_salient

        if saliency_prediction > accuracy_percentage_threshold:
            image_patch_metadata_object_scaled_to_new_resolution = svs_utils.scale_image_patch_metadata_object_to_new_resolution_level(
                image_patch_metadata_object, enums.ResolutionLevel.THUMBNAIL, svs_image)
            thumbnail = image_utils.draw_annotation_box_onto_image(thumbnail, image_patch_metadata_object_scaled_to_new_resolution)

    return thumbnail


parser = argparse.ArgumentParser(description='Saliency visualization.')
parser.add_argument("-svs", "--svs_input_folder_path", type=str, help=" The path to the SVS input folder.",
                    required=True)
parser.add_argument("-csv", "--csv_input_folder_path", type=str, help="The path to the CSV input folder.",
                    required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)
parser.add_argument("-apt", "--accuracy_percentage_threshold", type=float,
                    help="Accuracy percentage threshold for showing annotations",
                    required=True)

args = parser.parse_args()

svs_input_folder_path = args.svs_input_folder_path
csv_input_folder_path = args.csv_input_folder_path
output_folder_path = args.output_folder_path
accuracy_percentage_threshold = args.accuracy_percentage_threshold

path_utils.halt_script_if_path_does_not_exist(svs_input_folder_path)
path_utils.halt_script_if_path_does_not_exist(csv_input_folder_path)

path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)

output_folder_path_for_visualization_directory = output_folder_path + '/' + "visualizations"
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path_for_visualization_directory)

output_folder_path_for_saliancy_prediction_visualization_directory = output_folder_path_for_visualization_directory + '/' + "saliency_prediction_overview_visualization"
path_utils.create_directory_if_directory_does_not_exist_at_path(
    output_folder_path_for_saliancy_prediction_visualization_directory)

output_folder_path_for_most_salient_image_patch_high_res_visualization_directory = output_folder_path_for_visualization_directory + '/' + "most_salient_image_patch_high_res"
path_utils.create_directory_if_directory_does_not_exist_at_path(
    output_folder_path_for_saliancy_prediction_visualization_directory)

tcga_download_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    svs_input_folder_path)

case_image_patch_metadata_objects_csv_paths = path_utils.create_full_paths_to_files_in_directory_path(
    csv_input_folder_path)
CID_indexed_image_patch_metadata_objects_dict = image_patch_metadata_object_utils.case_image_patch_metadata_csv_paths_to_dict_indexed_by_CID(
    case_image_patch_metadata_objects_csv_paths)


def create_saliency_prediction_overview_visualization_for_case(
        output_folder_path_for_saliancy_prediction_visualization_directory,
        svs_image,
        case_ID,
        image_patch_metadata_objects_corresponding_to_CID):
    output_path = output_folder_path_for_saliancy_prediction_visualization_directory + '/' + case_ID + '/'
    path_utils.create_directory_if_directory_does_not_exist_at_path(output_path)

    thumbnail = create_jpeg_thumbnail_of_wsi(image_paths_of_sample[0])
    thumbnail = thumbnail.convert("RGB")
    thumbnail_path = output_path + case_ID + "_original.jpeg"
    thumbnail.save(thumbnail_path, 'JPEG')

    thumbnail = thumbnail.convert("RGBA")
    thumbnail_with_predictions_above_threshold = draw_saliency_prediction_annotation_boxes_onto_thumbnail(svs_image,
                                                                                                          thumbnail,
                                                                                                          image_patch_metadata_objects_corresponding_to_CID,
                                                                                                          accuracy_percentage_threshold)
    thumbnail_with_predictions_above_threshold_path = output_path + case_ID + "_multiple_annotations.jpeg"
    thumbnail_with_predictions_above_threshold.save(thumbnail_with_predictions_above_threshold_path, 'JPEG')

    thumbnail = thumbnail.convert("RGBA")
    image_patch_metadata_object_with_highest_saliency = image_patch_metadata_object_utils.get_image_patch_metadata_object_with_the_highest_saliency(
        image_patch_metadata_objects_corresponding_to_CID)
    thumbnail_with_single_predication = draw_prediction_annotations_onto_thumbnail(svs_image,
                                                                                   thumbnail,
                                                                                   [
                                                                                       image_patch_metadata_object_with_highest_saliency],
                                                                                   accuracy_percentage_threshold)
    thumbnail_with_single_predication_path = output_path + case_ID + "_single_annotations.jpeg"
    thumbnail_with_single_predication.save(thumbnail_with_single_predication_path, 'JPEG')

    merged_thumbnail_image = image_utils.merge_images_horizontally(
        [thumbnail_path, thumbnail_with_predictions_above_threshold_path, thumbnail_with_single_predication_path])
    merged_thumbnail_image_path = output_path + case_ID + "_all_thumbnail_images.jpeg"
    merged_thumbnail_image.save(merged_thumbnail_image_path, 'JPEG')


def create_most_salient_image_patch_high_res_visualization(
        output_folder_path_for_most_salient_image_patch_visualization_directory,
        svs_image_path,
        case_ID,
        image_patch_metadata_objects_corresponding_to_CID):
    output_path = output_folder_path_for_most_salient_image_patch_visualization_directory + '/' + case_ID + '/'
    path_utils.create_most_if_directory_does_not_exist_at_path(output_path)
    image_patch_metadata_object_with_highest_saliency = image_patch_metadata_object_utils.get_image_patch_metadata_object_with_the_highest_saliency(
        image_patch_metadata_objects_corresponding_to_CID)
    svs_image_patch_extractor.extract_image_patch_jpeg(svs_image_path, output_path,
                                                       to_resolution_level=enums.ResolutionLevel.LEVEL_3,
                                                       from_resolution_level=image_patch_metadata_object_with_highest_saliency.resolution_level,
                                                       patch_area_x=image_patch_metadata_object_with_highest_saliency.x_coordinate,
                                                       patch_area_y=image_patch_metadata_object_with_highest_saliency.y_coordinate,
                                                       patch_area_width=image_patch_metadata_object_with_highest_saliency.width,
                                                       patch_area_height=image_patch_metadata_object_with_highest_saliency.height)


for tcga_download_directories_path_index, tcga_download_directory_path in enumerate(
        tcga_download_directory_paths):
    image_paths_of_sample = path_utils.create_full_paths_to_files_in_directory_path(tcga_download_directory_path)
    image_path_of_first_svs_image = image_paths_of_sample[0]
    case_ID = image_path_of_first_svs_image.split('/')[-1][:-4]
    image_patch_metadata_objects_corresponding_to_CID = CID_indexed_image_patch_metadata_objects_dict[case_ID]

    svs_image = svs_utils.get_svs_image_of_wsi_from_path(image_path_of_first_svs_image)
    create_saliency_prediction_overview_visualization_for_case(
        output_folder_path_for_saliancy_prediction_visualization_directory,
        svs_image,
        case_ID,
        image_patch_metadata_objects_corresponding_to_CID)

    create_most_salient_image_patch_high_res_visualization(
        output_folder_path_for_saliancy_prediction_visualization_directory,
        image_path_of_first_svs_image,
        case_ID,
        image_patch_metadata_objects_corresponding_to_CID)

copy_tree(csv_input_folder_path + "/saliency_predictions_csvs", output_folder_path + "/saliency_predictions_csvs")
