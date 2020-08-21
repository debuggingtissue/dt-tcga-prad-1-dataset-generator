from .path_utils import *
import csv

def is_case_already_classified_into_output_csv(input_case_folder_to_predictor_path, case_prediction_csv_path):
    csv_for_case_exists = does_path_exist(case_prediction_csv_path)
    # check if CSV file exists for input folder; no: do classificatoin
    if not csv_for_case_exists:
        print("NO CSV EXISTS")
        return False
    print(case_prediction_csv_path)
    csv_file = open(case_prediction_csv_path)
    reader = csv.reader(csv_file)
    lines_in_csv = len(list(reader)) - 1 #Top row is meta info, therefore remove this from count
    input_files = create_full_paths_to_files_in_directory_path(input_case_folder_to_predictor_path)
    input_images_count = len(input_files)

    # get image_count_of input folder open the csv and see if number matches; no: do classification
    if lines_in_csv == input_images_count:
        print(lines_in_csv)
        print(input_images_count)
        print("CSV LINE COUNT IS EQUAL INPUT IMAGE COUNT")
        return True

    print(lines_in_csv)
    print(input_images_count)
    print("CSV LINE COUNT IS NOT EQUAL INPUT IMAGE COUNT")
    return False

def is_case_already_classified_into_output_directory(input_directory_path, output_directory_path):
    output_directory_path = does_path_exist(output_directory_path)
    if not output_directory_path:
        return False
    input_file_paths = create_full_paths_to_files_in_directory_path(input_directory_path)
    output_file_paths = create_full_paths_to_files_in_directory_path(output_directory_path)
    if len(input_file_paths) == len(output_file_paths):
        return True
    return False

