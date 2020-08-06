class SVSLoader:

    # parameterized constructor
    def __init__(self,
                 TCGA_download_directory_path=None):
        self.TCGA_download_directory_path = TCGA_download_directory_path
        self.zero_indexed_svs_images_for_all_cases = self.get_0_indexed_svs_for_all_cases()
        self.zero_indexed_svs_images_dict_indexed_by_CID = self.get_0_indexed_svs_dict_indexed_by_CID()

    def get_0_indexed_svs_for_all_cases(self):
        zero_indexed_svs_path_from_all_cases = []
        case_paths = path_utils.create_full_paths_to_directories_in_directory_path(self.TCGA_download_directory_path)
        for case_path in case_paths:
            image_paths_of_case = path_utils.create_full_paths_to_files_in_directory_path(case_path)
            image_path_of_first_svs_image = image_paths_of_case[0]
            zero_indexed_svs_path_from_all_cases.append(image_path_of_first_svs_image)
        return zero_indexed_svs_path_from_all_cases

    def get_0_indexed_svs_dict_indexed_by_CID(self):
        dict = {}
        for zero_indexed_svs in self.zero_indexed_svs_images_for_all_cases:
            svs_case_id = first_image_name_path.split('/')[-1][:-4]
            dict[svs_case_id] = zero_indexed_svs
        return dict

    def get_0_indexed_svs_path_for_CID(self, cid):
        return self.zero_indexed_svs_images_dict_indexed_by_CID[cid]
