import csv
from .image_patch_metadata_object import *


def case_image_patch_metadata_csv_paths_to_dict_indexed_by_CID(csv_paths):
    dict = {}
    for csv_path in csv_paths:
        image_patch_metadata_objects, case_id = create_image_patch_metadata_objects_from_csv_path(csv_path)
        dict[case_id] = image_patch_metadata_objects
    return dict


def create_image_patch_metadata_objects_from_csv_path(csv_path):
    case_id = None
    with open(csv_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        image_patch_metadata_objects = []
        for row in reader:
            case_id = row[CASE_ID]
            image_patch_metadata_object = image_patch_metadata_object_from_csv_row(row)
            image_patch_metadata_objects.append(image_patch_metadata_object)
    return image_patch_metadata_objects, case_id

def get_image_patch_metadata_object_with_the_highest_saliency(image_patch_metadata_objects):
    highest_predicted_saliency_value = 0
    image_patch_metadata_object_with_highest_saliency = None
    for image_patch_metadata_object in image_patch_metadata_objects:
        saliency_prediction_value = image_patch_metadata_object.prediction_value_salient
        if saliency_prediction_value > highest_predicted_saliency_value:
            highest_predicted_saliency_value = saliency_prediction_value
            image_patch_metadata_object_with_highest_saliency = image_patch_metadata_object

    return image_patch_metadata_object_with_highest_saliency


def case_directory_paths_containing_image_patches_to_dict_indexed_by_CID(case_directory_paths):
    dict = {}
    for case_directory_path in case_directory_paths:
        image_patch_paths = path_utils.create_full_paths_to_files_in_directory_path(case_directory_path)
        first_image_patch_path = image_patch_paths[0]
        image_name = first_image_patch_path.split('/')[-1]
        image_patch_metadata_object = parse_image_patch_file_name_into_image_patch_metadata_object(image_name)
        dict[image_patch_metadata_object.case_id] = image_patch_metadata_object
    return dict
