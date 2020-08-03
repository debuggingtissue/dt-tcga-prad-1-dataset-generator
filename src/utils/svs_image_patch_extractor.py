from os.path import isfile, join
from PIL import Image
import openslide
from utils import path_utils, enums, svs_utils, image_patch_file_name_builder

compression_factor = 1
Image.MAX_IMAGE_PIXELS = 1e10


def get_start_positions(start_position, width, height, window_size, axis, overlapping_percentage):
    start_positions = []

    start_positions.append(start_position)
    first_start_position = start_position

    dimension = width if axis == enums.Axis.X else height

    while not (start_position + (window_size * (1 - overlapping_percentage))) > dimension + first_start_position:
        start_position = start_position + (window_size * (1 - overlapping_percentage))
        start_positions.append(int(start_position))

    return start_positions


def split_to_jpeg_image_patches(full_image_path,
                                full_output_path,
                                to_resolution_level,
                                overlapping_percentage,
                                window_size,
                                from_resolution_level=enums.ResolutionLevel.LEVEL_0_BASE,
                                patching_area_x=None,
                                patching_area_y=None,
                                patching_area_width=None,
                                patching_area_height=None):

    file_type = full_image_path[-4:]
    if file_type != ".svs":
        return

    img = openslide.OpenSlide(full_image_path)

    has_specific_patching_area = patching_area_x is not None and patching_area_y is not None and patching_area_width is not None and patching_area_height is not None
    if has_specific_patching_area:
        original_start_position_x = int(patching_area_x)
        original_start_position_y = int(patching_area_y)
        width, height = int(patching_area_width), int(patching_area_height)
    else:
        original_start_position_x = 0
        original_start_position_y = 0
        width, height = img.level_dimensions[from_resolution_level]



    original_start_position_x_label = int(svs_utils.scale(
        int(original_start_position_x), from_resolution_level, to_resolution_level, img))
    original_start_position_y_label = int(svs_utils.scale(int(original_start_position_y), from_resolution_level, to_resolution_level, img))
    width = int(svs_utils.scale(int(width), from_resolution_level, to_resolution_level, img))
    height = int(svs_utils.scale(int(height), from_resolution_level, to_resolution_level, img))


    x_start_positions_labels = get_start_positions(original_start_position_x_label, width, height, window_size, enums.Axis.X,
                                            overlapping_percentage)
    y_start_positions_label = get_start_positions(original_start_position_y_label, width, height, window_size, enums.Axis.Y,
                                            overlapping_percentage)

    total_number_of_patches = len(x_start_positions_labels) * len(y_start_positions_label)
    tile_number = 1

    for x_index, x_start_position in enumerate(x_start_positions_labels):
        for y_index, y_start_position in enumerate(y_start_positions_label):

            #make sure to not extract image outside of image frame or patching area
            x_end_position = min(original_start_position_x_label + width, x_start_position + window_size)
            y_end_position = min(original_start_position_y_label + height, y_start_position + window_size)
            patch_width = x_end_position - x_start_position
            patch_height = y_end_position - y_start_position

            is_image_patch_size_equal_to_window_size = ((patch_height == window_size) and (patch_width == window_size))
            if not is_image_patch_size_equal_to_window_size:
                continue

            #must always convert to resolution 0 when doing patch extraction
            reader_x_start_position = x_start_position
            reader_y_start_position = y_start_position
            if to_resolution_level != enums.ResolutionLevel.LEVEL_0_BASE:
                reader_x_start_position = int(svs_utils.scale(x_start_position, to_resolution_level, from_resolution_level, img))
                reader_y_start_position = int(svs_utils.scale(y_start_position, to_resolution_level, from_resolution_level, img))

            patch = img.read_region((reader_x_start_position, reader_y_start_position),
                                    to_resolution_level,
                                    (patch_width, patch_height))
            patch.load()
            patch_rgb = Image.new("RGB", patch.size, (255, 255, 255))
            patch_rgb.paste(patch, mask=patch.split()[3])

            print("\n")
            print("Patch data", x_start_position, y_start_position, to_resolution_level, patch_width, patch_height)
            print("Tile size for tile number " + str(tile_number) + ":" + str(patch.size))

            # compress the image
            # patch_rgb = patch_rgb.resize(
            #    (int(patch_rgb.size[0] / compression_factor), int(patch_rgb.size[1] / compression_factor)),
            #    Image.ANTIALIAS)

            # save the image

            case_id = full_image_path.split('/')[-1][:-4]

            output_subfolder = join(full_output_path, case_id)
            path_utils.create_directory_if_directory_does_not_exist_at_path(output_subfolder)

            output_image_name = join(output_subfolder,
                                     image_patch_file_name_builder.build_image_patch_file_name(
                                         case_id, to_resolution_level, x_start_position,
                                         y_start_position, patch_width, patch_height))

            patch_rgb.save(output_image_name)
            print("Tile", tile_number, "/", total_number_of_patches, "created")
            tile_number = tile_number + 1

def extract_image_patch_jpeg(full_image_path,
                            full_output_path,
                            to_resolution_level,
                            from_resolution_level=enums.ResolutionLevel.LEVEL_0_BASE,
                            patch_area_x=None,
                            patch_area_y=None,
                            patch_area_width=None,
                            patch_area_height=None):

    img = openslide.OpenSlide(full_image_path)

    original_start_position_x = int(patch_area_x)
    original_start_position_y = int(patch_area_y)
    width, height = int(patch_area_width), int(patch_area_height)

    original_start_position_x_label = int(svs_utils.scale(
        int(original_start_position_x), from_resolution_level, to_resolution_level, img))
    original_start_position_y_label = int(svs_utils.scale(int(original_start_position_y), from_resolution_level, to_resolution_level, img))
    width = int(svs_utils.scale(int(width), from_resolution_level, to_resolution_level, img))
    height = int(svs_utils.scale(int(height), from_resolution_level, to_resolution_level, img))

    x_end_position = original_start_position_x_label + width
    y_end_position = original_start_position_y_label + height
    patch_width = width
    patch_height = height

    # must always convert to resolution 0 when doing patch extraction
    reader_x_start_position = original_start_position_x_label
    reader_y_start_position = original_start_position_y_label
    if to_resolution_level != enums.ResolutionLevel.LEVEL_0_BASE:
        reader_x_start_position = int(
            svs_utils.scale(original_start_position_x_label, to_resolution_level, from_resolution_level, img))
        reader_y_start_position = int(
            svs_utils.scale(original_start_position_y_label, to_resolution_level, from_resolution_level, img))

    patch = img.read_region((reader_x_start_position, reader_y_start_position),
                            to_resolution_level,
                            (patch_width, patch_height))
    patch.load()
    patch_rgb = Image.new("RGB", patch.size, (255, 255, 255))
    patch_rgb.paste(patch, mask=patch.split()[3])

    print("\n")
    print("Patch data", original_start_position_x_label, original_start_position_y_label, to_resolution_level, patch_width, patch_height)

    # compress the image
    # patch_rgb = patch_rgb.resize(
    #    (int(patch_rgb.size[0] / compression_factor), int(patch_rgb.size[1] / compression_factor)),
    #    Image.ANTIALIAS)

    # save the image

    case_id = full_image_path.split('/')[-1][:-4]

    output_subfolder = join(full_output_path, case_id)
    path_utils.create_directory_if_directory_does_not_exist_at_path(output_subfolder)

    output_image_name = join(output_subfolder,
                             image_patch_file_name_builder.build_image_patch_file_name(
                                 case_id, to_resolution_level, original_start_position_x_label,
                                 original_start_position_y_label, patch_width, patch_height))

    patch_rgb.save(output_image_name)


