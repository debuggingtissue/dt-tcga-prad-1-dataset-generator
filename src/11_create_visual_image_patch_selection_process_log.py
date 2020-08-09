import argparse

parser = argparse.ArgumentParser(description='Label image patches with gene mutation data.')
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-svs", "--svs_input_folder_path", type=str, help=" The path to the SVS input folder.",
                    required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.", required=True)
