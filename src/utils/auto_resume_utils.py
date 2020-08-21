
def is_case_already_classified_into_output_csv(input_case_folder_to_predictor_path, predicted_cases_csv_path):
    csv_for_case_exists = path_utils.does_path_exist(predicted_cases_csv_path)
    # check if CSV file exists for input folder; no: do classificatoin
    if not csv_for_case_exists:
        return False

    csv_file = open(predicted_csv_for_case_path)
    reader = csv.reader(csv_file)
    lines_in_csv = len(list(reader))
    input_files = path_utils.create_full_paths_to_files_in_directory_path(input_case_folder_to_predictor_path)
    input_images_count = input_files.count()

    # get image_count_of input folder open the csv and see if number matches; no: do classification
    if lines_in_csv is input_images_count:
        return True
    return False

def is_case_already_classified_into_output_directory(input_directory_path, output_directory_path):
    output_directory_path = path_utils.does_path_exist(output_directory_path)
    if not output_directory_path:
        return False
    input_file_paths = path_utils.create_full_paths_to_files_in_directory_path(input_directory_path)
    output_file_paths = path_utils.create_full_paths_to_files_in_directory_path(output_directory_path)
    if input_file_paths.count() is output_file_paths.count():
        return True
    return False

