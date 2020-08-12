from .enums import ResolutionLevel
from .image_patch_metadata_object import *

import openslide

def get_SVS_level_ratio(svs_image, from_resolution_level, to_resolution_level):
    if from_resolution_level == ResolutionLevel.THUMBNAIL:
        from_resolution_level_width = svs_image.associated_images["thumbnail"].size[0]
    else:
        from_resolution_level_width = svs_image.level_dimensions[from_resolution_level][0]

    if to_resolution_level == ResolutionLevel.THUMBNAIL:
        to_resolution_level_width = svs_image.associated_images["thumbnail"].size[0]
    else:
        to_resolution_level_width = svs_image.level_dimensions[to_resolution_level][0]

    ratio = (to_resolution_level_width / from_resolution_level_width)

    return ratio


def get_svs_image_of_wsi_from_path(full_image_name_path):
    img = openslide.OpenSlide(full_image_name_path)
    return img


def scale(value, from_resolution_level, to_resolution_level, svs_image):
    return value * get_SVS_level_ratio(svs_image, from_resolution_level, to_resolution_level)


def scale_image_patch_metadata_object_to_new_resolution_level(image_patch_metadata_object,
                                                              to_resolution_level,
                                                              svs_image):
    resolution_level = int(image_patch_metadata_object.resolution_level)
    to_resolution_level = int(to_resolution_level)

    x_coordinate = scale(int(image_patch_metadata_object.x_coordinate), resolution_level,
                                   to_resolution_level, svs_image)
    y_coordinate = scale(int(image_patch_metadata_object.y_coordinate), resolution_level,
                                   to_resolution_level, svs_image)

    width = scale(int(image_patch_metadata_object.width), resolution_level,
                            to_resolution_level, svs_image)
    height = scale(int(image_patch_metadata_object.height), resolution_level,
                             to_resolution_level, svs_image)

    return ImagePatchMetadataObject(resolution_level=to_resolution_level, x_coordinate=x_coordinate, y_coordinate=y_coordinate, width=width, height=height)
