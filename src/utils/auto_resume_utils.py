
def is_case_already_classified_into_csv(input_case_folder_to_predictor_path, predicted_cases_csv_folder_path):

    case_name = input_case_folder_to_predictor_path.split()[-1]
    predicted_csv_for_case_path = predicted_cases_csv_folder_path + case_name + ".csv"
    csv_for_case_exists = path_utils.does_path_exist(predicted_csv_for_case_path)

    # check if CSV file exists for input folder; no: do classificatoin
    if not csv_for_case_exists:
        return False

    csv_file = open(predicted_csv_for_case_path)
    reader = csv.reader(csv_file)
    lines_in_csv = len(list(reader))
    input_files = path_utils.create_full_paths_to_files_in_directory_path

    # get image_count_of input folder open the csv and see if number matches; no: do classification
    if lines_in_csv is input_files.count():
        return False
    return True





