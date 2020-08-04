from .image_patch_file_name_constants import *
from .image_patch_predictions_constants import *

class ImagePatchMetadataObject:

    # parameterized constructor
    def __init__(self,
                 case_id=None,
                 resolution_level=None,
                 x_coordinate=None,
                 y_coordinate=None,
                 width=None,
                 height=None,
                 prediction_value_salient=None,
                 prediction_value_non_salient=None,
                 prediction_nuclei_count=None,
                 image_patch_path=None):
        self.case_id = case_id
        self.resolution_level = resolution_level
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width = width
        self.height = height
        self.prediction_value_salient = prediction_value_salient
        self.prediction_value_non_salient = prediction_value_non_salient
        self.prediction_nuclei_count = prediction_nuclei_count
        self.image_patch_path = image_patch_path


def image_patch_metadata_object_from_image_patch_dict(image_patch_dict):
    return ImagePatchMetadataObject(image_patch_dict.get(CASE_ID, None),
                                    image_patch_dict.get(RESOLUTION_LEVEL, None),
                                    image_patch_dict.get(X_COORDINATE, None),
                                    image_patch_dict.get(Y_COORDINATE, None),
                                    image_patch_dict.get(WIDTH, None),
                                    image_patch_dict.get(HEIGHT, None),
                                    image_patch_dict.get(PREDICTION_VALUE_SALIENT, None),
                                    image_patch_dict.get(PREDICTION_VALUE_NON_SALIENT, None),
                                    image_patch_dict.get(PREDICTION_NUCLEI_COUNT, None))


def image_patch_metadata_object_from_csv_row(csv_row):
    return ImagePatchMetadataObject(csv_row[CASE_ID],
                                    int(csv_row[RESOLUTION_LEVEL]),
                                    int(csv_row[X_COORDINATE]),
                                    int(csv_row[Y_COORDINATE]),
                                    int(csv_row[WIDTH]),
                                    int(csv_row[HEIGHT]),
                                    float(csv_row[PREDICTION_VALUE_SALIENT]))