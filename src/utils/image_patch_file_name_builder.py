from .image_patch_file_name_constants import *
from .image_patch_predictions_constants import *

def build_image_patch_file_name(case_id, resolution_level, x_coordinate, y_coordinate, width, height):
    return CASE_ID + EQUAL + case_id + SEPARATOR + RESOLUTION_LEVEL + EQUAL + str(
        resolution_level) + SEPARATOR + X_COORDINATE + EQUAL + str(
        x_coordinate) + SEPARATOR + Y_COORDINATE + EQUAL + str(y_coordinate) + SEPARATOR + WIDTH + EQUAL + str(
        width) + SEPARATOR + HEIGHT + EQUAL + str(height) + JPEG_ENDING

def extend_image_patch_nuclei_count(current_file_name, predicted_nuclei_count):
    return current_file_name + SEPARATOR + PREDICTION_NUCLEI_COUNT + EQUAL + predicted_nuclei_count

