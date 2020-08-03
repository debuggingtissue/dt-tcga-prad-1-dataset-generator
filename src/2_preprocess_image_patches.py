from PIL import Image
import argparse
from os.path import join
from utils import path_utils, image_preprocessing_utils
from PIL import Image


def output_preprocessed_image_patch_to_output_directory(full_image_path,
                                                        output_directory_path,
                                                        first_centermost_crop_size,
                                                        downscale_to_size,
                                                        second_centermost_crop_size):
    input_image = Image.open(full_image_path)
    first_centermost_crop_image = image_preprocessing_utils.crop_to_the_centermost(input_image,
                                                                                   first_centermost_crop_size)
    scaled_image = image_preprocessing_utils.scale_image(first_centermost_crop_image, downscale_to_size)
    second_centermost_crop_image = image_preprocessing_utils.crop_to_the_centermost(scaled_image,
                                                                                    second_centermost_crop_size)
    is_mostly_white_pixels = is_image_mostly_white_pixels(0.95, second_centermost_crop_image)

    case_id = full_image_path.split('/')[-2]
    image_patch_id = full_image_path.split('/')[-1][:-4]

    output_case_subfolder = join(output_directory_path, case_id)
    path_utils.create_directory_if_directory_does_not_exist_at_path(output_case_subfolder)

    if is_mostly_white_pixels:
        path_utils.create_directory_if_directory_does_not_exist_at_path(output_case_subfolder +"/white_background_image_patches")

        output_image_name = join(output_case_subfolder +"/white_background_image_patches/",
                                 image_patch_id + '.jpg')
        second_centermost_crop_image.save(output_image_name)
    else:
        output_image_name = join(output_case_subfolder,
                                 image_patch_id + '.jpg')
        second_centermost_crop_image.save(output_image_name)



def is_image_mostly_white_pixels(white_pixel_count_threshold, image):
    print(image)
    pixels = image.getdata()  # get the pixels as a flattened sequence
    white_threshold = 230
    number_of_white_pixels = 0
    for pixel in pixels:
        if pixel[0] > white_threshold and pixel[1] > white_threshold and pixel[2] > white_threshold:
            number_of_white_pixels += 1
    n = len(pixels)

    if (number_of_white_pixels / float(n)) > white_pixel_count_threshold:
        print("mostly white")
        return True
    return False

parser = argparse.ArgumentParser(description='Scale image patches for DeepScope.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)
parser.add_argument("-fc", "--first_centermost_crop_size", type=int, default=0, help="First centermost crop size."
                                                                                     " Default value is 0.")

parser.add_argument("-ds", "--downscale_to_size", type=int, default=0,
                    help="Size to scale first centermost image crop down to."
                         " Default value is 0.")

parser.add_argument("-sc", "--second_centermost_crop_size", type=int, default=0, help="Second centermost crop size."
                                                                                      " Default value is 0.")

args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path
first_centermost_crop_size = args.first_centermost_crop_size
downscale_to_size = args.downscale_to_size
second_centermost_crop_size = args.second_centermost_crop_size

path_utils.halt_script_if_path_does_not_exist(input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)
case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(input_folder_path)

for case_directory_path in case_directory_paths:
    full_image_patch_paths = path_utils.create_full_paths_to_files_in_directory_path(case_directory_path)
    for full_image_patch_path in full_image_patch_paths:
        output_path = output_folder_path + '/'
        output_preprocessed_image_patch_to_output_directory(full_image_patch_path,
                                                            output_folder_path,
                                                            first_centermost_crop_size,
                                                            downscale_to_size,
                                                            second_centermost_crop_size)
