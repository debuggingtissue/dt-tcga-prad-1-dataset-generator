#!/bin/bash
source config.sh

###################################
#               RUN               #
###################################

source "${S0_VIRTUAL_ENV_36}/bin/activate"
python3.6 1_split_svs_images_to_image_patches.py \
  -i $S1_SPLIT_SVS_S0_INPUT_DIRECTORY_PATH \
  -o $S1_SPLIT_SVS_OUTPUT_DIRECTORY_PATH \
  -r $S1_RESOLUTION_LEVEL \
  -op $S1_OVERLAP_PERCENTAGE \
  -ws $S1_WINDOW_SIZE

python3.6 2_preprocess_image_patches.py \
  -i $S2_PREPROCESS_IMAGE_PATCHES_INPUT_DIRECTORY_PATH \
  -o $S2_PREPROCESS_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH \
  -fc $S2_FIRST_CENTERMOST_CROP_SIZE \
  -ds $S2_DOWNSCALED_SIZE \
  -sc $S2_SECOND_CENTERMOST_CROP_SIZE
#rm -r $S2_DIRECTORY_TO_DELETE
#
#source "${S0_VIRTUAL_ENV_27}/bin/activate"
#python 3_predict_saliency_for_image_patches.py \
#  -i $S3_PREDITCT_SALIENCY_INPUT_DIRECTORY_PATH \
#  -o $S3_PREDITCT_SALIENCY_OUTPUT_DIRECTORY_PATH
#rm -r $S3_PREDITCT_SALIENCY_DIRECTORY_TO_DELETE
#
#source "${S0_VIRTUAL_ENV_36}/bin/activate"
#python3.6 4_create_saliency_visualization.py \
#  -svs $S4_CREATE_SALIENCY_VISUALIZATION_SVS_INPUT_DIRECTORY_PATH \
#  -csv $S4_CREATE_SALIENCY_VISUALIZATION_CSV_INPUT_DIRECTORY_PATH \
#  -o $S4_CREATE_SALIENCY_VISUALIZATION_OUTPUT_DIRECTORY_PATH \
#  -apt $S4_CREATE_SALIENCY_ACCURACY_PERCENTAGE_THRESHOLD
#
#python3.6 5_convert_salient_image_patches_to_high_resolution_image_patches.py \
#  -svs $S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_SVS_INPUT_DIRECTORY \
#  -csv $S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_CSV_INPUT_DIRECTORY \
#  -o $S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH \
#  -r $S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_TARGET_RESOLUTION_LEVEL \
#  -op $S5_CREATE_HIGH_RESOLUTION_IMAGE_OVERLAP_PERCENTAGE \
#  -ws $S5_CREATE_HIGH_RESOLUTION_IMAGE_WINDOW_SIZE
#rm -r $S5_CREATE_HIGH_RESOLUTION_DIRECTORY_TO_DELETE_FIRST
#rm -r $S5_CREATE_HIGH_RESOLUTION_DIRECTORY_TO_DELETE_SECOND
#
#source "${S0_VIRTUAL_ENV_36}/bin/activate"
#python3.6 6_preprocess_high_resolution_image_patches.py \
#  -i $S6_PREPROCESS_HIGH_RESOLUTION_IMAGE_PATCHES_INPUT_DIRECTORY_PATH \
#  -o $S6_PREPROCESS_HIGH_RESOLUTION_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH \
#  -ds $S6_HIGH_RESOLUTION_IMAGE_PATCH_DOWNSCALED_SIZE
#rm -r $S6_PREPROCESS_HIGH_RESOLUTION_DIRECTORY_TO_DELETE
#
#python3.6 7_reorganize_directories_for_segmentor.py \
#  -i $S7_REORGANIZE_DIRECTORIES_FOR_SEGMENTOR_INPUT_DIRECTORY_PATH \
#  -o $S7_REORGANIZE_DIRECTORIES_FOR_SEGMENTOR_OUTPUT_DIRECTORY_PATH \
#  -im $S7_REORGANIZE_DIRECTORIES_FOR_SEGMENTOR_IMAGE_MODE
##
#source "${S0_VIRTUAL_NUCLEI_ENV_36}/bin/activate"
#python3.6 8_count_and_annotate_nuclei_in_sub_image_patches.py \
#  -i $S8_NUCLEI_SEGMENTOR_INPUT_DIRECTORY_PATH \
#  -o $S8_NUCLEI_SEGMENTOR_OUTPUT_DIRECTORY_PATH
##rm -r $S8_NUCLEI_SEGMENTOR_DIRECTORY_TO_DELETE
##
#python3.6 9_find_sub_image_patch_with_highest_nuclei_density.py \
#  -i $S9_FIND_SUB_IMAGE_PATCH_WITH_HIGHEST_NUCLEI_DENSITY_INPUT_DIRECTORY_PATH \
#  -o $S9_FIND_SUB_IMAGE_PATCH_WITH_HIGHEST_NUCLEI_DENSITY_OUTPUT_DIRECTORY_PATH \
#  -aip $S9_FIND_SUB_IMAGE_PATCH_WITH_HIGHEST_NUCLEI_DENSITY_ALL_IMAGE_PATCHES_DIRECTORY_PATH \
#  -im $S9_FIND_SUB_IMAGE_PATCH_WITH_HIGHEST_NUCLEI_DENSITY_IMAGE_MODE
#rm -r $S9_FIND_SUB_IMAGE_PATCH_WITH_HIGHEST_NUCLEI_DENSITY_DIRECTORY_TO_DELETE
#rm -r $S7_REORGANIZE_DIRECTORIES_FOR_SEGMENTOR_DIRECTORY_TO_DELETE

#python3.6 10_create_highest_nuclei_count_visualization \
#  -i $S10_CREATE_HIGHEST_NUCLEI_COUNT_VISUALIZATION_INPUT_DIRECTORY_PATH \
#  -svs $S10_CREATE_HIGHEST_NUCLEI_COUNT_VISUALIZATION_SVS_INPUT_DIRECTORY_PATH \
#  -o $S10_CREATE_HIGHEST_NUCLEI_COUNT_VISUALIZATION_OUTPUT_DIRECTORY_PATH \
#rm -r $S10_CREATE_HIGHEST_NUCLEI_COUNT_VISUALIZATION_DIRECTORY_TO_DELETE

#python3.6 11_label_image_patches_with_gene_mutation.py \
#  -i $S10_LABEL_IMAGE_PATCHES_WITH_GENE_MUTATION_INPUT_DIRECTORY_PATH \
#  -o $S10_LABEL_IMAGE_PATCHES_WITH_GENE_MUTATION_OUTPUT_DIRECTORY_PATH \
#  -mf $S10_LABEL_IMAGE_PATCHES_WITH_GENE_MUTATION_MUTATION_FILE_PATH \
#  -goi $S10_LABEL_IMAGE_PATCHES_WITH_GENE_MUTATION_GENE_OF_INTEREST \
#  -do $S10_LABEL_IMAGE_PATCHES_WITH_GENE_MUTATION_DISC_OPERATION
##rm -r $S10_LABEL_IMAGE_PATCHES_WITH_GENE_MUTATION_DIRECTORY_TO_DELETE
