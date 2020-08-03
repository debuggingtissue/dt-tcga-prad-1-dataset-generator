from .image_patch_file_name_constants import *
from .image_patch_predictions_constants import *


#This code always assumes that the ending of a file is four letters long, this may backfire and should be fixed
def parse_image_patch_file_name_to_dict(image_patch_file_name):
    file_name_without_file_type = image_patch_file_name[:-4]
    file_properties_key_value_pairs = file_name_without_file_type.split(SEPARATOR)
    dict = {}
    for file_property_key_value_pair in file_properties_key_value_pairs:
        file_properties_key_value_pairs_separated = file_property_key_value_pair.split(EQUAL)
        key = file_properties_key_value_pairs_separated[0]
        value = file_properties_key_value_pairs_separated[-1]
        dict[key] = value
    return dict

def parse_image_patch_for_nuclei_count_prediction(image_patch_file_name):
    file_name_without_file_type = image_patch_file_name[:-4]
    file_properties_key_value_pairs = file_name_without_file_type.split(SEPARATOR)
    dict = {}
    for file_property_key_value_pair in file_properties_key_value_pairs:
        file_properties_key_value_pairs_separated = file_property_key_value_pair.split(EQUAL)
        key = file_properties_key_value_pairs_separated[0]
        value = file_properties_key_value_pairs_separated[-1]
        if key == PREDICTION_NUCLEI_COUNT:
            return value

def get_value_for_key(image_patch_file_name, key):
    dict = parse_image_patch_file_name_to_dict(image_patch_file_name)
    return dict[key]
