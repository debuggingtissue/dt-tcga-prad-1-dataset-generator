from .enums import ResolutionLevel
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
